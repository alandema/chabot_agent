from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv('config.env')


model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.2,
    max_tokens=500,
    timeout=None,
    max_retries=2
)


def get_completion(prompt):
    response = model.invoke(prompt)
    return response.content