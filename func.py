from openai import OpenAI
import sqlite3
import faiss
import numpy as np
import os
import socket


DB_PATH = "database.db"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
TOP_K = 3

command_map = {
    "qr": "Generate and display QR code",
    "nothing": "Do nothing or say no action needed, just greeting or interesting about products, ask about products and purchase",
}

client = OpenAI(api_key=OPENAI_API_KEY)


def get_all_info_products():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        return cursor.fetchall()


def format_product(row) -> str:
    return f"""Product Name: {row[1]}
Price: ${row[2]}
Stock: {row[3]}
Spec: {row[4]}
"""


def get_embedding(text):
    response = client.embeddings.create(input=[text], model="text-embedding-3-small")
    return np.array(response.data[0].embedding, dtype="float32")


def build_command_index():
    command_texts = list(command_map.values())
    command_keys = list(command_map.keys())

    embeddings = [get_embedding(text) for text in command_texts]
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    return index, command_keys


def get_best_command(user_input: str, index, command_keys):
    emb = get_embedding(user_input).reshape(1, -1).astype("float32")
    distances, indices = index.search(emb, 1)
    best_index = indices[0][0]
    return command_keys[best_index]


def get_private_wifi_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"
