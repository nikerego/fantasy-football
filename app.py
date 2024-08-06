import streamlit as st
import pandas as pd
from utils.endpoints import endpoints
from utils.app_core import (
    get_positions_df,
    get_teams_df,
    get_players_df,

)
import requests

st.set_page_config(
    page_title="API",
    page_icon="⚙️",
    layout="wide",
)

# Inject CSS into the Streamlit app
# with open('.streamlit/styles.css') as f:
#     css = f.read()
# st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

endpoint = st.sidebar.selectbox('Endpoint', endpoints.keys())

if endpoint == 'individual_players':
    url_key = st.sidebar.selectbox(
        'URL:',
        endpoints.get(endpoint).get('urls').keys(),
    )
    url = endpoints.get(endpoint).get('urls').get(url_key).get('url')
    if url_key == 'player-id':
        player_id = st.sidebar.text_input('Player ID:')
        url = url.format(player_id=player_id)
    else:
        gw = st.sidebar.text_input('Game Week:')
        url = url.format(gw=gw)

elif endpoint == 'individual_managers':
    url_key = st.sidebar.selectbox(
        'URL:',
        endpoints.get(endpoint).get('urls').keys(),
    )
    url = endpoints.get(endpoint).get('urls').get(url_key).get('url')
    team_id = st.sidebar.text_input('Team ID:')
    if url_key == 'team-id/game-week/picks':
        gw = st.sidebar.text_input('Game Week:')
        url = url.format(team_id=team_id, gw=gw)
    else:
        url = url.format(team_id=team_id)

elif endpoint == 'leagues':
    league = st.sidebar.selectbox('League:', endpoints.get(endpoint).keys())
    league_id = st.sidebar.text_input('League ID:')
    url = endpoints.get(endpoint).get(league).get('url')
    url = url.format(league_id=league_id)

else:
    url = endpoints.get(endpoint).get('url')


submit_click = st.sidebar.button('Submit')

if submit_click:
    response = requests.get(url)
    status_code = response.status_code
    if status_code == 200:
        response_json = response.json()

# General Info:
    if endpoint == 'general_information':

        # Teams
        st.subheader('Team Information:')
        teams_df = get_teams_df(data=response_json)
        st.dataframe(teams_df, hide_index=True)

        # Player Information
        st.subheader('Player Information:')
        players_df = get_players_df(data=response_json)
        st.dataframe(players_df, hide_index=True)

        # Positions
        st.subheader('Player Position Information:')
        positions_df = get_positions_df(data=response_json)
        st.dataframe(positions_df, hide_index=True)

    else:
        st.json(response_json)


if __name__ == '__main__':
    pass
