import streamlit as st
from transformers import BertTokenizer, BertForSequenceClassification
import PyPDF2
import nltk
from nltk.tokenize import word_tokenize
import mysql.connector
from mysql.connector import Error
import boto3

# Initialize clients
s3 = boto3.client('s3')

# Database connection configuration
config = {
    'user': 'username',
    'password': 'password',
    'host': 'autobiography-db.cfgznmmh4qfo.us-east-1.rds.amazonaws.com',
    'database': 'autobiography',
    'raise_on_warnings': True
}


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


# Define the PDF to tokens function & save the text to S3
def pdf_to_tokens(pdf_file, book_name):
    reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(reader.pages)
    all_text = ''
    for page_num in range(num_pages):
        page = reader.pages[page_num]
        all_text += page.extract_text() + ' '

    # save the text to S3
    s3.put_object(
        Bucket='autobiography-raw-data',
        Key=book_name,
        Body=all_text
    )

    tokens = word_tokenize(all_text)
    chunks = [' '.join(tokens[i:i + 1000]) for i in range(0, len(tokens), 1000)]
    return chunks


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
        # Insert into persons table
        cursor.execute("""
            INSERT INTO persons (person_name, Extroversion, Neuroticism, Agreeableness, Conscientiousness, Openness, book_title) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (person_name, scores['Extroversion'], scores['Neuroticism'],
                  scores['Agreeableness'], scores['Conscientiousness'],
                  scores['Openness'], book_name))

        # Insert into books table
        cursor.execute("""
            INSERT INTO books (book_title, Extroversion, Neuroticism, Agreeableness, Conscientiousness, Openness, person_name) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (book_name, scores['Extroversion'], scores['Neuroticism'],
                  scores['Agreeableness'], scores['Conscientiousness'],
                  scores['Openness'], person_name))

        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        st.error(f"Failed to insert data into database: {e}")


# Streamlit app interface
st.title('Personality Detection from Autobiographies')

# Text input for person name and book name
person_name = st.text_input("Enter the person's name")
book_name = st.text_input("Enter the book's name")

if person_name and book_name:
    db_result = check_database(person_name, book_name)
    if db_result:
        traits = ['Extroversion', 'Neuroticism', 'Agreeableness',
                  'Conscientiousness', 'Openness']
        personality_scores = dict(zip(traits, db_result))
        st.write("Retrieved Personality Scores from Database:")
        st.json(personality_scores)
    else:
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        if uploaded_file is not None:
            chunks = pdf_to_tokens(uploaded_file, book_name)
            results = []
            for chunk in chunks:
                results.append(personality_detection(chunk))

            # Sum and average the results
            if results:
                sums = {trait: 0 for trait in results[0]}
                for person in results:
                    for trait in person:
                        sums[trait] += person[trait]
                averages = {trait: sum_val / len(results) for trait, sum_val in
                            sums.items()}
                st.write("Computed Personality Scores:")
                st.json(averages)
                # Insert results into the database
                insert_into_database(person_name, book_name, averages)
