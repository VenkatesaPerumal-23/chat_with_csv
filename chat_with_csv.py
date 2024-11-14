# -*- coding: utf-8 -*-
"""chat_with_csv.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fQ_7hG0bhcCbPZnHZibeMwurkEUKhAcN
"""

!pip install pandas transformers sentence-transformers
!pip install gradio

import gradio as gr
import pandas as pd
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util

# Load the CSV file
def load_csv(file_path):
    return pd.read_csv(file_path)

# Convert each row of the CSV to text format for question answering
def preprocess_csv(dataframe):
    rows_text = []
    for _, row in dataframe.iterrows():
        row_text = " | ".join([f"{col}: {val}" for col, val in row.items()])
        rows_text.append(row_text)
    return rows_text

# Initialize Hugging Face Models
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")
embedding_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

# Function to find the most relevant row based on the question
def find_relevant_row(question, rows_text):
    question_embedding = embedding_model.encode(question, convert_to_tensor=True)
    rows_embeddings = embedding_model.encode(rows_text, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(question_embedding, rows_embeddings)
    best_row_idx = similarities.argmax().item()
    return rows_text[best_row_idx]

# Ask question and get an answer
def ask_question(question, dataframe, rows_text):
    relevant_row_text = find_relevant_row(question, rows_text)
    answer = qa_pipeline({
        "context": relevant_row_text,
        "question": question
    })
    return answer["answer"]

# Gradio interface function
def gradio_chat(question, file):
    # Load and preprocess CSV file on first interaction
    if 'dataframe' not in gradio_chat.__dict__:
        gradio_chat.dataframe = load_csv(file.name)
        gradio_chat.rows_text = preprocess_csv(gradio_chat.dataframe)

    # Get answer to question
    answer = ask_question(question, gradio_chat.dataframe, gradio_chat.rows_text)
    return answer

# Create Gradio Interface
gradio_interface = gr.Interface(
    fn=gradio_chat,
    inputs=[
        gr.Textbox(lines=2, placeholder="Ask a question about the CSV data..."),
        gr.File(label="Upload CSV file")
    ],
    outputs="text",
    title="CSV Chatbot",
    description="Ask questions about your CSV data and get answers instantly!"
)

# Launch the interface
gradio_interface.launch()

