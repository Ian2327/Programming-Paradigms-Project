# Welcome to CampusMart
## Setup & Running CampusMart
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

## Logging In/Creating Account 
1. Click on "Login/Signup". <br>
2. If you have an existing account, type in the username and password. <br>
3. Otherwise, click on "Create User". <br>
a. Enter a name, username, email, and password. <br>
4. Once you have successfully create a user, log in using those credentials. (You should now be at the home page)

## Navigating CampusMart
* <u><b>Home</b></u>: redirects you back to the home page (same as clicking CampusMart in top-left corner)
* <u><b>Browse</b></u>: displays all items being sold (20 per page)
* <u><b>Sell</b></u>: brings you to "create-listing" page
* <u><b>Search Bar</b></u>: search for items based on title or description

# (The following require you to be logged in)
## Creating a Listing
1. Enter a title that is displayed for the item (max: 200 character) <br>
2. Enter a description (only first 100 characters are displayed) (max: 4000 characters)<br>
3. Enter a price for the item <br>
4. Select the item's condition from the dropdown (new, good, acceptable, poor, etc.)<br>
5. Add an image of the item <br>
a. If you want to upload more than 1 image, click on "Add Another Image", then upload an image

## Updating/Deleting a Listing
1. Navigate to the listing details or click "My Listings" under the dropdown after selecting the white box in the top-right corner with your username
2. Select "Edit Item" to edit the description, availability, price, add images, etc.
3. Select "Delete Item" to delete the listing (note: you will receive a listing credit back) 


## Sending Messages
1. Click on a listing
2. Click "Chat with Seller"
3. Type your message and hit "Send"

## Responding to Messages
1. Click on the white box with the dropdown arrow in the top-right corner
2. Click "Messages" (you will be redirected to view all message chats)
3. Click the chat room you want to reply to
4. Type a response and hit "Send"

## Buying Listings
1. Click on the white box with the dropdown arrow in the top-right corner
2. Click "Buy Listings"
3. Enter the number of listings you would like to purchase and hit "Buy"

## Logging Out
1. Click on the white box with the dropdown arrow in the top-right corner
2. Click "Logout"