import re


def check(message):
    return re.search(r"WHO-OK ([\w\.-]+) ([\w\.-]+)", message)


while True:
    mess = input("> ")
    flag = check(mess)
    if flag:
        print("Sender: ", flag.group(1))
        print("Recipient: ", flag.group(2))
    else:
        print("NONONOP")
