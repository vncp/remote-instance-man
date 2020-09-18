#!/usr/bin/env python3
import random
import string



def get_random_alphaNumeric_string(stringLength=8):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))

# sudo -u newellz2 bash -c "echo testing543 | vncpasswd -f > /home/newellz2/.vnc/passwd"

if __name__ == "__main__":
    print(get_random_alphaNumeric_string())
