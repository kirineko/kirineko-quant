import data.stock as st
from datetime import datetime

# 调用一只股票行情数据
code = '000001.XSHE'
data = st.get_single_price(code=code,
                           time_freq='daily',
                           start_date='2021-02-01',
                           end_date='2021-03-01')
# 存入csv
st.save_csv_data(data=data, code=code, stock_type='price')

# 从csv中获取数据
data = st.get_csv_data(code, 'price')
print(data)

# 实时更新数据: 假设每天更新日K数据 > 存到csv文件里面 > df.to_csv(append)
# data = st.get_single_price(code=code,
#                            time_freq='daily',
#                            start_date=datetime.today(),
#                            end_date=datetime.today())
#
# st.save_csv_data(data=data, code=code, stock_type='price')

