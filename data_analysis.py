from logging import exception
from this import d
import streamlit as st
from PIL import Image
import cv2

def cv2_image_from_champion(champion_name, flag):
    try:
        return st.image(cv2.imread('champions_image/' + champion_name + 'Square.webp', flag))
    except Exception as e:
        return st.write(champion_name + ' has no stored image')

def image_from_champion(champion_name):
    try:
        return st.image(Image.open('champions_image/' + champion_name + 'Square.webp'))
    except Exception as e:
        return st.write(champion_name + ' has no stored image')


def presence_winrate_per_position(pos, top_champs_per_position, df):
    champions_shortlist = top_champs_per_position[pos]
    cols = st.columns(len(champions_shortlist))
    for i, champion in enumerate(champions_shortlist):
        with cols[i]:
            st.markdown(champion)
            image_from_champion(champion.replace(' ', '_').replace("'", "%27").replace(" & ", "_%26_"))
        
    st.dataframe(df[df.champion.isin(champions_shortlist)])