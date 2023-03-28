from django.test import SimpleTestCase
from django.urls import resolve, reverse
from LIBSYS import views


class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, views.index)

    def test_home_user_view_url_resolves(self):
        url = reverse('home_user_view')
        self.assertEqual(resolve(url).func, views.indexuserview)

    def test_add_url_resolves(self):
        url = reverse('add')
        self.assertEqual(resolve(url).func, views.addBookstoShelf)

    def test_manage_url_resolves(self):
        url = reverse('manage')
        self.assertEqual(resolve(url).func, views.manageBook)

    def test_updateBook_url_resolves(self):
        url = reverse('updateBook', args=['serial_number'])
        self.assertEqual(resolve(url).func, views.updateBook)

    def test_deletebook_url_resolves(self):
        url = reverse('deletebook', args=['serial_number'])
        self.assertEqual(resolve(url).func, views.deleteBook)

    def test_deletebook_confirm_url_resolves(self):
        url = reverse('deletebook_confirm', args=['serial_number'])
        self.assertEqual(resolve(url).func, views.deleteBookConfirmation)

    def test_blog_url_resolves(self):
        url = reverse('blog')
        self.assertEqual(resolve(url).func, views.PostNews)

    def test_books_url_resolves(self):
        url = reverse('books')
        self.assertEqual(resolve(url).func, views.ListOfBooks)

    def test_bookview_url_resolves(self):
        url = reverse('bookview', args=['serial_number'])
        self.assertEqual(resolve(url).func, views.bookView)

    def test_update_news_url_resolves(self):
        url = reverse('update_news', args=[1])
        self.assertEqual(resolve(url).func, views.NewsUpdate)

    def test_filtered_view_url_resolves(self):
        url = reverse('filtered_view', args=['genre'])
        self.assertEqual(resolve(url).func, views.Filter)

    def test_404_url_resolves(self):
        url = reverse('404')
        self.assertEqual(resolve(url).func, views.Notfound)

    def test_search_books_url_resolves(self):
        url = reverse('search_books')
        self.assertEqual(resolve(url).func, views.search_book)

    def test_dashboard_url_resolves(self):
        url = reverse('dashboard')
        self.assertEqual(resolve(url).func, views.dashboard)

    def test_booking_url_resolves(self):
        url = reverse('booking')
        self.assertEqual(resolve(url).func, views.booking)

    def test_issuebookrequest_url_resolves(self):
        url = reverse('issuebookrequest', args=[1,'isbn'])
        self.assertEqual(resolve(url).func, views.issuebookrequest)

    def test_IssueBook_url_resolves(self):
        url = reverse('IssueBook')
        self.assertEqual(resolve(url).func, views.issueBook)

    def test_view_issued_books_url_resolves(self):
        url = reverse('view_issued_books')
        self.assertEqual(resolve(url).func, views.viewIssuedBooks)

    def test_overdue_url_resolves(self):
        url = reverse('overdue')
        self.assertEqual(resolve(url).func, views.overdue)

    def test_bookacquire_url_resolves(self):
        url = reverse('bookacquire')
        self.assertEqual(resolve(url).func, views.bookAcquisitionRequest)

    def test_getthisbook_url_resolves(self):
        url = reverse('getthisbook')
        self.assertEqual(resolve(url).func, views.getthisbook)

    def test_status_update_url_resolves(self):
        url = reverse('status_update', args=[1])
        self.assertEqual(resolve(url).func, views.questCompleted)
    def test_bookreturned_url_resolves(self):
        url = reverse('bookreturned', args=[1])
        self.assertEqual(resolve(url).func, views.returnedBook)

    def test_viewreturnedbooks_url_resolves(self):
        url = reverse('viewreturnedbooks')
        self.assertEqual(resolve(url).func, views.viewReturnedBooks)

    def test_exams_url_resolves(self):
        url = reverse('Exams')
        self.assertEqual(resolve(url).func, views.exams)

    def test_examsrepo_url_resolves(self):
        url = reverse('examrepo')
        self.assertEqual(resolve(url).func, views.examsrepo)

    def test_search_book_RUD_url_resolves(self):
        url = reverse('search_book_RUD')
        self.assertEqual(resolve(url).func, views.search_book_RUD)

    def test_extendBook_url_resolves(self):
        url = reverse('extendBook', args=[1])
        self.assertEqual(resolve(url).func, views.extendBook)

    def test_searchissuedbooks_url_resolves(self):
        url = reverse('searchissuedbook')
        self.assertEqual(resolve(url).func, views.searchissuedbooks)

    def test_rate_url_resolves(self):
        url = reverse('rate', args=['username', 'serial_number'])
        self.assertEqual(resolve(url).func, views.rate)

    def test_patronpage_url_resolves(self):
        url = reverse('mypage')
        self.assertEqual(resolve(url).func, views.patronpage)

    def test_finepaid_url_resolves(self):
        url = reverse('finepaid', args=[1])
        self.assertEqual(resolve(url).func, views.finepaid)

    def test_bookmark_url_resolves(self):
        url = reverse('bookmark', args=['book'])
        self.assertEqual(resolve(url).func, views.bookmark)