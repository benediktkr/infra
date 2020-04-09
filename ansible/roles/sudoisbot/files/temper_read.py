#!/usr/bin/env python3

from temper import Temper

temper = Temper()
t = temper.read()
temp = t[0]['internal temperature']

print(temp)
