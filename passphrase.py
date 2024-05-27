import random

import xkcdpass.xkcd_password as xp

# https://github.com/redacted/XKCD-password-generator
# https://github.com/redacted/XKCD-password-generator/blob/master/examples/example_import.py
# https://pypi.org/project/xkcdpass/
# pip install `pip install xkcdpass'

class Passphrase:
    def random_capitalisation(self, s, chance):
        new_str = []
        for i, c in enumerate(s):
            new_str.append(c.upper() if random.random() < chance else c)
        return "".join(new_str)

    def capitalize_first_letter(s):
        new_str = []
        s = s.split(" ")
        for i, c in enumerate(s):
            new_str.append(c.capitalize())
        return "".join(new_str)

    # Generate passphrase
    def generate_passphrase(self):
        words = xp.locate_wordfile()
        mywords = xp.generate_wordlist(wordfile=words, min_length=5, max_length=8)
        raw_password = xp.generate_xkcdpassword(mywords, numwords=15, delimiter='@')

        # for i in range(5):
        #     print(random_capitalisation(raw_password, i/10.0))

        # print(capitalize_first_letter(raw_password))

        passphrase = self.random_capitalisation(raw_password, 0/10.0)
        passphrase = passphrase.replace("@", " " ) 
        #self.label_passphrase.setText( str(passphrase)  ) 
        #print(passphrase)

        return passphrase

    if __name__ == "__main__":
        generate_passphrase()