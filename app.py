import base64
import hashlib
import io
import os
import re
import secrets
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(32))

MAGIC = b"CSHIELD1"  # File format marker
SALT_SIZE = 16
NONCE_SIZE = 12
ITERATIONS = 600_000

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
    )
    return kdf.derive(password.encode("utf-8"))

def encrypt_bytes(data: bytes, password: str) -> bytes:
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    key = derive_key(password, salt)
    ciphertext = AESGCM(key).encrypt(nonce, data, MAGIC)
    return MAGIC + salt + nonce + ciphertext

def decrypt_bytes(blob: bytes, password: str) -> bytes:
    header_len = len(MAGIC) + SALT_SIZE + NONCE_SIZE
    if len(blob) <= header_len or not blob.startswith(MAGIC):
        raise ValueError("This is not a valid CryptoShield encrypted file.")
    offset = len(MAGIC)
    salt = blob[offset:offset + SALT_SIZE]
    nonce = blob[offset + SALT_SIZE:header_len]
    ciphertext = blob[header_len:]
    key = derive_key(password, salt)
    try:
        return AESGCM(key).decrypt(nonce, ciphertext, MAGIC)
    except Exception:
        raise ValueError("Decryption failed. Check your password or file integrity.")

def safe_filename(name: str) -> str:
    name = os.path.basename(name or "file")
    return re.sub(r"[^A-Za-z0-9._-]", "_", name) or "file"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/encrypt", methods=["POST"])
def encrypt():
    uploaded = request.files.get("file")
    password = request.form.get("password", "")
    if not uploaded or not uploaded.filename:
        flash("Choose a file first.", "error")
        return redirect(url_for("index"))
    if len(password) < 8:
        flash("Use a password with at least 8 characters.", "error")
        return redirect(url_for("index"))
    data = uploaded.read()
    if not data:
        flash("The selected file is empty.", "error")
        return redirect(url_for("index"))
    encrypted = encrypt_bytes(data, password)
    output = io.BytesIO(encrypted)
    output.seek(0)
    name = safe_filename(uploaded.filename) + ".cshield"
    return send_file(output, as_attachment=True, download_name=name, mimetype="application/octet-stream")

@app.route("/decrypt", methods=["POST"])
def decrypt():
    uploaded = request.files.get("file")
    password = request.form.get("password", "")
    if not uploaded or not uploaded.filename:
        flash("Choose a .cshield file first.", "error")
        return redirect(url_for("index"))
    if not password:
        flash("Enter the encryption password.", "error")
        return redirect(url_for("index"))
    try:
        decrypted = decrypt_bytes(uploaded.read(), password)
    except ValueError as exc:
        flash(str(exc), "error")
        return redirect(url_for("index"))
    original = safe_filename(uploaded.filename)
    if original.endswith(".cshield"):
        original = original[:-8]
    output = io.BytesIO(decrypted)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name="decrypted_" + original,
                     mimetype="application/octet-stream")

@app.route("/tools", methods=["GET", "POST"])
def tools():
    result = None
    if request.method == "POST":
        text = request.form.get("text", "")
        result = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return render_template("tools.html", result=result)

@app.route("/health")
def health():
    return {"status": "ok", "app": "CryptoShield"}

if __name__ == "__main__":
    app.run(debug=True)
