import streamlit as st
from transformers import BertTokenizer, BertForSequenceClassification
import PyPDF2
import nltk
from nltk.tokenize import word_tokenize

# Ensure nltk resources are downloaded
nltk.download('punkt')

# Define the personality detection function
def personality_detection(text):
    tokenizer = BertTokenizer.from_pretrained("Minej/bert-base-personality")
    model = BertForSequenceClassification.from_pretrained("Minej/bert-base-personality")
    inputs = tokenizer(text, truncation=True, padding=True, return_tensors="pt")
    outputs = model(**inputs)
    predictions = outputs.logits.squeeze().detach().numpy()
    label_names = ['Extroversion', 'Neuroticism', 'Agreeableness', 'Conscientiousness', 'Openness']
    result = {label_names[i]: predictions[i] for i in range(len(label_names))}
    return result

# Define the PDF to tokens function
def pdf_to_tokens(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(reader.pages)
    all_text = ''
    for page_num in range(num_pages):
        page = reader.pages[page_num]
        all_text += page.extract_text() + ' '
    tokens = word_tokenize(all_text)
    chunks = [' '.join(tokens[i:i + 1000]) for i in range(0, len(tokens), 1000)]
    return chunks

# Streamlit app interface
st.title('Personality Detection from Autobiographies')
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is not None:
    chunks = pdf_to_tokens(uploaded_file)
    results = []
    for chunk in chunks:
        results.append(personality_detection(chunk))

    # Sum and average the results
    if results:
        sums = {trait: 0 for trait in results[0]}
        for person in results:
            for trait in person:
                sums[trait] += person[trait]
        averages = {trait: sum_val / len(results) for trait, sum_val in sums.items()}
        st.write("Average values for each trait:")
        for trait, average in averages.items():
            st.write(f"{trait}: {average}")

