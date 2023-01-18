from draftkings_class import DraftKings

dk = DraftKings(league = "NHL")

games = dk.get_pregame_odds()

dk.store_as_json()


