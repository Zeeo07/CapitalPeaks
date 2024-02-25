from flask import Flask, render_template, request
from openai import OpenAI
import os
from dotenv import load_dotenv

client = OpenAI()
load_dotenv()
OpenAI.api_key = os.environ["OPENAI_API_KEY"]

#print(openai.api_key)

app = Flask(__name__)

chat_history = []

@app.route("/")
def home():
    return render_template("openai.html")

@app.route("/chatbot", methods=["POST"])
def chatbot():
    global chat_history
    
    user_input = request.form["message"]
    prompt = f"User: {user_input}\nChatbot:"
    
    response = client.completions.create(
        
        model="gpt-3.5-turbo-instruct",
        #engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=60,
        #top_p=1,
        n=1,
        frequency_penalty=0,
        stop=["\nUser: ", "\nChatbot: "]
    )

    bot_response = response.choices(0).text
    chat_history.append(f"User: {user_input}\nChatbot: {bot_response}")

    return render_template(
        "chatbot.html",
        user_input=user_input,
        bot_response=bot_response,
        chat_history=chat_history
    )

if __name__ == "__main__":
    app.run(debug=True)