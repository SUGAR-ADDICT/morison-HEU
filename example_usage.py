"""
波浪参数:
- 波高:4 m
- 波长:100 m
- 水深:60 m
杆件参数：
- 直径:5 m
- 起始点: (0,0,0)
- 终止点: (0,0,-10)
Morison参数:
- 拖曳力系数: 1.0
- 惯性力系数: 2.0
Force_cal参数:
- 水密度: 1000

"""

from src.equation import maximum_force
from src.force_calculate import ForceCal
from src.Morison import Morsion
from src.MateWave import *
from src.Cylinder import Cylinder


# 初始化波浪类，这里选用流函数波浪理论
wave_height = 4
wave_length = 100
water_depth = 10
order = 5  # 流函数阶数
my_wave = FentonWave(wave_height, water_depth, wave_length, order)

# 初始化Cylinder类
my_cylinder = Cylinder(10, (0, 0, 0), (0, 0, -10))

# 初始化Morsion类
my_morison = Morsion(1.0, 2.0)

# 创建一个荷载计算实例, 是计算的核心代码，通过其中的方法可以返回荷载的numpy表达式
force_cal = ForceCal(my_cylinder, my_wave, my_morison, rho=1000)

force_eq = force_cal.cal_force_x()  # 计算水平波浪荷载的方法

# 在一个波浪周期内寻找荷载的最大值

bounds = [(0, my_wave.wave_period)]  # 定义搜索范围

max_force, _ = maximum_force(force_eq, bounds)  # 这样就得到了荷载的最大值

# 还可以对公式进行可视化
