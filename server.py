from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from openai import OpenAI
import os
import func as fn
import markdown
import qrcode
import io

DB_PATH = "database.db"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
TOP_K = 3
PORT = 5000


client = OpenAI(api_key=OPENAI_API_KEY)

system_prompt = """
You are electronic seller that can tell customer about your products
if they ask about and you can generate qr-code also use this [QR] while customer gonna buy it
before succeed buying of customer that will ask customer again
list product below: \n
"""
for prod in fn.get_all_info_products():
    system_prompt += fn.format_product(prod)
    system_prompt += "-------------------------------------\n"
print(system_prompt)

app = Flask(__name__)
CORS(app)

chat_history = []
qr_status = False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/qr-gen")
def generate_qr():
    with open("qr-code.jpeg", "rb") as f:
        img_bytes = f.read()

    buf = io.BytesIO(img_bytes)
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


@app.route("/chat", methods=["POST"])
def chat():
    global qr_status
    index, keys = fn.build_command_index()
    user_input = request.json["message"]
    chat_history.append({"role": "user", "content": user_input})

    print(fn.get_best_command(user_input, index, keys))

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            }
        ]
        + chat_history,
        max_tokens=500,
    )

    reply = response.choices[0].message.content.strip()
    reply = markdown.markdown(reply)

    if "[QR]" in reply:
        reply = reply.replace("[QR]", "")
        qr_status = True
    else:
        qr_status = False

    chat_history.append({"role": "assistant", "content": reply})

    return jsonify({"response": reply, "qr_status": qr_status})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=PORT)
