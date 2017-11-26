# -*- cofing utf-8 -*-
import hashlib
from os import path

def user_login():
	c = True
	user_name = input("Username: ")
	user_pass = input("Password: ")
	user = user_name+user_pass
	while(c):
		user_hash = "user_list/"+hashlib.sha256(user.encode('utf-8')).hexdigest()
		if path.exists(user_hash):
			c = False
		else:
			print("This user is not beign.Please type agein.")
			user_name = input("Username: ")
			user_pass = input("Password: ")
			user = user_name+user_pass
	return user

def user_create():
	c = True
	user_name = input("Username: ")
	user_pass = input("Password: ")
	user = user_name+user_pass
	while(c):
		user_hash = "user_list/"+hashlib.sha256(user.encode('utf-8')).hexdigest()
		if not path.exists(user_hash):
			user_file = open(user_hash,'w')
			user_file.close()
			c = False
		else:
			print("This user is being.Please type agein.")
			user_name = input("Username: ")
			user_pass = input("Password: ")
			user = user_name+user_pass
	return user
