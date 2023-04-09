from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import OverDueDetection, FineCalculation, SendReminder
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.triggers.cron import CronTrigger

    
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(
        OverDueDetection, 
        trigger=CronTrigger(minute="*/10"),
        id="Overduedetector",
        max_instances=1,
        replace_existing=True, 
        )    
    # scheduler.start()
    # scheduler.shutdown()
    scheduler.add_job(
        FineCalculation, 
        trigger=CronTrigger(minute="*/30"),
        id="finecalc",
        max_instances=1,
        replace_existing=True, 
        )
    # scheduler.start()
    # scheduler.shutdown()
    scheduler.add_job(
        SendReminder, 
       trigger=CronTrigger(minute="*/40"),
        id="reminder",
        max_instances=1,
        replace_existing=True, 
        )
    scheduler.start()
    # scheduler.shutdown()
    # scheduler.shut    down()