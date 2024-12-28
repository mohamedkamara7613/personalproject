#coding:utf-8
import cv2

detector = cv2.QRCodeDetector()


try :
	image = input("Entrez le chemin du qrcode à décoder : ")
	val, points, qrcode = detector.detectAndDecode(cv2.imread(image))
except:
	print("Entrée incorrect")

print(val)

