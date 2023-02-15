import schedule
import time
from addInformation import addInform


def UpdateInfo():
    schedule.every(15).minutes.do(addInform)

    while True:
        schedule.run_pending()
        time.sleep(1)
