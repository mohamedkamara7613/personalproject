#!/usr/bin/python3
# coding:utf-8

import os
#import nmap
#scanner = nmap.PortScanner()

print("\n\n**************************************************************************************************\n")

print("CODE ASCII")


# /////////////////////////////////////////////////////////////////////////////////////////////////////
def main():
    while True:
        
        print("\n**************************************************************************************************\n")

        enter = input("1- Network Scanner\n2- Vulnerabilities Detector\n3- Exploit\n4- Exit\n\nPlease Enter a number : ")

        if enter == "1":
            os.system("clear")
            # nmap()
            print("Network Scanner is unavailable now !!")

        elif enter == "2":
            os.system("clear")
            vuln()

        elif enter == "3":
            os.system("clear")
            os.system("./start_msfconsole.sh")

            enter = 0

        elif enter == "4":
            break;

        else:
            print("Please choose a number between 1 and 3.")


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
"""
def nmap():
    print("**************************************************************************************************")
    print("************************* Welcome to the Network Scanner *****************************************")
    print("**************************************************************************************************\n")

    target_ip = input("Please enter the IP address : ")
    scanner.nmap(target_ip, "1-1024")
    print(scanner.scaninfo())
    print(scanner[target_ip]["tcp"].keys())
"""

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def vuln():
    print("**************************************************************************************************")
    print("************************* Welcome to the Vulnerabilities Detector ********************************")
    print("**************************************************************************************************\n")
    target_ip = input("Please enter the IP address : ")

    print(os.system("nmap -sV --script vuln " + target_ip))


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
if __name__ == "__main__":
    main()
