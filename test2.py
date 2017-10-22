from bittrex import Bittrex
import config
from operator import itemgetter
import json, ast
from pybittrex.client import Client
import requests
import time
from pybittrex.auth import BittrexAuth
c = Client(api_key=config.key, api_secret=config.secret)
market = "BTC-VTC"

class Client(object):
    """Create a new session to the Bittrex exchange."""
    def __init__(self, api_key, api_secret):
        self.api_version = 'v1.1'
        self.api_base = 'https://bittrex.com/api/%s' % (self.api_version)

        self.api_key = api_key
        self.api_secret = api_secret

        # create a session object
        self.session = requests.Session()

    def get_api_version(self):
        return self.api_version

    def _get_nonce(self):
        """Authenticated requests all require a nonce."""
        return str(round(time.time()))

    def _build_url(self, endpoint):
        """Helper function to build the full URL."""
        return self.api_base + endpoint

    def _call(self, url, params=None):
        """Call the API """

        if not params:
            # for authenticated requests with no parameters
            params = {}

        # figure out if we need to authenticate or not
        if 'public' in url:
            auth = None
        else:
            auth = BittrexAuth(self.api_secret)
            params['apikey'] = self.api_key
            params['nonce'] = self._get_nonce()

        return self.session.get(url, params=params, auth=auth)

                                    # Public API
    # ----------

    def get_markets(self):
        """Used to get the open and available trading markets at Bittrex along with other metadata."""
        url = self._build_url('/public/getmarkets')

        return self._call(url)

    markets = c.get_markets().json()['result']
#For specific currency  markets[0] index means the number of currency pair
    print (markets[2])['MarketName']
    #market = (markets[2])['MarketName']
    print "     "
#For all markets
#for i in markets:
#    print(i['MarketName'])
    def get_currencies(self):
        """Used to get all supported currencies at Bittrex along with other metadata."""
        url = self._build_url('/public/getcurrencies')

        return self._call(url)
    currencies = c.get_currencies().json()['result']
    print (currencies[3])['Currency']


    def get_ticker(self, market, *args, **kwargs):
        """Used to get the current tick values for a market."""
        url = self._build_url('/public/getticker')

        payload = {'market': market}

        return self._call(url, params=payload)
    ticker = c.get_ticker(market).json()['result']
    print (ticker)['Ask']
    print (ticker)['Bid']





    def get_market_summaries(self):
        """Used to get the last 24 hour summary of all active exchanges."""
        url = self._build_url('/public/getmarketsummaries')

        return self._call(url)

    def get_market_summary(self, market, *args, **kwargs):
        """Used to get the last 24 hour summary of all active exchanges."""
        url = self._build_url('/public/getmarketsummary')

        payload = {'market': market}

        return self._call(url, params=payload)

    def get_orderbook(self, market, type, *args, **kwargs):
        """Used to get retrieve the orderbook for a given market."""
        url = self._build_url('/public/getorderbook')

        payload = {'market': market, 'type': type}

        return self._call(url, params=payload)

    def get_market_history(self, market, *args, **kwargs):
        """Used to retrieve the latest trades that have occured for a specific market."""
        url = self._build_url('/public/getmarkethistory')

        payload = {'market': market}

        return self._call(url, params=payload)