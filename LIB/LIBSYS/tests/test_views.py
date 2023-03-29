from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from LIBSYS import models
from LIBSYS import views

class TestViews(TestCase):
    def setUp(self):
        self.client = Client() # sim a client
        self.staff_user = User.objects.create_user(
            username='staffuser', password='testpassword', is_staff=True)# create library staff
        self.client.login(username='staffuser', password='testpassword') # librarian login
        # creating a book's instance
        # self.booktest = models.AddBook.objects.create(
        #     title = 'One Piece',
        #     Author = 'Eichiro Oda',
        #     serial_number = 'OP101',
        #     copies=12,
        #     copies_remaining=12,
        #     description='A boy named Monkey D. Luffy wants to be the pirate king',
        #     Cover_image='',
        #     state='ebook',
        #     genre='Novel',
        #     ebook='',
        #     pages=23,
        #     edition='second',
        #     publisher='shounen jump',
        #     co_authors='none',
        #     year='1998'
        # )
    def test_notfound_get(self):
      
        response = self.client.get(reverse('404')) # client sending a get request
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, '404.html')
    
    def test_addBookstoShelf_GET(self):
        # test get request to access the page for managing the lib repo

        response = self.client.get(reverse('add')) # client sending a get request
        self.assertEquals(response.status_code, 200)
        # self.assertRedirects(response, reverse('add'))
        self.assertTemplateUsed(response, 'shelfs/addbooks.html')

    def test_addBookstoShelf_POST(self):
        response = self.client.post(reverse('add'), {
           ' title':'One Piece',
            'Author':'Eichiro Oda',
            'serial_number':'OP101',
            'copies':12,
            'copies_remaining':12,
            'description':'A boy named Monkey D. Luffy wants to be the pirate king',
            'Cover_image':'',
            'state':'ebook',
            'genre':'Novel',
            'ebook':'',
            'pages':23,
            'edition':'second',
            'publisher':'shounen jump',
            'co_authors':'none',
            'year':'1998',

        })# client sending a post request of the book added to the lib DB
        self.assertEquals(response.status_code, 302) # 302 means there is a redirect
        self.assertEquals(models.AddBook.objects.all().first().title, 'One Piece')
        storage = get_messages(response.wsgi_request)
        messages = [msg.message for msg in storage]
        self.assertEqual(messages, ['Book added successfully!'])

    def test_addBookstoShelf_POST_failure(self):
        #testing whether no book is added when fields are invalid
        response = self.client.post(reverse('add'), {
           ' title':12, # invalid
            'Author':'Eichiro Oda',
            'serial_number':'OP101',
            'copies':12,
            'copies_remaining':"yes", # invalid
            'description':'A boy named Monkey D. Luffy wants to be the pirate king',
            'Cover_image':'',
            'state':'ebook',
            'genre':'Novel',
            'ebook':'',
            'pages':23,
            'edition':'second',
            'publisher':'shounen jump',
            'co_authors':'none',
            'year':'1998',

        })
        self.assertEquals(response.status_code, 302) # 302 means there is a redirect
        self.assertEquals(models.AddBook.objects.all().count(), 0)
        storage = get_messages(response.wsgi_request) # messsage is shown upon each CRUD op.
        messages = [msg.message for msg in storage]
        self.assertEqual(messages, ['Something went wrong, please try again!'])
    
    def test_managebook_GET(self):
        response = self.client.get(reverse('manage'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'shelfs/manage.html')

    
    def test_deletebook_GET(self):
        response = self.client.get(reverse('deletebook', args=['ew212']))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'shelfs/updates/confirm_delete.html')
    
    def test_deletebook_GET(self):
        response = self.client.get(reverse('deletebook_confirm', args=['ew212']))
        self.assertEquals(response.status_code, 302)
        # self.assertTemplateUsed(response, 'shelfs/updates/confirm_delete.html')
        
    def test_returnfinedbook_GET(self):
        response = self.client.get(reverse('finedbookreturned', args=[37]))
        self.assertEquals(response.status_code, 302)