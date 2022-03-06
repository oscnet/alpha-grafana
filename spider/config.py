import os

_ = os.path.abspath(os.path.dirname(__file__))  # 返回当前文件路径

root_path = os.path.abspath(os.path.join(_, '..'))  # 返回根目录文件夹

LOG_SAVE_DIR = os.path.join(_, 'log')
# 币安api设置

## 从环境变量中取得配置信息

Wechat_Config = {
    'corpsecret': os.environ.get('wechat_secret', 'FoJsxkyVOs'),
    'agentid': os.environ.get('wechat_agentid', 100),
    'corpid': os.environ.get('wechat_corpid', 'ww73'),
}

database_config = {
    'user': os.environ.get('mysql_user', 'root'),
    'passwd': os.environ.get('mysql_password', '3ctMcfmlKKPwwNaI'),
    'database': os.environ.get('mysql_database', 'ns_data'),
    'host': os.environ.get('mysql_host', 'db'),
    'port': os.environ.get('mysql_port', 3306),
}

keys = dict(os.environ).keys()

keys = [x for x in keys if x.startswith('account_')]


def get_account_name(key):
    names = key.split('_')
    if len(names) == 3:
        return names[1]


accounts = list(map(get_account_name, keys))
accounts = set(accounts)
# print(accounts)

INITIAL_CASH = {account: os.environ.get(f'account_{account}_cash') for account in accounts}
API_DICT = {
    account:
        {'apiKey': os.environ.get(f'account_{account}_apiKey'),
         'secret': os.environ.get(f'account_{account}_secret'), }
    for account in accounts}

# print(INITIAL_CASH)
# print(API_DICT)
