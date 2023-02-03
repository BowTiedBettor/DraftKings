class ScraperException(Exception):
    """
    Base class for Scraper Exceptions.
    """
    pass


class WSEventTypeException(ScraperException):
    """
    ...
    """

    def __init__(self, event: str):
        self.event = event

    def __str__(self):
        return (f"Wrong WS event type: {self.event}")


class EventIdException(ScraperException):
    """
    ...
    """

    def __init__(self, event_id: str):
        self.event_id = event_id

    def __str__(self):
        return (f"Wrong event_id: {self.event_id}")


class MarketException(ScraperException):
    """
    ...
    """

    def __init__(self, market: str):
        self.market = market

    def __str__(self):
        return (f"Wrong market: {self.market}")
