import pickle
import random

def get_credentials():
    username = input('Please type your user name: ')
    password = input('Please type your password: ')
    return username, password

def authenticate(username, password, pwdb):
    status = False
    if username in pwdb:
        if pwdb[username] == password:
            status = True
            salt = get_salt()
            print(pwhash(password,salt))
    else:
        ans = input('User not known. Add it to db? [y/n]')
        if ans == 'y':
            add_user(username, password, pwdb)
            status = True
    return status

def add_user(username, password, pwdb):
    if username not in pwdb:
        pwdb[username] = password
        write_pwdb(pwdb)
    else:
        print('User already known!')

def read_pwdb():
    pwdb_path = get_path()
    try:
        with open(pwdb_path, 'rb') as pwdb_file:
            pwdb = pickle.load(pwdb_file)
    except FileNotFoundError:
        pwdb = {}
    return pwdb

def write_pwdb(pwdb):
    pwdb_path = get_path()
    with open(pwdb_path, 'wb') as pwdb_file:
        pickle.dump(pwdb, pwdb_file)

def get_path():
    return '/tmp/pwdb.pkl'

def pwhash(password,salt):
    passSalt = password + str(salt)
    print(passSalt)
    hash = 0
    for i,char in enumerate(passSalt):
        hash += (i+1) * ord(char)
    return(hash)

def get_salt():
    population = range(10)
    salt = 0
    digits = random.choices(population,k=16)
    for i,digit in enumerate(digits):
        salt += 10**i*digit
    return(salt)

pwdb = read_pwdb()
username, password = get_credentials()
if authenticate(username, password, pwdb):
    print(pwdb)
else:
    print('No match!')
