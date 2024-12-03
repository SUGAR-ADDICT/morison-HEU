"""
计算时需要用到的公式
"""
from sympy import sin, cos, exp, symbols
from scipy.optimize import differential_evolution


def velocity_component(a, omega, k, z, x, t):
    # 定义函数表示速度分量
    u = a * omega * exp(k * z) * cos(k * x - omega * t)
    w = a * omega * exp(k * z) * sin(k * x - omega * t)
    return u, w


def acceleration_component(a, omega, k, z, x, t):
    # 定义函数表示加速度分量
    dudt = a * omega**2 * exp(k * z) * sin(k * x - omega * t)
    dwdt = -a * omega**2 * exp(k * z) * cos(k * x - omega * t)
    return dudt, dwdt


def velocity_derivative(dudt, dwdt, e_x, e_z):
    # 加速度
    return (1-e_x**2)*dudt-e_x*e_z*dwdt


def velocity_squared(u, w, e_x, e_z):
    # 速度的平方
    return u**2+w**2-(e_x*u+e_z*w)**2


def expression_linear_x_z(start=(float, float), end=(float, float)):
    x_start = start[0]
    z_start = start[1]
    x_end = end[0]
    z_end = end[1]

    slope = (x_end-x_start)/(z_end-z_start)
    intercept = x_start-slope*z_start

    z = symbols('z')

    f_z = slope*z-intercept

    return f_z


def maximum_force(objective_function, bounds):

    # 使用 differential_evolution 函数寻找函数的最大值
    result = differential_evolution(objective_function, bounds)

    # 打印结果
    if result.success:
        max_value = -result.fun  # 最大值为目标函数的负值
        max_time = result.x[0]
        # print(rf"Maximum value of the function: {max_value:.2f} N")
        print(rf"F_x = {max_value:.2f}N")
        return max_value
        # print(rf"Time at which the maximum occurs: {max_time:.2f} s")
    else:
        print("Optimization failed:", result.message)
