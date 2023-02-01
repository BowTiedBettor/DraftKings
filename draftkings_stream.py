import asyncio
import websockets
import json
from traceback import print_exc

async def stream(uri, league_id, event_id, markets):
    """
    Sets up a connection with the server which is pushing new odds to the DraftKings website.
    Awaits further updates. As soon as updated odds information arrives it prints all the relevant
    information regarding the specific odds update.

    The function is meant to be called from the live_odds_stream method inside the DraftKings class

    :param uri str: URI for the web server
    :param league_id str: Id for the league
    :param timeout int: Number of seconds for the stream to keep on going
    :param event_id: If an event_id is specified [else it's None], the stream/listener considers updates
                     only if they're updates for that particular game
    :param markets list: If a list of markets is specified [else markets == None], the stream/listener considers updates
                         only if they're updates for those particular markets
                         Hint: If uncertain about market names, run it for a minute for all markets and collect the correct
                         names of the markets this way

    :rtype: Returns nothing, continues collecting and presenting new odds info until stopped
    """
    try:
        # connects to the web server
        ws = await websockets.connect(uri)
        # sends a subscription message to the server with info regarding the odds data we want to receive updates on
        await ws.send(
            json.dumps({"event":"pusher:subscribe","data":{"auth":"","channel":f"nj_ent-eventgroupv2-{league_id}"}}
                )
            )
        while True:
            try:
                new_message = await ws.recv()
                message_json = json.loads(new_message)
                event = message_json['event']
                if not event == "offer-updated":
                    # only interested in events containing odds updates
                    raise Exception("wrong_event_type")

                content = json.loads(message_json['data'])
                if event_id:
                    # if a specific event_id is provided, this checks whether
                    # the update is relevant or not
                    if not event_id == content['data'][0]['eventId']:
                        raise Exception("wrong_event_id")

                label = content['data'][0]['label']
                if markets:
                    # if a list of wanted markets is provided, this checks whether
                    # the update is relevant or not
                    if not label in markets:
                        raise Exception("wrong_market")

                outcomes = content['data'][0]['outcomes']
                print(f"New odds update for '{label}'")
                for outcome in outcomes:
                    print("Line:", outcome['line'])
                    print("Outcome:", outcome['label'])
                    print("Price:", outcome['oddsDecimal'])
                    if not outcome == outcomes[-1]:
                        print()
                print("Awaits more updates...")
                print()

            except websockets.WebSocketException:
                # if there's a problem with the connection it breaks the while loop
                # and closes the connection [could easily be adjusted to reconnect and so on]
                print_exc()
                break

            except Exception as e:
                if str(e) == "wrong_event_type":
                    if event == 'pusher:connection_established':
                        print("Connection established!")
                        continue
                    elif event == 'pusher_internal:subscription_succeeded':
                        print("Subscription succeeded, awaits new odds uppdates...")
                        continue
                    else:
                        continue
                elif str(e) == "wrong_event_id":
                    continue
                elif str(e) == "wrong_market":
                    continue
                else:
                    print_exc()
        await ws.close()
    except:
        print_exc()
