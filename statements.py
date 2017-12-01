# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    def __init__ (self):
        self.tupleList = []
    def add (self, stem, cat):
        self.tupleList.append((stem, cat))
    def getAll (self, cat):
        lst = []
        for t in self.tupleList:
            if (t[1] == cat):
                add (lst, t[0])
        return lst

class FactBase:
    def __init__ (self):
        self.unary = []
        self.binary = []
    def addUnary (self, pred, e1):
        self.unary.append((pred, e1))
    def addBinary (self, pred, e1, e2):
        self.binary.append((pred, e1, e2))
    def queryUnary (self, pred, e1):
        for u in self.unary:
            if (u == (pred, e1)):
                return True
                break
        return False
    def queryBinary (self, pred, e1, e2):
        if ((pred, e1, e2) in self.binary):
            return True
        else:
            return False


import re
from nltk.corpus import brown
def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    ok = 0

    if (re.match("\w*([^aeiousxyzh]|[^cs]h)s$", s)):
        stem = s[:-1]
    elif (re.match("(\w*)[aeiou]ys$", s)):
        stem = s[:-1]
    elif (re.match("\w+[^aeiou]ies$", s)):
        stem = s[:-3]+'y'
    elif (re.match("[^aeiou]ies$", s)):
        stem = s[:-1]
    elif (re.match("\w*([ox]|ch|sh|ss|zz)es$", s)):
        stem = s[:-2]
    elif (re.match("\w*(([^s]se)|([^z]ze))s$", s)):
        stem = s[:-1]
    elif (re.match("has", s)):
        stem = "have"
    elif (re.match("\w*([^iosxzh]|[^cs]h)es$", s)):
        stem = s[:-1]
    else:
        stem = ""

    if (stem != "" and ok != 1):
        for (word, tag) in brown.tagged_words():
            if word == stem and tag in ('VB', 'VBZ'):
                return stem
                ok = 1
                break

    if (ok == 0):
        return ""


def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg

# End of PART A.