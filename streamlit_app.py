import streamlit as st
import data_loading as load



# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(page_icon="⚙️", page_title="DBT Dashboard", layout="wide")

def main():
    st.dataframe(load.raw)
    patch_range = st.slider(label= 'Chose patch range', min_value=load.raw.patch.min(), max_value=load.raw.patch.max(), value=[12., load.raw.patch.max()])
    st.markdown(patch_range)
    return


if __name__ == "__main__":
    main()