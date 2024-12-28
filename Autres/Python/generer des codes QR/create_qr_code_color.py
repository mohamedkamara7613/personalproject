#coding:utf-8

import qrcode
from qrcode.constants import ERROR_CORRECT_L
#Data must be a text valor not pictures

try:

	data = input("Enter text for coding in qrcode : ")

except:
	print("Incorrect input !!")

qr = 	qrcode.QRCode(
	version = 3, 
	error_correction = 	ERROR_CORRECT_L,
	box_size = 7,
	border = 5
	)


qr.add_data(data)
qr.make(fit = True)


img = qr.make_image(fill_color = "red", back_color = "white")
img.save("qrcode.png")