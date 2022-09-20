# TEST CASE

## TemplateDoesNotExist
- Incorrect path given at views.py.
- App not installed.

## Data entered in forms not been stored at its respective models.
- Make sure the input name is the same as the field names of the models.
- Make sure during checking if it's a post request, the 'request.post or None' parameter is passed, i.e form = YourForm(request.POST or None)

## first name and last name in custom usercreationform not to added to db after registration
- I had written 'first_Name' and 'last_Name' instead of 'first_name' and 'last_name'

## Image not uploaded through form even though form is_valid
- add enctype="multipart/form-data" in the opening form tag

## RelatedObjectDoesNotExist error
- add signals to create an instance of the related models
