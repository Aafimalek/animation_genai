import google.generativeai as genai
import os
from dotenv import load_dotenv
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

models = genai.list_models()
for model in models:
    print(model.name)
