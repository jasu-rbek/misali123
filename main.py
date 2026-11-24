import sqlite3
import requests
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
app = Flask(__name__)
load_dotenv()
BOT_TOKEN = "API"
CHAT_ID = "8976515963"

SAMPLE_PHONES = [
    {
        "id": 1,
        "brand": "Samsung",
        "name": "Galaxy S24",
        "price": 9500000,
        "image_url": "data:image/webp;base64,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",
    },
    {
        "id": 2,
        "brand": "Apple",
        "name": "iphon15",
        "price": 10800000,
        "image_url": "data:image/jpeg;base64,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",
    },
    {
        "id": 3,
        "brand": "Xiaomi",
        "name": "Redmi Note 13",
        "price": 2900000,
        "image_url": "data:image/jpeg;base64,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",
    },
]


def send_telegram(text):
    if not BOT_TOKEN or not CHAT_ID or "SIZDIN" in BOT_TOKEN:
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": text}, timeout=5)
    except Exception as e:
        print("Telegram qátesi:", e)


def get_db():
    conn = sqlite3.connect("store.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS phones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            brand TEXT NOT NULL,
            price INTEGER NOT NULL,
            image_url TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()


@app.route("/")
@app.route("/home")
def home():
    conn = get_db()
    phones = conn.execute("SELECT * FROM phones").fetchall()
    conn.close()

    if not phones:
        phones = SAMPLE_PHONES

    return render_template("home.html", phones=phones)


@app.route("/order/<int:phone_id>", methods=["POST"])
def order(phone_id):
    customer_name = request.form["customer_name"]
    customer_phone = request.form["customer_phone"]

    conn = get_db()
    phone = conn.execute("SELECT * FROM phones WHERE id = ?", (phone_id,)).fetchone()
    conn.close()

    if phone is None:
        for item in SAMPLE_PHONES:
            if item["id"] == phone_id:
                phone = item
                break

    if phone:
        msg = (
            f"📱 Jańa buyırtpa!\n"
            f"Telefon: {phone['brand']} {phone['name']}\n"
            f"Bahası: {phone['price']} sum\n"
            f"Xaridar: {customer_name}\n"
            f"Tel: {customer_phone}"
        )
        send_telegram(msg)

    return redirect(url_for("home"))


@app.route("/admin", methods=["GET", "POST"])
def admin():
    conn = get_db()
    if request.method == "POST":
        name = request.form["name"]
        brand = request.form["brand"]
        price = int(request.form["price"])
        image_url = request.form.get("image_url", "")
        conn.execute(
            "INSERT INTO phones (name, brand, price, image_url) VALUES (?, ?, ?, ?)",
            (name, brand, price, image_url),
        )
        conn.commit()
        send_telegram(f"✅ Admin jańa telefon qostı: {brand} {name} ({price} sum)")
        return redirect(url_for("admin"))

    phones = conn.execute("SELECT * FROM phones").fetchall()
    conn.close()
    return render_template("admin.html", phones=phones)


@app.route("/delete/<int:phone_id>")
def delete_phone(phone_id):
    conn = get_db()
    conn.execute("DELETE FROM phones WHERE id = ?", (phone_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(debug=True)