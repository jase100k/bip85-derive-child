#!/usr/bin/env python
#
# Copyright (c) 2020 Ethan Kosakovsky <ethankosakovsky@protonmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


from bip85 import BIP85
from mnemonic import Mnemonic 
from bip85 import app
from pycoin.symbols.btc import network as BTC
import getpass

def _bip32_master_seed_to_xprv(bip32_master_seed: bytes):
    if len(bip32_master_seed) < 16 or len(bip32_master_seed) > 64:
        raise ValueError('BIP32 master seed must be between 128 and 512 bits')
    xprv = BTC.keys.bip32_seed(bip32_master_seed).hwif(as_private=True)
    return xprv

# english wordlist 
language = 'english'
bip39 = Mnemonic(language)
bip85 = BIP85()


# How many words for the BIP85 mnemomic
num_words = 12
index = 0

print("Please input your master seed words. ")
seed_words = input()
if bip39.check(seed_words) == False:
    print("Seed words check: FAIL")
    print("Exiting: -1.")
    exit(-1)

print("Seed words check: OK")

passphrase = getpass.getpass(prompt="Please input passphrase: ")
passphrase2 = getpass.getpass(prompt="Passphrase again: ")

if passphrase != passphrase2:
    print("Error: passphrase don't match")
    print("Exiting: -3")
    exit(-3)

num_words = int(input("Enter choose the amount of words, 12, 18 or 24: "))

if num_words in (12,18,24):
    num_words = num_words
else:
    print("Error: amount of words should be 12, 18 or 24.")
    print("Exiting: -4")
    exit(-4)

index = int(input("Please input the BIP85 index: "))

xprv = _bip32_master_seed_to_xprv(bip39.to_seed(seed_words, passphrase))

print("Child seed words from index: " + str(index))
print(app.bip39(xprv, language, num_words, index))






