import numpy as np
import matplotlib.pyplot as plt
import os
import re
import argparse  # 导入 argparse 模块

os.environ["TCL_LIBRARY"] = r"D:/Application/Python3.13.0/tcl/tcl8.6"


# 使用 argparse 获取命令行参数
parser = argparse.ArgumentParser(
    description="Plot forces over time from a specified data file."
)
parser.add_argument("fpath", type=str, help="Path to the data file (e.g., results.txt)")
args = parser.parse_args()  # 解析命令行参数

file_path = args.fpath  # 获取文件路径file_path = "results.txt"

legend_lst = []
with open(file_path, "r") as f:
    first_line = f.readline().strip()  # 读取文件的第一行并去掉两端的空白字符
    case_name_lst = re.split(r"\s+", first_line)
    case_name_lst.pop(0)  # 删掉开头的#case name 关键字


data = np.loadtxt(file_path, comments="#")
time = data[:, 0]
plt.figure(figsize=(10, 6))

for i, case_name in enumerate(case_name_lst):
    force = data[:, i + 1]
    plt.plot(time, force)


# 设置图表标题和标签
plt.title("Forces Over Time")
plt.xlabel("Time (s)")
plt.ylabel("Force (N)")
plt.legend(case_name_lst)
plt.show()
