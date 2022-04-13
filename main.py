import streamlit as st
import data_loading as load
import data_processing as process
from constants import major_leagues
import data_analysis as analysis

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(page_icon="⚙️", page_title="LoLStats Dashboard", layout="wide")

st.title('LolStats')
st.markdown('Welcome to LolStats, an interactive webapp for competitive league of legends data exploration')


def main():
    raw = load.load_raw()
    patches = process.get_patches(raw)
    with st.form('Select data range'):
        patch_start, patch_end = st.select_slider(
            label='Chose patch range',
            options=patches,
            value=(patches[0], patches[-1])
        )
        leagues = st.multiselect('Select league range', options=process.get_leagues(raw), default=major_leagues)
        positions = st.multiselect('Select positions you want to study', options=['top', 'jng', 'mid', 'bot', 'sup'], default=['top', 'jng']) 
        submit_form = st.form_submit_button('Submit choices')

    if submit_form:
        raw = process.select_on_leagues(process.select_on_patch(raw, patch_start, patch_end), leagues)
        macro_db = process.get_macro_db(raw)
        micro_db = process.get_micro_db(raw)
        stats = process.get_df_champions_statistics(micro_db)
        champions_df = process.champs_dataframe(micro_db, macro_db, stats)
        top_champs_per_position = process.get_top_champs_per_position(micro_db)

        for pos in positions:
            with st.expander('+ Pick analysis for ' + pos + ' position'):
                analysis.presence_winrate_per_position(pos, top_champs_per_position, champions_df)


if __name__ == "__main__":
    main()
