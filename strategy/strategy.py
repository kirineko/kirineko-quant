import data.stock as st
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt


def compose_signal(data: pd.DataFrame) -> pd.DataFrame:
    # 整合信号
    data['buy_signal'] = np.where((data['buy_signal'] == 1) & (data['buy_signal'].shift(1) == 1), 0, data['buy_signal'])
    data['sell_signal'] = np.where((data['sell_signal'] == -1) & (data['sell_signal'].shift(1) == -1), 0,
                                   data['sell_signal'])
    data['signal'] = data['buy_signal'] + data['sell_signal']
    return data


def calculate_profit_pct(data: pd.DataFrame) -> pd.DataFrame:
    # data = data[data['signal'] != 0]
    # data['profit_pct'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(1)
    data.loc[data['signal'] != 0, 'profit_pct'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(1)
    data = data[data['signal'] == -1]
    return data


def calculate_cum_pct(data: pd.DataFrame)-> pd.DataFrame:
    """
    计算累积收益率 = (1+单次收益率)*(1+单次收益率) - 1
    :param data: 
    :return: 
    """
    data['cum_profit'] = pd.DataFrame(1 + data['profit_pct']).cumprod() - 1
    return data


def week_period_strategy(code, time_freq, start_date, end_date):
    data = st.get_single_price(code, time_freq, start_date, end_date)
    # 新建周期字段
    data['weekday'] = data.index.weekday
    # 周四买入，周一卖出
    data['buy_signal'] = np.where((data['weekday'] == 3), 1, 0)
    # 周一卖出
    data['sell_signal'] = np.where((data['weekday'] == 0), -1, 0)
    # 整合信号
    data = compose_signal(data)
    # 计算单次收益率：开仓、平仓（开仓的全部股数）
    data = calculate_profit_pct(data)
    # 计算累积收益率
    data = calculate_cum_pct(data)
    return data


if __name__ == '__main__':
    df = week_period_strategy('000001.XSHE', 'daily', None, datetime.date.today())
    print(df[['close', 'signal', 'profit_pct', 'cum_profit']])
    print(df.describe())
    df['cum_profit'].plot()
    plt.show()
