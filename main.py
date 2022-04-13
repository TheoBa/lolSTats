from re import sub
import streamlit as st
import data_loading as load
import data_processing as process
from constants import major_leagues
import data_analysis as analysis

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(page_icon="⚙️", page_title="LoLStats Dashboard", layout="wide")

st.title('LolStats')
st.markdown('Welcome to LolStats, an interactive webapp for competitive league of legends data exploration')


def main_position():
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


def main_team():
    raw = load.load_raw()
    patches = process.get_patches(raw)
    with st.form('Select data range'):
        patch_start, patch_end = st.select_slider(
            label='Chose patch range',
            options=patches,
            value=(patches[0], patches[-1])
        )
        leagues = st.multiselect('Select league range', options=process.get_leagues(raw), default=major_leagues)
        submit_form = st.form_submit_button('Submit choices')
    
    if submit_form:
        raw = process.select_on_leagues(process.select_on_patch(raw, patch_start, patch_end), leagues)
        macro_db = process.get_macro_db(raw)
        stats = process.get_df_team_statistics(macro_db)
        top_teams_per_league = process.get_top_team_per_league(stats) 

        for league in leagues:
            with st.expander('+ Pick analysis for the ' + league + ' league'):
                analysis.winrate_side_per_league(league, top_teams_per_league, stats)

        
            


st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">',
    unsafe_allow_html=True,
)
query_params = st.experimental_get_query_params()
tabs = ["Position analysis", "Team analysis", "Player visualization"]
if "tab" in query_params:
    active_tab = query_params["tab"][0]
else:
    active_tab = "Position analysis"

if active_tab not in tabs:
    st.experimental_set_query_params(tab="Position analysis")
    active_tab = "Position analysis"

li_items = "".join(
    f"""
    <li class="nav-item">
        <a class="nav-link{' active' if t==active_tab else ''}" href="/?tab={t}">{t}</a>
    </li>
    """
    for t in tabs
)
tabs_html = f"""
    <ul class="nav nav-tabs">
    {li_items}
    </ul>
"""

st.markdown(tabs_html, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

if active_tab == "Position analysis":
    main_position()
elif active_tab == "Team analysis":
    main_team()
elif active_tab == "Player visualization":
    st.write("If you'd like to contact me, then please don't.")
else:
    st.error("Something has gone terribly wrong.")

#if __name__ == "__main__":
    #main()
