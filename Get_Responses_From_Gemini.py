import google.generativeai as genai
import os
import pandas as pd 
import time

genai.configure(api_key='YOUR_API_KEY')

def read_questions_from_excel(input_file_path, column_name="questions"):
    #Reads questions from a specified column in an Excel file.
    df = pd.read_excel(input_file_path)
    questions = df[column_name].tolist()
    return questions

def write_responses_to_excel(output_file_path, responses, column_name="responses"):
    #Writes responses to a specified column in an Excel file.
    df = pd.DataFrame({column_name: responses})
    df.to_excel(output_file_path, index=False)

def generate_responses_with_gemini(input_file_path, output_file_path):
    # Initialize the Gemini model
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Read questions from the input Excel file
    questions = read_questions_from_excel(input_file_path)
    responses = []

    # Generate responses for each question
    for question in questions:
        response = model.generate_content(question)
        responses.append(response.text)
        
        time.sleep(60) #Gemini requires time to write responses, otherwise a quota error arises
    
    # Write responses to the output Excel file
    write_responses_to_excel(output_file_path, responses)
    print("Responses written to Excel file.")

input_file_path = ''  # Excel file containing questions in "questions" column
output_file_path = ''  # Excel file to save responses in "responses" column
generate_responses_with_gemini(input_file_path, output_file_path)

