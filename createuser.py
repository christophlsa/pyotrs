from sys import stderr, exit
import argparse

from pyotrs import id_generator, create_user, send_mail


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Creates OTRS agent')
    parser.add_argument('firstname')
    parser.add_argument('lastname')
    parser.add_argument('username')
    parser.add_argument('email')
    parser.add_argument('group', nargs='*')
    args = parser.parse_args()

    generated_password = id_generator()

    if create_user(args.firstname, args.lastname, args.username, generated_password, args.email, args.group) != 0:
        print('creating user failed', file=stderr)
        exit(1)

    print('user created')

    send_mail(args.email, args.username, generated_password)

    print('email send')