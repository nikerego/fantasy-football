

endpoints = {
    "general_information": {
        "description": "The ‘bootstrap-static’ call returns a huge amount o"
                       " information, and is all you really need if you "
                       "don’t want to get into specific FPL managed teams.",
        "data_included": ""
                         " - A summary of all 38 game-weeks \n"
                         " - The game’s settings \n"
                         " - Basic information on all 20 PL teams \n"
                         " - Total number of FPL Users and overall chip"
                         " usage \n"
                         " - Basic information on all Premier League"
                         " players \n"
                         " - List of stats that FPL keeps track of \n"
                         " - The different FPL positions \n",
        "url": "https://fantasy.premierleague.com/api/bootstrap-static/",
    },
    "fixtures": {
        "description": "This call shows some useful information on every "
                       "single fixture that has happened, as well as "
                       "placeholder info for upcoming game-weeks/fixtures. "
                       "For past fixtures, you’ll need to know the IDs of "
                       "the teams from the bootstrap-static call.",
        "data_included": "Per match, it shows: \n"
                         " - Goals \n"
                         " - Assists \n"
                         " - Cards \n"
                         " - Saves \n"
                         " - Pens missed \n"
                         " - Bonus points \n"
                         " - Own goals \n"
                         " - Pens saved \n",
        "url": "https://fantasy.premierleague.com/api/fixtures/",
    },
    "individual_players": {
        "description": "This one is handy if you want in-depth info on a "
                       "specific player, including past performance and "
                       "upcoming fixtures. You’ll need to grab the player’s "
                       "ID from the bootstrap-static call. ",
        "urls": {
            "player-id": {
                "data_included": ""
                                 " - Remaining fixtures for the player, "
                                 "including: \n"
                                 "     - Kickoff time \n"
                                 "     - game-week number \n"
                                 "     - Home or Away \n"
                                 "     - Difficulty \n"
                                 " - Previous fixtures and performance, "
                                 "including: \n"
                                 "     - Minutes played \n"
                                 "     - Goals \n"
                                 "     - Assists \n"
                                 "     - Conceded \n"
                                 "     - Cards \n"
                                 "     - Bonus \n"
                                 "     - Influence \n"
                                 "     - Creativity \n"
                                 "     - xG \n"
                                 "     - xA \n"
                                 "     - Value \n"
                                 "     - Transfer delta for that game-week "
                                 "\n",
                "url": "https://fantasy.premierleague.com/api/"
                       "element-summary/{player_id}/",
            },
            "game-week": {
                "data_included": "Shows all of the above stats, but for the "
                                 "game-week for every player, rather than a "
                                 "single player for every game-week.",
                "url": "https://fantasy.premierleague.com/api/event/"
                       "{gw}/live/"
            }
        }
    },
    "individual_managers": {
        "description": "Using this set of endpoints, you can retrieve "
                       "information on any individual FPL manager. "
                       "Your manager ID can be found on the my-team page "
                       "in the URL.",
        "urls": {
            "team-id": {
                "data_included": ""
                                 " - Name \n"
                                 " - Team Name \n"
                                 " - Favourite team \n"
                                 " - game-week started \n"
                                 " - Points \n"
                                 " - Transfers \n"
                                 " - Overall Rank \n"
                                 " - Last game-week rank \n"
                                 " - Last game-week points \n"
                                 " - All league information, including: \n"
                                 "     - Max entries \n"
                                 "     - Scoring type \n"
                                 "     - Cup qualification \n"
                                 "     - Your rank within the league \n"
                                 "     - League name \n"
                                 "     - Date created \n",
                "url": "https://fantasy.premierleague.com/api/entry/"
                       "{team_id}/",
            },
            "team-id/transfers": {
                "data_included": "A full history of transfers for that "
                                 "manager, including: \n"
                                 " - Cost \n"
                                 " - game-week \n"
                                 " - Time of transfer \n"
                                 " - Players in and out \n",
                "url": "https://fantasy.premierleague.com/api/entry/"
                       "{team_id}/transfers/"
            },
            "team-id/game-week/picks": {
                "data_included": "Shows the detail of your 15 players for "
                                 "any given game-week. the ‘Event’ "
                                 "parameter in the URL is the game-week"
                                 " number. This includes: \n"
                                 " - The general info for the game-week, "
                                 " such as: \n"
                                 "     - Points \n"
                                 "     - Total points \n"
                                 "     - Rank \n"
                                 "     - Team value \n"
                                 "     - Money in the bank \n"
                                 "     - Transfers made that game-week \n"
                                 "The stats of the individual players in "
                                 "the team, including: \n"
                                 "     - Element ID (cross reference with "
                                 "bootstrap-static data) \n"
                                 "     - Whether they’re captain or vice "
                                 "captain \n"
                                 "     - Position in the team \n",
                "url": "https://fantasy.premierleague.com/api/entry/"
                       "{team_id}/event/{gw}/picks/",
            },
            "team-id/history": {
                "data_included": "This shows a high level stats for each "
                                 "game-week gone by, plus the manager’s "
                                 "overall career performance form "
                                 "previous seasons: \n"
                                 " - Game-week-by-game-week data, "
                                 "including: \n"
                                 "     - Points \n"
                                 "     - Rank \n"
                                 "     - Overall rank \n"
                                 "     - Money in the Bank \n"
                                 "     - Team value \n"
                                 "     - Transfers made \n"
                                 "     - Chips played \n"
                                 " - Past season history data, including: \n"
                                 "    - Season year \n"
                                 "    - Overall points \n"
                                 "    - Overall rank \n",
                "url": "https://fantasy.premierleague.com/api/entry/"
                       "{team_id}/history/",
            },
        }
    }
}
