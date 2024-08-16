import pandas as pd
from pyomo.opt import SolverFactory
import requests
import streamlit as st
from utils.endpoints import endpoints
from utils.model_core import generate_optimizer_data
from utils.model import model
from utils.app_core import get_players_df
from datetime import datetime as dt
# Inject CSS into the Streamlit app
st.set_page_config(
    page_title="Squad Optimizer",
    page_icon="📈",
    layout="wide",
)


# Inject CSS into the Streamlit app
with open('.streamlit/styles.css') as f:
    css = f.read()

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


@st.cache_data
def fetch_fpl_data():
    with st.spinner('Making FPL API Request ...'):
        url = endpoints.get('general_information').get('url')
        response = requests.get(url)
        status_code = response.status_code
        if status_code == 200:
            response_json = response.json()
            df = get_players_df(response_json)
        else:
            st.error("Failed to fetch data from the FPL API.")
            df = None
    if df is not None:
        snapshot = dt.now()
        df['snapshot'] = snapshot
        st.success(f'Player data available as of '
                   f'{snapshot.strftime("%Y-%m-%d %H:%M:%S")}')
    return df


progress_bar = st.progress(0)
players_df = fetch_fpl_data()
progress_bar.progress(20)
st.dataframe(players_df)

submit_click = st.sidebar.button('Optimize Squad!')
if submit_click:
    optimizer_input = generate_optimizer_data(players_df)
    progress_bar.progress(40)
    team_model = model.create_instance(optimizer_input)
    progress_bar.progress(50)
    solver = SolverFactory('cbc')
    results = solver.solve(team_model)
    progress_bar.progress(90)
    final_team = {
        p: bool(v)
        for p, v in team_model.players_selected.extract_values().items()
        if v == 1
    }
    selected_team_df = pd.DataFrame(final_team, index=[0]).T
    selected_team_df.reset_index(inplace=True)
    selected_team_df.rename(
        columns={
            'level_0': 'Club',
            'level_1': 'Position',
            'level_2': 'Player',
            0: 'Selected',
        },
        inplace=True,
    )
    st.subheader('Fantasy Team')
    st.dataframe(selected_team_df)
    progress_bar.progress(100)

st.sidebar.image('assets/premier-league-2-logo.png', width=150)
