from .models import AddBook

def genreList():
        books = AddBook.objects.all()        
        lst = []
        for x in books:
            lst.append(x.genre)
            # print(lst)
        return set(lst)