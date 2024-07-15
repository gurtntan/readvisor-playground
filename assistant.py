from dotenv import load_dotenv
from openai import OpenAI
from datasets import load_dataset
from config import openai_api_key

load_dotenv()
client = OpenAI()

def create_new_assistant(business_name,instructions):
    assistant = client.beta.assistants.create(
        name=business_name,
        instructions=instructions,
        tools=[{"type": "code_interpreter", "type": "file_search"}],
        model="gpt-4-turbo",
     )
    return assistant.id

def create_new_thread():
    thread = client.beta.threads.create()
    return thread.id

def update_assistant_with_files(assistant_id, file_paths):

    vector_store = client.beta.vector_stores.create(name="Reviews") #TODO filter for respective restaurant only, filter for sentiment, ...
    file_streams = [open(path, "rb") for path in file_paths]
    
    # Use the upload and poll SDK helper to upload the files, add them to the vector store,
    # and poll the status of the file batch for completion.
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, files=file_streams
    )

    assistant = client.beta.assistants.update(
    assistant_id=assistant_id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )
    return assistant_id

def run(assistant_id, thread_id):
    while True:
        # TODO instead of prompting to use the knowledge base and upload files, find relevant reviews for user input and post user prompt including review text
        text = "Based on your knowledge base" + input("Type a question (Type 'quit' to exit)\n >>> ")
        if text.lower() == 'quit':
            break

        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=text,
        )
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

        response_message = None
        messages = client.beta.threads.messages.list(thread_id=thread_id).data

        for message in messages:
            if message.role == "assistant" and message.created_at > run.created_at:
                response_message = message
                break

        if response_message:
            print(f"Readvisor: {response_message.content}\n")
        else:
            print("No response.\n")