import pandas as pd


def generate_optimizer_data(data: pd.DataFrame) -> dict:
    optimizer_df = data.copy()
    optimizer_df['PLAYER'] = (
            optimizer_df['player_first_name'] +
            ' ' +
            optimizer_df['player_second_name']
    )
    players = optimizer_df['PLAYER'].to_list()
    clubs = optimizer_df['team_name'].unique().tolist()
    clubs.sort()
    positions = optimizer_df[
        ['position_id', 'player_position']
    ].drop_duplicates().sort_values('position_id')['player_position'].unique(
    ).tolist()
    positions.sort()
    index_cols = ['team_name', 'player_position', 'PLAYER']
    optimizer_df.set_index(index_cols, inplace=True)
    player_prices = optimizer_df['player_price'].to_dict()
    player_values = optimizer_df['player_total_points'].to_dict()
    required_players = {
        'Goalkeeper': 2,
        'Defender': 5,
        'Midfielder': 5,
        'Forward': 3,
    }
    team_size = 15
    team_budget = 1000
    single_club_max_players = 3

    optimizer_data = {
        None: {
            'CLUBS': {None: clubs},
            'POSITIONS': {None: positions},
            'PLAYERS': {None: players},
            'team_size': {None: team_size},
            'team_budget': {None: team_budget},
            'single_club_max_players':{None: single_club_max_players},
            'player_prices': player_prices,
            'player_values': player_values,
            'required_players': required_players,
        }
    }
    return optimizer_data
