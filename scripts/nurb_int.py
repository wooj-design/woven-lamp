import numpy as np

with open('NURBS.txt') as f:
    output = f.read()

curves = output.split('{0;')

for i, curve in enumerate(curves):
    clean = curve.split('\n')[1:]
    if i == 3:
        print(clean)


