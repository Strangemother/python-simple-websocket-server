"""A Layer for google authenticator style login suite
"""
import onetimepass as otp
from rand import gen_16
import pyqrcode
import os

"""
import authenticator as au

# signup:
secret =  au.gen_16() # User record.



# Add to app:
label = "My Company"
url = au.gen_auth_string(label, secret)
qr = au.create_qr(secret, label, filename='qr-image')
# CLI present for scan
au.print_text(qr)

# Scan in auth app.



# Authenticate:
token = 230948 # from user
val = validate_time_auth(token, secret)
"""

def main():
    global url

    url = create_qr(filename='image')
    print_text(url)


def gen_time_token(secret=None):
    """Generate a time token for use with an external authenticator.
    """
    secret = secret or gen_16()
    return otp.get_totp(secret)


def gen_auth_string(name=None, secret=None):
    secret = secret or gen_16()
    name = 'authenticator' if name is None else name
    template = f"otpauth://totp/{name}?secret={secret}"
    return template


def validate_time_auth(token, secret):
    return  otp.valid_totp(token=token, secret=secret)


def create_qr(secret=None, name=None, filename=None):
    rstr = gen_auth_string(name, secret)
    url = pyqrcode.create(rstr)
    if filename:
        url.svg(f'{filename}.svg', scale=8)
    return url


def print_text(url):
    t = url.text(quiet_zone=1)
    os.system('color f0')
    for x in t:
        if x == '\n':
            print()
            continue
        s = ("██" if x == '1' else '  ')
        print(s, end='')
    input('press any key to continue')
    os.system('color 02')
    return url

if __name__ == '__main__':
    main()
