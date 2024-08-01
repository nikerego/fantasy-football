import pandas as pd


def get_positions_df(data: dict) -> pd.DataFrame:
    positions_df = pd.DataFrame(data.get('element_types'))
    positions_df = positions_df[[
        'id', 'singular_name_short', 'singular_name', 'squad_select',
        'squad_min_select', 'squad_max_select', 'squad_min_play',
        'squad_max_play', 'element_count',
    ]]

    position_df_column_names = {
        'id': 'position_id',
        'singular_name_short': 'position_name_short',
        'singular_name': 'position_name',
        'element_count': 'total_players',
    }
    positions_df.rename(columns=position_df_column_names, inplace=True)
    positions_df.sort_values(by="position_id", inplace=True)
    return positions_df


def get_teams_df(data: dict) -> pd.DataFrame:
    teams_df = pd.DataFrame(data.get('teams'))
    teams_df = teams_df[[
        'id', 'position', 'short_name', 'name', 'form', 'played', 'win',
        'draw', 'loss', 'points', 'strength', 'strength_overall_home',
        'strength_overall_away', 'strength_attack_home',
        'strength_attack_away', 'strength_defence_home',
        'strength_defence_away', 'team_division', 'unavailable', 'code',
        'pulse_id',
    ]]
    teams_df_column_names = {
        'id': 'team_id',
        'short_name': 'team_name_short',
        'name': 'team_name',
    }
    teams_df.rename(columns=teams_df_column_names, inplace=True)
    teams_df.sort_values(by="position", inplace=True)
    return teams_df


def get_players_df(data: dict) -> pd.DataFrame:
    positions_df = get_positions_df(data)
    teams_df = get_teams_df(data)
    players_df = pd.DataFrame(data.get('elements'))
    return players_df





