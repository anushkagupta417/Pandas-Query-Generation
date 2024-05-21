import re
import os
import pandas as pd
import seaborn as sns
import torch
from DataLoader import create_csv
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from abc import ABC, abstractmethod

class MethodNotImplementedError(Exception):
    """
    Raised when a method is not implemented.

    Args:
        Exception (Exception): MethodNotImplementedError
    """


class QueryLanguage:
    """Base class to implement multiple querying languages"""

    @abstractmethod
    def load_model(self) -> object:
        """
        Load the corresponding model for query generation

        Raises:
            MethodNotImplementedError: load_model method has not been implemented
        """
        raise MethodNotImplementedError("load_model method has not been implemented")

    @abstractmethod
    def generate_query(
        self,
        textual_query: str,
        num_beams: int,
        max_length: int,
        repetition_penalty: int,
        length_penalty: int,
        early_stopping: bool,
        top_p: int,
        top_k: int,
        num_return_sequences: int,
    ) -> str:
        """
        Execute the CodeT5 to generate the query in the corresponding language.

        Raises:
            MethodNotImplementedError: generate_query method has not been implemented
        """
        raise MethodNotImplementedError(
            "generate_query method has not been implemented"
        )

    @abstractmethod
    def preprocess(self, text) -> str:
        """
        Pre-Process the user's textual query by converting all to lowercase and inserting columns/attributes/keys in the query itself.

        Raises:
            MethodNotImplementedError: load_model method has not been implemented
        """
        raise MethodNotImplementedError("load_model method has not been implemented")

class PandasQuery(QueryLanguage):
    """Base QueryLanguage class extended to perform query generation for Pandas"""

    def __init__(self, df: object, df_name: str, path: str = "MajorProject/nl2pandas"):
        """Constructor for PandasQuery class"""
        self.path = path
        self.df = df
        self.df_name = df_name
        self.col_mapping = {
            "'" + col.lower() + "'": "'" + col + "'" for col in self.df.columns
        }
        self._load_model()

    def _load_model(self) -> object:
        print(self.path)
        """Constructor for PandasQuery class"""
        model = AutoModelForSeq2SeqLM.from_pretrained(self.path)
        self.tokenizer = AutoTokenizer.from_pretrained(self.path)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = model.to(device)
        return self.model, self.tokenizer

    def preprocess(self, text: str) -> str:
        """Pre-Process the user's textual query by converting all the text to lowercase and inserting columns of dataframe in the query itself."""
        text = (
            "pandas: "
            + text
            + " | "
            + self.df_name
            + " : "
            + ", ".join(self.df.columns)
        )
        upper_text = {i.lower(): i for i in text.split() if i.lower() != i}

        # print(text.lower())
        return text.lower(), upper_text

        # return text

    def generate_query(
        self,
        textual_query: str,
        num_beams: int = 10,
        max_length: int = 128,
        repetition_penalty: int = 2.5,
        length_penalty: int = 1,
        early_stopping: bool = True,
        top_p: int = 0.95,
        top_k: int = 50,
        num_return_sequences: int = 1,
    ) -> str:
        """Execute the CodeT5 to generate the query for the pandas framework."""
        query, upper_text = self.preprocess(textual_query)
        input_ids = self.tokenizer.encode(
            query, return_tensors="pt", add_special_tokens=True
        )
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        input_ids = input_ids.to(device)

        generated_ids = self.model.generate(
            input_ids=input_ids,
            num_beams=num_beams,
            max_length=max_length,
            repetition_penalty=repetition_penalty,
            length_penalty=length_penalty,
            early_stopping=early_stopping,
            top_p=top_p,
            top_k=top_k,
            num_return_sequences=num_return_sequences,
        )
        query = [
            self.tokenizer.decode(
                generated_id,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=True,
            )
            for generated_id in generated_ids
        ][0]
        # print(query)
        pattern = "|".join(
            re.escape(key) for key in {**self.col_mapping, **upper_text}.keys()
        )
        query = re.sub(
            pattern, lambda x: {**self.col_mapping, **upper_text}[x.group()], query
        )

        return query

# input_file_path = 'sample_pvg.txt'
# new_csv_file_path = 'sample_data.csv'
# if not os.path.exists(new_csv_file_path):
#     create_csv(input_file_path)

# new_data = pd.read_csv(new_csv_file_path)

# # Use PandasQuery with the new data
# queryfier = PandasQuery(new_data, 'new_data')
# t=queryfier.generate_query("Select the records which have Frame Number less than 1")
# index_of_comma = t.find(',')
# if index_of_comma != -1:  # If comma exists in the string
#     modified_string = t[:index_of_comma] + "]"
# # Load the Titanic dataset
# new_data = pd.read_csv('/Users/anushkagupta/Desktop/Major Project/npToPandas/sample_data.csv')
# result = new_data.loc[lambda x: x['FRAME_ID'] < 1]
# # Display the result
# print(result)