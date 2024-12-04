"""
算法扩展
"""
from scipy.optimize import differential_evolution


def maximum_force(objective_function, bounds):

    # 使用 differential_evolution 函数寻找函数的最大值
    result = differential_evolution(objective_function, bounds)

    # 打印结果
    if result.success:
        max_value = -result.fun  # 最大值为目标函数的负值
        max_time = result.x[0]
        print(rf"F_x = {max_value:.2f} N, in {max_time:.2f} s")
        return max_value, max_time
    else:
        print("Optimization failed:", result.message)
