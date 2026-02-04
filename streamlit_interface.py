#date started: 3 feb 2026
#by: Batiste Decat
#status: not finished !!!!!
#notes: still learning streamlit library
from time import sleep

import atexit
import subprocess
import streamlit as st
import requests

st.title('BapiCoin', text_alignment="center")
st.header('A Minimal Educational Blockchain in Python')
st.subheader("features mining, transactions and viewing the full chain", divider="gray")

url = "https://bapicoin-blockchain.onrender.com"

# def start_bapicoin_node():
#     process = subprocess.Popen(["python", "bapicoin.py"])
#     return process
#
# def cleanup_node():
#     if "server_process" in st.session_state:
#         st.session_state.server_process.terminate()
#         #wait then force kill if needed
#         try:
#             st.session_state.server_process.wait(timeout=3)
#         except subprocess.TimeoutExpired:
#             st.session_state.server_process.kill()

def view_full_chain():
    if st.button("view full Chain"):
        with col1.container(height=600):
            chain_url = url + '/chain'
            response = requests.get(chain_url)
            st.json(response.text, expanded=False)

def mine_it():
    if st.button("mine"):
        chain_url = url + '/mine'
        with st.spinner("mining the block...", show_time=True):
            while True:
                response = requests.get(chain_url)
                if response.status_code == 200:
                    break
        st.json(response.text)

def transaction_form(form):
    temp_transaction = {
        "sender": "standard sender id",
        "recipient": "standard recipient id",
        "amount": 0.0
    }
    with st.form(form):
        st.write("Transaction Form")
        st.write('Please fill out the info below and submit your transaction into the transaction pool ;)')
        sender = st.text_input('Sender')
        recipient = st.text_input('Recipient')
        amount = st.number_input('amount')

        submitted = st.form_submit_button('--- register payment ---')
        if submitted:
            temp_transaction["sender"] = sender
            temp_transaction["recipient"] = recipient
            temp_transaction["amount"] = amount

            url_post = url + "/transactions/new"

            response = requests.post(url_post, json=temp_transaction)
            response.raise_for_status()
            json_response = response.json()

            progress_text = "Registering Payment, Please wait."
            my_bar = st.progress(0, text=progress_text)

            for percent_complete in range(100):
                sleep(0.005)
                my_bar.progress(percent_complete + 1, text=progress_text)
            sleep(1)
            my_bar.empty()

            st.success(json_response["message"], icon="✅")
            sleep(1.5)
            st.rerun()

###------------------------------------

# if "server_started" not in st.session_state:
#     with st.spinner("Starting the bapicoin node...", show_time=True):
#         st.session_state.server_process = start_bapicoin_node()
#         st.session_state.server_started = True
#
#         atexit.register(cleanup_node) #is there a zombie process? if yes than kill it
#
#         sleep(2)
#         st.toast('node succesfully initiated')

transaction_form("form_1")

col1, col2 = st.columns(2)
with col1:
    view_full_chain()

with col2:
    mine_it()

st.button('RESET', type="primary")