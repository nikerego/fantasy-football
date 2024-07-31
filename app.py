import streamlit as st
from utils.endpoints import endpoints
import requests


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
    if response.status_code == 200:
        st.json(response.json())


if __name__ == '__main__':
    pass
