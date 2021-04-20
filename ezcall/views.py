from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
#from django.shortcuts import render_to_response
#from django import forms
#from django.shortcuts import redirect
from .models import Phone
from django.contrib import messages
import requests
import hashlib
import xlrd
import os
#import time
#import zerorpc
from ezcall import logger
from bs4 import BeautifulSoup
#from requests.exceptions import ConnectionError

logger = logger.logger
logger.warning('app reloaded')

tel_book_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'example.xlsx')
excel_data_file = xlrd.open_workbook(tel_book_path)
sheet = excel_data_file.sheet_by_index(0)

name_arr = []
number_arr = []
mobile_arr = []

name_arr_raion = []
number_arr_raion = []
mobile_arr_raion = []

name_arr_urm = []
number_arr_urm = []
mobile_arr_urm = []
fio_arr_urm = []

pc_ip = []
tel_ip = []

row_num = sheet.nrows

#считываем данные из excel файла
if row_num > 0:
        #DIR
    for row in range(0,row_num):
        if str(sheet.row(row)[2]).replace("text:", "").replace("'", "") == "empty:":
            continue
        name_arr.append(str(sheet.row(row)[2]).replace("text:", "").replace("'", ""))
        number_arr.append(str(sheet.row(row)[3]).replace("number:", "").replace(".0", ""))
        mobile_arr.append(str(sheet.row(row)[4]).replace("number:", "").replace(".0", ""))
        #RAION
    for row in range(0,row_num):
        if str(sheet.row(row)[15]).replace("text:", "").replace("'", "") == "empty:":
            continue
        name_arr_raion.append(str(sheet.row(row)[15]).replace("text:", "").replace("'", ""))
        number_arr_raion.append(str(sheet.row(row)[16]).replace("number:", "").replace(".0", ""))
        #mobile_arr_raion.append(str(sheet.row(row)[17]).replace("number:", "").replace(".0", ""))
        #URM
    for row in range(0,row_num):
        name_arr_urm.append(str(sheet.row(row)[8]).replace("text:", "").replace("'", ""))
        number_arr_urm.append(str(sheet.row(row)[10]).replace("number:", "").replace(".0", ""))
        mobile_arr_urm.append(str(sheet.row(row)[9]).replace("number:", "").replace(".0", ""))
        fio_arr_urm.append(str(sheet.row(row)[13]).replace("text:", "").replace("'", ""))
        #IP DIR
    for row in range(0,row_num):
        pc_ip.append(str(sheet.row(row)[5]).replace("text:", "").replace("'", ""))
        #pc_ip.append(str(sheet.row(row)[19]).replace("text:", "").replace("'", ""))
        pc_ip.append(str(sheet.row(row)[11]).replace("text:", "").replace("'", ""))
        tel_ip.append(str(sheet.row(row)[6]).replace("text:", "").replace("'", ""))
        #tel_ip.append(str(sheet.row(row)[18]).replace("text:", "").replace("'", ""))
        tel_ip.append(str(sheet.row(row)[12]).replace("text:", "").replace("'", ""))
else:
    print("Пустой файл")

iptable = dict(zip(pc_ip, tel_ip))
phone_book = zip(number_arr, name_arr, mobile_arr)
phone_book_raion = zip(number_arr_raion, name_arr_raion, mobile_arr_raion)
phone_book_urm = zip(mobile_arr_urm, number_arr_urm, name_arr_urm, fio_arr_urm)

def main(req):

    comp_ip = req.META.get('REMOTE_ADDR')

    favorites = Phone.objects.filter(userip=comp_ip)

    phone_book = zip(number_arr, name_arr, mobile_arr)
    phone_book_raion = zip(number_arr_raion, name_arr_raion, mobile_arr_raion)
    phone_book_urm = zip(mobile_arr_urm, number_arr_urm, name_arr_urm, fio_arr_urm)

    context = {
        'phone_book': phone_book,
        'phone_book_raion': phone_book_raion,
        'phone_book_urm': phone_book_urm,
        "favorites": favorites
        }

    if comp_ip in iptable:
        """ ip = iptable[comp_ip]
        number = req.GET.get("callee", "")
        if number != "":
            make_call(ip, number, comp_ip) """
        return render(req, 'ezcall/makecall4.html', context)
    else:
        #return render(req, 'ezcall/error.html')
        return render(req, 'ezcall/makecall4.html', context)

