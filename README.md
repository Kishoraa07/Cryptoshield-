# CryptoShield — Cryptography & Cybersecurity Mini Project

CryptoShield is a beginner-friendly web application that demonstrates practical cryptography concepts through file encryption, file decryption, and SHA-256 hashing.

## Features

- **File encryption:** AES-256-GCM authenticated encryption.
- **Password-based key derivation:** PBKDF2-HMAC-SHA256 with a random 16-byte salt and 600,000 iterations.
- **File decryption:** Authenticates the encrypted data before returning the original file.
- **SHA-256 hash generator:** Generates a one-way digest for text integrity demonstrations.
- **Responsive interface:** Simple dark-themed Flask web UI.

## Tech stack

- Python 3
- Flask
- `cryptography` library
- HTML5 and CSS3

## Project structure

```text
CryptoShield/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   ├── index.html
│   └── tools.html
└── static/
    └── style.css
```

## Run locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/CryptoShield.git
cd CryptoShield
```

### 2. Create and activate a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

## How it works

1. The user selects a file and supplies a password.
2. CryptoShield generates a random salt and nonce.
3. PBKDF2 derives a 256-bit key from the password and salt.
4. AES-GCM encrypts the file and authenticates the ciphertext.
5. The output stores a format marker, salt, nonce, and encrypted data.
6. During decryption, the same password derives the key. AES-GCM verifies authenticity before releasing plaintext.

SHA-256 hashing is available separately. Hashing is one-way; it is not a way to decrypt data.

## Security notes

- Keep your password safe. There is no password recovery mechanism.
- Use a unique, strong password for each sensitive file.
- This is an educational mini project, not a professionally audited file-storage service.
- For real deployments, add upload-size limits, CSRF protection, authentication, rate limiting, secure deployment configuration, and security testing.
- Do not expose Flask's development server to the public internet. Use a production WSGI server and HTTPS for deployment.
- Files are handled in memory by this demo; very large files may use significant memory.

## Suggested GitHub repository description

`A Python Flask mini project demonstrating AES-256-GCM file encryption, PBKDF2 password-based key derivation, and SHA-256 hashing.`

## License

MIT
