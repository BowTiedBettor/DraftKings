from draftkings_class import DraftKings

"""
Create a DraftKings class object
"""
dk = DraftKings(league="NBA")

"""
Find all games & their event_ids
"""
game_ids = dk.get_event_ids()
for game, event_id in game_ids.items():
    print(game, event_id)

"""
Set up a stream awaiting odds updates for the Moneyline market
"""
dk.live_odds_stream(
    event_ids=["28335346", "28335344", "28335347"], markets=['Moneyline'])