def index(request):
    return main(request)

def create(request):
    comp_ip = request.META.get('REMOTE_ADDR')
    if request.method == "POST":
        response_data = {}
        contact = Phone()
        contact.userip = comp_ip
        contact.name = request.POST.get("name")
        if request.POST.get("number") == '':
            contact.number = None
        else:
            contact.number = request.POST.get("number")
        if request.POST.get("mobile") == '':
            contact.mobile = None
        else:
            contact.mobile = request.POST.get("mobile")
        contact.save()

        response_data['id'] = contact.id
        response_data['name'] = contact.name
        response_data['number'] = contact.number
        response_data['mobile'] = contact.mobile

        logger.warning('%a добавил новый контакт', comp_ip)
    return JsonResponse({
        'id': contact.id, 
        'name': contact.name,
        'number': contact.number,
        'mobile': contact.mobile
        },status=200)
    #return HttpResponseRedirect("/ezcall")

def delete(request):
    comp_ip = request.META.get('REMOTE_ADDR')
    id = request.GET['id']
    contact = Phone.objects.get(id=id)
    contact.delete()
    logger.warning('%a удалил контакт', comp_ip)
    return HttpResponse()
    #return HttpResponseRedirect("/ezcall")

def make_call(request,caller,callee,comp_ip):  
    session = requests.Session()
    url = "http://"+caller
    LOGIN = "admin"
    PASSWORD = "gtctw"

    call_message = caller+' is trying to call '+callee
    print(call_message)

    try:
        p = session.get(url, timeout=5)
    except:
        message = 'Телефон недоступен'
        #messages.error(request, 'Телефон недоступен')
        print('Телефон недоступен', caller)
        logger.warning('%a не удалось подключиться к телефону', comp_ip)
        return JsonResponse({
            'message': message
            },status=200)
    
    if p is None:
        print('оп-па сессия неактивна')
        return False
    else:
        print('соединение установлено')
        soup = BeautifulSoup(p.content, "html.parser")        
        if soup is None:
            print('не удалось спарсить страницу')
            return False
        else:
            if soup.find("input", {'id': 'logonButton'}) is not None:
                a = session.cookies.get_dict()['auth']
                post_data = dict(encoded=str(LOGIN) + ":" + hashlib.md5((str(LOGIN) + ":" + str(PASSWORD) + ":" + a).encode('utf-8')).hexdigest(), ReturnPage="/")
                #print(post_data)
                #print(a)
                ## авторизуемся на телефоне
                session.post(url, post_data)
                # print(soup.find("input", {'id': 'username'}).get('value'))
                url_call = "http://" + caller + "/network.htm"

                post_data2=dict(ReturnPage="/",PHB_AutoDialLine=1,AutoDialSubmit="submit",PHB_AutoDialNumber=callee)
                #print(post_data2)
                session.post(url, post_data2)
                #записываем в лог
                call_info = caller+" calling "+callee
                logger.warning('%a', call_info)

                post_data2=dict(DefaultLogout="Logout")
                r = session.post(url, post_data2)

            else:                
                a = soup.find("input", {'name': 'nonce'}).get('value')
                post_data = dict(encoded=str(LOGIN) + ":" + hashlib.md5((str(LOGIN) + ":" + str(PASSWORD) + ":" + a).encode('utf-8')).hexdigest(), LOG_Language=12,nonce=str(a),URL="/",goto="Logon")
                ## авторизуемся на телефоне
                session.post(url, post_data)
                url_function = "http://" + caller + "/webdial.htm"

                post_data2=dict(ReturnPage="/webdial.htm",WEB_LineTab_R=1,AutoDialSubmit="Dial",WEB_DialNumber=callee)

                session.post(url_function, data=post_data2)
                #записываем в лог
                """ if callee != '': """
                call_info = caller+" calling "+callee
                logger.warning('%a', call_info)
                url_function = "http://" + caller + "/LogOut.htm"
                post_data2=dict(ReturnPage="/LogOut.htm",DefaultLogout="Logout")
                r = session.post(url_function, data=post_data2)
        
        return False
    
def calling(req):
    comp_ip = req.META.get('REMOTE_ADDR')
        
    if comp_ip in iptable:
        ip = iptable[comp_ip]
        number = req.GET['callee']
        if number != "":
            response = make_call(req, ip, number, comp_ip)
    
    return HttpResponse(response)