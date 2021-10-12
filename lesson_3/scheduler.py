import schedule
import time
import hh_parser


schedule.every().day.at("13:39").do(hh_parser.main, 'PHP', 3)

while True:
    schedule.run_pending()
    time.sleep(2)
