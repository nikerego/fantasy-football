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
        'singular_name_short': 'player_position_short',
        'singular_name': 'player_position',
        'element_count': 'total_players',
    }
    positions_df.rename(columns=position_df_column_names, inplace=True)
    positions_df.sort_values(by="position_id", inplace=True)
    positions_df = positions_df.convert_dtypes()
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
        'position': 'team_position',
        'short_name': 'team_name_short',
        'name': 'team_name',
        'form': 'team_form',
        'points': 'team_points',
        'code': 'team_code',
    }
    teams_df.rename(columns=teams_df_column_names, inplace=True)
    teams_df.sort_values(by="team_position", inplace=True)
    teams_df = teams_df.convert_dtypes()
    return teams_df


def get_players_df(data: dict) -> pd.DataFrame:
    positions_df = get_positions_df(data)
    positions_df = positions_df[['position_id', 'player_position']]
    teams_df = get_teams_df(data)
    teams_df = teams_df[
        ['team_id', 'team_position', 'team_name_short', 'team_name']
    ]
    players_df = pd.DataFrame(data.get('elements'))
    players_df = players_df.convert_dtypes()
    players_df = players_df[[
        'id',
        'first_name',
        'second_name',
        'web_name',
        'team_code',
        'team',
        'element_type',
        'total_points',
        'now_cost',
        'points_per_game',
        'points_per_game_rank',
        'selected_rank',
        'selected_by_percent',
        'status',
        'transfers_in',
        'chance_of_playing_next_round',
        'chance_of_playing_this_round',
        'news',
        'news_added',
        'squad_number',
        'transfers_in_event',
        'transfers_out',
        'transfers_out_event',
        'value_form',
        'value_season',
        'minutes',
        'goals_scored',
        'assists',
        'clean_sheets',
        'goals_conceded',
        'own_goals',
        'penalties_saved',
        'penalties_missed',
        'yellow_cards',
        'red_cards',
        'saves',
        'bonus',
        'bps',
        'influence',
        'creativity',
        'threat',
        'ict_index',
        'ict_index_rank',
        'ict_index_rank_type',
        'starts',
        'expected_goals',
        'expected_assists',
        'expected_goal_involvements',
        'expected_goals_conceded',
        'influence_rank',
        'influence_rank_type',
        'creativity_rank',
        'creativity_rank_type',
        'threat_rank',
        'threat_rank_type',
        'corners_and_indirect_freekicks_order',
        'corners_and_indirect_freekicks_text',
        'direct_freekicks_order',
        'direct_freekicks_text',
        'penalties_order',
        'penalties_text',
        'expected_goals_per_90',
        'saves_per_90',
        'expected_assists_per_90',
        'expected_goal_involvements_per_90',
        'expected_goals_conceded_per_90',
        'goals_conceded_per_90',
        'now_cost_rank',
        'now_cost_rank_type',
        'form_rank',
        'form_rank_type',
        'points_per_game_rank_type',
        'selected_rank_type',
        'starts_per_90',
        'clean_sheets_per_90',
        'cost_change_event',
        'cost_change_event_fall',
        'cost_change_start',
        'cost_change_start_fall',
        'dreamteam_count',
        'ep_next',
        'ep_this',
        'event_points',
        'form',
        'in_dreamteam',
        'photo',
        'special',
        'code',
    ]]
    players_df_column_names = {
        'id': 'player_id',
        'first_name': 'player_first_name',
        'second_name': 'player_second_name',
        'web_name': 'player_web_name',
        'team': 'team_id',
        'total_points': 'player_total_points',
        'element_type': 'position_id',
        'form': 'player_form',
        'code': 'player_code',
        'now_cost': 'player_price',
    }
    players_df.rename(columns=players_df_column_names, inplace=True)
    players_df = pd.merge(
        left=players_df,
        right=teams_df,
        on="team_id",
        how="inner",
    )
    players_df = pd.merge(
        left=players_df,
        right=positions_df,
        on="position_id",
        how="inner",
    )
    players_df.sort_values(
        by="player_total_points",
        ascending=False,
        inplace=True,
    )

    players_df['player_price'] = players_df['player_price']/10.0

    players_df = players_df[[
        'player_id',
        'player_first_name',
        'player_second_name',
        'player_web_name',
        'player_position',
        'team_name',
        'team_position',
        'team_name_short',
        'player_total_points',
        'player_price',
        'points_per_game',
        'points_per_game_rank',
        'selected_rank',
        'selected_by_percent',
        'status',
        'transfers_in',
        'chance_of_playing_next_round',
        'chance_of_playing_this_round',
        'news',
        'news_added',
        'squad_number',
        'transfers_in_event',
        'transfers_out',
        'transfers_out_event',
        'value_form',
        'value_season',
        'minutes',
        'goals_scored',
        'assists',
        'clean_sheets',
        'goals_conceded',
        'own_goals',
        'penalties_saved',
        'penalties_missed',
        'yellow_cards',
        'red_cards',
        'saves',
        'bonus',
        'bps',
        'influence',
        'creativity',
        'threat',
        'ict_index',
        'ict_index_rank',
        'ict_index_rank_type',
        'starts',
        'expected_goals',
        'expected_assists',
        'expected_goal_involvements',
        'expected_goals_conceded',
        'influence_rank',
        'influence_rank_type',
        'creativity_rank',
        'creativity_rank_type',
        'threat_rank',
        'threat_rank_type',
        'corners_and_indirect_freekicks_order',
        'corners_and_indirect_freekicks_text',
        'direct_freekicks_order',
        'direct_freekicks_text',
        'penalties_order',
        'penalties_text',
        'expected_goals_per_90',
        'saves_per_90',
        'expected_assists_per_90',
        'expected_goal_involvements_per_90',
        'expected_goals_conceded_per_90',
        'goals_conceded_per_90',
        'now_cost_rank',
        'now_cost_rank_type',
        'form_rank',
        'form_rank_type',
        'points_per_game_rank_type',
        'selected_rank_type',
        'starts_per_90',
        'clean_sheets_per_90',
        'cost_change_event',
        'cost_change_event_fall',
        'cost_change_start',
        'cost_change_start_fall',
        'dreamteam_count',
        'ep_next',
        'ep_this',
        'event_points',
        'player_form',
        'in_dreamteam',
        'photo',
        'special',
        'player_code',
        'team_code',
        'team_id',
        'position_id',
    ]]

    return players_df
