# TEST CASE

## TemplateDoesNotExist
- Incorrect path given at views.py

## Data entered in forms not been stored at its respective models.
- Make sure the input name is the same as the field names of the models.
- Make sure during checking if its a post request, the 'request.post or None' parameter is passed, i.e form = YourForm(request.POST or None)

