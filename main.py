# main.py
import os
import re
import pandas as pd
from DataLoader import create_csv
from nlp_query import PandasQuery

def validate_and_correct_query(query, df):
    """
    Corrects the query by ensuring only valid columns are included for selection.
    If the query contains a selection of non-existent columns, those are removed.
    """
    # Detect if a column selection part exists in the query
    selection_pattern = re.compile(r",\s*\['(.*?)'\]")
    print(selection_pattern)
    selection_match = selection_pattern.search(query)
    print(selection_match)
    
    if selection_match:
        # Extract columns from the selection part of the query
        columns_in_query = selection_match.group(1).split("', '")
        
        # Get actual column names from the DataFrame
        actual_columns = df.columns.tolist()
        
        # Keep only those columns that actually exist in the DataFrame
        valid_columns = [col for col in columns_in_query if col in actual_columns]
        
        # If no valid columns were found in the query, remove the selection part entirely
        if not valid_columns:
            query = selection_pattern.sub("", query)
        else:
            # Otherwise, replace the selection part with the corrected, valid columns
            corrected_columns_str = "', '".join(valid_columns)
            query = selection_pattern.sub(f", ['{corrected_columns_str}']", query)
    
    return query


def main():
    input_file_path = 'sample_pvg.txt'
    new_csv_file_path = 'sample_data.csv'

    # Check if CSV file exists and create it if it doesn't
    if not os.path.exists(new_csv_file_path):
        create_csv(input_file_path)

    # Load the new data
    new_data = pd.read_csv(new_csv_file_path)

    column_list = new_data.columns.tolist()
    # Initialize the PandasQuery object with the new data
    queryfier = PandasQuery(new_data, 'new_data')

    # Generate the query
    generated_query = queryfier.generate_query("show rows with frame number less than 1")

    # Check and remove unwanted reference to 'unnamed'
    # if "'unnamed'" in generated_query:
    #     generated_query = generated_query.replace(", 'unnamed'", "")  # Remove if it's part of a selection
    #     generated_query = generated_query.replace("'unnamed'", "")    # Remove if it's the only selection
    
    # Further trimming if necessary

    final_query = validate_and_correct_query(generated_query, new_data)

    if generated_query.endswith(','):
        generated_query = generated_query[:-1]

    print("Final query:", generated_query)

    # Execute the corrected generated query
    try:
        result = eval(generated_query)
        print(result)
    except Exception as e:
        print(f"Error executing generated query: {e}")

if __name__ == '__main__':
    main()
