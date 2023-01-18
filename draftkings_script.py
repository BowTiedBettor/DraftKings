from draftkings_class import DraftKings

dk = DraftKings()

games = dk.get_pregame_odds()

dk.store_as_json(games)


