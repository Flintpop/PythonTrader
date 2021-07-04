from cryptography.fernet import Fernet
import os

class Encrypt:
    def __init__(self):
        self.write_key()

        self.one = "".encode()
        self.two = "".encode()

        self.key = self.load_key()

        # initialize the Fernet class
        self.f = Fernet(self.key)
        self.encrypted = self.f.encrypt(self.one)
        self.encrypted_two = self.f.encrypt(self.two)

        self.write_data()

    def get_data_one(self):
        return str(self.f.decrypt(self.encrypted)).replace("b", " ").strip()

    @staticmethod
    def write_key():
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)

    @staticmethod
    def load_key():
        return open("key.key", "rb").read()

    def write_data(self):
        with open("../Output/some_data.txt", "wb") as file:
            file.write(self.f.encrypt(self.one))
            file.write("\n".encode())
            file.write(self.f.encrypt(self.two))
            file.write("\n".encode())


class GetData:
    @staticmethod
    def load_key():
        return open("key.key", "rb").read()

    @staticmethod
    def get_data(key):
        f = open("src/Output/some_data.txt", "r")
        k = Fernet(key)
        infos = []
        decrypted = []
        for x in f:
            infos.append(x)
        for items in infos:
            temp = k.decrypt(bytes(items.encode())).decode()
            decrypted.append(temp)
        f.close()
        return decrypted

    @staticmethod
    def login():
        keys = GetData()
        password = GetData.get_password()
        key = keys.get_data(password)
        return key

    @staticmethod
    def get_password():
        import platform
        print(os.getcwd())
        current_os = platform.system()
        if current_os == 'Windows':
            password = input("Please enter password : ")
        elif current_os == 'Linux' or current_os == 'Darwin':
            from getpass import getpass
            password = getpass()
        else:
            password = 0
            print("Critical error, could not determine the os.")
        return password