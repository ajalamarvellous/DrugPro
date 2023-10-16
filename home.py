import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

FILE_PATH = "salesweekly.csv"

st.set_page_config(page_title="Homepage", page_icon="🏡", layout="centered")

@st.cache_data
def read_file(file, format):
    """Reads the file depending on the format specified"""
    try:
        if format == "excel":
            df = pd.read_xlsx(file, index_col)
        elif format == "csv":
            df = pd.read_csv(file)
    except:
        st.write("Seems an error occured, please try again")
    return df


def column_dtypes(df):
    """Group the columns based on the different datatypes"""
    columns = df.columns  # get columns
    dtypes = {}
    for col in columns:
        dtype = df[col].dtype.__str__()  # get the datatype and return as str
        if dtype in dtypes.keys(): # check if the data type already exist
            dtypes[dtype].append(col)  # add to the group if it exist
        else:
            dtypes[dtype] = [col]  # if it doesn't, create a new separate group


    if ("col_dtypes" not in st.session_state) or (st.session_state["col_dtypes"] != dtypes):
        st.session_state["col_dtypes"] = dtypes
    return dtypes


def parse_date(df, dtypes):
    # ask user to select which may be the date column
    date = st.selectbox("Which of these is the date column", ["None"] + dtypes["object"])
    if date != "None":
        df[date] = pd.to_datetime(df[date])  # pass as date if it is not null
        df = df.set_index(date)
    return df

def main():
    logo = Image.open('PHOTO-2023-09-30-22-48-20.jpg').crop((150, 120, 370, 340))

    st.image(logo)
    st.title("Hello there 👋, welcome to DrugPro")

    st.markdown(
        """
        Our goal at DrugPro is to reimagine how the pharma supply chain works \
        and a system **where every pill count** \n

        Our mission is simple *To empower pharmacies with latest technology in \
        artificial intelligence for precise drug ordering and data insights*
        """)


    st.sidebar.markdown("# Homepage")
    st.write("To get started, please upload your data and specify the data type")
    file = st.file_uploader("Please upload your file here")
    format = st.selectbox("What format is the data", ("csv", "excel"))


    if (file is not None) and (format is not None):
        data = read_file(file, format)
        col_dtypes = column_dtypes(data)
        data = parse_date(data, col_dtypes)
        if data not in st.session_state:
            st.session_state["data"] = data
        try:
            show_data_btn = st.toggle("Proceed to show data")
            if show_data_btn:
                st.table(data.head())
        except:
            st.write("Seems an error occured, maybe you haven't uploaded the file yet")



if __name__ == "__main__":
    main()
