from .models import AddBook, History, Bookmark, IssueBook, ReturnedBook, Rating, BookDetail, Book
# BY: BEN MUNYASIA BCSC01/0018/2018

def content_based_recommender_sys(req):
    import pandas as pd
    import numpy
    from sklearn.feature_extraction.text import TfidfVectorizer as Tfidf
    from sklearn.metrics.pairwise import linear_kernel
    import random
    
    # get_title = 'Recommendations'
    if Book.objects.count() != 0 and BookDetail.objects.count != 0:

        books = pd.DataFrame(list(Book.objects.all().values()))
        books.rename(columns={"book_details_id": "id"},inplace=True)
        books_details = pd.DataFrame(list(BookDetail.objects.all().values()))
        book_repo = pd.merge(books, books_details, on="id", how="inner")
        patron_history = History.objects.filter(username=req.user).exists()
        patron_circulation = ReturnedBook.objects.filter(username=req.user).exists()
        patron_borrowed_books = IssueBook.objects.filter(username=req.user).exists()
        patrons_bookmarks = Bookmark.objects.filter(username=req.user).exists()
        get_title = ''
        if patrons_bookmarks:
            patrons_bookmarks = Bookmark.objects.filter(username=req.user)
            get_title = patrons_bookmarks[random.randint(0,len(patrons_bookmarks)-1)].book.title
            msg = f'Recommendation based on your bookmarks'

        elif patron_history:
            patron_history = History.objects.filter(username=req.user)
            get_title = patron_history[random.randint(0,len(patron_history)-1)].book_viewed.title
            msg = f'Because you viewed {get_title}'
        elif patron_circulation:
            patron_circulation = ReturnedBook.objects.filter(username=req.user)
            get_title = patron_circulation[random.randint(0,len(patron_circulation)-1)].returned_book.title
            msg = f'Based on recent return history "{get_title}"'
        elif patron_borrowed_books:
            patron_borrowed_books = IssueBook.objects.filter(username=req.user)
            get_title = patron_borrowed_books[random.randint(0,len(patrons_bookmarks)-1)].isbn.title
            msg = f'Because you borrowed {get_title}'

        tfidf = Tfidf(stop_words='english')
        book_repo["description"] = book_repo["description"].fillna('')
        description = book_repo["description"]
        tfidf_matrix = tfidf.fit_transform(description)
        # cosine sim
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

        indices = pd.Series(book_repo.index, index=book_repo['title']).drop_duplicates()
        # print(indices['EFFECTS OF PRACTICAL WORK ON STUDENTS’ ACHIEVEMENT'])
        def get_recommendations(title, cosine_sim=cosine_sim):
            ind = indices[title]
            sm_list = []
            sim_score = enumerate(cosine_sim[ind])
            sim_score = sorted(sim_score, key=lambda x:x[1], reverse=True)
            sim_score = sim_score[1:11] # this will show the top ten books similar to target, while not having the target in the list
            cleaned_sim_score = [x for x in sim_score if x[1] >= 0.05]
            for i in sim_score:
                print(i[1])
            sim_index = [i[0] for i in cleaned_sim_score]
            rec_list = book_repo['title'].iloc[sim_index]
            
            sm_list.append(rec_list)
            return sm_list
        if get_title != "":
            return get_recommendations(get_title)
    

