import numpy as np
import re

file_path = rf"morison\force_temporal.txt"  # 输入文件路径
output_path = rf"morison\result.txt"  # 输出文件路径

# 读取数据文件
with open(file_path, "r") as f:
    # 读取文件的第一行，去掉两端空白字符
    first_line = f.readline().strip()
    # 获取 Case Name 列表（第二列到最后一列）
    case_name_lst = re.split(r"\s+", first_line)[1:]

# 读取数据（跳过注释行）
data = np.loadtxt(file_path, comments="#")

# 获取时间列和力值数据
time = data[:, 0]  # 第一列是时间
forces = data[:, 1:]  # 第二列到最后是各个力值数据


# 提取波长、波高、水深和波周期信息
def extract_wave_parameters(case_name):
    match = re.match(r"L([\d\.]+)H([\d\.]+)D([\d\.]+)T([\d\.]+)", case_name)
    if match:
        wave_length = float(match.group(1))
        wave_height = float(match.group(2))
        water_depth = float(match.group(3))
        wave_period = float(match.group(4))
        return wave_period,wave_length, wave_height, water_depth 
    return None, None, None, None  # 如果没有匹配到格式，返回 None


# 找到每列的最大值
max_forces = np.max(forces, axis=0)  # 每列的最大值

# 打开结果文件进行写入
with open(output_path, "w") as out_f:
    # 写入文件头部
    out_f.write(
        "# wave_period(s) wave_length(m) wave_height(m) water_depth(m) force(N)\n"
    )

    # 遍历每个 case_name 和对应的最大值，写入文件
    for case_name, max_force in zip(case_name_lst, max_forces):
        wave_length, wave_height, water_depth, wave_period = extract_wave_parameters(
            case_name
        )
        if wave_length is not None:
            out_f.write(
                f"{wave_length:.3f} {wave_height:.3f} {water_depth:.3f} {wave_period:.3f} {max_force:.3f}\n"
            )

print(f"Results have been written to {output_path}")
