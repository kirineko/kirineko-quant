from typing import List

from jqdatasdk import *
import pandas as pd
from datetime import datetime

from pandas import Index

auth('17620708831', 'As798360687')
pd.set_option('display.max_rows', 30)
pd.set_option('display.max_columns', 20)

# stocks = list(get_all_securities(['stock']).index)
# print(stocks)

# df = get_price(['000001.XSHE','600519.XSHG'], count=100, end_date='2021-06-15',
#                frequency='daily')

# print(df)

"""
df = get_price('000001.XSHE', start_date='2021-01-01', end_date='2021-01-31', frequency='daily')
df['weekday'] = df.index.weekday
print(df)

df_month = pd.DataFrame()
df_month['open'] = df['open'].resample('M').first()
df_month['close'] = df['close'].resample('M').last()
df_month['high'] = df['high'].resample('M').max()
df_month['low'] = df['low'].resample('M').min()
print(df_month)
"""

# df = get_price('000001.XSHE', start_date='2020-01-01', end_date='2020-12-31', frequency='daily')
# df_month = pd.DataFrame()
# df_month['sum(volume)'] = df['volume'].resample('M').sum()
# df_month['sum(money)'] = df['money'].resample('M').sum()
# print(df_month)

"""
获取财务指标
"""

"""
df = get_fundamentals(query(indicator), statDate='2020')
# df.to_csv('./finance/finance2020.csv')

df = df[(df['eps'] > 0) & (df['operating_profit'] > df['operating_profit'].mean())
        & (df['roe'] > df['roe'].mean())
        & (df['inc_net_profit_year_on_year'] > df['inc_net_profit_year_on_year'].mean())]

# print(df)
# df.to_csv('./finance/finance2020_c.csv')
df.index = df['code']
"""


"""
获取股票估值指标
"""

"""
df_valuation = get_fundamentals(query(valuation), statDate='2020')
df_valuation.index = df_valuation['code']

df['pe_ratio'] = df_valuation['pe_ratio']
df = df[(df['pe_ratio'] < 50) & (df['pe_ratio'] > 0)]
print(df)
"""

"""
# df = get_price('600519.XSHG', count=1, end_date='2021-06-16',frequency='daily')
# print(df)
current_date = datetime.datetime.today()
current_date_strf = current_date.strftime("%Y-%m-%d")

all_stocks = get_all_securities()
gzmt_stock_code = all_stocks[all_stocks['display_name'] == '贵州茅台'].index[0]

gzmt_current_data = get_price(security=gzmt_stock_code, start_date=current_date_strf, end_date=current_date_strf,
                              frequency='daily')
gzmt_current_close = gzmt_current_data.iloc[0, 1]

gzmt_fundamentals = get_fundamentals(
    query(valuation).filter(
        valuation.code.in_([gzmt_stock_code])
    ),
    date=current_date
)

print(gzmt_fundamentals)

total_capitalization = gzmt_fundamentals.capitalization[0]
current_market_val = gzmt_current_close * total_capitalization
print('当日{}收盘价为:{}'.format(gzmt_stock_code, gzmt_current_close))
print('{}当日市值为:{}'.format(gzmt_stock_code, current_market_val))


# query参数问题

'''
第二题
使用 Python 计算贵州茅台的市盈率（静态），并验证其是否正确。
Tips：市盈率（静态） = 每股股价 / 每股收益（或者：市值 / 母公司净利润）
'''

gzmt_indicator = get_fundamentals(
    query(indicator).filter(
        indicator.code.in_(
            [gzmt_stock_code]
        )
    ),
    statDate='2020'
)

# 每股盈利 (Earnings per share)
gzmt_eps = gzmt_indicator.loc[0, 'eps']

# 静态市盈率 (股价[当日收盘价] / 每股收益)
print('静态市盈率为: {:.2f}'.format(gzmt_current_close / gzmt_eps))
"""

