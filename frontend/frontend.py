import streamlit as st
import requests
import pandas as pd

# URL of the Flask backend
API_URL = "http://backend:5000"

# CSV upload functionality
st.title('CSV Upload and Query App')
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    table_name = st.text_input("Enter a table name for the CSV", "")
    if table_name:
        response = requests.post(
            f"{API_URL}/upload",
            files={"file": uploaded_file},
            data={"table_name": table_name}
        )
        if response.status_code == 200:
            st.success("CSV uploaded successfully!")
        else:
            st.error("Upload failed.")

# Display tables in the public schema
if st.button('Show Tables'):
    response = requests.get(f"{API_URL}/tables")
    tables = response.json()
    st.write("Tables in the public schema:")
    st.write(tables)

# SQL query functionality
query = st.text_area("Enter your SQL query:")
if st.button('Run Query'):
    response = requests.post(
        f"{API_URL}/query", json={"query": query}
    )
    if response.status_code == 200:
        results = response.json()['results']
        st.write(pd.DataFrame(results))
    else:
        st.error("Query execution failed.")
