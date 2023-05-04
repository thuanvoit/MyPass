import clearbit
import pyperclip as pc
import urllib.parse
import random, string
from cryptography.fernet import Fernet


clearbit.key = "sk_4bc7685e9fffe1869718ab9953b47611"

def find_company_by_domain(url):
    company_info = {}
    try:
        company = clearbit.Company.find(domain=url)
        if company['name'] != None:
            company_info = {
            'name': company['name'],
            'domain': company['domain'],
            'logo': company['logo'],
            }
        else:
            company_info = {
            'name': url,
            'domain': url,
            'logo': "https://icons-for-free.com/iconfiles/png/512/high+quality+social+social+media+square+website+www+icon-1320192619856305568.png",
        }
    except: 
        company_info = {
            'name': url,
            'domain': url,
            'logo': "https://icons-for-free.com/iconfiles/png/512/high+quality+social+social+media+square+website+www+icon-1320192619856305568.png",
        }
    return company_info

def copy(content):
    pc.copy(content)

def encodeURL(address, city, state, zipcode):
    full_address = f"{address}, {city}, {state}, {zipcode}"
    encoded_address = urllib.parse.quote(full_address, safe="")
    return f"https://maps.google.com/maps?q={encoded_address}&t=&z=15&ie=UTF8&iwloc=&output=embed"
    
def name_to_company_logo(name):
    company = clearbit.NameToDomain.find(name=name)
    if company != None:
        return company['logo']
    else: 
        return "https://cdn.iconscout.com/icon/free/png-256/data-not-found-1965034-1662569.png"

def generate_url():
    size = random.randrange(5,10)
    chars = string.ascii_uppercase + string.digits
    url_part = ''
    for _ in range(size):
        url_part += random.choice(chars)
    return url_part
    
def check_card_al(card_number):
    size = len(card_number)
    if size != 16:
        return False
    sum = 0
    for i in range(size-1, -1, -1):
        if i%2==0:
            num = int(card_number[i])*2
            while (num>9):
                num=str(num)
                num = int(num[0]) + int(num[1])
            temp = list(card_number)
            temp[i] = str(num)
            card_number = ''.join(temp)
        sum += int(card_number[i])
    if sum%10==0:
        return True
    else: return False


 
def encrypt(content):
    key = Fernet.generate_key()
    fernet = Fernet(key)

    if isinstance(content, str):
        encrypt_content = ""
        encContent = fernet.encrypt(content.encode())
        encrypt_content = encContent

    elif isinstance(content, dict):
        encrypt_content = {}
        for i in range(len(content)):
            encContent = fernet.encrypt(content[i].encode())
            encrypt_content[i] = encContent

    return { 'key': key, 'encrypt_content': encrypt_content, }
    
def decrypt(encContent, key):
    fernet = Fernet(key)
    
    if isinstance(encContent, bytes):
        decContent = ""
        decContent = fernet.decrypt(encContent).decode()
   
    elif isinstance(encContent, dict):
        decContent = {}
        for i in range(len(encContent)):
            decContent[i] = fernet.decrypt(encContent[i]).decode()
            
    return decContent