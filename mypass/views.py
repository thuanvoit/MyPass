from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import *
from django.db import IntegrityError
from . import utils
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.contrib.auth.hashers import check_password
import pyperclip as pc
from django.core.paginator import PageNotAnInteger, Paginator
from django.contrib.auth.hashers import check_password


def index(request):
    return render(request, "mypass/index.html", {
        'pageTitle': 'Home',
        'modalTitle': 'Index',
    })


@login_required
@csrf_exempt
def profile(request):
    size = {
        'password_len': len(Password.objects.filter(user=request.user)),
        'note_len': len(Note.objects.filter(user=request.user)),
        'address_len': len(Address.objects.filter(user=request.user)),
        'card_len': len(Card.objects.filter(user=request.user)),
        'bankaccount_len': len(BankAccount.objects.filter(user=request.user)),
    }

    return render(request, "mypass/profile.html", {
        'pageTitle': 'Profile',
        'pageCode': 'profile_view',
        'size': size,
    })
 

@login_required
def password(request):

    data = Password.objects.filter(
        user=request.user).order_by('date_edit').reverse()
    
    data_paged = Paginator(data, 12)
    page_number = request.GET.get('page')

    try: page_obj = data_paged.get_page(page_number)
    except PageNotAnInteger: page_obj = data_paged.page(1)


    if request.method == 'POST':
        form = PasswordForm(request.POST)

        if form.is_valid():
            # data
            url = form.cleaned_data['url']
            url = utils.find_company_by_domain(url)['domain']
            domain_name = utils.find_company_by_domain(url)['name']
            domain_username = form.cleaned_data['domain_username']
            domain_password = form.cleaned_data['domain_password']
            note = form.cleaned_data['note']
            logo = utils.find_company_by_domain(url)['logo']

            try:
                if request.POST.get("favorite-checkbox", False) == False:
                    favorite_bool = False
                else: favorite_bool = True
            except: favorite_bool = False

            # encrypt contents
            encryptData = utils.encrypt(domain_password)
            encrypt_password = encryptData['encrypt_content']
            key = encryptData['key']

            new_password = Password(user=request.user,
                                    url=url,
                                    domain_name=domain_name,
                                    domain_username=domain_username,
                                    domain_password=encrypt_password,
                                    note=note,
                                    favorite=favorite_bool,
                                    logo=logo,
                                    )
            new_password.save()

            encrypt_key = EncryptPassword(user=request.user,
                                            password=new_password,
                                            key=key,
                                            )
            encrypt_key.save()

            return HttpResponseRedirect(reverse("password_view"))

    else:
        form = PasswordForm()

    return render(request, "mypass/password.html", {
        'pageTitle': 'Password',
        'modalTitle': 'New Password',
        'form': form,
        'pageCode': 'password_view',
        'data': page_obj,
    })


@login_required
def note(request):

    data = Note.objects.filter(
        user=request.user).order_by('date_edit').reverse()

    data_paged = Paginator(data, 12)
    page_number = request.GET.get('page')

    try: page_obj = data_paged.get_page(page_number)
    except PageNotAnInteger: page_obj = data_paged.page(1)

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            # data
            name = form.cleaned_data['note_name']
            note = form.cleaned_data['note']

            #favorite checkbox
            try:
                if request.POST.get("favorite-checkbox", False) == False:
                    favorite_bool = False
                else:
                    favorite_bool = True
            except:
                favorite_bool = False

            #share checkbox
            try:
                if request.POST.get("shareCheckBox", False) == False:
                    share_bool = False
                else:
                    share_bool = True
            except:
                share_bool = False
            
            share_url = utils.generate_url()

            new_item = Note(user=request.user,
                            name=name,
                            note=note,
                            favorite=favorite_bool,
                            share=share_bool,
                            share_url=share_url,
                            )
            new_item.save()

            return HttpResponseRedirect(reverse("note_view"))
    else:
        form = NoteForm()

    return render(request, "mypass/note.html", {
        'pageTitle': 'Note',
        'modalTitle': 'New Note',
        'form': form,
        'pageCode': 'note_view',
        'data': page_obj,
    })


