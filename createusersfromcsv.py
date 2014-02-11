from sys import stderr, exit
from os.path import isfile
from csv import DictReader
import argparse

from pyotrs import id_generator, create_user, send_mail


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Creates OTRS agents from csv')
    parser.add_argument('csvfile')
    args = parser.parse_args()

    if not isfile(args.csvfile):
        print("file {} not found or not a file".format(args.csvfile), file=stderr)
        exit(1)

    with open(args.csvfile, newline='') as csvfile:
        csvreader = DictReader(csvfile, delimiter=";")

        for name in ['firstname', 'lastname', 'username', 'email', 'groups']:
            if name not in csvreader.fieldnames:
                print("fieldname {} not set".format(name), file=stderr)
                exit(1)

        for row in csvreader:
            generated_password = id_generator()

            if create_user(row['firstname'], row['lastname'], row['username'], generated_password, row['email'],
                           row['groups'].split(',')) != 0:
                print('creating user {} failed'.format(row['username']), file=stderr)
                continue

            print('user {} created'.format(row['username']))

            send_mail(row['email'], row['username'], generated_password)

            print('email to user {} send'.format(row['username']))