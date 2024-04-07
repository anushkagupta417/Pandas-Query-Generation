import pandas as pd
import numpy as np
import re

def create_csv(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    third_line = lines[2]
    num_cols = int(third_line)

    col_names = []
    for i in range(num_cols):
        col_names.append(lines[3 + i])

    df = pd.read_csv(file_path, delimiter='\s+', skiprows=3 + num_cols + 16, header=None)
    df = df.drop(df.index[-1])

    df_cols = ["Date", "Time", "Frame_Number"]

    pattern = r'\{([^}]+)\}'
    extracted_strings = [re.search(pattern, col_name).group(1).strip() for col_name in col_names]
    df_cols.extend(extracted_strings)
    df.columns = df_cols
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S:%f', errors='coerce')
    df['Frame_Number'] = df['Frame_Number'].astype(int)
    
    output_file_path = "sample_data.csv"
    df.to_csv(output_file_path,index=False)
    print(f"CSV file created at {output_file_path}")
