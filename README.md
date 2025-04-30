Setup & Running CampusMart
=====
Run the following in the command line:
```
cd src/marketplace
python3 manage.py makemigrations campusmart
python3 manage.py migrate
python3 manage.py runserver
```
If you get "`Error: That port is already in use`", run the following:
```
python3 manage.py runserver 129.74.152.125:<PORT>
```
where `<PORT>` is your assigned port number.
# Logging In/Creating Account 
1. Click on "Login/Signup". <br>
2. If you have an existing account, type in the username and password. <br>
3. Otherwise, click on "Create User". <br>
a. Enter a name, username, email, and password. <br>
4. Once you have successfully create a user, log in using those credentials. (You should now be at the home page)
# Navigating CampusMart
* <u><b>Home</b></u>: redirects you back to the home page (same as clicking CampusMart in top-left corner)
* <u><b>Browse</b></u>: displays all items being sold (20 per page)
* <u><b>Sell</b></u>: brings you to "create-listing" page
* <u><b>Search Bar</b></u>: search for items based on title or description


