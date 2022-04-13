import subprocess
import requests
from bs4 import BeautifulSoup as bs
import argparse
from urllib.parse import quote
import os

verbose = False


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('-a', '--automatic', help="automatic mode. automatically searches for 'Uniball Signo'", action='store_true')
    ap.add_argument('-n', '--noemail', help="Print status but do not send the email with the content", action='store_true')
    ap.add_argument('-q', '--query', help="Search query. If not specified, the user will be prompted for it")
    ap.add_argument('-v', '--verbose', help="Print status to stdout", action='store_true')
    return ap.parse_args()


def say(message):
    if verbose:
        print(message)


def main():
    global verbose
    args = parse_args()
    verbose = args.verbose

    say("*** GATHERING DATA ***")
    say("Beginning Jetpens Request")
    if args.automatic:
        say("Automatic mode")
        r = requests.get('https://www.jetpens.com/search?q=uniball+signo&v=2&ip=48')
    else:
        if args.query:
            say("Searching for: " + args.query)
            query = args.query
        else:
            query = input("Search query: ")
        r = requests.get('https://www.jetpens.com/search?q=' + quote(query) + '&v=2&ip=48')

    say("Parsing...")
    soup = bs(r.text, features="html.parser")

    content = ''
    say("Searching...")
    for i in soup.select('div[class*="last-chance"]'):
        content += ('Found a last chance: {}\n'.format(i.parent.select('a[class*="product-name"]')[0].text))
    content += ('\n')
    say("Search done!")

    if args.noemail:
        say('\n*** NO EMAIL MODE ***')
        print(content)
    else:
        say("\n*** PREPARING EMAIL ***")
        with open('./lastchance.txt', 'w') as f:
            f.write(content)
        say("Starting Javascript Mailer")
        if verbose:
            os.putenv('VERBOSE', '1')
        subprocess.call(['node', './mailer.js'])


if __name__ == '__main__':
    main()
