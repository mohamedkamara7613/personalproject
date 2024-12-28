#coding:utf-8
age = 45

def ver():
	global age
	age = 22

def vor():
	global age
	age = 33

print(age)
ver()
print(age)
vor()
print(age)