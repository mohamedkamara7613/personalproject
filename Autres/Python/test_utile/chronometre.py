#coding:utf-8

import time

def get_number() -> int :
	while True:
		try:
			number = int(input())
			return number
		except ValueError as e:
			print("Chiffre invalide")


def countdown():
	print("Ecrivez un nombre de secondes : ", end='')
	number = get_number()

	for i in range(number):
		print(f"{number - (i+1)} restants...")
		time.sleep(1)

	print('Tu as fini !!')


countdown()