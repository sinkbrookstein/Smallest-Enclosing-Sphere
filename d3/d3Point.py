import random


# defines methods and classes needed to build the smallest enclosing sphere


# stores x, y, and z coordinate for a point
class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"


# returns the distance squared between two points
def distance(p1, p2):
    return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2 + (p1.z - p2.z) ** 2


def minus(a, b):
    p = Point(a.x - b.x, a.y - b.y, a.z - b.z)
    return p


# used to find determinant of a 2x2 matrix
def det(a, b, c, d):
    return a * d - b * c


# used to find the equation of a plane going through 3 points
def cross(u, v):
    a = det(u.y, u.z, v.y, v.z)
    b = det(u.x, u.z, v.x, v.z)
    c = det(u.x, u.y, v.x, v.y)
    p = Point(a, -1 * b, c)
    return p


def plane(u, v, point):
    p = cross(u, v)
    c = p.x * point.x + p.y * point.y + p.z * point.z
    return [p.x, p.y, p.z, c]


def eq(u, v):
    return [2 * (v.x - u.x), 2 * (v.y - u.y), 2 * (v.z - u.z),
            (v.x ** 2 + v.y ** 2 + v.z ** 2 - u.x ** 2 - u.y ** 2 - u.z ** 2)]


def solveSystem(l1, l2, l3):
    x = [-1 * l1[1] / l1[0], -1 * l1[2] / l1[0], l1[3] / l1[0]]
    l = [l2[0] * x[0], l2[0] * x[1], l2[0] * x[2]]
    l = [l[0] + l2[1], l[1] + l2[2], l2[3] - l[2]]
    y = [-1 * l[1] / l[0], l[2] / l[0]]
    m = [l3[0] * x[0], l3[0] * x[1], l3[0] * x[2]]
    m = [m[0] + l3[1], m[1] + l3[2], l3[3] - m[2]]
    t = [m[0] * y[0] + m[1], m[2] - m[0] * y[1]]
    z = t[1] / t[0]
    y = y[0] * z + y[1]
    x = x[0] * y + x[1] * z + x[2]
    return [x, y, z]


def tempRad(l, p):
    return (p.x - l[0]) ** 2 + (p.y - l[1]) ** 2 + (p.z - l[2]) ** 2


def constant(l, rad, pl, p):
    f = -1 * (tempRad(l, p) - rad)
    s = pl[0] * p.x + pl[1] * p.y + pl[2] * p.z - pl[3]
    return f / s


def coefs(l, d, k, pl):
    x = k * pl[0] - 2 * l[0]
    y = k * pl[1] - 2 * l[1]
    z = k * pl[2] - 2 * l[2]
    const = l[0] ** 2 + l[1] ** 2 + l[2] ** 2 - d - k * pl[3]
    return [x, y, z, const]


def center(l, d, k, pl):
    co = coefs(l, d, k, pl)
    return [co[0] / -2, co[1] / -2, co[2] / -2]


def radius(l, d, k, pl):
    co = coefs(l, d, k, pl)
    cent = center(l, d, k, pl)
    return cent[0] ** 2 + cent[1] ** 2 + cent[2] ** 2 - co[3]


# finds sphere given 2 points
def Sphere2(p1, p2):
    r = distance(p1, p2) / 4
    c = [(p1.x + p2.x) / 2, (p1.y + p2.y) / 2, (p1.z + p2.z) / 2]
    return [r, c]


# finds sphere given 3 points also returns plane to be used if a 4th point is added
def Sphere3(p1, p2, p3):
    # use vectors between points to create plane
    AB = minus(p2, p1)
    BC = minus(p3, p2)
    p = plane(AB, BC, p1)

    # find other equations to make system with plane
    eq1 = eq(p1, p2)
    eq2 = eq(p2, p3)

    # solve system
    c = solveSystem(p, eq1, eq2)

    # find radius squared
    r = tempRad(c, p1)

    # return radius squared and center
    return [r, c, p]


# finds sphere given 4 points
def Sphere4(p1, p2, p3, p4):
    # finds associated sphere from 3 points
    l = Sphere3(p1, p2, p3)

    # uses answer from 3 to solve system of spheres
    k = constant(l[1], l[0], l[2], p4)

    # find center and radius
    c = center(l[1], l[0], k, l[2])
    r = radius(l[1], l[0], k, l[2])

    # return radius squared and center
    return [r, c]


def miniSphere3(n, p1, p2, p3):
    # start by finding sphere defined by p1, p2, p3
    ans = Sphere3(p1, p2, p3)
    r = ans[0]
    c = Point(ans[1][0], ans[1][1], ans[1][2])
    dpts = [p1, p2, p3]

    # go through incrementally and find smallest enclosing sphere so far
    for i in range(len(n)):
        if distance(c, n[i]) > (r + .000000001):    # because of rounding error
            ans = Sphere4(dpts[0], dpts[1], dpts[2], n[i])
            r = ans[0]
            c = Point(ans[1][0], ans[1][1], ans[1][2])
            dpts = [dpts[0], dpts[1], dpts[2], n[i]]

    return [r, c, dpts]


def miniSphere2(n, p1, p2):
    # randomly permute input
    random.shuffle(n)

    # start with p1 and p2 since they must be included
    ans = Sphere2(p1, p2)
    r = ans[0]
    c = Point(ans[1][0], ans[1][1], ans[1][2])
    dpts = [p1, p2]

    # go through incrementally and find smallest enclosing sphere so far
    for i in range(len(n)):
        if distance(c, n[i]) > (r + .000000001):    # because of rounding error
            ans = miniSphere3(n[:i], p1, p2, n[i])
            r = ans[0]
            c = ans[1]
            dpts = ans[2]

    return [r, c, dpts]


def miniSphere1(n, p):
    # randomly permute input
    random.shuffle(n)

    # start with p and n[0]
    ans = Sphere2(p, n[0])
    r = ans[0]
    c = Point(ans[1][0], ans[1][1], ans[1][2])
    dpts = [p, n[0]]

    # go through the rest of n incrementally
    for i in range(1, len(n)):
        if distance(c, n[i]) > (r + .000000001):    # because of rounding error
            ans = miniSphere2(n[:i], p, n[i])
            r = ans[0]
            c = ans[1]
            dpts = ans[2]

    return [r, c, dpts]


def miniSphere(n):
    # randomly permute input
    random.shuffle(n)

    # start with first two elements
    ans = Sphere2(n[0], n[1])
    r = ans[0]
    c = Point(ans[1][0], ans[1][1], ans[1][2])
    dpts = [n[0], n[1]]

    # go through the rest of n incrementally
    for i in range(2, len(n)):
        if distance(c, n[i]) > (r + .000000001):  # because of rounding error
            ans = miniSphere1(n[:i], n[i])
            r = ans[0]
            c = ans[1]
            dpts = ans[2]

    return [r, c]
