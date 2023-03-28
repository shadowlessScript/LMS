from django_cron import CronJobBase, Schedule
from .models import IssueBook, Fine
from datetime import datetime, date
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
                fine_cost = 10
                patron = x.username
                mails = User.objects.get(username=patron).email
                if getduedate.month == int(d.month):
                    over_due_by = int(d.day) - getduedate.day
                else:
                    over_due_by = date(d) - date(getduedate)
                if Fine.objects.filter(username=patron, serial_number=x.isbn).exists():
                    for i in Fine.objects.filter(username=patron, serial_number=x.isbn):
                        i.price = fine_cost * over_due_by
                        i.over_due_by = over_due_by
                        i.save()
                    send_mail(
                        f'{x.isbn.title}',
                        f' Hi {patron.first_name} {patron.last_name}, you an over due book: {x.isbn.title}, \n by  '
                        f'{int(d.day) - getduedate.day} days. \n \n do not reply to this email.',
                        'settings.EMAIL_HOST_USER',
                        [mails],
                        fail_silently=False
                    )
                    print('Already inside')
                else:
                    send_mail(
                        f'{x.isbn.title}',
                        f' Hi {patron.first_name} {patron.last_name}, you an over due book: {x.isbn.title}, \n by  '
                        f'{int(d.day) - getduedate.day} days. \n \n do not reply to this email.',
                        'settings.EMAIL_HOST_USER',
                        [mails],
                        fail_silently=False
                    )
                    add_to_fine = Fine(username=patron, serial_number=x.isbn, over_due_by = over_due_by, price=(fine_cost * over_due_by))
                    add_to_fine.save()
                    print(f'{patron} email {mails}')
                # x.status = 'Over Due'
                x.delete()

class FineCalculation(CronJobBase):
    RUN_EVERY_MINS = 5
    RETRY_AFTER_FAILURE_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'finecal.cron_job'
        
    def do(self): 
        a = str(datetime.now()) # today
        d = datetime.strptime(a.split(' ')[0], "%Y-%m-%d")
        finebook = Fine.objects.all()
        fined_patrons = []
        fined_books = []
        for i in finebook:             
            fined_patrons.append(i.username)
            fined_books.append(i.serial_number)
        fined_patrons = set(fined_patrons)
        fined_books = set(fined_books)
        fine_cost = 10
        for j in fined_patrons:
            for q in fined_books:
                fine_update = Fine.objects.filter(username=j, serial_number=q)
                if fine_update.exists():
                    for x in fine_update:
                        getduedate = x.due_date
                        if getduedate.month == int(d.month):
                            over_due_by = int(d.day) - getduedate.day
                            print(over_due_by)
                        else:
                            over_due_by = date(d) - date(getduedate)
                            print(over_due_by)
                        x.price = fine_cost * over_due_by
                        x.over_due_by = over_due_by
                        x.save()
                # print(j)
