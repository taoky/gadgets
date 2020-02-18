import isa
from scipy.misc import *
from scipy.optimize import *
from geographiclib.geodesic import Geodesic
from math import *
import numpy as np
import sys
geod = Geodesic.WGS84  # define the WGS84 ellipsoid

mass = 100 # kg
d = 203 * 10 ** -3 # m
C_d = 0.04 # 阻力系数
earth_omega = 7.292 * 10 ** -5 # rad/s
earth_R = 6371 * 1000 # 地球半径

def dms_to_dd(d, m, s):
    dd = d + float(m) / 60 + float(s) / 3600
    return dd

hefeiLatitude = dms_to_dd(31, 51, 49)
hefeiLongitude = dms_to_dd(117, 16, 46)
chizhouLatitude = dms_to_dd(30, 39, 22)
chizhouLongitude = dms_to_dd(117, 29, 20)

def g(h): # h: m 万有引力
    return -9.80665 / ((1 + h / earth_R) ** 2)

def a_c(omegax, omegay, omegaz, x, y, z, thisomega, thisr): # maybe totally wrong. FIXME
    return thisomega * (omegax * x + omegay * y + omegaz * z) - earth_omega ** 2 * thisr

def air_density(h):
    return isa.isa_den(h)

def a_D(v, h): # calculate F_Dx, F_Dy, F_Dz
    return -(0.5 * air_density(h) * v * v * C_d * 2 * pi * ((d / 2) ** 2)) / mass

def a_cor(omega, v): # calculate f_corx, f_cory, f_corz
    return -2 * omega * v

v0 = 1500

def simulate(finput):
    theta = finput[0] / 180.0 * pi; alpha = (finput[1] + 90.0) / 180 * pi
    delta = 0.01 # sec
    x = 0; y = 0; z = 0.0000001
    vx = -v0 * cos(theta) * cos(alpha); vy = v0 * cos(theta) * sin(alpha)
    vz = v0 * sin(theta)
    omega_x = -earth_omega * cos(hefeiLatitude / 180 * pi); omega_y = 0; omega_z = earth_omega * sin(hefeiLatitude / 180 * pi)
    ax = 0; ay = 0; az = 0
    count = 0
    #print(omega_x, omega_y, omega_z)
    #print(x, y, z, vx, vy, vz, ax, ay, az, count)
    
    maxz = 0
    while z > 0 and count <= 1500000: # no longer than 1500 sec
        ax = a_D(vx, z) - a_cor(omega_z, vy) + a_c(omega_x, omega_y, omega_z, x, y, z, omega_x, x)
        ay = a_D(vy, z) - a_cor(omega_x, vz) + a_cor(omega_z, vx) + a_c(omega_x, omega_y, omega_z, x, y, z, omega_y, y)
        az = g(z) + a_D(vz, z) + a_cor(omega_x, vy) + a_c(omega_x, omega_y, omega_z, x, y, z, omega_z, z)
        vx += ax * delta
        vy += ay * delta
        vz += az * delta
        x += vx * delta
        y += vy * delta
        z += vz * delta
        # if z < maxz:
        #     # print("Highest:", x, y, z, vx, vy, vz, ax, ay, az, count)
        #     maxz = -100
        # elif maxz != -100:
        #     maxz = z
        count += 1
        print("%f,%f,%f,%f,%f,%f,%f,%f,%f,%f" % (x, y, z, vx, vy, vz, ax, ay, az, count * delta))
    res = (x, y, z, vx, vy, vz, ax, ay, az, count)
    resx = res[0]; resy = res[1]
    return (resx - chizhouX) ** 2 + (resy - chizhouY) ** 2

gg = geod.Inverse(hefeiLatitude, hefeiLongitude, chizhouLatitude, chizhouLongitude)
oriazi = gg["azi1"]; oridis = gg["s12"]
chizhouX = -oridis * cos(oriazi / 180 * pi)
chizhouY = oridis * sin(oriazi / 180 * pi)
# print(chizhouX, chizhouY)
# origin: (0, 0, 0)
# target: (chizhouX, chizhouY, 0)

print(simulate([67.8234, 80.6826]))

# When v = 1500 m/s
# print(fmin(simulate, np.array([ 45.0 , 45.0]))) # deg
# print(simulate(np.array([ 50.76358153,  51.24629029])))

# cal v_0 min
# x0 = [45.0, 45.0]
# xmin = [10.0, 10.0]
# xmax = [85.5, 85.0]
# bounds = [(low, high) for low, high in zip(xmin, xmax)]
# minimizer_kwargs = dict(method="L-BFGS-B", bounds=bounds)
# for i in range(1300, 1310, 1):
#     v0 = i
#     print("v0: %d" % v0)
#     print(basinhopping(simulate, x0, minimizer_kwargs=minimizer_kwargs))