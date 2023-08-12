from .models import AddBook
from scholarly import scholarly, ProxyGenerator
from asgiref.sync import sync_to_async
import asyncio

def genreList():
        books = AddBook.objects.all()        
        lst = []
        for x in books:
            lst.append(x.genre)
            # print(lst)
        return set(lst)


def grab_author_details(context, author):
        try:
            search_query = scholarly.search_author(f'{author[0].Author}')
            author = scholarly.fill(next(search_query))
            strip_author = author['publications'] # seleting dict with publications
            # print(strip_author)
            counter = 0
            pub = []
            citedby = []
            num = []
            # asyncio.sleep(5)
            for k in strip_author:
                if counter < 4:
                    for v in k:
                        if v == 'bib':
                            pub.append(k[v])

                        elif  v == 'citedby_url':
                            citedby.append(k[v])

                        elif v == 'num_citations':
                            num.append(k[v])
                else:
                    break
                counter += 1
            context['pub'] = pub
            context['citedby'] = citedby
            context['num'] = num

            print(pub)
        except:
            context['author404'] = f'Did not find books related to {author[0].Author} in Google scholar'


def affiliation(request):
    """Returns a clients library branch :param:request"""
    return request.user.profile.affiliation
