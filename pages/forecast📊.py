import streamlit as st
import pandas as pd
from catboost import CatBoostRegressor
import matplotlib.pyplot as plt

TRAIN_SIZE = 0.7

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
    return dtypes

@st.cache_resource
def train_data(df, parameter_tune=False):
    train_size= int(len(df) * TRAIN_SIZE)
    train, test = df.iloc[:train_size], df.iloc[train_size:]
    x_train, y_train = process_data(train, train=True)
    x_test, y_test = process_data(train, train=True)
    col_dtypes = column_dtypes(x_train)
    if not parameter_tune:
        model = CatBoostRegressor(random_state=2023, cat_features=col_dtypes["object"], iterations=100, learning_rate=0.1, depth= 3)
        model.fit(x_train, y_train)
        return model


def process_data(df, train=False):
    df = df.reset_index()
    if train:
        df = df.melt(id_vars=["datum"], var_name="drugclass", value_name="salesvolume")
    #Get day of month as integer
    df['date_of_month']=df['datum'].dt.day
    #Check for week in the year
    df['week_of_the_year']=df['datum'].dt.isocalendar().week
    #Get month of the year
    df['month_name']=df['datum'].dt.month_name()
    #Get year of the date
    df['year']=df['datum'].dt.year
    if train:
        return df.drop("salesvolume", axis=1), df["salesvolume"].values
    return df


def main():
    st.markdown("# Forecast📊")
    st.sidebar.markdown("# Forecast📊")
    data = st.session_state.data
    model = train_data(data)
    product = st.selectbox("which product do you want to forecast", ["None"] + list(data.columns))
    duration = int(st.number_input("For how long (in weeks)"))
    if product == "None":
        pass
    else:
        pred_data = pd.DataFrame()
        pred_data["datum"] = pd.date_range(start=data.index.max(), periods=duration*7)
        pred_data["drugclass"] = product
        pred_data = pred_data.set_index("datum")
        pred_data_ = process_data(pred_data)
        # if st.toggle("Show data"):
        #     st.table(data[product].head())
        #     st.table(pred_data.head())

        pred_data["forecast"] = model.predict(pred_data_)
        st.metric(f"Quantity to order for the next {duration} weeks", int(pred_data["forecast"].sum())
        if st.toggle("Show forecast for those weeks"):

            #  st.line_chart(data[product], color="#fd0")
            st.line_chart(pred_data["forecast"], color="#04f")


if __name__ == "__main__":
    main()
