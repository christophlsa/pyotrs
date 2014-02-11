from email.mime.text import MIMEText
from textwrap import wrap
from random import choice
from subprocess import call
from sys import stderr
from os import access, X_OK
from os.path import dirname, join
import smtplib
import string


def read_text_from_template():
    script_dir = dirname(__file__)
    with open(join(script_dir, 'email.txt'), encoding="utf-8") as f:
        return f.read()


def format_text(oldtext):
    newtext = ''
    for s in oldtext.splitlines(True):
        newtext += "\n".join(wrap(s, 72, expand_tabs=False, drop_whitespace=False, replace_whitespace=False))
    return newtext


def send_mail(email, username, password):
    text = read_text_from_template()
    text = text.format(username, password)
    text = format_text(text)

    msg = MIMEText(text, 'plain', 'utf-8')

    msg["From"] = "noreply@piraten-lsa.de"
    msg["Reply-To"] = "it@piraten-lsa.de"
    msg["To"] = email
    msg["Subject"] = "ein test"

    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()


def create_user(firstname, lastname, username, password, email, groups):
    command = '/opt/otrs/bin/otrs.AddUser.pl'

    if not access(command, X_OK):
        print('you have no permission to create the user', file=stderr)
        return 1

    cmdargs = [command, '-f', firstname, '-l', lastname, '-p', password, '-e', email]

    if len(groups) != 0:
        for group in groups:
            cmdargs.append('-g')
            cmdargs.append(group)

    cmdargs.append(username)

    return call(cmdargs)


def id_generator(size=16, chars=string.ascii_letters + string.digits):
    return ''.join(choice(chars) for _ in range(size))