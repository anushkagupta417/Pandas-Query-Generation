import streamlit as st
import generate_query
import os 


def main():
    st.title("Data Query Chatbot")

    # User uploads a data file
    uploaded_file = st.file_uploader("Upload your data file here:", type=["txt", "csv"])
    if uploaded_file is not None:
    # To read file as string:
        string_data = uploaded_file.getvalue().decode("utf-8")
        
        # To save the file to a new path:
        filePath =  f'/Users/anushkagupta/Desktop/Major Project/npToPandas/{uploaded_file.name}'
        with open(os.path.join(filePath), "wb") as f:
            f.write(uploaded_file.getbuffer())
        
    # User inputs a query
    user_query = st.text_input("Enter your query here:")

    if st.button("Execute Query"):
        if uploaded_file is not None and user_query:
            # Convert the uploaded file to a CSV and execute the query
            response = generate_query.process_uploaded_file_and_query(filePath, user_query)
            st.text_area("Query Result", value=response, height=300, max_chars=None, key=None)
        else:
            st.warning("Please upload a file and enter a query.")

if __name__ == "__main__":
    main()
