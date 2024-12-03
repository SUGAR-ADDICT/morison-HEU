"""
模块: 杆件类 (Cylinder)
该模块定义了一个 `Cylinder` 类，表示一个三维空间中的圆柱体。通过该类，可以计算圆柱的单位体积、单位面积、单位矢量以及给定坐标下的直线方程。

功能:
- 计算圆柱的单位体积
- 计算圆柱的单位面积
- 计算给定两个端点坐标的单位矢量
- 求解给定端点坐标下，`x` 与 `z` 之间的线性关系

"""

from sympy import symbols, pi, core
import numpy as np


class Cylinder:
    """
    圆柱类，表示一个圆柱体，通过直径以及端点坐标来定义。

    :params diameter (float): 圆柱的直径
    :params start (tuple): 圆柱起始点的坐标，格式为 (x, y, z)
    :params end (tuple): 圆柱终点的坐标，格式为 (x, y, z)

    Methods
        - :func:`unit_volume`: 计算单位体积。
        - :func:`unit_area`: 计算单位面积。
        - :func:`unit_vector`: 计算从起始点到终点的单位矢量。
        - :func:`expression_linear_x_z`: 给定端点坐标，返回 `x` 关于 `z` 的线性方程。
    """

    def __init__(self, diameter: float, start=(float, float, float), end=(float, float, float)) -> None:
        """

        """
        self.diameter = diameter
        self.start = start
        self.end = end
        try:
            self.unit_vector()
        except ValueError:
            print("两个点坐标相同，请检查坐标输入")
        else:
            print("cylinder创建成功")

    def unit_volume(self) -> float:
        """
        返回单位体积，`V=pi*D^2/4`

        :return V (float):
        """
        return pi*self.diameter**2/4

    def unit_area(self) -> float:
        """
        返回单位面积，`A=D`

        :return A (float):
        """
        return self.diameter

    def unit_vector(self) -> np.ndarray:
        """
        计算两个点之间的单位矢量。

        :param point1: 点1的坐标 (x1, y1, z1)，类型为元组或列表。
        :param point2: 点2的坐标 (x2, y2, z2)，类型为元组或列表。

        :return unit_vector (np.ndarray): 单位矢量[e1,e2,e3]
        """
        # 将点转换为NumPy数组
        p1 = np.array(self.start)
        p2 = np.array(self.end)

        # 计算矢量
        vector = p2 - p1

        # 计算矢量的模
        magnitude = np.linalg.norm(vector)

        if magnitude == 0:
            raise ValueError(
                "The two points are identical; cannot compute a unit vector.")

        # 计算单位矢量
        unit_vector = vector / magnitude

        return unit_vector

    def expression_linear_x_z(self) -> core.numbers.Float:
        """
        通过坐标得到x关于z的函数`x = k*z + b`

        :return linear_x_z (sympy.core.numbers.Float):
        """
        x_start = self.start[0]
        # y_start = self.start[1]
        z_start = self.start[2]
        x_end = self.end[0]
        # y_end = self.end[1]
        z_end = self.end[2]

        slope = (x_end-x_start)/(z_end-z_start)
        intercept = x_start-slope*z_start

        z = symbols('z')

        linear_x_z = slope*z-intercept

        return linear_x_z
