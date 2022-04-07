
import subprocess
import requests
from bs4 import BeautifulSoup as bs
import argparse
from urllib.parse import quote


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('-a', '--automatic', help="automatic mode. automatically searches for 'Uniball Signo'", action='store_true')
    ap.add_argument('-n', '--noemail', help="Print status but do not send the email with the content", action='store_true')
    return ap.parse_args()


def main():
    args = parse_args()
    if args.automatic:
        r = requests.get('https://www.jetpens.com/search?q=uniball+signo&v=2&ip=48')
    else:
        query = input('Enter search query: ')
        r = requests.get('https://www.jetpens.com/search?q=' + quote(query) + '&v=2&ip=48')

    soup = bs(r.text, features="html.parser")

    content = ''
    for i in soup.select('div[class*="last-chance"]'):
        content += ('Found a last chance: {}\n'.format(i.parent.select('a[class*="product-name"]')[0].text))
    content += ('\n')

    if args.noemail:
        print('*** NO EMAIL MODE ***')
        print(content)
    else:
        with open('./lastchance.txt', 'w') as f:
            f.write(content)
        subprocess.call(['node', './mailer.js'])


if __name__ == '__main__':
    main()
