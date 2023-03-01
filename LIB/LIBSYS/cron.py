from django_cron import CronJobBase, Schedule
from .models import IssueBook
from datetime import datetime

class OverDueDetection(CronJobBase):
    RUN_EVERY_MINS = 5
    RETRY_AFTER_FAILURE_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'fine.cron_job'

    def do(self):
        self.schedule
        issuedBooks = IssueBook.objects.all()[1]
        a = str(datetime.now()) # today
        d = datetime.strptime(a.split(' ')[0], "%Y-%m-%d")
        getduedate = issuedBooks.due_date
        if getduedate.day > int(d.day) and getduedate.month == int(d.month):
            print('Not over due')

