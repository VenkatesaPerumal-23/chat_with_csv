import google.generativeai as genai
import pandas as pd
import time
import streamlit as st

# Configure the API key
genai.configure(api_key="AIzaSyDUKuFJ49VVqgPIfVJAzwcw2Q6NCKiDRtI")

# Function to load and preview Excel data
def load_excel_data(file_path):
    # Load the Excel file into a DataFrame
    data = pd.read_excel(file_path)
    # Convert the entire DataFrame to a readable string format for the prompt
    data_context = data.to_string(index=False)
    return data_context

# Function to send a request to the model
def send_request(chat, context, question):
    try:
        # Combine context and question into a single prompt
        prompt = f"Here is the data:\n\n{context}\n\nQuestion: {question}"
        response = chat.send_message(prompt)
        return response
    except Exception as e:
        print("Error occurred:", e)
        time.sleep(5)  
        return None

def ask_model_with_excel(file_path, question):
    # Load Excel data and format it
    data_context = load_excel_data(file_path)
    
    # Start a chat with the model
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")
    chat = model.start_chat()
    
    # Send the request with the data context and question
    response = send_request(chat, data_context, question)
    
    if response:
        # Extract and return the answer from the model's response
        answer = response.candidates[0].content.parts[0].text
        return answer
    else:
        return "No response received."

# Streamlit app
st.title("QueryMate")
st.write("Upload an Excel file and ask questions.")

# File upload
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

# Question input
question = st.text_input("Enter your question")

# Display the response
if uploaded_file and question:
    answer = ask_model_with_excel(uploaded_file, question)
    st.write("Answer:", answer)
