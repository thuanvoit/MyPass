from django import forms

class PasswordForm(forms.Form):
    
    url = forms.CharField(max_length=2048, label="Domain", widget=forms.TextInput(attrs={'class': 'form-control my-modal-form-control'}))
    domain_username = forms.CharField(max_length=20, label="Username", widget=forms.TextInput(attrs={'class': 'form-control my-modal-form-control'}))
    domain_password = forms.CharField(max_length=20, label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control my-modal-form-control'}))
    note = forms.CharField(required=False, widget=forms.Textarea(
                                attrs={
                                    'class': 'form-control  my-modal-form-control',
                                    'rows': 5
                                }))
    # formid = forms.CharField(max_length=2048,required=False ,label="ID", widget=forms.TextInput(attrs={'class': 'form-control my-modal-form-control',
                                                                        
    #                                                                     'disabled':None}))
    

class NoteForm(forms.Form):
    note_name = forms.CharField(max_length=2048, label="Name", widget=forms.TextInput(attrs={'class': 'form-control my-modal-form-control'}))
    note = forms.CharField(widget=forms.Textarea(
                                attrs={
                                    'class': 'form-control  my-modal-form-control',
                                    'rows': 15
                                }))

class AddressForm(forms.Form):
    first_name = forms.CharField(max_length=50, label="First Name", widget=forms.TextInput(attrs={'class': 'form-control my-modal-form-control'}))
    middle_name = forms.CharField(required=False, max_length=50, label="Middle Name", widget=forms.TextInput(attrs={'class': 'form-control my-modal-form-control'}))
    last_name = forms.CharField(max_length=50, label="Last Name", widget=forms.TextInput(attrs={'class': 'form-control my-modal-form-control'}))

    address = forms.CharField(max_length=95, label="Address", widget=forms.TextInput(attrs={'class': 'form-control my-modal-form-control'}))
    city = forms.CharField(max_length=35, label="City", widget=forms.TextInput(attrs={'class': 'form-control my-modal-form-control'}))
    state = forms.CharField(max_length=35, label="State", widget=forms.TextInput(attrs={'class': 'form-control my-modal-form-control'}))
    zipcode = forms.CharField(max_length=6, label="Zip Code", widget=forms.TextInput(attrs={'class': 'form-control my-modal-form-control'}))
    email = forms.EmailField(max_length=200, required=False, label="Email", widget=forms.EmailInput(attrs={'class': 'form-control my-modal-form-control'}))
    phone = forms.CharField(max_length=10, required=False, label="Phone Number", widget=forms.NumberInput(attrs={'class': 'form-control my-modal-form-control'}))
    
    note = forms.CharField(required=False, widget=forms.Textarea(
                                attrs={
                                    'class': 'form-control  my-modal-form-control',
                                    'rows': 5
                                }))

class CardForm(forms.Form):
    card_name = forms.CharField(max_length=160, label="Name", widget=forms.TextInput(attrs={'class': 'form-control my-modal-form-control'}))
    card_number = forms.CharField(max_length=20, label="Card Number", widget=forms.NumberInput(attrs={'class': 'form-control my-modal-form-control'}))
    security_code = forms.CharField(max_length=20, label="Security Code", widget=forms.PasswordInput(attrs={'class': 'form-control my-modal-form-control'}))
    expiration_date = forms.CharField(max_length=10, label="Expiration Date", widget=forms.TextInput(attrs={'class': 'form-control my-modal-form-control'}))
    note = forms.CharField(required=False, widget=forms.Textarea(
                                attrs={
                                    'class': 'form-control  my-modal-form-control',
                                    'rows': 5
                                }))

class BankAccountForm(forms.Form):
    bank_name = forms.CharField(max_length=160, label="Bank Name", widget=forms.TextInput(attrs={'class': 'form-control my-modal-form-control'}))
    bank_type = forms.CharField(max_length=160, label="Account Type", widget=forms.TextInput(attrs={'class': 'form-control my-modal-form-control'}))
    routing_number = forms.CharField(max_length=20, label="Routing Number", widget=forms.NumberInput(attrs={'class': 'form-control my-modal-form-control'}))
    account_number = forms.CharField(max_length=20, label="Account Number", widget=forms.NumberInput(attrs={'class': 'form-control my-modal-form-control'}))
    pin_number = forms.CharField(max_length=20, min_length=4, label="PIN Number", widget=forms.NumberInput(attrs={'class': 'form-control my-modal-form-control'}))
    address = forms.CharField(max_length=95, label="Branch Address", widget=forms.TextInput(attrs={'class': 'form-control my-modal-form-control'}))
    phone = forms.CharField(max_length=10, label="Branch Phone Number", widget=forms.NumberInput(attrs={'class': 'form-control my-modal-form-control'}))

    note = forms.CharField(required=False, widget=forms.Textarea(
                                attrs={
                                    'class': 'form-control  my-modal-form-control',
                                    'rows': 5
                                }))