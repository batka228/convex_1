#!/usr/bin/env -S python3 -B
from r2point import R2Point
from convex import Void

f = Void()
q = 0
card = 0

try:
    while True:
        f = f.add(R2Point())
        print(f"S = {f.area()}, P = {f.perimeter()}")
        print(type(f))
        if f.area() == 0:
            card = f.cardinality()
        else:
            if not(q):
                card = f.cardinality()
                q = 1
            elif f.ind():
                card = f.cardinality()
        print(f"число пересечений {card}\n")
except(EOFError, KeyboardInterrupt):
    print("\nStop")
