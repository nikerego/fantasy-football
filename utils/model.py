import pyomo.environ as pyo
from pyomo.opt import SolverFactory
import requests
from utils.app_core import get_players_df
from utils.model_core import (
    generate_optimizer_data,
)

url = "https://fantasy.premierleague.com/api/bootstrap-static/"
response = requests.get(url)
status_code = response.status_code
response_json = {}
if status_code == 200:
    response_json = response.json()
players_df = get_players_df(data=response_json)
sample_data = generate_optimizer_data(players_df)

# Initialise a pyomo AbstractModel
team_model = pyo.AbstractModel()

# Sets:
team_model.CLUBS = pyo.Set(name="CLUBS")
team_model.POSITIONS = pyo.Set(name="POSITIONS")
team_model.PLAYERS = pyo.Set(name="PLAYERS")

# ===========================================================================
# Parameters:
# ===========================================================================

# Cost of selecting player in squad:
team_model.player_prices = pyo.Param(
    team_model.CLUBS,
    team_model.POSITIONS,
    team_model.PLAYERS,
    domain=pyo.Integers,
    initialize_as_dense=False,
    name='player_prices',
)

# Value of selecting player in squad:
team_model.player_values = pyo.Param(
    team_model.CLUBS,
    team_model.POSITIONS,
    team_model.PLAYERS,
    domain=pyo.Integers,
    initialize_as_dense=False,
    name='player_values',
)

# Required players in squad of a particular position:
team_model.required_players = pyo.Param(
    team_model.POSITIONS,
    domain=pyo.Integers,
    name='required_players'
)

# Max team size:
team_model.team_size = pyo.Param(
    domain=pyo.Integers,
    name='team_size'
)

# Team budget:
team_model.team_budget = pyo.Param(
    domain=pyo.Integers,
    name='team_budget'
)

# Single club maximum players:
team_model.single_club_max_players = pyo.Param(
    domain=pyo.Integers,
    name='single_club_max_players'
)

# ===========================================================================
# Decision Variables: If a player is selected in the squad
# ===========================================================================

team_model.players_selected = pyo.Var(
    team_model.CLUBS,
    team_model.POSITIONS,
    team_model.PLAYERS,
    domain=pyo.Integers,
    initialize=0,
    bounds=(0, 1),
    dense=False,
    name='players_selected',
)


# Objective Function:
def objective_rule(model: pyo.ConcreteModel) -> pyo.simple_objective_rule:
    team_value = 0
    for club in model.CLUBS:
        for position in model.POSITIONS:
            for player in model.PLAYERS:
                try:
                    team_value += (
                            model.player_values[club, position, player] *
                            model.players_selected[club, position, player]
                    )
                except ValueError:
                    continue
    return team_value


team_model.total_team_value = pyo.Objective(
    rule=objective_rule,
    sense=pyo.maximize,
)

# Constraints:
"""
# Selecting Your Initial Squad Size

To join the game select a fantasy football squad of 15 players, 
consisting of:

2 Goalkeepers
5 Defenders
5 Midfielders
3 Forwards

Budget
The total value of your initial squad must not exceed £100 million.

Players Per Team
You can select up to 3 players from a single Premier League team.

Source: https://fantasy.premierleague.com/help/rules
"""


# (1) Total Team Size:
def team_size_rule(model: pyo.ConcreteModel) -> pyo.simple_constraint_rule:
    return pyo.summation(model.players_selected) == model.team_size


team_model.team_size_constraint = pyo.Constraint(rule=team_size_rule)


# (2) Appropriate numbers of players in each position:
def required_players_in_positions_rule(
        model: pyo.ConcreteModel,
        position: str,
) -> pyo.simple_constraint_rule:
    total_players = 0
    for club in model.CLUBS:
        for position in model.POSITIONS:
            for player in model.PLAYERS:
                try:
                    total_players += (
                        model.players_selected[club, position, player]
                    )
                except ValueError:
                    continue
    return total_players == model.required_players[position]


team_model.required_players_in_positions_constraint = pyo.Constraint(
    team_model.PLAYERS,
    rule=required_players_in_positions_rule,
)


# (3) Appropriate numbers of players from each club:
def max_players_in_club_rule(
        model: pyo.ConcreteModel,
) -> pyo.simple_constraint_rule:
    total_players = 0
    for club in model.CLUBS:
        for position in model.POSITIONS:
            for player in model.PLAYERS:
                try:
                    total_players += (
                        model.players_selected[club, position, player]
                    )
                except ValueError:
                    continue
        return total_players <= model.single_club_max_players


team_model.max_players_in_position_constraint = pyo.Constraint(
    rule=max_players_in_club_rule,
)


# (4) Budget:
def team_budget_rule(
        model: pyo.ConcreteModel,
) -> pyo.simple_constraint_rule:
    team_price = 0
    for club in model.CLUBS:
        for position in model.POSITIONS:
            for player in model.PLAYERS:
                try:
                    team_price += (
                            model.player_prices[club, position, player] *
                            model.players_selected[club, position, player]
                    )
                except ValueError:
                    continue
    return team_price <= model.team_budget


concrete_model = team_model.create_instance(sample_data)

concrete_model.pprint()

# Solve:
solver = SolverFactory('glpk')
results = solver.solve(concrete_model)  # tee=True will display solver output

final_team = {
    p: bool(v)
    for p, v in concrete_model.players_selected.extract_values().items()
    if v == 1
 }