# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 23:07:28 2025

@author: casey
"""

import numpy

class domino( object ):
    def __init__(self, side_a=0, side_b=0, trump=0):
        self.side_a = side_a
        self.side_b = side_b
        self.trump = trump
        
    def set_trump(self, trump):
        self.trump = trump
    
    def is_trump(self):
        retval = False
        if self.side_a == self.trump:
            retval = True
        if self.side_b == self.trump:
            retval = True
            
        return retval
    
    def is_member(self, suit=0):
        retval = -1
        if self.is_trump():
            if suit == self.trump:
                pass
            else:
                return retval
        if self.side_a == suit:
            retval = self.side_b
            if self.side_a == self.side_b:  # double
                retval = 7
        elif self.side_b == suit:
            retval = self.side_a
        return retval
    
    def gt(self, other, lead):
        if other.is_trump():
            if self.is_trump():
                return self.is_member(self.trump) > other.is_member(self.trump)
            else:
                return False
        else:
            if self.is_trump():
                return True
            else:
                return self.is_member(lead) > other.is_member(lead)
        return True
    
    def __str__(self):
        return "%d:%d"  % (self.side_a, self.side_b)

def play_trick(h, l, t):
    numpy.random.shuffle(h[l])
    d = h[l].pop()
    print(d)
    

def play_hand(hands, t):
    lead = 0
    while(len(hands[lead]) > 0):
        points = play_trick(hands, lead, trump)

dominoes = []

for i in range(7):
    for j in range(i+1):
        print(i, j)
        dominoes.append(domino(side_a = i, side_b = j))
        

numpy.random.shuffle(dominoes)

Hands = [[ dominoes.pop() for j in range (7) ] for i in range(4)] 

North = Hands[0]
East = Hands[1]
South = Hands[2]
West = Hands[3]


trump = numpy.random.randint(7)   # -1 is no trump, 7 is doubles
print("Trump = %d" % trump)
print("North")
for d in North:
    print(d)
    d.set_trump(trump)
    
print("East")
for d in East:
    print(d)
    d.set_trump(trump)

print("South")
for d in South:
    print(d)
    d.set_trump(trump)
    
print("West")
for d in West:
    print(d)
    d.set_trump(trump)


play_hand([North, East, South, West], trump)
#for trick in range(7):
    