#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 22:36:55 2019

@author: rmoctezuma
"""

import pandas as pd

tree = [['Roby', 'Abo','Abu'],
        ['Sandro','Abo','Abu'],
        ['Pao','Roby','Krisz'],
        ['Tami','Roby','Krisz'],
        ['Isa','Sandro','Caro'],
        ['Dani','Sandro','Cato'],
        ['Krisz','Tati','Nani'],
        ['Angi','Tati','Nani'],
        ['Zali','Angi','Ivi'],
        ['Samu','Angi','Ivi'],
        ['Zsizso','Angi','Ivi'],
        ['Ivi','X','Mara']]

df = pd.DataFrame(tree)
df.columns = ['me','dad','mom']

print(df)

def find_up_direct(me,target):
    s = find_down(target,me).split('>')
    s.reverse()
    return '>'.join(s)


def find_down(me,target):
    if me == target:
        return [target]
    children = df[(df.dad == me) | (df.mom == me)]
    for child in children.me:
        n = find_down(child,target)
        if len(n)>0:
            return  [me] + ['is the parent of'] + n
    return []
    
def find_relative(me,target):
    # If you are my descendant (or me)
    n = find_down(me, target)
    if len(n)>0:
        return n
    # You are not my descendant. If I have parents in the DB...
    if (me in df.me.values):
        n = find_relative(df[df.me==me].dad.iloc[0], target)
        if len(n)>0:
            return [me] + ['is the child of'] + n
        n = find_relative(df[df.me==me].mom.iloc[0], target)
        if len(n)>0:
            return [me] + ['is the child of'] + n
    return []

def find_relationship(me,target):
    r = find_relative(me,target)
    if len(r)==0:
        return ['No relationship']
    check_again = True
    while check_again:
        check_again = False
        # Find cousins
        if len(r)>6:
            for i in range(0,len(r)-2):
                if ((r[i] == 'is the child of') and 
                   (r[i+2]=='is the sibling of') and
                   (r[i+4]=='is the parent of')):
                    r = r[0:i] + ['is the cousin of'] + r[i+5:]
                    check_again=True
                    break
        # Find children
        if len(r)>4:
            for i in range(0,len(r)-2):
                if (r[i] == 'is the child of') and (r[i+2]=='is the child of'):
                    r = r[0:i] + ['is the grandchild of'] + r[i+3:]
                    check_again=True
                    break
        # Find grandparents
        if len(r)>4:
            for i in range(0,len(r)-2):
                if (r[i] == 'is the parent of') and (r[i+2]=='is the parent of'):
                    r = r[0:i] + ['is the grandparent of'] + r[i+3:]
                    check_again=True
                    break        # Find siblings
        if len(r)>4:
            for i in range(0,len(r)-2):
                if (r[i] == 'is the child of') and (r[i+2]=='is the parent of'):
                    r = r[0:i] + ['is the sibling of'] + r[i+3:]
                    check_again=True
                    break
    return r
                
        
# find relative
    # if your my descendant
        # TRUE
    # return
        # if you are a relative of my dad's family OR
        # if you are a relative of my mom's family
            # TRUE
        # else 
            # FALSE







