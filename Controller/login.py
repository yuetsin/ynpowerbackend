from dao import *
def login(username, password):
    b = getUserByPsAndName(username, password)
    return b

