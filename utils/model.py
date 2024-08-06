import pyomo.environ as pyo

# ===========================================================================
# pyomo AbstractModel
# ===========================================================================
model = pyo.AbstractModel()

# ===========================================================================
# Sets:
# ===========================================================================
model.CLUBS = pyo.Set(name="CLUBS")
model.POSITIONS = pyo.Set(name="POSITIONS")
model.PLAYERS = pyo.Set(name="PLAYERS")

# ===========================================================================
# Parameters:
# ===========================================================================

# Cost of selecting player in squad:
model.player_prices = pyo.Param(
    model.CLUBS,
    model.POSITIONS,
    model.PLAYERS,
    domain=pyo.NonNegativeReals,
    initialize_as_dense=False,
    name='player_prices',
)

# Value of selecting player in squad:
model.player_values = pyo.Param(
    model.CLUBS,
    model.POSITIONS,
    model.PLAYERS,
    domain=pyo.Reals,
    initialize_as_dense=False,
    name='player_values',
)

# Required players in squad of a particular position:
model.required_players = pyo.Param(
    model.POSITIONS,
    domain=pyo.Integers,
    name='required_players',
)

# Max team size:
model.team_size = pyo.Param(
    domain=pyo.Integers,
    name='team_size',
)

# Team budget:
model.team_budget = pyo.Param(
    domain=pyo.NonNegativeReals,
    name='team_budget',
)

# Single club maximum players:
model.single_club_max_players = pyo.Param(
    domain=pyo.Integers,
    name='single_club_max_players',
)

# ===========================================================================
# Decision Variables: If a player is selected in the squad
# ===========================================================================

model.players_selected = pyo.Var(
    model.CLUBS,
    model.POSITIONS,
    model.PLAYERS,
    domain=pyo.Integers,
    initialize=0,
    bounds=(0, 1),
    dense=False,
    name='players_selected',
)


# ===========================================================================
# Objective Function:
# ===========================================================================
def objective_rule(m: pyo.ConcreteModel) -> pyo.simple_objective_rule:
    team_value = 0
    for club in m.CLUBS:
        for position in m.POSITIONS:
            for player in m.PLAYERS:
                try:
                    team_value += (
                            m.player_values[club, position, player] *
                            m.players_selected[club, position, player]
                    )
                except ValueError:
                    continue
    return team_value


model.total_team_value = pyo.Objective(
    rule=objective_rule,
    sense=pyo.maximize,
)

# ===========================================================================
# Constraints:
# ===========================================================================

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


# (1) Total Team Size: VERIFIED
# ===========================================================================
def team_size_rule(m: pyo.ConcreteModel) -> pyo.simple_constraint_rule:
    return pyo.summation(m.players_selected) == m.team_size


model.team_size_constraint = pyo.Constraint(rule=team_size_rule)


# (2) Appropriate numbers of players in each position: VERIFIED
# ===========================================================================
def required_players_in_positions_rule(
        m: pyo.ConcreteModel,
        position: str,
) -> pyo.simple_constraint_rule:
    total_players = 0
    for club in m.CLUBS:
        for player in m.PLAYERS:
            try:
                total_players += (
                    m.players_selected[club, position, player]
                )
            except ValueError:
                continue
    return total_players == m.required_players[position]


model.required_players_in_positions_constraint = pyo.Constraint(
    model.POSITIONS,
    rule=required_players_in_positions_rule,
)


# (3) Appropriate numbers of players from each club: VERIFIED
# ===========================================================================
def max_players_in_club_rule(
        m: pyo.ConcreteModel,
        club: str,
) -> pyo.simple_constraint_rule:
    total_players = 0
    for position in m.POSITIONS:
        for player in m.PLAYERS:
            try:
                total_players += (
                    m.players_selected[club, position, player]
                )
            except ValueError:
                continue
    return total_players <= m.single_club_max_players


model.max_players_in_club_constraint = pyo.Constraint(
    model.CLUBS,
    rule=max_players_in_club_rule,
)


# (4) Budget:
# ===========================================================================
def team_budget_rule(
        m: pyo.ConcreteModel,
) -> pyo.simple_constraint_rule:
    team_price = 0
    for club in m.CLUBS:
        for position in m.POSITIONS:
            for player in m.PLAYERS:
                try:
                    team_price += (
                            m.player_prices[club, position, player] *
                            m.players_selected[club, position, player]
                    )
                except ValueError:
                    continue
    return team_price <= m.team_budget


model.team_budget_constraint = pyo.Constraint(
    rule=team_budget_rule,
)
