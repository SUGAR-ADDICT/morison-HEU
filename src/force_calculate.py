from src.Cylinder import Cylinder
from src.Morison import Morsion
from src.MateWave import MateWave
from sympy import symbols, integrate, lambdify


class ForceCal():
    """
    计算荷载随时间变化的表达式的类。

    该类接受一个柱体（Cylinder），波浪（MateWave），以及Morison方程的计算类（Morsion），
    并计算荷载随时间的变化表达式 `force = f(t)`。通过波浪的水流速度和加速度，结合Morison方程
    计算阻力和惯性力，最终得到总的荷载表达式。

    Attributes:
        cylinder (Cylinder): 柱体对象，包含柱体的几何参数（长度、直径、起止点）。
        wave (MateWave): 波浪对象，用于计算水流速度、加速度等。
        morison (Morsion): Morison方程对象，用于计算阻力力和惯性力。
        rho (float): 水的密度，默认为1000.0 kg/m^3。
        e_x, e_y, e_z (float): 单位矢量的分量，表示柱体的方向。
        water_vel_u, water_vel_w (sympy expressions): 分别表示x和z方向的水流速度表达式。
        water_acc_u, water_acc_w (sympy expressions): 分别表示x和z方向的水流加速度表达式。
    """

    def __init__(self, cylinder: Cylinder, wave: MateWave, morison: Morsion, rho=1000.0) -> None:
        """
        初始化类实例并计算所需的基本参数。

        Args:
            cylinder (Cylinder): 一个 Cylinder 类的实例，包含柱体的几何信息。
            wave (MateWave): 一个 MateWave 类的实例，包含波浪信息。
            morison (Morsion): 一个 Morsion 类的实例，用于计算荷载。
            rho (float): 水的密度（默认1000.0 kg/m^3）。
        """
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
        计算波浪水质点的运动速度矢量表达式

        Returns:
            (sympy expression)
        """
        return self.e_x * self.water_vel_u + self.e_z * self.water_vel_w

    def velocity_x(self):
        """
        计算柱体轴线正交的水质点速度矢量的x方向分量表达式

        Returns:
            (sympy expression)
        """
        return self.water_vel_u - self.e_x * self.water_velocity_vector()

    def velocity_y(self):
        """
        计算柱体轴线正交的水质点速度矢量的z方向分量表达式

        Returns:
            (sympy expression)
        """
        return -self.e_y * self.water_velocity_vector()

    def velocity_z(self):
        """
        计算柱体轴线正交的水质点速度矢量的x方向分量表达式

        Returns:
            (sympy expression)
        """

        return self.water_vel_w-self.e_z * self.water_velocity_vector()

    def water_velocity_abs(self):
        """
        与柱体正交的水质点速度矢量的绝对值表达式

        Returns:
            (sympy expression)
        """
        return (self.water_vel_u**2 + self.water_vel_w**2 - (self.e_x * self.water_vel_u + self.e_z * self.water_vel_w)**2)**0.5

    def acc_x(self):
        """
        x方向的水质点加速度表达式

        Returns:
            (sympy expression)
        """
        return (1 - self.e_x**2) * self.water_acc_u - self.e_z * self.e_x * self.water_acc_w

    def acc_y(self):
        """
        返回y方向的加速度表达式

        Returns:
            (sympy expression)     
        """
        return -1 * self.e_x * self.e_y * self.water_acc_u - self.e_z * self.e_y * self.water_acc_w

    def acc_z(self):
        """
        返回z方向的加速度表达式

        Returns:
            (sympy expression)     
        """
        return -1 * self.e_x * self.e_z * self.water_acc_u + (1 - self.e_x**2) * self.water_acc_w

    def cal_force_x(self):
        """
        计算x方向的总荷载随时间变化的表达式

        Returns:
            (sympy expression)     
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
