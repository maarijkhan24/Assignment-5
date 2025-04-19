import streamlit as st
from cryptography.fernet import Fernet
import os
import time
from hashlib import sha256
import pickle
from pathlib import Path

if 'data_store' not in st.session_state:
    st.session_state.data_store = {}
if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0
if 'locked_out' not in st.session_state:
    st.session_state.locked_out = False
if 'lockout_time' not in st.session_state:
    st.session_state.lockout_time = 0

# Generate or load encryption key
def get_key():
    if 'encryption_key' not in st.session_state:
        st.session_state.encryption_key = Fernet.generate_key()
    return st.session_state.encryption_key

# Encrypt data
def encrypt_data(data, passkey):
    cipher_suite = Fernet(get_key())
    combined = f"{data}::{passkey}"
    encrypted_data = cipher_suite.encrypt(combined.encode())
    return encrypted_data

# Decrypt data
def decrypt_data(encrypted_data, passkey):
    try:
        cipher_suite = Fernet(get_key())
        decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
        stored_data, stored_passkey = decrypted_data.split("::")
        if stored_passkey == passkey:
            return stored_data
        return None
    except:
        return None

# Save data to file with error handling
def save_to_file():
    try:
        data = {
            'data_store': st.session_state.data_store,
            'encryption_key': get_key()
        }
        file_path = os.path.join(os.getcwd(), 'encrypted_data.pkl')
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)
        st.session_state.file_saved = True
    except Exception as e:
        st.error(f"Failed to save data: {str(e)}")

# Load data from file with error handling
def load_from_file():
    try:
        file_path = os.path.join(os.getcwd(), 'encrypted_data.pkl')
        if Path(file_path).exists():
            with open(file_path, 'rb') as f:
                data = pickle.load(f)
                st.session_state.data_store = data['data_store']
                st.session_state.encryption_key = data['encryption_key']
    except Exception as e:
        st.error(f"Failed to load data: {str(e)}")

# Login page
def login_page():
    st.title("🔒 Re-authorization Required")
    st.warning("Too many failed attempts. Please login to continue.")
    
    login_passkey = st.text_input("Enter your master passkey:", 
                                type="password", 
                                key="master_passkey")
    
    if st.button("Login", key="login_btn"):
        if sha256(login_passkey.encode()).hexdigest() == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824":  # hello
            st.session_state.failed_attempts = 0
            st.session_state.locked_out = False
            st.rerun()
        else:
            st.error("Incorrect passkey. Try again.")

# Insert data page
def insert_data_page():
    st.title("🔐 Store New Data")
    
    data = st.text_area("Enter data to encrypt:", 
                      key="data_input")
    
    passkey = st.text_input("Create a passkey for this data:", 
                          type="password", 
                          key="new_passkey")
    
    if st.button("Encrypt and Store", key="store_btn"):
        if data and passkey:
            encrypted = encrypt_data(data, passkey)
            data_id = sha256(passkey.encode()).hexdigest()[:8]
            st.session_state.data_store[data_id] = encrypted.hex()
            save_to_file()
            
            st.success("Data stored successfully!")
            st.markdown(f"**Your Data ID:** `{data_id}`")
            st.info("Please save both your Data ID and passkey carefully.")
        else:
            st.warning("Please enter both data and passkey")

# Retrieve data page
def retrieve_data_page():
    st.title("🔓 Retrieve Encrypted Data")
    
    data_id = st.text_input("Enter your Data ID:", 
                          key="data_id_input")
    
    passkey = st.text_input("Enter your passkey:", 
                          type="password", 
                          key="retrieve_passkey")
    
    if st.button("Decrypt Data", key="decrypt_btn"):
        if st.session_state.locked_out:
            remaining_time = 30 - (time.time() - st.session_state.lockout_time)
            if remaining_time > 0:
                st.error(f"System locked. Try again in {int(remaining_time)} seconds.")
                return
            else:
                st.session_state.locked_out = False
                st.session_state.failed_attempts = 0
        
        if not data_id or not passkey:
            st.warning("Please enter both Data ID and passkey")
            return
            
        encrypted_hex = st.session_state.data_store.get(data_id)
        if not encrypted_hex:
            st.error("Data ID not found")
            return
            
        encrypted_data = bytes.fromhex(encrypted_hex)
        decrypted = decrypt_data(encrypted_data, passkey)
        
        if decrypted is not None:
            st.session_state.failed_attempts = 0
            st.success("✅ Decrypted Successfully")
            st.text_area("Decrypted Data:", 
                       value=decrypted, 
                       height=200,
                       key="decrypted_output")
        else:
            st.session_state.failed_attempts += 1
            if st.session_state.failed_attempts >= 3:
                st.session_state.locked_out = True
                st.session_state.lockout_time = time.time()
                st.error("❌ Too many failed attempts. System locked for 30 seconds.")
            else:
                st.error(f"❌ Incorrect passkey. {3 - st.session_state.failed_attempts} attempts remaining.")

# Main app
def main():
    # Debug info
    st.sidebar.write("Debug Info:")
    st.sidebar.write(f"Data entries: {len(st.session_state.data_store)}")
    
    load_from_file()
    
    if st.session_state.locked_out:
        if time.time() - st.session_state.lockout_time > 30:
            st.session_state.locked_out = False
            st.session_state.failed_attempts = 0
        else:
            login_page()
            return
    
    st.sidebar.title("Secure Data Vault")
    app_mode = st.sidebar.radio("Choose action:", 
                              ["Store Data", "Retrieve Data"],
                              key="app_mode")
    
    if app_mode == "Store Data":
        insert_data_page()
    else:
        retrieve_data_page()

if __name__ == "__main__":
    main()