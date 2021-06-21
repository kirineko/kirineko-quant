import data.stock as st
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler


def job():
    stocks = st.get_stock_list()
    for code in stocks:
        data = st.get_single_price(code=code,
                                   time_freq='daily',
                                   start_date=datetime.now(),
                                   end_date=datetime.now()
                                   )
        st.save_csv_data(data=data, code=code, stock_type='price')
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '==============' + code)


cron_job = BlockingScheduler()
cron_job.add_job(job, 'cron', day_of_week='*', hour='15', minute='1')
cron_job.start()
