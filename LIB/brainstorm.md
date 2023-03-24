# Extension Function
This increases the due date of the book the patron borrowed. Ways of doing this:-

    - Have a fixed extension duration, ie. the number of days added is fixed.
    - Allow the librarian to choose the numbers of days/ date.
## Method One:
When the extend button is clicked a function is called that adds number of days to `IssueBook.due_date`.

## Method Two:
When the extend button is clicked it opens the IssueBookForm where the other fields except the due date field are inactive.
Maybe I should create `ExtendBookForm`...

##Addition
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