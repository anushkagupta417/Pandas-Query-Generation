import pandas as pd
from DataLoader import create_csv  # Assuming this function now accepts a file-like object and returns a DataFrame
from nlp_query import PandasQuery
import os

def process_uploaded_file_and_query(filePath, user_query):
    """
    Takes an uploaded file and a query string from the user,
    processes the file to create a DataFrame, generates a query based on the user input,
    executes it, and returns the results.
    """
    try:
        new_csv_file_path = 'sample_data.csv'
        print(filePath, filePath.endswith('.txt'))
        if filePath.endswith('.txt'):
            print("check1")
            # Check if CSV file exists and create it if it doesn't
            if not os.path.exists(new_csv_file_path):
                print("check2")
                create_csv(filePath)
                # new_csv_file_path = 'sample_data.csv'
        else:
            new_csv_file_path = filePath

        # Load the new data
        print(new_csv_file_path)
        new_data = pd.read_csv(new_csv_file_path)
        # Initialize the query processing object
        queryfier = PandasQuery(new_data, 'new_data')
        # Generate the query
        generated_query = queryfier.generate_query(user_query)

        if generated_query.endswith(','):
            generated_query = generated_query[:-1]

        print("Final query:", generated_query)
        # Execute the query and return results
        result = eval(generated_query)  # Be cautious with eval()
        print(type(result))

        # Check if the result is not a DataFrame
        # if not isinstance(result, pd.DataFrame) or not isinstance(result, pd.Series):
        #     # Assuming the result can be converted to a string
        #     print("check3")
        #     result = str(result)
        # print(type(result))

        # Assuming the result is a DataFrame; if it's already a string, this line will have no effect
        return result
    except Exception as e:
        return f"Error processing query: {e}"

if __name__ == '__main__':
    print("This script is intended to be used as a module.")

#find the names and age of passengers with age greater than 35