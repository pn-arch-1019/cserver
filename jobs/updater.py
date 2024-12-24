from apscheduler.schedulers.background import BackgroundScheduler 
from .tasks import * 


def start():
    scheduler = BackgroundScheduler()
    # add job
    scheduler.add_job(update_coint_price_vnd, 'interval', seconds=15)
    scheduler.add_job(get_trans_new, 'interval', seconds=30, max_instances=5)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown(wait=True)
