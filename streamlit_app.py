import streamlit as st
import data_loading as load



# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(page_icon="⚙️", page_title="DBT Dashboard", layout="wide")

def main():
    st.dataframe(load.raw_2021)
    return


if __name__ == "__main__":
    main()