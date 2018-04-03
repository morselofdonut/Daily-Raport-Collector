import schedule
import time
import datetime
from datetime import timedelta
import glob

def clear():
    date= datetime.datetime.now().strftime('%Y-%m-%d')

    with open('daily-stats-graph_output_example','r') as plot:
        read= plot.read()
       
    with open('daily-stats-graph_output_example' % date, 'w') as plot2:
        plot2.write(read)
    list = glob.glob('*.txt')
    for name in list:
        open('%s' % name, 'w').close()
    return

schedule.every().day.at("21:59").do(clear)

while True:
    schedule.run_pending()
    time.sleep(15)
