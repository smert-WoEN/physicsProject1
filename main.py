import math

import matplotlib.pyplot as plt
import numpy as np
import scipy.constants
import scipy.optimize


def sign(n):
    if n > 0.0:
        return 1.0
    if n < 0.0:
        return -1.0
    return 0.0


def plot(x, y, string, number):
    plt.figure(number)
    plt.clf()
    plt.plot(x, y, linewidth=2, color="Red")
    plt.grid(True)
    plt.title(string, fontsize=14, fontweight="bold")
    plt.xlabel('x', fontsize=14)
    plt.ylabel('y', fontsize=14)
    plt.savefig(str(number) + ".png", dpi=500)


def startSpeedAndAngleWithOutWind():
    print("input start speed:", end=" ")
    v0 = float(input())
    print("input start angle:", end=" ")
    a = math.radians(float(input()))

    vx = v0 * math.cos(a)
    vy = v0 * math.sin(a)
    t = vy / scipy.constants.g
    print(t)
    x = [i / 1000000 * vx for i in range(int(t * 2 * 1000000))]
    y = [i / 1000000 * vy - scipy.constants.g * ((i / 1000000) ** 2) / 2 for i in range(int(t * 2 * 1000000))]
    print(x[-1], y[-1])
    plot(x, y, "angle and speed no wind", str(v0) + "angle" + str(a))
    return vx * (t * 2), t


def euler(aLoc, v0Loc, xMaxLoc, h=0.001):
    x = [0]
    y = [0]
    while x[-1] < xMaxLoc:
        y.append(y[-1] + h * function(aLoc, v0Loc, x[-1]))
        x.append(x[-1] + h)
    return x, y


def function(aLoc, v0Loc, x):
    return math.tan(aLoc) - scipy.constants.g * x / (v0Loc ** 2 * math.cos(aLoc) ** 2)


def startToCoordinatesWithOutWind():
    print("input x coordinate:", end=" ")
    X = float(input())
    print("input y coordinate:", end=" ")
    Y = float(input())
    v0 = 0.001
    s = sign(X)
    X = abs(X)
    flag = True
    while flag:
        for a in range(int(math.pi / 2 * 1000)):
            angle = a / 1000
            yPas = X * math.tan(angle) - scipy.constants.g * X ** 2 / (2 * v0 ** 2 * math.cos(angle) ** 2)
            if abs(yPas - Y) <= 0.001:
                print(v0, math.degrees(angle))
                xMat, yMat = euler(angle, v0, X)
                xMat = np.array(xMat)
                xMat = xMat * s
                plot(xMat, yMat, "to coordinates y(x) no wind", str(s * X) + "coordinates" + str(Y))
                flag = False
                break
        v0 += 0.001


def function2(x, v0, a, k, m):
    if 1 - x * k / (m * v0 * math.cos(a)) < 0:
        return "error"
    return m / k * ((v0 * math.sin(a) + m * scipy.constants.g / k) * x * k / (m * v0 * math.cos(a)) + scipy.constants.g * m / k * math.log(1 - x * k / (m * v0 * math.cos(a))))


def startSpeedAndAngleWithWind():
    print("input start speed:", end=" ")
    v0 = float(input())
    print("input start angle:", end=" ")
    a = math.radians(float(input()))
    print("input k:", end=" ")
    k = float(input())
    x = [0]
    y = [0]
    i = 0.001
    while y[-1] >= 0:
        x.append(i)
        y.append(function2(x[-1], v0, a, k, 1))
        i += 0.001
    print(x[-1], y[-1])
    plot(x, y, "angle and speed", str(x[-1]) + "angleWind" + str(y[-1]))


def startToCoordinatesWithWind():
    print("input x coordinate:", end=" ")
    X = float(input())
    print("input y coordinate:", end=" ")
    Y = float(input())
    print("input k:", end=" ")
    k = float(input())
    v0 = 0.001
    s = sign(X)
    X = abs(X)
    flag = True
    while flag:
        for a in range(int(math.pi / 2 * 1000)):
            angle = a / 1000
            yPas = function2(X, v0, angle, k, 1)
            if yPas != "error":
                if abs(float(yPas) - Y) <= 0.001:
                    print(v0, math.degrees(angle))
                    x = [0]
                    y = [0]
                    i = 0.001
                    while x[-1] < X:
                        yPAss = (function2(x[-1] + 0.001, v0, angle, k, 1))
                        if yPAss == "error":
                            break
                        x.append(i)
                        y.append(yPAss)
                        i += 0.001
                    x = np.array(x)
                    x = x * s
                    plot(x, y, "cords wind y(x)", str(s * X) + "coordinatesWind" + str(Y))
                    flag = False
                    break
        v0 += 0.001



startSpeedAndAngleWithOutWind()
startToCoordinatesWithOutWind()
startSpeedAndAngleWithWind()
startToCoordinatesWithWind()
