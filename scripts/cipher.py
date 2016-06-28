#!/usr/bin/python

import sys

def caesar(plainText, shift): 
  cipherText = ""
  for ch in plainText:
    if ch == " ":
      finalLetter = " "
      cipherText += finalLetter
    elif ch.isalpha():
      stayInAlphabet = ord(ch) + shift 
      if stayInAlphabet > ord('z'):
        stayInAlphabet -= 26
      finalLetter = chr(stayInAlphabet)
      cipherText += finalLetter
  #print "Your ciphertext is: ", cipherText
  return cipherText

for x in range(1,27):
	print str(x) + "::" + caesar(sys.argv[1].lower(), x)
