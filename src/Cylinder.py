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
        - :func:`discretize` : 根据杆件端点坐标离散。
    """

    def __init__(self, diameter: float, start=(float, float, float), end=(float, float, float), resolution=10) -> None:
        """

        """
        self.diameter = diameter
        self.start = np.array(start)
        self.end = np.array(end)
        self.resolution = resolution
        try:
            self.unit_vector()
        except ValueError:
            print("两个点坐标相同，请检查坐标输入")

    def unit_volume(self) -> float:
        """
        返回单位体积，`V=pi*D^2/4`

        :return V (float):
        """
        return np.pi*self.diameter**2/4

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

    def discretize(self):
        """
        离散化圆柱体，将圆柱体从起始点到终点沿着轴线方向分割为若干点。
        这里只考虑两个端点，返回一个包含起始点和终点的离散点列表。

        :params resolution (int): 离散点的数量
        :return: 离散点的坐标数组
        """
        # 离散点直接通过插值
        step = np.linspace(0, 1, self.resolution)
        points = np.array(
            [self.start + s * (self.end - self.start) for s in step])
        distances = np.linalg.norm(np.diff(points, axis=0), axis=1)

        return points, distances
