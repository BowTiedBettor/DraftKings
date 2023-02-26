import asyncio
import websockets
import requests
import json
from traceback import print_exc
from draftkings_stream import stream

id_dict = {"NHL": "42133", "NFL": "88808",
           "NBA": "42648", "England - Premier League": "40253"}


class DraftKings:
    def __init__(self, league="NHL"):
        """
        Initializes a class object
        Include more leagues simply by adding the league with its ID to id_dict above

        :league str: Name of the league, NHL by default
        """
        self.league = league
        self.pregame_url = f"https://sportsbook.draftkings.com//sites/US-SB/api/v5/eventgroups/{id_dict[self.league]}?format=json"
        self.uri = "wss://ws-draftkingseu.pusher.com/app/490c3809b82ef97880f2?protocol=7&client=js&version=7.3.0&flash=false"

    def get_event_ids(self) -> dict:
        """
        Finds all the games & their event_ids for the given league

        :rtype: dict
        """
        event_ids = {}
        response = requests.get(self.pregame_url).json()
        for event in response['eventGroup']['events']:
            event_ids[event['name']] = event['eventId']
        return event_ids

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
                try:
                    market_name = market['label']
                    if market_name == "Moneyline":
                        home_team = market['outcomes'][1]['label']
                        away_team = market['outcomes'][0]['label']
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
                        outcome_list.append(
                            {"label": outcome_label, "odds": outcome_odds})
                    market_list.append(
                        {"marketName": market_name, "outcomes": outcome_list})
                except Exception as e:
                    if self.league == "NBA" and "label" in str(e):
                        # odds for NBA totals are not available as early as the other markets for
                        # games a few days away, thus raises a KeyError: 'label'
                        # in this case we simply ignore the error and continue with the next market
                        continue
                    else:
                        # if there was another problem with a specific market, print the error and
                        # continue with the next one...
                        print_exc()
                        print()
                        continue
            games_list.append(
                {"game": f"{home_team} v {away_team}", "markets": market_list})

        return games_list

    def live_odds_stream(self, event_ids=None, markets=None):
        """
        Sets up the live odds stream by calling the async stream function with given parameters

        :param event_id list: If a list of event_ids is specified [else it's None], the stream/listener considers updates
                              only if they're updates for those particular games
        :param markets list: If a list of markets is specified [else markets == None], the stream/listener considers updates
                             only if they're updates for those particular markets
                             Hint: If uncertain about market names, run it for a minute for all markets and collect the correct
                             names of the markets this way
        """
        asyncio.run(stream(
            uri=self.uri, league_id=id_dict[self.league], event_ids=event_ids, markets=markets))

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

    def send_email(self, content):
        """
        ...
        """
        pass
