"""function"""

from binance import Client
from config import API_DICT
import pandas as pd
import time
import math
from utils.wrapper import retry


class BinanceTrade(object):
    """
    deal with exchange
    """

    def __init__(self, _account_name):
        self.account_name = _account_name
        self.exchange = self.connect_to_exchange()
        # self.futures_exchange_info = self.futures_exchange_info()

    @retry(3, _sleep_seconds=1)
    def connect_to_exchange(self):
        """
        hh
        :return:
        """
        return Client(API_DICT[self.account_name]['apiKey'], API_DICT[self.account_name]['secret'])

    @retry(3,_sleep_seconds=1)
    def future_balance(self):
        """
        hh
        """
        return self.exchange.futures_account_balance()

    def usdt_futures_info(self):
        """
        hh
        """
        return self.exchange.futures_exchange_info()

    def futures_history_trade_list(self,parm):
        """
        hh
        """
        return self.exchange.futures_account_trades(**parm)


    def futures_create_order(self, parm):
        """
        hh
        """
        return self.exchange.futures_create_order(**parm)

    def future_position_risk(self):
        """
        hh
        """
        return self.exchange.futures_position_information()

    def future_account(self):
        """
        hh
        """
        return self.exchange.futures_account()

    def futures_exchange_info(self):
        """
        hh
        """
        return self.exchange.futures_exchange_info()

    def spot_account_info(self):
        """hh"""

        return self.exchange.get_account()

    def spot_exchange_info(self):

        """hh"""
        return self.exchange.get_exchange_info()

    def spot_symbol_ticker(self):
        """hh"""
        return self.exchange.get_all_tickers()

    def get_symbol_list(self, data_type):
        """
        hh
        """

        if data_type == 'swap':

            _symbol_list = [x['symbol'] for x in self.futures_exchange_info()['symbols']]

            symbol_list_all = [symbol for symbol in _symbol_list if symbol.endswith('USDT')]

        elif data_type == 'spot':

            info = self.spot_exchange_info()
            # 转化为dataframe
            df = pd.DataFrame(info['symbols'])

            df = df[df['quoteAsset'] == 'USDT']
            df = df[df['status'] == 'TRADING']

            df = df[df['isSpotTradingAllowed'] == True]


            symbol_list_all = list(df['symbol'])

        else:
            raise ValueError

        return symbol_list_all

    def spot_futures_transfer(self, parm):
        """
        parm:

        asset	STRING	YES	The asset being transferred, e.g., USDT
        amount	DECIMAL	YES	The amount to be transferred
        type	INT	YES	1: 现货账户向USDT合约账户划转
                        2: USDT合约账户向现货账户划转
                        3: 现货账户向币本位合约账户划转
                        4: 币本位合约账户向现货账户划转
        recvWindow	LONG	NO
        timestamp	LONG	YES

        """
        return self.exchange.futures_account_transfer(**parm)

    def spot_market_buy(self, parm):
        """
        param symbol: required
        type symbol: str

        param quantity: required
        type quantity: decimal

        quoteOrderQty: required
        type quoteOrderQty: decimal

        """
        return self.exchange.order_market_buy(**parm)

    @retry(3, _sleep_seconds=1)
    def get_spot_asset_balance(self, asset):
        """
        hh
        """
        return self.exchange.get_asset_balance(asset)

    @retry(3, _sleep_seconds=1)
    def symbols_ticker(self):
        """
        hh
        """
        return self.exchange.futures_symbol_ticker()

    def futures_symbols_tick(self):
        """
        hh
        """

        tickers = self.symbols_ticker()
        tickers = pd.DataFrame(tickers, dtype=float)
        tickers.set_index('symbol', inplace=True)

        return tickers['price']

    def min_qty(self):
        """
        hh
        """
        _min_qty = {x['symbol']: int(math.log(float(x['filters'][1]['minQty']), 0.1)) \
                    for x in self.futures_exchange_info()['symbols']}

        return _min_qty

    def price_precision(self):
        """
        hh
        """
        _price_precision = {x['symbol']: int(math.log(float(x['filters'][0]['tickSize']), 0.1)) \
                            for x in self.futures_exchange_info()['symbols']}
        return _price_precision

    def replenish_bnb(self, _log):

        """

        hh

        """
        balance = self.future_balance()

        balance = pd.DataFrame(balance)

        amount_bnb = float(balance[balance['asset'] == 'BNB']['balance'].iloc[0])

        _log.info(f"当前合约账户剩余{amount_bnb} BNB")

        if amount_bnb < 0.001:
            spot_bnb_amount = float(self.get_spot_asset_balance('BNB')['free'])

            _log.info(f"当前现货账户持有{spot_bnb_amount} BNB")

            if spot_bnb_amount < 0.01:
                _log.info("从现货市场买入10 USDT等值BNB并转入合约账户")
                spot_usdt_amount = float(self.get_spot_asset_balance('USDT')['free'])
                _log.info(spot_usdt_amount)
                # exit()

                if spot_usdt_amount < 10:
                    # config the transfer parm
                    parm = {
                        'type': 2,
                        'asset': 'USDT',
                        'amount': 10.01 - spot_usdt_amount
                    }
                    self.spot_futures_transfer(parm)
                # config the order parm
                parm = {
                    'symbol': 'BNBUSDT',
                    'quoteOrderQty': 10

                }
                _log.info(self.spot_market_buy(parm))

                time.sleep(2)  # after 2s check asset

                spot_bnb_amount_new = float(self.get_spot_asset_balance('BNB')['free'])
                # config the transfer parm
                parm = {
                    'type': 1,
                    'asset': 'BNB',
                    'amount': spot_bnb_amount_new
                }
                self.spot_futures_transfer(parm)
                message = f"成功买入{spot_bnb_amount_new} BNB并转入U本位合约账户"
                _log.info(message)

            else:
                # config the transfer parm
                parm = {
                    'type': 1,
                    'asset': 'BNB',
                    'amount': spot_bnb_amount
                }
                self.spot_futures_transfer(parm)

                _log.info(f'把已有{spot_bnb_amount}BNB转入合约账户')


