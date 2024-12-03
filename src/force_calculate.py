"""
接受一个
    - cylinder class
    - my_wave class
    - morsion class
返回荷载关于时间的表达式
force=f(t)
"""
from src.Cylinder import Cylinder
from src.Morison import Morsion
from src.MateWave import (StokesWave, AiryWave, FentonWave, MateWave)
from sympy import symbols, integrate, lambdify


class ForceCal():
    def __init__(self, cylinder: Cylinder, wave: MateWave, morison: Morsion, rho=1000.0) -> None:
        self.cylinder = cylinder
        self.wave = wave
        self.morison = morison
        self.rho = rho

        _unit_vector = self.cylinder.unit_vector()
        self.e_x = _unit_vector[0]
        self.e_y = _unit_vector[1]
        self.e_z = _unit_vector[2]
        self.water_vel_u, self.water_vel_w = wave.water_velocity(
            cylinder.expression_linear_x_z())
        self.water_acc_u, self.water_acc_w = wave.water_acceleration(
            cylinder.expression_linear_x_z())

    def water_velocity_vector(self):
        """
        波浪水质点运动速度矢量
        """
        return self.e_x * self.water_vel_u + self.e_z * self.water_vel_w

    def velocity_x(self):
        """
        返回x方向的速度表达式
        `velocity_x = wave.water_velocity_u-e_x * (e_x*water_velocity_u+e_z*water_velocity_w)`
        """
        return self.water_vel_u - self.e_x * self.water_velocity_vector()

    def velocity_y(self):
        """
        返回y方向的速度表达式
        `velocity_y = -e_y*(e_x*water_velocity_u+e_z*water_velocity_w)`
        """
        return -self.e_y * self.water_velocity_vector()

    def velocity_z(self):
        """
        返回z方向的速度表达式
        `velocity_z = water_velocity_w-e_z * (e_x*water_velocity_u+e_z*water_velocity_w)`
        """

        return self.water_vel_w-self.e_z * self.water_velocity_vector()

    def water_velocity_abs(self):
        """
        与柱体正交的水质点速度矢量的绝对值
        `velocity_n_abs = (water_velocity_u**2+water_velocity_w**2 -(e_x*water_velocity_u+e_z*water_velocity_w)**2)**0.5`
        """
        return (self.water_vel_u**2 + self.water_vel_w**2 - (self.e_x * self.water_vel_u + self.e_z * self.water_vel_w)**2)**0.5

    def acc_x(self):
        """
        返回x方向的加速度表达式
        `acc_x = (1-e_x**2)*water_acc_u-e_z*e_x*water_acc_w`
        """
        return (1 - self.e_x**2) * self.water_acc_u - self.e_z * self.e_x * self.water_acc_w

    def acc_y(self):
        """
        返回y方向的加速度表达式
        `acc_y = -1*e_x*e_y*water_acc_u-e_z*e_y*water_acc_w`
        """
        return -1 * self.e_x * self.e_y * self.water_acc_u - self.e_z * self.e_y * self.water_acc_w

    def acc_z(self):
        """
        返回z方向的加速度表达式
        `acc_z = -1*e_x*e_z*water_acc_u+(1-e_z**2)*water_acc_w`
        """
        return -1 * self.e_x * self.e_z * self.water_acc_u + (1 - self.e_x**2) * self.water_acc_w

    def cal_force_x(self):
        """
        计算x方向的的荷载
        """
        z, t = symbols("z t")

        # 得到荷载关于z与t的函数，force_drag=f(t,z)
        force_drag_x_t_z = self.morison.force_drag(
            self.rho, self.cylinder.unit_area(), self.water_velocity_abs(), self.velocity_x())

        # 得到荷载关于z与t的函数，force_iner=f(t,z)
        force_iner_x_t_z = self.morison.force_inertial(
            self.rho,  self.cylinder.unit_volume(), self.acc_x())

        # 拖曳力含有速度的平方，难以积分，离散求和
        # TODO 优化求和算法，这样处理还是太简单了
        n_segments = 20  # 分片数
        delta_z = (self.cylinder.end[2] - self.cylinder.start[2]) / n_segments
        z_values = [self.cylinder.start[2] + i *
                    delta_z for i in range(n_segments)]
        force_drag_x_t = sum(
            force_drag_x_t_z.subs(z, z_val) * delta_z for z_val in z_values
        )

        force_iner_x_t = integrate(
            force_iner_x_t_z, (z, self.cylinder.start[2], self.cylinder.end[2]))

        force_total_x_t = force_drag_x_t + force_iner_x_t

        num_force_x_t = lambdify(
            t, force_total_x_t, 'numpy')  # 将sympy表达式转换为可操作的函数

        return num_force_x_t
