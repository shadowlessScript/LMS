from django.conf import settings
from LIBSYS.models import IssueBook, Fine
from datetime import datetime, date
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .job_helpers import export_notify_client


def over_due_detection():
    issuedBooks = IssueBook.objects.all()  # grab all books issued
    a = str(datetime.now())  # today
    d = datetime.strptime(a.split(' ')[0], "%Y-%m-%d")
    for x in issuedBooks:
        getduedate = x.due_date
        if getduedate == d.date():
            export_notify_client(x, d, getduedate)
            # print(f'{patron} email {mails}')
            x.delete()
        if getduedate < d.date():
            export_notify_client(x, d, getduedate, 10, False)
            x.delete()


def fine_calculation():
    a = str(datetime.now())  # today
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
                    # if getduedate.month == int(d.month):
                    #     over_due_by = int(d.day) - getduedate.day
                    #     # print(over_due_by)
                    #     # print((d.date()-getduedate).days)
                    # else:
                    over_due_by = (d.date() - getduedate).days
                    print(over_due_by)
                    x.price = fine_cost * over_due_by
                    x.over_due_by = over_due_by
                    x.save()


def send_reminder():
    for i in Fine.objects.all():
        if i.over_due_by % 2 == 0 and i.over_due_by != 0:  # remind user after two days pass
            send_mail(
                f'{i.serial_number.title}',
                f' Hi {i.username.first_name} {i.username.last_name}, this is to remind you that you have an overdue '
                f'book: {i.serial_number.title}, \n it over due by'
                f'{i.over_due_by} days. \n \n do not reply to this email, from fines reminder',
                'settings.EMAIL_HOST_USER',
                [i.username.email],
                fail_silently=False
            )
