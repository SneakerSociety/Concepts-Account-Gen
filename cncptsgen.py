# Concepts Account Generator
# Made by @ASnkrSociety or Sneaker Society#6999
# Built in proxy and captcha support
# Requirements: requests, random, names, proxymanager, anticaptcha client, bs4
# Uses anticaptcha, create an account and load $10
# Create a proxies.txt in a folder with script

import requests
import random
import names
import threading

from proxymanager import ProxyManager
from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask
from bs4 import BeautifulSoup

url = 'https://cncpts.com/account'

headers = {
'Content-Type': 'application/x-www-form-urlencoded',
'Referer': 'https://cncpts.com/account/login',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

def generator():
    global session
    s = requests.Session()

    first = names.get_first_name(gender= 'male') # random first name
    last = names.get_last_name() # random last name
    catchall = '@gmail.com' # input your catchall
    password = 'Wow12397ads' # input a password
    random_number = random.randint(1,10000)
    email = last+f'{random_number}'+catchall

    proxym = ProxyManager('proxies.txt') # create a proxies.txt file and paste in proxies
    proxyr = proxym.random_proxy()
    proxyf = proxyr.get_dict()

    info = {
    'form_type': 'create_customer',
    'utf8': '✓',
    'customer[first_name]': first,
    'customer[last_name]': last,
    'customer[email]': email,
    'customer[password]': password
    }

    submit_info = s.post(url, data=info, headers=headers, proxies=proxyf) # submits first request

    if submit_info.url == 'https://cncpts.com/': # if account was submitted then this will be the site after the request
        print('Successfully signed up!')
        print(f'{email}:{password}')

    else:
        print('Captcha needed, submitting now...') # otherwise you need a captcha
        url_cap = s.get('https://cncpts.com/challenge')
        soup = BeautifulSoup(url_cap.content, 'html.parser')
        auth_val = soup.findAll("input", {"name": "authenticity_token"}) # grabs hidden authenticity token from source
        auth_final = auth_val[0]["value"]

        api_key = 'faec17e0ddf795ab53a39e709e75290f' # api key from anticaptcha
        site_key = '6LeoeSkTAAAAAA9rkZs5oS82l69OEYjKRZAiKdaF' # site key from concepts
        cap_url = submit_info.url

        client = AnticaptchaClient(api_key)
        task = NoCaptchaTaskProxylessTask(cap_url, site_key)
        job = client.createTask(task)
        job.join()
        response = job.get_solution_response() # grabs token from anticaptcha

        cap_info = {
        'utf8': '✓',
        'authenticity_token': auth_final,
        'g-recaptcha-response': response
        }

        cap_headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://cncpts.com/challenge',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }

        submit_captcha = s.post(url, data=cap_info, headers=cap_headers, proxies=proxyf) # submits second request with captcha

        if submit_captcha.url == 'https://cncpts.com/': # if account was submitted then this will be the site after the request
            print('Captcha successfully submitted!')
            print(f'{email}:{password}')

        else:
            print('Account signup unsuccessful, please try again.') # otherwise there was a problem with the captcha

threads = []
x = int(input('How many accounts?'))
for i in range(x):
    t = threading.Thread(target=generator)
    threads.append(t)
    t.start()
