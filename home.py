import streamlit as st
import pandas as pd

FILE_PATH = "salesweekly.csv"

def read_file(FILEPATH):
    return pd.read_csv(FILEPATH)


def main():
    st.title("Here is our homepage")
    df = read_file(FILE_PATH)
    if st.checkbox("show data"):
        st.table(df.head())

if __name__ == "__main__":
    main()
