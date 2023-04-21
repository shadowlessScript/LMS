# What is this project about?
This project main objective was to a recommendation system to the OPAC (Open Public Access Catalog), which will recommend books to patrons. Two recommendation techniques were used:
- User-based collaborative filtering.
- Content based collaborative filtering.

# Get Started
- Ensure you have python installed in the system.
## virtual environment
- Then create a python virtual environment, preferably inside the project folder.
``` console
python -m venv <preferredname>
```
### Active the virtual environment
#### CMD 
```console
.\<preferredname>\Scripts\activate
``` 
#### Linux or gitbash
```console
source <preferredname>/Scripts/activate
```
## requirements
- install the project's necessary requirements from  requirements.txt
```console
pip install -r requirements.txt
```
## Launch
 ``` console
python manage.py runserver
``` 
(ensure in the folder name LIB)
