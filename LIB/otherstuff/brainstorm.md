# Extension Function
This increases the due date of the book the patron borrowed. Ways of doing this:-

    - Have a fixed extension duration, ie. the number of days added is fixed.
    - Allow the librarian to choose the numbers of days/ date.
## Method One:
When the extend button is clicked a function is called that adds number of days to `IssueBook.due_date`.

## Method Two:
When the extend button is clicked it opens the IssueBookForm where the other fields except the due date field are inactive.
Maybe I should create `ExtendBookForm`...

## Addition
### What if the user can request for an extension from the OPAC?
This means that there has to be a page which shows the books they borrowed and request extension function.<br>
When button is clicked the request is sent to the librarians waiting approval.

## At 11:43 18/03/2023, implemented Method Two
Added a pop up style view where the librarian will choose the date for themselves. However, it does have a datepicker, may implement later.

# Rating sys
I need to add a rating system this will possibly help when making a recommender system.
## Method
form-select on the bookview page
Show the avg rating of the book

# Bookmarking
Patron can bookmark a book they like or want to remember down the line.
I will need a bookmark model, with username, and book
I want two icons one showing a book that is bookmark by patron and vice versa.

# Patron history
Patron history can be used and possibly displayed to them. This can maybe help in building the content based recommendation sys.

# comment section/review section
Patrons can give a review about the book etc. and update or delete that post, also displaying the username which also functions as a link to their profile.