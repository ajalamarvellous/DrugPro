import streamlit as st
import matplotlib.pyplot as plt
#

def analytics():
    st.markdown("# Analytic 📈")
    st.sidebar.markdown("# analytic 📈")
    data = st.session_state.data
    question = st.selectbox("Desired analytics", [
        "Please make a selection",
        "Comparism of multiple product sales",
        "Sales trend of a particular product",
        "Best selling product",
        "Worst selling product"
    ])
    if question == "Please make a selection":
        pass
    elif question == "Sales trend of a particular product":
        columns = st.session_state.data.columns
        product = st.selectbox("Select products to compare", columns, key="01y384hf4f")
        start_date = st.date_input("Frome what date")
        end_date = st.date_input("To what date")
        show_plot = st.toggle("Show plot")
        if show_plot:
            data_1 = data.loc[start_date:end_date]
            st.line_chart(data_1[product])
            plt.show()
    elif question == "Comparism of multiple product sales":
        products = st.multiselect("Select products to compare", st.session_state.data.columns, key="uiefjbkvfk")
        start_date = st.date_input("Frome what date")
        end_date = st.date_input("To what date")
        show_plot = st.toggle("Show plot")
        if show_plot:
            data_1 = data.loc[start_date:end_date]
            st.line_chart(data_1[products])
    elif question == "Best selling product":
        start_date = st.date_input("Frome what date")
        end_date = st.date_input("To what date")
        number = int(st.number_input("Number of top values to check"))
        data_1 = data.loc[start_date:end_date]
        if number < 1:
            d = data_1.sum().sort_values(ascending=False)[:3]
        else:
            d = data_1.sum().sort_values(ascending=False)[:number]
        show_plot = st.toggle("Show plot")
        if show_plot:
            st.bar_chart(d)
    elif question == "Worst selling product":
        start_date = st.date_input("Frome what date")
        end_date = st.date_input("To what date")
        number = int(st.number_input("Number of least values to check"))
        data_1 = data.loc[start_date:end_date]
        if number < 1:
            d = data_1.sum().sort_values(ascending=True)[:3]
        else:
            d = data_1.sum().sort_values(ascending=True)[:number]
        show_plot = st.toggle("Show plot")
        if show_plot:
            st.bar_chart(d)

if __name__ == "__main__":
    analytics()