def share_note(request, share_url):
    
    try:
        if Note.objects.get(share_url=share_url).share:
            data = Note.objects.get(share_url=share_url)
        else: 
            data = None

    except Note.DoesNotExist:
        data = None


    return render(request, "mypass/sharenote.html", {
        'pageTitle': 'Note',
        'data': data,
    })


@login_required
def address(request):

    data = Address.objects.filter(
        user=request.user).order_by('date_edit').reverse()
    
    data_paged = Paginator(data, 12)
    page_number = request.GET.get('page')

    try: page_obj = data_paged.get_page(page_number)
    except PageNotAnInteger: page_obj = data_paged.page(1)

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            # data

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            middle_name = form.cleaned_data['middle_name']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            note = form.cleaned_data['note']

            
            try:
                if request.POST.get("favorite-checkbox", False) == False:
                    favorite_bool = False
                else:
                    favorite_bool = True

            except:
                favorite_bool = False

            #share checkbox
            try:
                if request.POST.get("shareCheckBox", False) == False:
                    share_bool = False
                else:
                    share_bool = True
            except:
                share_bool = False
            
            share_url = utils.generate_url()


            encoded_address = utils.encodeURL(address, city, state, zipcode)

            new_item = Address(user=request.user,
                               first_name=first_name,
                               last_name=last_name,
                               middle_name=middle_name,
                               address=address,
                               city=city,
                               state=state,
                               zipcode=zipcode,
                               email=email,
                               phone=phone,
                               note=note,
                               share=share_bool,
                               share_url=share_url,
                               favorite=favorite_bool,
                               encoded_address=encoded_address,

                               )
            new_item.save()

            return HttpResponseRedirect(reverse("address_view"))
    else:
        form = AddressForm()

    return render(request, "mypass/address.html", {
        'pageTitle': 'Address',
        'modalTitle': 'New Address',
        'form': form,
        'pageCode': 'address_view',
        'data': page_obj,
    })

def share_address(request, share_url):
    try:
        if Address.objects.get(share_url=share_url).share:
            data = Address.objects.get(share_url=share_url)
        else: 
            data = None

    except Address.DoesNotExist:
        data = None


    return render(request, "mypass/shareaddress.html", {
        'pageTitle': 'Note',
        'data': data,
    })

@login_required
def card(request):
    data = Card.objects.filter(
        user=request.user).order_by('date_edit').reverse()
    
    data_paged = Paginator(data, 12)
    page_number = request.GET.get('page')

    try: page_obj = data_paged.get_page(page_number)
    except PageNotAnInteger: page_obj = data_paged.page(1)

    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            # data

            card_name = form.cleaned_data['card_name']
            card_number = form.cleaned_data['card_number']
            card_number_ending = card_number[-4::]
            security_code = form.cleaned_data['security_code']
            expiration = form.cleaned_data['expiration_date']

            data_dict = {0: card_number, 1: security_code, 2: expiration}
            encrypt_data = utils.encrypt(data_dict)

            key = encrypt_data['key']
            encrypt_card_number = encrypt_data['encrypt_content'][0]
            encrypt_security_code = encrypt_data['encrypt_content'][1]
            encrypt_expiration = encrypt_data['encrypt_content'][2]

            note = form.cleaned_data['note']
            logo = utils.name_to_company_logo(card_name)

            try:
                if request.POST.get("favorite-checkbox", False) == False:
                    favorite_bool = False
                else:
                    favorite_bool = True

            except:
                favorite_bool = False
                #require_pass_bool = False

            new_item = Card(user=request.user,
                            card_name=card_name,
                            card_number=encrypt_card_number,
                            card_number_ending=card_number_ending,
                            security_code=encrypt_security_code,
                            expiration=encrypt_expiration,
                            note=note,
                            favorite=favorite_bool,
                            logo=logo,
                            )
            new_item.save()

            encrypt_key = EncryptCard(user=request.user,
                                        card=new_item,
                                        key=key,
                                        )
            encrypt_key.save()

            return HttpResponseRedirect(reverse("card_view"))
    else:
        form = CardForm()

    return render(request, "mypass/card.html", {
        'pageTitle': 'Card',
        'modalTitle': 'New Payment Card',
        'form': form,
        'pageCode': 'card_view',
        'data': page_obj,
    })


