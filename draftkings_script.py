from draftkings_class import DraftKings
import json

"""
Create a DraftKings class object
"""
dk = DraftKings(league = "Portugal - Primeira Liga")

"""
Find all games & their event_ids
"""
game_ids = dk.get_event_ids()
for game, event_id in game_ids.items():
    print(game, event_id)

"""
Set up a stream awaiting odds updates for the Moneyline market [all games]
"""
dk.live_odds_stream(markets = ['Moneyline'])
