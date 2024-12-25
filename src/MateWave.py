"""
通过参数构造不同的波浪类

"""

import raschii
from sympy import exp, cos, sin, symbols


class MateWave:
    """
    通用波浪模型类，用于构造不同的波浪模型实例。

    该类可以根据波浪模型名称（如 Airy、Fenton 或 Stokes）来生成相应的波浪实例。它提供了基本的水流速度和加速度计算方法。
    """

    def __init__(self, wave_height, water_depth, wave_length, model_order, wave_model: str) -> None:
        """
        初始化通用波浪模型。根据波浪模型名称创建波浪实例，并初始化相关参数。

        :param wave_height: 波高（单位：米）
        :param water_depth: 水深（单位：米）
        :param wave_length: 波长（单位：米）
        :param model_order: 模型阶数（例如，Stokes模型通常需要指定阶数）
        :param wave_model: 波浪模型名称（如 'Airy'、'Fenton'、'Stokes' 等）

        """
        self.wave_model = wave_model
        self.wave_height = wave_height
        self.wave_amp = self.wave_height/2

        self.wave_length = wave_length

        self.water_depth = water_depth

        self.model_order = model_order
        self.wave = self.get_custom_wave()
        self.wave_freq = self.wave.omega
        self.wave_number = self.wave.k
        self.wave_period = self.wave.T

    def get_custom_wave(self):
        """
        根据波浪模型名称创建波浪实例。

        根据传入的波浪模型名称，从 `raschii` 模块中获取相应的波浪模型，并生成一个波浪实例。

        :return: 波浪模型实例
        """
        WaveModel, _ = raschii.get_wave_model(self.wave_model)
        wave = WaveModel(self.wave_height, depth=self.water_depth,
                         length=self.wave_length, N=self.model_order)
        return wave

    def water_velocity(self, x, z, t):
        """
        计算水流速度分量。

        给定一个关于 `x` 和 `z` 的表达式，计算水流在水平方向和垂直方向的速度分量。

        :param expression_x_z: 关于 `x` 和 `z` 的表达式，通常是波浪运动的表达式。
        :return: 水流的水平和垂直速度分量（u 和 w）
        """
        # 定义函数表示水质点速度分量
        water_velocity_u = self.wave_amp * self.wave_freq * \
            exp(self.wave_number * z) * \
            cos(self.wave_number * x - self.wave_freq * t)

        water_velocity_w = self.wave_amp * self.wave_freq * \
            exp(self.wave_number * z) * \
            sin(self.wave_number * x - self.wave_freq * t)

        return water_velocity_u, water_velocity_w

    def water_acceleration(self, x, z, t):
        """
        计算水流加速度分量。

        给定一个关于 `x` 和 `z` 的表达式，计算水流在水平方向和垂直方向的加速度分量。

        :param expression_x_z: 关于 `x` 和 `z` 的表达式，通常是波浪运动的表达式。
        :return: 水流的水平和垂直加速度分量（acc_x 和 acc_z）
        """

        # 定义函数表示水质点加速度分量
        water_acc_x = self.wave_amp * self.wave_freq**2 * \
            exp(self.wave_number * z) * \
            sin(self.wave_number * x - self.wave_freq * t)
        water_acc_z = -self.wave_amp * self.wave_freq**2 * \
            exp(self.wave_number * z) * \
            cos(self.wave_number * x - self.wave_freq * t)
        return water_acc_x, water_acc_z


class AiryWave(MateWave):
    """
    Airy 波浪模型

    Airy 波浪模型是最简单的波浪模型，通常用于描述较小的波浪。它是一个线性波浪模型，适用于浅水区域。
    """

    def __init__(self, wave_height, water_depth, wave_length) -> None:
        """
        初始化 Airy 波浪模型。

        : param wave_height: 波高
        : param water_depth: 水深
        : param wave_length: 波长
        """
        super().__init__(wave_height, water_depth,
                         wave_length, model_order=1, wave_model='Airy')


class FentonWave(MateWave):
    """
    Fenton 波浪模型

    Fenton 波浪模型是一种用于描述较大波浪的近似模型，可以考虑波浪的非线性效应。
    """

    def __init__(self, wave_height, water_depth, wave_length, model_order) -> None:
        """
        初始化 Fenton 波浪模型。

        : param wave_height: 波高
        : param water_depth: 水深
        : param wave_length: 波长
        : param model_order: 模型阶数
        """
        super().__init__(wave_height, water_depth,
                         wave_length, model_order, wave_model='Fenton')


class StokesWave(MateWave):
    """
    Stokes 波浪模型

    Stokes 波浪模型用于描述波浪的非线性行为，适用于较大的波浪，具有多个阶数的近似。
    """

    def __init__(self, wave_height, water_depth, wave_length, model_order) -> None:
        """
        初始化 Stokes 波浪模型。

        : param wave_height: 波高
        : param water_depth: 水深
        : param wave_length: 波长
        : param model_order: 模型阶数
        """
        super().__init__(wave_height, water_depth,
                         wave_length, model_order, wave_model='Stokes')
