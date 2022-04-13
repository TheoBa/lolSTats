import streamlit as st
from PIL import Image
import cv2
import plotly.express as px
from utils import IMAGE_FOLDER


def cv2_image_from_champion(champion_name, flag):
    try:
        return st.image(cv2.imread(f'{IMAGE_FOLDER}/{champion_name}.png', flag))
    except Exception as _:
        return st.write(champion_name + ' has no stored image')


def image_from_champion(champion_name):
    try:
        return st.image(Image.open(f'{IMAGE_FOLDER}/{champion_name}.png'))
    except Exception as _:
        return st.write(champion_name + ' has no stored image')


def get_plot_champions(df, champions, axis1, axis2):
    fig = px.scatter(df, x=axis1, y=axis2, 
                     hover_name="champion", 
                     hover_data=["damageshare", "golddiffat15"],
                     width=500, height=500
    )
    for champion_name in champions:
        fig.add_layout_image(dict(
            source=f'{IMAGE_FOLDER}/{champion_name}.png',
            x=0.75,
            y=0.65,
        ))
    return fig


def presence_winrate_per_position(pos, top_champs_per_position, df):
    champions_shortlist = top_champs_per_position[pos]

    st.plotly_chart(
        get_plot_champions(df[df.champion.isin(champions_shortlist)],champions_shortlist, 'presence', 'winrate'),
                    #use_container_width=True
        )

    cols = st.columns(len(champions_shortlist))
    for i, champion in enumerate(champions_shortlist):
        with cols[i]:
            st.markdown(champion)
            image_from_champion(champion)

    #st.dataframe(df[df.champion.isin(champions_shortlist)])
