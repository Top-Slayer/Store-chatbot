from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
chat_history = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=['POST'])
def chat():
    user_input = request.json["message"]
    chat_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are JD's helpful assistant named Grandma Lara Respond clearly and kindy in English, not matter the topic."}
        ] + chat_history,
        max_tokens=500
    )

    print(response)

    reply = response.choices[0].message.content.strip()
    chat_history.append({"role": "assistant", "content": reply})

    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True, port=5000)