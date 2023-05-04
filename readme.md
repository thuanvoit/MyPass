# Overview

MyPass is a personal and secure information management solution that allows you to store passwords, notes, addresses, payment cards, and bank accounts safely. Access your MyPass data on any device, from anywhere. All your private data, such as passwords and financial information, is encrypted in our database and can only be revealed with valid credentials.


# Why I Made MyPass for CS50 Capstone

MyPass is a mobile-responsive web application built with the Django framework, utilizing JavaScript and Bootstrap for its user interface.

What sets MyPass apart from other projects is its focus on user privacy. Unlike social network or e-commerce projects, MyPass encrypts sensitive user data with a private key before storing it securely. This data remains encrypted even when the user is logged in, only revealing it upon request.

To enhance the user experience, MyPass employs Clearit API to retrieve domain and company information for visualization. Additionally, MyPass incorporates the Luhn Algorithm to instantly validate card numbers as users input them.

# Specification

- **Create New Item**: Users who are signed in can create a new item. On its view, they can retrieve its proper input form and click "Save" to save it to the database.

- **Password, Cards, and Bank Account Page**: Use Clearbit API to get the website name and logo URL based on the domain. An API key was included on utils.py.

- **Edit Item**: The encrypted data will be decrypted and allow the user to edit their data. When the user clicks the "Edit" button, the data will be encrypted with a new key and saved to a safe place.

- **Encrypt Data**: When the user clicks "Save" on a new item, the program will encrypt only sensitive information with a key. This key allows them to decrypt the encrypted data when they need to view it.

- **Favorite**: Users can click the "Star" button to toggle whether or not they have favorited the item.

- **Delete**: Users can click the "Trash Bin" button to delete item data from the database.

- **Share**: Users can share their notes and address to external users. They can toggle the item share options when creating a new item or while editing the item. The share function is only available for notes and addresses.

- **View**: Data will be decrypted, allowing users who are logged in to view it. Next to the link field, users can click on the "Open" button to open the link on a new tab. Next to any other fields, users can click on the "Clipboard" button to copy data in that field.

- **Address Page**: My Pass uses the Google Maps API to visualize the address.

- **Payment Card Page**: The Luhn Algorithm is used to check if a card number is valid. If it is valid, the card number field border will show green; if it is invalid, the border will show red.

- **Profile Page**: Users who are signed in can edit their last name, first name, email, and password. They are also allowed to completely delete their account and all related data.


# File Contents

## Front-end
### HTML
- **layout.html**: This is the base template for every page, which includes the navigation bar.

- **register.html**: This template contains the sign-up form.

- **login.html**: This template contains the login form.

- **profile.html**: This template shows the user profile.

- **password.html**: This template shows all the user passwords in the database.

- **note.html**: This template shows all the user notes in the database.

- **address.html**: This template shows all the user addresses in the database.

- **card.html**: This template shows all the user cards in the database.

- **bankaccount.html**: This template shows all the user bank accounts in the database.

- **sharenote.html**: This template shows the shared note contents.

- **shareaddress.html**: This template shows the shared address contents.

### CSS
- **styles.css**: This is the CSS that positions some components in every template.

### Javascript

- **script.js**: This is the script that runs functions in every template.

## Back-end

- **admin.py**: This file registers models into Django My Pass administration. Admin allows the user to control the database.

- **forms.py**: This file contains all the forms for the user to input information.

- **models.py**: This file defines any models for My Pass.

- **urls.py**: This file handles all the URLs of My Pass. It links the views.py functions and URLs.

- **utils.py**: This file contains functions that find company information, run the Luhn algorithm to check cards, and encrypt and decrypt sensitive information.

- **views.py**: This file contains and renders all the views and functions for My Pass. Views.py queries the My Pass database. The views.py functions send and receive HTTP requests and responses.


# How to Run

Use cd to the project directory.

Run `pip install -r requirements.txt` to install all necessary dependencies to run My Pass.

Run `python manage.py makemigrations` to make migrations for the network app.

Run `python manage.py migrate` to apply migrations to your database.

Run `python manage.py runserver` and access My Pass by typing `127.0.0.1:8000` or `localhost:8000` on browser.