def user_user_collab_filtering(req):
    # Data processing
    import pandas as pd
    import numpy as np
    import scipy.stats
    from sklearn.metrics.pairwise import cosine_similarity

    if Rating.objects.all().count() != 0 and Rating.objects.filter(username=req.user).exists():
        """ Recommender system algo """

        # Convert the data model to a dataframe
        ratings = pd.DataFrame(list(Rating.objects.all().values()))
        # renaming the columns of the ratings model to match with the key columns of the Addbook model
        ratings.rename(columns={"username_id":"username", "book_rated_id":"serial_number"},inplace=True)
        books = pd.DataFrame(list(Book.objects.all().values()))
        books.rename(columns={"book_details_id": "id"}, inplace=True)
        books_details = pd.DataFrame(list(BookDetail.objects.all().values()))
        books_repo = pd.merge(books, books_details, on="id", how="inner")
        df = pd.merge(ratings, books_repo, on='serial_number', how='inner')
        agg_ratings = df.groupby('serial_number').agg(mean_rating = ('rate', 'mean'),
                                                    number_of_rating=('rate', 'count')).reset_index()
        matrix = df.pivot_table(index='username', columns='serial_number', values='rate')
        # Normalize user-item matrix
        matrix_norm = matrix.subtract(matrix.mean(axis=1), axis='rows')
        # User similarity matrix using Pearson correlation
        user_similarity = matrix_norm.T.corr(method='pearson', min_periods=1)
        print(user_similarity)
        # Pick a user ID
        # check if user has rated any book
        print('Hi', req.user)
        print(Rating.objects.filter(username_id=req.user.id).exists())
        
        picked_userid = req.user.id

        # Remove picked user ID from the candidate list
        user_similarity.drop(index=picked_userid, inplace=True)

        # Take a look at the data
        print(picked_userid)
        # Number of similar users
        n = 10

        # User similarity threashold
        user_similarity_threshold = 0.5

        # Get top n similar users
        similar_users = user_similarity[user_similarity[picked_userid] >= user_similarity_threshold][
                            picked_userid].sort_values(ascending=False)[:n]
        # Books that the target user has read
        picked_userid_read = matrix_norm[matrix_norm.index == picked_userid].dropna(axis=1, how='all')

        # Print out top n similar users
        # print(f'The similar users for user {picked_userid} are', similar_users)
        # Books that similar users read. Remove books that none of the similar users have read
        similar_user_books = matrix_norm[matrix_norm.index.isin(similar_users.index)].dropna(axis=1, how='all')
        # Remove the read books from the book lists
        similar_user_books.drop(picked_userid_read.columns, axis=1, inplace=True, errors='ignore')
        # A dictionary to store item scores
        item_score = {}

        # Loop through items
        for i in similar_user_books.columns:
            # Get the ratings for book i
            book_rating = similar_user_books[i]
            # Create a variable to store the score
            total = 0
            # Create a variable to store the number of scores
            count = 0
            # Loop through similar users
            for u in similar_users.index:
                # If the book has rating
                if pd.isna(book_rating[u]) == False:
                    # Score is the sum of user similarity score multiply by the book rating
                    score = similar_users[u] * book_rating[u]
                    # Add the score to the total score for the book so far
                    total += score
                    # Add 1 to the count
                    count += 1
            # Get the average score for the item
            item_score[i] = total / count

        # Convert dictionary to pandas dataframe
        item_score = pd.DataFrame(item_score.items(), columns=['book', 'book_score'])

        # Sort the books by score
        ranked_item_score = item_score.sort_values(by='book_score', ascending=False)

        # Select top m books
        m = 10
        ranked_item_score.head(m)
        ranked_item_score.drop(['book_score'],axis=1, inplace=True, errors='ignore')
        recommended_list = []
        for k in ranked_item_score['book']:
            if k != 1:
                recommended_list.append(Book.objects.filter(serial_number=k))
        return recommended_list
    
def client_books_recommendation(request):
    """
        Merges the recommendations from user_user_collab_filtering and content_based_recommender_sys
    """
    user_user_list = user_user_collab_filtering(request)   
    
    r = content_based_recommender_sys(request)
    print("recommender sys",r)
    content_based_list = []
    if r:
        content_based_list = [Book.objects.filter(title=title) for title in r[0]]
    
    if user_user_list != [] and content_based_list != []:
        return list(set(*user_user_list,*content_based_list))
    elif user_user_list == [] and content_based_list != []:
        return content_based_list
    elif user_user_list != [] and content_based_list == []:
        
        return user_user_list
    else: 
        return False
    

