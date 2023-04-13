# trying to build a content recommender sys

from LIBSYS.models import AddBook

def content_based_recommender_sys():
    books_repo = pd.DataFrame(list(AddBook.objects.all().values()))
    print(books_repo.head())