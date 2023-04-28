import re
from datetime import datetime


def check_user_input(label):
    string = input(label)
    if not bool(re.match('^[0-9a-zA-Z ]*$', string)) or string == '':
        print("la chaîne de caractères contient des chiffres ou des caratères spéciaux")
        return check_user_input(label)
    return string


def check_date_input(label):
    date = input(label)
    try:
        date = datetime.strptime(date, "%d/%m/%Y")
        return date
    except ValueError:
        print("la date n'est pas de la forme jj/mm/aaaa")
        return check_date_input(label)


def check_number_input(label):
    number = input(label)
    if not bool(re.match('^[0-9]*$', number)) or number == '':
        print("veuillez entrer un nombre")
        return check_number_input(label)
    return int(number)


def check_yes_no_input(label):
    letter = input(label)
    if letter == 'o' or letter == 'n':
        return letter
    print("soit 'O' soit 'N'")
    return check_yes_no_input(label)


def check_time_control(label):
    time_control = input(label)
    time_control_list = ["bullet", "blitz", "coup rapide"]
    if time_control not in time_control_list:
        print("Mauvais choix du contrôle du temps (un bullet, un blitz ou un coup rapide)")
        return check_time_control(label)
    else:
        return time_control
