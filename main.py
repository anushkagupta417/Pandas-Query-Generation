import streamlit as st
import generate_query
import os 
import pandas as pd
from io import BytesIO


def main():
    st.title("Data Query Chatbot")
    print("=======")
    # User uploads a data file
    uploaded_file = st.file_uploader("Upload your data file here:", type=["txt", "csv"])
    if uploaded_file is not None:
    # To read file as string:
        string_data = uploaded_file.getvalue().decode("utf-8")
        print("=======")
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
            print("type",type(response))
            st.text_area("Query Result", value=str(response), height=300, max_chars=None, key=None)
            print(type(response))
            if  isinstance(response, pd.DataFrame) or  isinstance(response, pd.Series):
                to_excel = convert_df_to_excel(response)
                st.download_button(label="📥 Download Result as Excel",
                                        data=to_excel,
                                        file_name='query_results.xlsx')

        else:
            st.warning("Please upload a file and enter a query.")

def convert_df_to_excel(df):
    """
    Converts a DataFrame into an Excel file stream.
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
    processed_data = output.getvalue()
    return processed_data
    # filepath = 'result.xlsx'
    # df.to_excel(filepath)
    # return filepath

if __name__ == "__main__":
    main()
