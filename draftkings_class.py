import requests
import json

id_dict = {"NHL": "42133"}

class DraftKings:
    def __init__(self, league = "NHL"):
        """
        Initializes a class object
        Include more leagues simply by adding the league with its ID to id_dict above

        :league str: Name of the league, NHL by default
        """
        self.pregame_url = f"https://sportsbook.draftkings.com//sites/US-SB/api/v5/eventgroups/{id_dict[league]}?format=json"

    def get_pregame_odds(self) -> list:
        """
        Collects the market odds for the main markets [the ones listed at the league's main url] for the league

        E.g. for the NHL, those are Puck Line, Total and Moneyline

        Returns a list with one object for each game

        :rtype: list
        """
        # List that will contain dicts [one for each game]
        games_list = []

        # Requests the content from DK's API, loops through the different games & collects all the material deemed relevant
        response = requests.get(self.pregame_url).json()
        games = response['eventGroup']['offerCategories'][0]['offerSubcategoryDescriptors'][0]['offerSubcategory']['offers']
        for game in games:
            # List that will contain dicts [one for each market]
            market_list = []
            for market in game:
                market_name = market['label']
                if market_name == "Moneyline":
                    home_team = market['outcomes'][0]['label']
                    away_team = market['outcomes'][1]['label']
                # List that will contain dicts [one for each outcome]
                outcome_list = []
                for outcome in market['outcomes']:
                    try:
                        # if there's a line it should be included in the outcome description
                        line = outcome['line']
                        outcome_label = outcome['label'] + " " + str(line)
                    except:
                        outcome_label = outcome['label']
                    outcome_odds = outcome['oddsDecimal']
                    outcome_list.append({"label": outcome_label, "odds": outcome_odds})
                market_list.append({"marketName": market_name, "outcomes": outcome_list})
            games_list.append({"game": f"{home_team} v {away_team}", "markets": market_list})

        return games_list

    def store_as_json(self, games_list, file_path: str = None):
        """
        Dumps the scraped content into a JSON-file in the same directory

        :rtype: None, simply creates the file and prints a confirmation
        """
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(games_list, file)
            print(f"Content successfully dumped into '{file_path}'")
        else:
            with open('NHL.json', 'w') as file:
                json.dump(games_list, file)
            print("Content successfully dumped into 'NHL.json'")

    def to_excel(self, games_list):
        """
        ...
        """
        pass

    def live_odds_stream(self, game):
        """
        ...
        """
        pass

    def send_email(self, content):
        """
        ...
        """
        pass
