import numpy as np
import matplotlib.pyplot as plt

def Rho(h):
    T = 288.15 - 0.0065 * h
    if h > 0:
        return 1.225 * (T/288.15)**(4.2561)
    return 1.225

h0 = 10.5e3
m = 1000

# tungsten
rho_t = 19.3e3    # kg/m^3

# lead
rho_l = 11.34e3

# uranium
rho_u = 19.05


rho = rho_t
l = (m/rho) ** (1/3)
print(f"\nCube side: {l:.02f} m")

A = l**2 / 4

dt = 0.01

h = h0
v = 0
t = 0

h_lst = []
v_lst = []
t_lst = []

while h > 0:

    F_aero = 0.5 * A * v**2 * Rho(h) * 0.5
    F_g = - m * 9.80665

    a = (F_g + F_aero) / m

    v += a * dt
    h += v * dt
    t += dt

    h_lst.append(h)
    v_lst.append(v)
    t_lst.append(t)



v_terminal = ((m * 9.80665) / (1.17 * A * 1.225 * 0.5)) ** (1/2)
energy = 0.5 * m * v_terminal**2
print(f"Actual end velocity: {-v:.01f} m/s")
print(f"Terminal velocity: {v_terminal:.01f} m/s")
print(f"Energy: {energy/1e6:.0f} MJ")
print(f"Equivalent tons of TNT: {energy / 4.184e9:.03f}")

plt.plot(t_lst, v_lst, label="v [m/s]")
plt.plot(t_lst, np.array(h_lst)/1000, label="h [km]")
plt.grid()
plt.legend()
plt.show()