from openai import OpenAI
import dotenv
import time
import os 

dotenv.load_dotenv(dotenv.find_dotenv())

api_key = os.getenv("API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")

client = OpenAI(api_key=api_key)

while True:
    question = input("Pergunte algo ao normativo (ou digite 'sair' para encerrar): ")
    
    if question.lower() == "sair":
        print("Encerrando...")
        break
    
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant_id)
    print(f"Run created: {run.id}")

    while run.status !=  "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(f"Run status: {run.status}")
        time.sleep(1)
    else:
        print("Run Completed!")

    message_response = client.beta.threads.messages.list(thread_id=thread.id)
    messages = message_response.data

    latest_message = messages[0]
    print(f"Resposta: {latest_message.content[0].text.value}")
