import streamlit as st
import data_loading as load
import data_processing as process
from constants import major_leagues


# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(page_icon="⚙️", page_title="LoLStats Dashboard", layout="wide")

def main():
    raw = load.load_raw()
    patches = process.get_patches(raw)
    with st.form('Select data range'):
        leagues = st.multiselect('Select league range', options=process.get_leagues(raw), default=major_leagues)
        patch_start, patch_end = st.select_slider(label='Chose patch range', options=patches, value=(patches[0], patches[-1]))
        submit_form = st.form_submit_button('Submit choices')
    
    if submit_form:
        raw = process.select_on_leagues(process.select_on_patch(raw, patch_start, patch_end), leagues)
        macro_db = process.get_macro_db(raw)
        micro_db = process.get_micro_db(raw)
        stats = process.get_df_champions_statistics(micro_db)
        champions_df = process.champs_dataframe(micro_db, macro_db, stats)
        
        st.dataframe(champions_df)
    
    #st.image(load.im)
    return


if __name__ == "__main__":
    main()