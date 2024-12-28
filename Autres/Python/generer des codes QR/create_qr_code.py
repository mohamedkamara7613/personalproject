#coding:utf-8

import qrcode

#Data must be a text valor not pictures
try:

	data = input("Enter text for coding in qrcode : ")
	file_output = input("Enter name of output file : ")
	
	img = qrcode.make(data)

	img.save(file_output+".png")

except:
	print("Incorrect input !!")

