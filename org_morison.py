import os
import numpy as np
from sympy import sin, cos, exp, symbols, cot, integrate
from sympy.utilities.lambdify import lambdify
from scipy.optimize import differential_evolution
import raschii


# 环境参数
rho = 1000  # 水密度
C_D = 1.0  # 拖曳系数
C_M = 2.0  # 惯性系数


def maximum_force(objective_function, bounds):

    # 使用 differential_evolution 函数寻找函数的最大值
    result = differential_evolution(objective_function, bounds)

    # 打印结果
    if result.success:
        max_value = -result.fun  # 最大值为目标函数的负值
        max_time = result.x[0]
        # print(rf"Maximum value of the function: {max_value:.2f} N")
        print(rf"{max_value:.2f}")
        return max_value
        # print(rf"Time at which the maximum occurs: {max_time:.2f} s")
    else:
        print("Optimization failed:", result.message)


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


# 圆柱参数
scale_factor = 50  # 缩放因子
cylinder_diameter = 10/scale_factor  # 圆柱直径
draft = 45/scale_factor  # 吃水

# 算例倾斜角
d = 30

file_path = os.path.join(rf'd{d}', 'morsion', 'force.dat')

os.makedirs(os.path.dirname(file_path), exist_ok=True)  # 如果不存在，则创建文件夹

with open(file_path, mode="w") as file:

    file.write(f"period(s)  force(N)\n")

    for wave_length in range(55, 220, 5):

        # 构造波浪
        a = 2/scale_factor  # 波浪振幅
        wave_length /= scale_factor  # 波长
        water_depth = 60/scale_factor  # 水深

        WaveModel, AirModel = raschii.get_wave_model('Fenton')
        wave = WaveModel(height=2*a, depth=water_depth,
                         length=wave_length, N=5)

        alpha = 90-d  # 圆柱轴与z轴的夹角

        print(
            rf"For case d{d}t{wave.T*50**0.5:.2f}h{2*a},{wave_length}")

        # 函数表示拖曳力和惯性力
        e_x = np.sin(alpha/180*np.pi)  # x方向上的坐标分量
        e_z = np.cos(alpha/180*np.pi)  # z方向上的坐标分量

        # 定义符号变量
        z, t = symbols('z t')
        x = -z * cot(d / 180 * np.pi)  # 在圆柱轴线上x的坐标是一个关于z的函数

        u, w = velocity_component(a, wave.omega, wave.k, z, x, t)
        dudt, dwdt = acceleration_component(a, wave.omega, wave.k, z, x, t)

        dUdt = velocity_derivative(dudt, dwdt, e_x, e_z)
        U_square = velocity_squared(u, w, e_x, e_z)

        f_i = rho * C_M * np.pi * cylinder_diameter ** 2 / \
            4 / sin(d / 180 * np.pi) * dUdt
        f_d = -0.5 * C_D * rho * cylinder_diameter * U_square

        # 计算拖曳力、惯性力、总力关于时间的函数
        # z_min = (10-55*sin(d/180*np.pi))/scale_factor  # 确定积分下限
        z_min = -0.35
        # print(rf'draft={z_min:.2f} m')

        F_i = integrate(f_i, (z, 0, z_min))
        F_d = integrate(f_d, (z, 0, z_min))
        # F_t = F_i + F_d
        F_t = F_i

        # 使用数值方法求函数的最大值
        F = lambdify(t, F_t, 'numpy')  # 将sympy表达式转换为可操作的函数

        bounds = [(0, wave.T)]  # 定义搜索范围

        force = maximum_force(F, bounds)

        # 将结果写入文件，使用空格分隔
        file.write(f"{wave.T*50**0.5} {force}\n")

print(rf"数据已写入{file_path}")
