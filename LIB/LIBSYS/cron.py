from django_cron import CronJobBase, Schedule
from .models import IssueBook, Fine
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.models import User

class OverDueDetection(CronJobBase):
    RUN_EVERY_MINS = 5
    RETRY_AFTER_FAILURE_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'fine.cron_job'

    def do(self):
        
        issuedBooks = IssueBook.objects.all()
        a = str(datetime.now()) # today
        d = datetime.strptime(a.split(' ')[0], "%Y-%m-%d")
        for x in issuedBooks:
            getduedate = x.due_date
            if getduedate.day > int(d.day) and getduedate.month == int(d.month):
                print(f'{x.isbn.title} is not over due')
            else:
                
                x.status = 'Over Due'
                x.save()
                patron = x.username
                mails = User.objects.get(username=patron).email
                send_mail(
                    f'{x.isbn.title}',
                    f' Hi {patron.first_name} {patron.last_name}, you an over due book: {x.isbn.title}, \n by  '
                    f'{int(d.day) - getduedate.day} days. \n \n do not reply to this email.',
                    'settings.EMAIL_HOST_USER',
                    [mails],
                    fail_silently=False
                )
                add_to_fine = Fine(username=patron, serial_number=x.isbn, over_due_by = int(d.day) - getduedate.day)
                add_to_fine.save()
                print(f'{patron} email {mails}')


