from Crypto.Cipher import AES
from getpass import getpass

import zlib, json

class Locker():
	def encrypt(namehash):
		plaintext = input("\nEnter the key to be encrypted: ").encode()

		passed = False
		print("\n[INFO] If password is lost, there is no way to recover.\n")
		while not passed:
			passinit = getpass("Enter password: ")
			passnd = getpass("Enter password again: ")
			if str(passinit) != str(passnd):
				print("\nPasswords don't match.\n")
			elif len(passnd) < 8 or len(passnd) > 16:
				print("[ERROR] Password must be between 8 and 16 bytes long.")
			else:
				passed = True

		passwd = passnd.ljust(16,'#').encode()

		cipher = AES.new(passwd, AES.MODE_EAX)

		nonce = cipher.nonce
		ciphertext, tag = cipher.encrypt_and_digest(plaintext) 
		
		data_list = [ciphertext.decode('ISO-8859-1'), tag.decode('ISO-8859-1'), nonce.decode('ISO-8859-1')]
		
		with open("data/data.json","r") as data_file:
			data = json.load(data_file)

		data[namehash] = data_list

		with open("data/data.json","w") as data_file:
			json.dump(data, data_file, indent = 4)

		print("\n Your data is encrypted and saved. \n")
		exit()

	def decrypt(namehash):
		with open("data/data.json","r") as data_file:
			data = json.load(data_file)

		try:
			data[str(namehash)]
		except KeyError:		
			print("\nUsername not found.\n Exiting...\n")
			exit()
		
		data_list = data[str(namehash)]
		ciphertext = data_list[0].encode('ISO-8859-1')
		tag = data_list[1].encode('ISO-8859-1')
		nonce = data_list[2].encode('ISO-8859-1')

		passnd = getpass("Enter password: ")
		passwd = passnd.ljust(16,'#').encode()

		cipher = AES.new(passwd, AES.MODE_EAX, nonce = nonce)
		plaintext = cipher.decrypt(ciphertext)
		try:
			cipher.verify(tag)
			print(f"\nDecrypted Key:\t{plaintext.decode()}\n")
		except ValueError:
			print("\nIncorrect Password or Data is corrupted")

if __name__ == '__main__':
	choice = int(input("[1] - Encrypt\n[2] - Decrypt\n[0] - Exit\n: "))

	if choice == 1:
		print("\n[INFO] If username is lost, there is no way to recover.\n")	
	name = input("Enter a username: ")
	namehash = zlib.crc32(name.encode())

	if choice == 1:
		Locker.encrypt(namehash)
	elif choice == 2:
		Locker.decrypt(namehash)
	else:
		print("Good Bye")
		exit()