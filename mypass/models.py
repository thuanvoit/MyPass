from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from datetime import datetime
from . import utils

lst_unknown = [None,False,"","False","None"]

class User(AbstractUser):
    pass

class Password(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    url = models.CharField(max_length=2048)
    domain_name = models.CharField(max_length=160)
    domain_username = models.CharField(max_length=20)
    domain_password = models.BinaryField(max_length=500)
    note = models.TextField(blank=True)
    date_edit = models.DateTimeField(auto_now_add=True, editable=True)
    favorite = models.BooleanField(default=False)
    logo = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user} account on {self.domain_name}: username is {self.domain_username}, password is {self.domain_password[0]}***"

    def serialize(self):
        return {
            'id': self.id,
            'url': self.url,
            'domain_name': self.domain_name,
            'domain_username': self.domain_username,
            'domain_password': self.domain_password,
            'note': self.note,
            'date_edit': self.date_edit,
            'favorite': self.favorite,
            'pageCode': 'password_view',
        }

    def save(self, *args, **kwargs):
        if not self.favorite:
            self.date_edit = datetime.now()
        super().save(*args, **kwargs)


class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_note")
    name = models.CharField(max_length=160)
    note = models.TextField(blank=True)
    date_edit = models.DateTimeField(auto_now_add=True, editable=True)
    favorite = models.BooleanField(default=False)
    share = models.BooleanField(default=False)
    share_url = models.CharField(default=None, editable=False, max_length=100)

    def __str__(self):
        return f"{self.user} note {self.name}: {self.note}[:10]***"

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'note': self.note,
            'date_edit': self.date_edit,
            'favorite': self.favorite,
            'share': self.share,
            'share_url': self.share_url,
            'pageCode': 'note_view',
        }

    def save(self, *args, **kwargs):
        if self.favorite:
            pass
        elif self.share:
            if self.share_url in lst_unknown:
                self.share_url = utils.generate_url
        else:
            self.date_edit = datetime.now()
        super().save(*args, **kwargs)


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_address")
    first_name = models.CharField(max_length=160)
    middle_name = models.CharField(max_length=160, blank=True)
    last_name = models.CharField(max_length=160)
    address = models.CharField(max_length=95)
    city = models.CharField(max_length=35)
    state = models.CharField(max_length=35)
    zipcode = models.CharField(max_length=6)
    email = models.EmailField(max_length=200, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    note = models.TextField(blank=True)
    date_edit = models.DateTimeField(auto_now_add=True, editable=True)
    favorite = models.BooleanField(default=False)
    share = models.BooleanField(default=False)
    share_url = models.CharField(default=None, editable=False, max_length=100)
    encoded_address = models.CharField(max_length=500)

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zipcode': self.zipcode,
            'email': self.email,
            'phone': self.phone,
            'note': self.note,
            'date_edit': self.date_edit,
            'favorite': self.favorite,
            'share': self.share,
            'pageCode': 'address_view',
        }

    def save(self, *args, **kwargs):
        if self.favorite:
            pass
        elif self.share:
            if self.share_url in lst_unknown:
                self.share_url = utils.generate_url()
        else:
            self.date_edit = datetime.now()
        super().save(*args, **kwargs)


class Card(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_card")
    card_name = models.CharField(max_length=160)
    card_number = models.BinaryField(max_length=500)
    card_number_ending = models.CharField(max_length=4, default=None)
    security_code = models.BinaryField(max_length=500)
    expiration = models.BinaryField(max_length=500)
    note = models.TextField(blank=True)
    date_edit = models.DateTimeField(auto_now_add=True, editable=True)
    favorite = models.BooleanField(default=False)
    logo = models.URLField(blank=True)


    def serialize(self):
        return {
            'id': self.id,
            'card_name': self.card_name,
            'card_number': self.card_number,
            'security_code': self.security_code,
            'expiration': self.expiration,
            'note': self.note,
            'date_edit': self.date_edit,
            'favorite': self.favorite,
            'logo': self.logo,
            'pageCode': 'card_view',

        }
    def save(self, *args, **kwargs):
        if not self.favorite:
            self.date_edit = datetime.now()
        super().save(*args, **kwargs)


class BankAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bankaccount")
    bank_name = models.CharField(max_length=160)
    account_type = models.CharField(max_length=50)
    routing_number = models.BinaryField(max_length=500)
    account_number = models.BinaryField(max_length=500)
    account_number_ending = models.CharField(max_length=4, default=None)
    pin_number = models.BinaryField(max_length=500)
    branch_address = models.CharField(max_length=500)
    phone = models.CharField(max_length=10)
    note = models.TextField(blank=True)
    date_edit = models.DateTimeField(auto_now_add=True, editable=True)
    favorite = models.BooleanField(default=False)
    logo = models.URLField(blank=True)

    def serialize(self):
        return {
            'id': self.id,
            'bank_name': self.bank_name,
            'account_type': self.account_type,
            'routing_number': self.routing_number,
            'account_number': self.account_number,
            'account_number_ending': self.account_number_ending,
            'pin_number': self.pin_number,
            'branch_address': self.branch_address,
            'phone': self.phone,
            'note': self.note,
            'date_edit': self.date_edit,
            'favorite': self.favorite,
            'logo': self.logo,
            'pageCode': 'bankaccount_view',

        }

    def save(self, *args, **kwargs):
        if not self.favorite:
            self.date_edit = datetime.now()
        super().save(*args, **kwargs)


class EncryptPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_encrypt_pass")
    password = models.ForeignKey(Password, on_delete=models.CASCADE, related_name="encrypt_password")
    key = models.BinaryField(max_length=500)

class EncryptCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_encrypt_card")
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="encrypt_card")
    key = models.BinaryField(max_length=500)

class EncryptBankAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_encrypt_bankaccount")
    bankaccount = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name="encrypt_bankaccount")
    key = models.BinaryField(max_length=500)