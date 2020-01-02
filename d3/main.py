from FinalProject.d3 import d3Point

A = d3Point.Point(1, -1, 3)
B = d3Point.Point(4, 1, -2)
C = d3Point.Point(-1, -1, 1)
D = d3Point.Point(1, 1, 1)
E = d3Point.Point(1, 1, 0)
F = d3Point.Point(3, 3, 3)
H = d3Point.Point(3, 2.5, 2.5)

mylist = [A, B, C, D, E, F, H]

a = d3Point.miniSphere(mylist)
print("radius squared: ", a[0])
print("center: ", a[1])
