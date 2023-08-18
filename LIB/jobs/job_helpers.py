from LIBSYS.models import IssueBook, Fine
from django.core.mail import send_mail
from django.contrib.auth.models import User


def export_notify_client(issued_book_obj, d,
                         getduedate, fine_cost=0, is_ontime=True):
    """
    Add a patron to the fine model and emails them depending on the is_ontime parameter.
        Parameters:
            issued_book_obj: refers to the issue book object flagged to have reached its due or exceeded it.

            d: The current date slip into %y-%m-%d

            getduedate(date): issue book object's due date

            fine_cost: by default it's zero, assuming the due date is flagged on time, change to 10 if not

            is_ontime: a bool parameter that is True by default, meaning that the due date of the issue book object was flagged on time.
    """
    patron = issued_book_obj.username
    mails = User.objects.get(username=patron).email
    over_due_by = (d.date() - getduedate).days

    if is_ontime:
        send_mail(
            f'{issued_book_obj.book_issued.title}',
            f' Hi {patron.first_name} {patron.last_name}, this is to remind you, that: {issued_book_obj.book_issued.title}, \n /'
            f'by {issued_book_obj.book_issued.book_details.author}, '
            f' due date has reached, bring today to avoid being fined. \n \n do not reply to this email.',
            'settings.EMAIL_HOST_USER',
            [mails],
            fail_silently=False
        )
    else:
        # in case the server was down it or the overdue detection job was skipped

        send_mail(
            f'{issued_book_obj.book_issued.title}',
            f' Hi {patron.first_name} {patron.last_name}, this is to remind you, that: {issued_book_obj.book_issued.title}, \n /'
            f'by {issued_book_obj.book_issued.book_details.author}, '
            f' due date has reached, the fine incurred is {fine_cost * over_due_by}. \n \n do not reply to this email.',
            'settings.EMAIL_HOST_USER',
            [mails],
            fail_silently=False
        )
    add_to_fine = Fine(username=patron, serial_number=issued_book_obj.book_issued,
                       due_date=getduedate, over_due_by=over_due_by,
                       price=(fine_cost * over_due_by)
                       )
    add_to_fine.save()

