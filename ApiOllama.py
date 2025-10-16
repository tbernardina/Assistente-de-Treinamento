from fastapi import FastAPI
from pydantic import BaseModel
from ollama import Client
import uvicorn

app = FastAPI()
server = Client()

class Message(BaseModel):
    message: str

@app.post("/ia")
async def chat(msg: Message):
    messages = [
        {
            "role": "user",
            "content": msg.message,
        },
    ]
    response = ""
    for part in server.chat(model="granite3.3:8b", messages=messages, stream=True):
        response += part['message']['content']
    return response

if __name__ == "__main__":
    uvicorn.run("ApiOllama:app", host="0.0.0.0", port=3000, reload=True)

