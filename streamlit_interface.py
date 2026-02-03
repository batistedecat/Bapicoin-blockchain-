#date started: 3 feb 2026
#by: Batiste Decat
#status: not finished !!!!!
#notes: still learning streamlit library



import streamlit as st
import requests

st.title('BapiCoin', text_alignment="center")
st.header('A Minimal Educational Blockchain in Python')

url = "http://127.0.0.1:5001"
st.button('RESET Buttons', type="primary")

col1, col2 = st.columns(2)
with col1:
    if st.button("view full Chain"):
        chain_url = url + '/chain'
        response = requests.get(chain_url)
        st.json(response.text)

with col2:
    if st.button("mine"):
        chain_url = url + '/mine'
        response = requests.get(chain_url)
        st.json(response.text)

### need to add a way to perform a transaction