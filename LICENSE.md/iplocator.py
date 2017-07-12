#!/usr/bin/python
#-*-Coding:UTF-8 -*-

import geocoder 
import socket


print "\n*******************************************************************"
print "* iplocator Ver. 0.1                                                *"
print "* Write by TheRipper                                                *"
print "* john.theripper225@gmail.com                                       *"
print "*******************************************************************\n\n"

print "* Before dto launch this script, install geocoder module on python: *"
print "* pip install geocoder                                              *"


print("Do you want to locate an website or ip address? y or n:\n")
print("1. for website")
print("2. for ip addres")
print("3. for place,(place city, country) for example (PALAIS PRESIDENTIEL ABIDJAN, CI):\n")

ch = raw_input("Please, choose one option:")

def websitelocate():

            try:
                       host = raw_input("Enter your website:")
                       num = socket.gethostbyname(host)
                       localisation = geocoder.maxmind(num)
                       i = localisation.json
                       for key,value in i.items():
                                      print key,":",value
            except socket.gaierror:

                       print("\nwebsite format unknow!, please try again...")

def iplocate():
           host = raw_input('Enter your ip address:')
           localisation = geocoder.ipinfo(host)
           i = localisation.json
           for key,value in i.items():
                        print key,":",value
def placelocate():
           host = raw_input('Enter your place:')
           localisation = geocoder.osm(host)
           i = localisation.json
           for key,value in i.items():
                        print key,":",value

if ch == "1":
         websitelocate()
elif ch == "2":
         iplocate()
elif ch == "3":
         placelocate()
else:
         print("Bad keys, BYE!")