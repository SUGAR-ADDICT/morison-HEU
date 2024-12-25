from src.Cylinder import Cylinder
from src.Morison import Morsion


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

    def __init__(self, cylinder: Cylinder, wave, morison: Morsion, rho=1000.0, t=0) -> None:
        """
        初始化类实例并计算所需的基本参数。

        Args:
            cylinder (Cylinder): 一个 Cylinder 类的实例，包含柱体的几何信息。
            wave : 一个类的实例，包含波浪信息。
            morison (Morsion): 一个 Morsion 类的实例，用于计算荷载。
            rho (float): 水的密度（默认1000.0 kg/m^3）。
        """
        self.cylinder = cylinder
        self.wave = wave
        self.morison = morison
        self.rho = rho
        self.t = t

        _unit_vector = self.cylinder.unit_vector()
        self.e_x = _unit_vector[0]
        self.e_y = _unit_vector[1]
        self.e_z = _unit_vector[2]
        self.points, self.distances = self.cylinder.discretize()
        self.water_u_lst, self.water_w_lst = self.get_vel()
        self.water_acc_x_lst, self.water_acc_z_lst = self.get_acc()
        self.vel_vector_lst = self.get_vel_vector()

    def sum(self, values):
        """
        梯形法对传入的所有值沿着杆件求和

        Args:
            values (_type_): _description_

        Returns:
            _type_: _description_
        """
        total_value = 0
        for i in range(1, self.cylinder.resolution):
            total_value += (values[i-1]+values[i])*self.distances[i-1]/2
        return total_value

    def get_values_lst(self, expr_func):
        values_lst = []
        for i in range(len(self.points)):
            value = expr_func(i)
            values_lst.append(value)
        return values_lst

    def get_vel(self):
        """
        获得与坐标对应的速度list

        Returns:
            _type_: _description_
        """
        u_lst = []
        w_lst = []

        for point in self.points:
            x = point[0]
            z = point[2]
            vel = self.wave.velocity(x, z, self.t)
            u_lst.append(vel[0][0])
            w_lst.append(vel[0][1])

        return u_lst, w_lst

    def get_acc(self):
        """
        获得与坐标对应的加速度list

        Returns:
            _type_: _description_
        """
        a_x_lst = []
        a_z_lst = []
        for point in self.points:
            x = point[0]
            z = point[2]
            acc = self.wave.acceleration(x, z, self.t)
            a_x_lst.append(acc[0][0])
            a_z_lst.append(acc[0][1])

        return a_x_lst, a_z_lst

    def get_vel_vector(self):
        """
        计算波浪水质点的运动速度矢量表达式

        Returns:
            (sympy expression)：self.e_x * self.water_vel_u + self.e_z * self.water_vel_w

        """
        vel_vector_lst = []
        for i in range(len(self.points)):
            vel_vector = self.e_x * \
                self.water_u_lst[i] + self.e_z * self.water_w_lst[i]
            vel_vector_lst.append(vel_vector)
        return vel_vector_lst

    def get_vel_x(self):
        """
        计算柱体轴线正交的水质点速度矢量的x方向分量表达式

        Returns:
            (sympy expression)
        """
        def expr_func(i):
            return self.e_x * self.water_u_lst[i] + self.e_z * self.water_w_lst[i]
        return self.get_values_lst(expr_func)

    def get_vel_y(self):
        """
        计算柱体轴线正交的水质点速度矢量的z方向分量表达式

        Returns:
            (sympy expression)
        """
        def expr_func(i):
            return -self.e_y * self.vel_vector_lst[i]
        return self.get_values_lst(expr_func)

    def get_vel_z(self):
        """
        计算柱体轴线正交的水质点速度矢量的x方向分量表达式

        Returns:
            (sympy expression)
        """
        def expr_func(i):
            return self.water_w_lst[i]-self.e_z * self.vel_vector_lst[i]
        return self.get_values_lst(expr_func)

    def get_vel_abs(self):
        """
        与柱体正交的水质点速度矢量的绝对值表达式

        Returns:
            (sympy expression)
        """
        def expr_func(i):
            return (self.get_vel_x()[i] ** 2 + self.get_vel_y()[i] ** 2 + self.get_vel_z()[i] ** 2) ** 0.5
        return self.get_values_lst(expr_func)

    def get_acc_x(self):
        """
        x方向的水质点加速度表达式

        Returns:
            (sympy expression)
        """
        def expr_func(i):
            return (1 - self.e_x**2) * self.water_acc_x_lst[i] - self.e_z * self.e_x * self.water_acc_z_lst[i]
        return self.get_values_lst(expr_func)

    def get_acc_y(self):
        """
        返回y方向的加速度表达式

        Returns:
            (sympy expression)     
        """
        def expr_func(i):
            return -1 * self.e_x * self.e_y * self.water_acc_x_lst[i] - self.e_z * self.e_y * self.water_acc_z_lst[i]
        return self.get_values_lst(expr_func)

    def get_acc_z(self):
        """
        返回z方向的加速度表达式

        Returns:
            (sympy expression)     
        """
        def expr_func(i):
            return -1 * self.e_x * self.e_z * self.water_acc_x_lst[i] + (1 - self.e_x**2) * self.water_acc_z_lst[i]
        return self.get_values_lst(expr_func)

    def cal_force_x(self):
        """
        计算x方向的总荷载随时间变化的表达式

        Returns:
            (sympy expression)     
        """

        def drag_expr(i):
            return self.morison.force_drag(self.rho, self.cylinder.unit_area(), self.get_vel_abs()[i], self.get_vel_x()[i])

        def iner_expr(i):
            return self.morison.force_inertial(self.rho, self.cylinder.unit_volume(), self.get_acc_x()[i])
        force_drag_lst = self.get_values_lst(drag_expr)
        force_iner_lst = self.get_values_lst(iner_expr)

        force_drag = self.sum(force_drag_lst)
        froce_iner = self.sum(force_iner_lst)

        return force_drag + froce_iner
