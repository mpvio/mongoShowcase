def getUsername():
    with open("username.txt", "r") as file:
        for line in file:
            return line

def getPassword():
    with open("password.txt", "r") as file:
        for line in file:
            return line