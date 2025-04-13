Setup & Running Campusmart
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