@login_required
def bankaccount(request):
    data = BankAccount.objects.filter(
        user=request.user).order_by('date_edit').reverse()

    data_paged = Paginator(data, 12)
    page_number = request.GET.get('page')

    try: page_obj = data_paged.get_page(page_number)
    except PageNotAnInteger: page_obj = data_paged.page(1)

    if request.method == 'POST':
        form = BankAccountForm(request.POST)
        if form.is_valid():
            # data

            bank_name = form.cleaned_data['bank_name']
            account_type = form.cleaned_data['bank_type']

            routing_number = form.cleaned_data['routing_number']
            account_number = form.cleaned_data['account_number']
            account_number_ending = account_number[-4::]
            pin_number = form.cleaned_data['pin_number']

            data_dict = {0: routing_number, 1: account_number, 2: pin_number}
            encrypt_data = utils.encrypt(data_dict)

            key = encrypt_data['key']
            encrypt_routing_number = encrypt_data['encrypt_content'][0]
            encrypt_account_number = encrypt_data['encrypt_content'][1]
            encrypt_pin_number = encrypt_data['encrypt_content'][2]

            branch_address = form.cleaned_data['routing_number']
            phone = form.cleaned_data['phone']
            note = form.cleaned_data['note']
            logo = utils.name_to_company_logo(bank_name)

            try:
                if request.POST.get("favorite-checkbox", False) == False:
                    favorite_bool = False
                else:
                    favorite_bool = True

            except:
                favorite_bool = False

            new_item = BankAccount(user=request.user,
                                   bank_name=bank_name,
                                   account_type=account_type,
                                   routing_number=encrypt_routing_number,
                                   account_number=encrypt_account_number,
                                   account_number_ending=account_number_ending,
                                   pin_number=encrypt_pin_number,
                                   branch_address=branch_address,
                                   phone=phone,
                                   note=note,
                                   favorite=favorite_bool,
                                   logo=logo,
                                   )
            new_item.save()

            encrypt_key = EncryptBankAccount(user=request.user,
                                        bankaccount=new_item,
                                        key=key,
                                        )
            encrypt_key.save()

            return HttpResponseRedirect(reverse("bankaccount_view"))
    else:
        form = BankAccountForm()

    return render(request, "mypass/bankaccount.html", {
        'pageTitle': 'Bank Account',
        'modalTitle': 'New Bank Account',
        'form': form,
        'pageCode': 'bankaccount_view',
        'data': page_obj,
    })


