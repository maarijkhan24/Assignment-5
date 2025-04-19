# 🔐 Streamlit Secure Data Vault

A secure and simple data encryption and retrieval system built with **Streamlit** and **Fernet Encryption (cryptography)**. This app allows users to safely store and retrieve sensitive data using a custom passkey. Includes a lockout mechanism for added protection against brute-force attempts.

---

## 🚀 Features

- Encrypt and store user input securely using a custom passkey.
- Retrieve and decrypt data using the correct Data ID and passkey.
- Three failed attempts trigger a **30-second lockout** to prevent brute-force.
- Master login to unlock the system if locked.
- Persistent storage using **Pickle** for session-safe encrypted data.

---

## 🔧 How It Works

1. **Store Data**:
   - Input any sensitive information.
   - Create a passkey to encrypt the data.
   - Get a unique **Data ID** that will be used for retrieval.

2. **Retrieve Data**:
   - Input your Data ID and corresponding passkey.
   - On success, your decrypted data will be shown.
   - After 3 incorrect attempts, the system locks for 30 seconds.

3. **Master Login**:
   - A hardcoded hash of the master passkey (`hello`) allows unlocking during lockout.

---

## 🛡️ Encryption Details

- Uses **Fernet** from the `cryptography` package for symmetric encryption.
- Data is encrypted as a combination of the input + passkey.
- Key is stored in the session and saved to `encrypted_data.pkl`.

---

## 📁 File Structure

📦 your_project/ ├── encrypted_data.pkl # Encrypted data storage file ├── secure_vault_app.py # Main Streamlit application file └── README.md # Project documentation 


---

## 💻 Installation

### 1. Clone the repository
```bash
https://github.com/maarijkhan24/Assignment-5.git

2. Install dependencies
pip install streamlit cryptography

3. Run the Streamlit app
streamlit run app.py

```

✅ Default Master Passkey
The master login passkey is set to: hello

(This is hashed and checked using SHA-256)

🔒 Security Note
This is a demo vault. For production use:

Use environment variables for keys.

Replace hardcoded hashes.

Improve encryption key management.
