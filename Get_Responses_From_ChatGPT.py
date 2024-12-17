import openai 
from openai import OpenAI
import pandas as pd

client = OpenAI(
    api_key="YOUR-API-KEY",
)

def read_questions_from_excel(input_file_path, column_name="questions"):
    #Reads questions from a specified column in an Excel file.
    df = pd.read_excel(input_file_path)
    questions = df[column_name].tolist()
    return questions

def write_responses_to_excel(output_file_path, responses, column_name="responses"):
    #Writes responses to a specified column in an Excel file.
    df = pd.DataFrame({column_name: responses})
    df.to_excel(output_file_path, index=False)

def process_questions_with_chatgpt(input_file_path, output_file_path):
    questions = read_questions_from_excel(input_file_path)
    responses = []
    
    # Initialize the conversation with a system message
    messages = [{"role": "system", "content": "You are an intelligent assistant, helping students solve math problems"}]
    
    for question in questions:
        # Append the user question to the conversation
        messages.append({"role": "user", "content": question})
        
        # Get ChatGPT's response using the provided client code structure
        chat = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=messages
        )
        
        reply = chat.choices[0].message.content
        responses.append(reply)
        
        # Append the assistant's response back to the conversation
        messages.append({"role": "assistant", "content": reply})
        
    # Write all responses to the output Excel file
    write_responses_to_excel(output_file_path, responses)
    print("Responses written to Excel file.")

input_file_path = ''  # Excel file containing questions in "questions" column
output_file_path = ''  # Excel file to save responses in "responses" column
process_questions_with_chatgpt(input_file_path, output_file_path)