@csrf_exempt
def copyit(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        pc.copy(data['content'])
        return JsonResponse({
            'msg': 'copied'
        })

@csrf_exempt
def check_card(request):

    if request.method == "PUT":
        data = json.loads(request.body)
        card_number = data['card_number']
        return JsonResponse({
            'status': utils.check_card_al(card_number)
        })

@csrf_exempt
def edit_account_info(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        username = data['user']
        user_current_last_name = data['user_current_last_name']
        user_current_first_name = data['user_current_first_name']
        user_current_email = data['user_current_email']

        if User.objects.filter(username=username):

            if user_current_email != "" and user_current_first_name != "" and user_current_last_name != "":
                
                this_user = User.objects.get(username=username)

                this_user.last_name = user_current_last_name
                this_user.first_name = user_current_first_name
                this_user.email = user_current_email
                this_user.save()

                return JsonResponse({
                    'status': 200,
                    'message': "Changed"
                })
            else:
                return JsonResponse({
                    'status': 406,
                    'message': "Please check all these fields above"
                })
        return JsonResponse({
                    'status': 406,
                    'message': "User not found"
                })


@csrf_exempt
@login_required
def get_it(request, pageCode, id):
    try:
        if pageCode == "password_view":
            item = Password.objects.get(id=id).serialize()
            password = Password.objects.get(id=id)
            key = EncryptPassword.objects.get(password=password).key
            item['domain_password'] = utils.decrypt(password.domain_password, key)

        elif pageCode == "note_view":
            item = Note.objects.get(id=id).serialize()
        elif pageCode == "address_view":
            item = Address.objects.get(id=id).serialize()
        elif pageCode == "card_view":
            item = Card.objects.get(id=id).serialize()
            card = Card.objects.get(id=id)
            key = EncryptCard.objects.get(card=card).key

            card_number = item['card_number']
            security_code = item['security_code']
            expiration = item['expiration']

            decrypt_data = utils.decrypt({0:card_number, 1:security_code, 2:expiration}, key)

            item['card_number'] = decrypt_data[0]
            item['security_code'] = decrypt_data[1]
            item['expiration'] = decrypt_data[2]

            print(item)

        elif pageCode == "bankaccount_view":
            item = BankAccount.objects.get(id=id).serialize()

            bankaccount = BankAccount.objects.get(id=id)
            key = EncryptBankAccount.objects.get(bankaccount=bankaccount).key

            routing_number = item['routing_number']
            account_number = item['account_number']
            pin_number = item['pin_number']

            decrypt_data = utils.decrypt({0:routing_number, 1:account_number, 2:pin_number}, key)

            item['routing_number'] = decrypt_data[0]
            item['account_number'] = decrypt_data[1]
            item['pin_number'] = decrypt_data[2]
            
    except:
        return JsonResponse({"error": "Item not found"}, status=404)

    if request.method == "PUT":
        return JsonResponse(item)


@csrf_exempt
@login_required
def save_edit_item(request, pageCode, id):

    try:
        if pageCode == "password_view":
            item = Password.objects.get(id=id)
            encrypt_item = EncryptPassword.objects.get(password=item)
        elif pageCode == "note_view":
            item = Note.objects.get(id=id)
        elif pageCode == "address_view":
            item = Address.objects.get(id=id)
        elif pageCode == "card_view":
            item = Card.objects.get(id=id)
        elif pageCode == "bankaccount_view":
            item = BankAccount.objects.get(id=id)
    except:
        return JsonResponse({"error": "Item not found"}, status=404)

    if request.method == "POST":
        data = json.loads(request.body)

        if pageCode == "password_view":
            url = utils.find_company_by_domain(data['url'])['domain']
            item.url = url
            item.domain_name = utils.find_company_by_domain(url)['name']
            item.domain_username = data['domain_username']

            # encrypt contents
            encryptData = utils.encrypt(data['domain_password'])
            encrypt_password = encryptData['encrypt_content']
            encrypt_key = encryptData['key']

            encrypt_item.key = encrypt_key
            encrypt_item.save()

            item.domain_password = encrypt_password
            item.note = data['note']
            item.favorite = data['favorite']
            item.logo = utils.find_company_by_domain(url)['logo']

        elif pageCode == "note_view":
            item.note_name = data['note_name']
            item.note = data['note']
            item.favorite = data['favorite']
            item.share = data['share']

        elif pageCode == "address_view":
            item.first_name = data['first_name']
            item.middle_name = data['middle_name']
            item.last_name = data['last_name']
            item.address = data['address']
            item.city = data['city']
            item.state = data['state']
            item.zipcode = data['zipcode']
            item.email = data['email']
            item.phone = data['phone']
            item.note = data['note']
            item.favorite = data['favorite']
            item.encoded_address = utils.encodeURL(data['address'], data['city'], data['state'], data['zipcode'])
            item.share = data['share']

        elif pageCode == "card_view":
            item.card_name = data['card_name']

            card_number = data['card_number']
            security_code = data['security_code']
            expiration = data['expiration_date']
        
            data_dict = {0: card_number, 1: security_code, 2: expiration}
            encrypt_data = utils.encrypt(data_dict)

            key = encrypt_data['key']

            item.card_number = encrypt_data['encrypt_content'][0]
            item.security_code = encrypt_data['encrypt_content'][1]
            item.expiration = encrypt_data['encrypt_content'][2]

            item.card_number_ending = card_number[-4::]

            encrypt_key = EncryptCard.objects.get(card=item)
            encrypt_key.key = key

            encrypt_key.save()

            item.note = data['note']
            item.favorite = data['favorite']
            item.logo = utils.name_to_company_logo(data['card_name'])


        elif pageCode == "bankaccount_view":
            item.bank_name = data['bank_name']
            item.account_type = data['bank_type']

            #
            routing_number = data['routing_number']
            account_number = data['account_number']
            pin_number = data['pin_number']
        
            data_dict = {0: routing_number, 1: account_number, 2: pin_number}
            encrypt_data = utils.encrypt(data_dict)

            key = encrypt_data['key']

            item.routing_number = encrypt_data['encrypt_content'][0]
            item.account_number = encrypt_data['encrypt_content'][1]
            item.pin_number = encrypt_data['encrypt_content'][2]

            item.account_number_ending = account_number[-4::]

            encrypt_key = EncryptBankAccount.objects.get(bankaccount=item)
            encrypt_key.key = key

            encrypt_key.save()
            #

            item.branch_address = data['address']
            item.phone = data['phone']
            item.note = data['note']
            item.favorite = data['favorite']
            item.logo = utils.name_to_company_logo(data['bank_name'])

        item.save()
        return JsonResponse({'status': "finish"})

    else:
        return HttpResponseRedirect(reverse(pageCode))


@csrf_exempt
@login_required
def star_item(request, pageCode, id):
    try:
        if pageCode == "password_view":
            item = Password.objects.get(id=id)
        if pageCode == "note_view":
            item = Note.objects.get(id=id)
        if pageCode == "address_view":
            item = Address.objects.get(id=id)
        if pageCode == "card_view":
            item = Card.objects.get(id=id)
        if pageCode == "bankaccount_view":
            item = BankAccount.objects.get(id=id)
    except:
        return JsonResponse({"error": "Item not found"}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)['stared']
        if item.favorite == False:
            item.favorite = True
        else:
            item.favorite = False
        print("SAVED TIME COMPLETELY")
        item.save()
        return JsonResponse({'favorite': item.favorite})


@csrf_exempt
@login_required
def delete_item(request, pageCode, pass_id):
    try:
        if pageCode == "password_view":
            item = Password.objects.get(id=pass_id)
        if pageCode == "note_view":
            item = Note.objects.get(id=pass_id)
        if pageCode == "address_view":
            item = Address.objects.get(id=pass_id)
        if pageCode == "card_view":
            item = Card.objects.get(id=pass_id)
        if pageCode == "bankaccount_view":
            item = BankAccount.objects.get(id=pass_id)
    except:
        return JsonResponse({"error": "Item not found"}, status=404)

    if request.method == "POST":
        item.delete()
        return JsonResponse({
            'hello': 'hello',
        })
    else:
        return HttpResponseRedirect(reverse(pageCode))


@csrf_exempt
def get_password(request, id):
    try:
        item = Password.objects.get(user=request.user, id=id).serialize()
        password = Password.objects.get(user=request.user, id=id)
        key = EncryptPassword.objects.get(password=password).key
        item['domain_password'] = utils.decrypt(password.domain_password, key)
    except Password.DoesNotExist:
        return JsonResponse({"error": "Password not found"}, status=404)

    if request.method == "PUT":

        return JsonResponse(item)

    else:
        return JsonResponse(item)

@csrf_exempt
def get_card(request, id):
    try:
        
        item = Card.objects.get(id=id).serialize()
        card = Card.objects.get(id=id)
        key = EncryptCard.objects.get(card=card).key

        card_number = item['card_number']
        security_code = item['security_code']
        expiration = item['expiration']

        decrypt_data = utils.decrypt({0:card_number, 1:security_code, 2:expiration}, key)

        item['card_number'] = decrypt_data[0]
        item['security_code'] = decrypt_data[1]
        item['expiration'] = decrypt_data[2]
        
    except Card.DoesNotExist:
        return JsonResponse({"error": "Card not found"}, status=404)

    if request.method == "PUT":

        return JsonResponse(item)

    else:
        return JsonResponse(item)

@csrf_exempt
def get_bankaccount(request, id):
    try:
        item = BankAccount.objects.get(id=id).serialize()
        bankaccount = BankAccount.objects.get(id=id)
        key = EncryptBankAccount.objects.get(bankaccount=bankaccount).key

        routing_number = item['routing_number']
        account_number = item['account_number']
        pin_number = item['pin_number']

        decrypt_data = utils.decrypt({0:routing_number, 1:account_number, 2:pin_number}, key)

        item['routing_number'] = decrypt_data[0]
        item['account_number'] = decrypt_data[1]
        item['pin_number'] = decrypt_data[2]
        
    except BankAccount.DoesNotExist:
        return JsonResponse({"error": "Account not found"}, status=404)

    if request.method == "PUT":

        return JsonResponse(item)

    else:
        return JsonResponse(item)


def login_view(request):
    if request.method == "POST":
        username = request.POST['input-username'].lower()
        password = request.POST['input-password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "mypass/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "mypass/login.html", {
            'pageTitle': 'Login',
        })


def register_view(request):
    if request.method == "POST":
        firstname = request.POST['input-first-name']
        lastname = request.POST['input-last-name']
        username = request.POST['input-username'].lower()
        email = request.POST['input-email'].lower()
        password = request.POST['input-password']
        confirmation = request.POST['reinput-password']

        if password != confirmation:
            return render(request, "mypass/register.html", {
                "message": "Confirm password does not match password"
            })

        try:
            user = User.objects.create_user(
                first_name=firstname, last_name=lastname,
                email=email, username=username, password=password)

        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })

        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "mypass/register.html", {
            'pageTitle': 'Register',
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
@login_required
def change_password(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        user = data['user']

        new_password = data['new_password']
        confirmation = data['confirmation']
        current_password = data['current_password']
        
        if new_password != "" and confirmation != "" and current_password != "":
            if check_password(current_password, request.user.password):
                if new_password != confirmation:
                    return JsonResponse({
                    'message': 'Password not match',
                    'status': 406,
                    })
                else:
                    user = User.objects.get(username=user)
                    user.set_password(new_password)
                    user.save()
                    
                    login(request, user)

                    return JsonResponse({
                        'message': 'Password changed',
                        'status': 200,
                        })
            else:
                return JsonResponse({
                    'message': 'Password entered invalid',
                    'status': 406,
                    })
        else:
            return JsonResponse({
                    'message': 'Password entered invalid',
                    'status': 406,
                    })


@csrf_exempt
@login_required
def delete_account(request):
    if request.method == "PUT":

        data = json.loads(request.body)

        user = data['user']
        currentpassword= request.user.password
        enterpassword = data['current_password']

        if not check_password(enterpassword, currentpassword):
            return JsonResponse({
                'message': 'Password wrong',
                'status': 406,
                })
        
        user = User.objects.get(username=user)
        user.delete()

        return JsonResponse({
            'direction': '/',
            'message': 'Password changed',
            'status': 200,
            })
