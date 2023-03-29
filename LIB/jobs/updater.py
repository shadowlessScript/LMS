from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import OverDueDetection, FineCalculation

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(OverDueDetection, 'interval', minutes=32)    
    scheduler.add_job(FineCalculation, 'interval', minutes=35)
    scheduler.start()