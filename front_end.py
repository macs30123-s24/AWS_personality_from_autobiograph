import nltk
import streamlit as st
from transformers import BertTokenizer, BertForSequenceClassification
import PyPDF2
from ebooklib import epub
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
import mysql.connector
from mysql.connector import Error
import boto3
import logging
import os
import numpy as np
from numba import njit

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize clients
s3 = boto3.client('s3')

# Database connection configuration using environment variables
config = {
    'user': 'username',
    'password': 'password',
    'host': 'autobiography-db.cvb2z3vt9fut.us-east-1.rds.amazonaws.com',
    'database': 'autobiography',
    'raise_on_warnings': True
}

# Download the punkt tokenizer
nltk.download('punkt')


# Function to read PDF
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    num_pages = len(reader.pages)
    all_text = ''
    for page_num in range(num_pages):
        page = reader.pages[page_num]
        all_text += page.extract_text() + ' '
    return all_text


# Function to read TXT
def read_txt(file):
    all_text = file.read().decode('utf-8')
    return all_text

# Function to read EPUB
def read_epub(file):
    book = epub.read_epub(file)
    all_text = ''
    for item in book.get_items():
        if item.get_type() == epub.EpubHtml:
            soup = BeautifulSoup(item.get_body_content(), 'html.parser')
            all_text += soup.get_text() + ' '
    return all_text

# Function to convert text to tokens and save to S3
def text_to_tokens(text, book_name):
    # Save the text to S3
    s3.put_object(
        Bucket='autobiography-raw-data',
        Key=book_name,
        Body=text
    )

    tokens = word_tokenize(text)
    chunks = [' '.join(tokens[i:i + 1000]) for i in range(0, len(tokens), 1000)]
    return chunks


# Define the document to tokens function & save the text to S3
def document_to_tokens(file, file_extension, book_name):
    if file_extension == 'pdf':
        text = read_pdf(file)
    elif file_extension == 'txt':
        text = read_txt(file)
    elif file_extension == 'epub':
        text = read_epub(file)
    else:
        raise ValueError("Unsupported file type")
    return text_to_tokens(text, book_name)


# Define the personality detection function
def personality_detection(text):
    tokenizer = BertTokenizer.from_pretrained("Minej/bert-base-personality")
    model = BertForSequenceClassification.from_pretrained(
        "Minej/bert-base-personality")
    inputs = tokenizer(text, truncation=True, padding=True, return_tensors="pt")
    outputs = model(**inputs)
    predictions = outputs.logits.squeeze().detach().numpy()
    label_names = ['Extroversion', 'Neuroticism', 'Agreeableness',
                   'Conscientiousness', 'Openness']
    result = {label_names[i]: predictions[i] for i in range(len(label_names))}
    return result


def check_database(person_name, book_name):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT Extroversion, Neuroticism, Agreeableness, Conscientiousness, Openness FROM persons WHERE person_name = %s AND book_title = %s",
            (person_name, book_name))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    except Error as e:
        st.error(f"Database connection failed: {e}")
        return None


def insert_into_database(person_name, book_name, scores):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Print the parameters to debug
        print("Inserting into persons table:", person_name, book_name, scores)

        # Insert into persons table with alias for ON DUPLICATE KEY UPDATE
        cursor.execute("""
            INSERT INTO persons (person_name, Extroversion, Neuroticism, Agreeableness, Conscientiousness, Openness, book_title)
            VALUES (%s, %s, %s, %s, %s, %s, %s) AS new_vals
            ON DUPLICATE KEY UPDATE
                Extroversion=new_vals.Extroversion,
                Neuroticism=new_vals.Neuroticism,
                Agreeableness=new_vals.Agreeableness,
                Conscientiousness=new_vals.Conscientiousness,
                Openness=new_vals.Openness,
                book_title=new_vals.book_title
            """, (person_name, scores['Extroversion'], scores['Neuroticism'],
                  scores['Agreeableness'], scores['Conscientiousness'],
                  scores['Openness'], book_name))

        # Print the parameters to debug
        print("Inserting into books table:", book_name, person_name, scores)

        # Insert into books table with alias for ON DUPLICATE KEY UPDATE
        cursor.execute("""
            INSERT INTO books (book_title, Extroversion, Neuroticism, Agreeableness, Conscientiousness, Openness, person_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s) AS new_vals
            ON DUPLICATE KEY UPDATE
                Extroversion=new_vals.Extroversion,
                Neuroticism=new_vals.Neuroticism,
                Agreeableness=new_vals.Agreeableness,
                Conscientiousness=new_vals.Conscientiousness,
                Openness=new_vals.Openness,
                person_name=new_vals.person_name
            """, (book_name, scores['Extroversion'], scores['Neuroticism'],
                  scores['Agreeableness'], scores['Conscientiousness'],
                  scores['Openness'], person_name))

        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        st.error(f"Failed to insert data into database: {e}")

def compute_averages(results):
    sums = {trait: 0 for trait in results[0]}
    for person in results:
        for trait in person:
            sums[trait] += person[trait]
    averages = {trait: sum_val / len(results) for trait, sum_val in
                sums.items()}
    return averages

# Streamlit app interface
st.title('Personality Detection from Autobiographies')

# Text input for person name and book name
person_name = st.text_input("Enter the person's name").lower()
book_name = st.text_input("Enter the book's name").lower()

if person_name and book_name:
    db_result = check_database(person_name, book_name)
    if db_result:
        traits = ['Extroversion', 'Neuroticism', 'Agreeableness',
                  'Conscientiousness', 'Openness']
        personality_scores = dict(zip(traits, db_result))
        st.write("Retrieved Personality Scores from Database:")
        st.json(personality_scores)
    else:
        uploaded_file = st.file_uploader("Choose a file",
                                         type=["pdf", "docx", "txt", "epub"])
        if uploaded_file is not None:
            file_extension = uploaded_file.name.split('.')[-1].lower()

            # Initialize session state if not already done
            if 'uploaded_file' not in st.session_state:
                st.session_state.uploaded_file = uploaded_file

            if 'chunks' not in st.session_state:
                chunks = document_to_tokens(uploaded_file, file_extension,
                                            book_name)
                st.session_state.chunks = chunks
            else:
                chunks = st.session_state.chunks

            results = []
            for chunk in chunks:
                results.append(personality_detection(chunk))

            # Sum and average the results
            if results:
                averages = compute_averages(results)
                st.write("Computed Personality Scores:")
                st.json(averages)
                # Insert results into the database
                insert_into_database(person_name, book_name, averages)
