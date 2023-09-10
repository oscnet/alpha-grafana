"""监控主程序"""
import schedule
import time
from utils.alert import WeChat
from function import Account, Order
from config import database_config as dc_, API_DICT

import pymysql
import pandas as pd
from sqlalchemy import create_engine
import traceback

pymysql.install_as_MySQLdb()
pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


# schedule.every().minute.at(":10").do(future_position)
# schedule.every(30).seconds.do(spot_position)
# schedule.every().hour.at(":03").do(future_cash)
# schedule.every().hour.at(":03").do(future_leverage)
# schedule.every().hour.at(":03").do(spot_cash)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every(1).minute.do(future_cash)

def future_balance():
    """账户资金记录"""

    database_connect = create_engine(f"mysql://{dc_['user']}:{dc_['passwd']}@{dc_['host']}:{dc_['port']}/{dc_['database']}")
    for account_name in account_list:
        psy_ns_account = Account(account_name)
        df = psy_ns_account.account_balance()

        try:

            sql = f"select * from {account_name}_balance"

            old_ = pd.read_sql(sql, con=database_connect)

            dd = old_.tail(1)
            dd.reset_index(inplace=True)

            df['deposit_cash'] = dd.loc[0, 'deposit_cash']
            df['withdraw_cash'] = dd.loc[0, 'withdraw_cash']

        except:

            pass
        #
        df.to_sql(name=f'{account_name}_balance', if_exists='append', con=database_connect, index=False)
    database_connect.dispose()  # 释放数据库连接


# def future_account_change():
#     """订单记录"""
#
#     for account_name in account_list:
#         psy_ns_account = Order(account_name)
#         psy_ns_account.account_record_booking()


def future_cash():
    """账户资金记录"""

    database_connect = create_engine(f"mysql://{dc_['user']}:{dc_['passwd']}@{dc_['host']}:{dc_['port']}/{dc_['database']}")
    for account_name in account_list:
        psy_ns_account = Account(account_name)
        df = psy_ns_account.account_equity()
        df.to_sql(name=f'{account_name}_equity', if_exists='append', con=database_connect, index=False)
    database_connect.dispose()  # 释放数据库连接


def future_position():
    """实时仓位记录"""

    database_connect = create_engine(f"mysql://{dc_['user']}:{dc_['passwd']}@{dc_['host']}:{dc_['port']}/{dc_['database']}")
    for account_name in account_list:
        psy_ns_account = Account(account_name)
        df = psy_ns_account.account_position()
        df.to_sql(name=f'{account_name}_position', if_exists='replace', con=database_connect, index=False)
    database_connect.dispose()  # 释放数据库连接


def future_order():
    """订单记录"""

    for account_name in account_list:
        psy_ns_account = Order(account_name)
        psy_ns_account.order_record_booking()
        psy_ns_account.account_record_booking()


alert = WeChat('NsSupervisor')
account_list = API_DICT.keys()
future_order()

# add by oscar
future_cash()
future_balance()
future_position()

schedule.every().hour.at(":03").do(future_cash)  # 每小时的03分钟时记录账户资金
schedule.every().hour.at(":10").do(future_balance)  # 每小时的03分钟时记录账户资金
schedule.every().minute.at(":10").do(future_position)  # 每分钟10s的时候更新仓位

while True:
    try:

        schedule.run_pending()
        time.sleep(1)

    except Exception:

        alert.error_report(traceback.format_exc())
