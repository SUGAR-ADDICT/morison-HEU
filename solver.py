import os
import sys
import time
import raschii
import numpy as np
from src.Cylinder import Cylinder
from src.force_calculate import ForceCal
from src.Morison import Morsion
from src.parse_config import parse_yaml_config


# 定义一个修饰器来计算和打印运行时间
def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"Execution time is {elapsed_time:.2f} seconds.")
        return result

    return wrapper


def read_mesh(file_path, resolution):
    """Read the Mesh.cy file and create Cylinder objects."""
    cylinders = []
    with open(file_path, "r") as f:
        for line in f.readlines():
            if line.startswith("#") or not line:  # Skip comments and empty lines
                continue
            elif line.strip():  # Skip empty lines
                start_x, start_y, start_z, end_x, end_y, end_z, diameter = map(
                    float, line.split()
                )
                start = (start_x, start_y, start_z)
                end = (end_x, end_y, end_z)
                # Create Cylinder objects
                cylinders.append(Cylinder(diameter, start, end, resolution))
    return cylinders


@time_it
def main(config_file_path):
    config = parse_yaml_config("config.yaml")

    C_D = config["env"]["C_D"]
    C_M = config["env"]["C_M"]
    RHO = config["env"]["RHO"]

    GEO_FILE = config["geo"]["GEO_FILE"]
    base_name = GEO_FILE.split(".")[0]  # 使用 '.' 分割，取第一个部分

    WAVE_MODEL = config["wave"]["WAVE_MODEL"]
    WAVE_ORDER = config["wave"]["WAVE_ORDER"]
    WAVE_LENGTH_lst = config["wave"]["WAVE_LENGTH"]
    WAVE_HEIGHT_lst = config["wave"]["WAVE_HEIGHT"]
    WATER_DEPTH_lst = config["wave"]["WATER_DEPTH"]

    wave_case_lst = [
        (wave_length, wave_height, wave_depth)
        for wave_length in WAVE_LENGTH_lst
        for wave_height in WAVE_HEIGHT_lst
        for wave_depth in WATER_DEPTH_lst
    ]

    MESH_RESOLUTION = config["solver"]["MESH_RESOLUTION"]
    TIME_RESOLUTION = config["solver"]["TIME_RESOLUTION"]

    # Initialize wave model
    temp_value_lst = []
    case_name_lst = []
    for i, wave_case in enumerate(wave_case_lst):

        print(f"Progress: {i}/{len(wave_case_lst)}", end="\r")  # 打印计算进度

        wave_length = wave_case[0]
        wave_height = wave_case[1]
        water_depth = wave_case[2]

        wave_model, _ = raschii.get_wave_model(WAVE_MODEL)
        # Airy 模型不需要指定阶数，其他模型需要
        if WAVE_MODEL == "Airy":
            my_wave = wave_model(wave_height, water_depth, wave_length)
        else:
            my_wave = wave_model(wave_height, water_depth, wave_length, WAVE_ORDER)

        period = my_wave.T
        t_lst = np.linspace(0, period, TIME_RESOLUTION)

        case_name = rf"L{wave_length}H{wave_height}D{water_depth}T{period:.4f}"
        case_name_lst.append(case_name)

        # Initialize Morison class
        my_morison = Morsion(C_D, C_M)

        # Read Mesh.cy file and create Cylinder objects
        geo_file_path = rf"{base_name}D{water_depth}.cy"

        cylinders = read_mesh(geo_file_path, MESH_RESOLUTION)

        val_lst = []
        for t in t_lst:
            total_force = 0
            for my_cylinder in cylinders:
                my_force_cal = ForceCal(my_cylinder, my_wave, my_morison, RHO, t)
                force = my_force_cal.cal_force_x()
                total_force += force  # Accumulate the total force for all cylinders
            val_lst.append(total_force)
        normal_t_lst = t_lst  # 不直接写入
        temp_value_lst.append(val_lst)

    # 打开文件进行写入
    folder_path = "morison"
    file_path = os.path.join(folder_path, "force_temporal.txt")

    # 如果文件夹不存在，则创建文件夹
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with open(file_path, "w") as f:
        # 写入列标题
        f.write(
            "#Casename\t"
            + "\t".join([f"{case_name}" for case_name in case_name_lst])
            + "\n"
        )
        f.write(
            "#Time(s)\t"
            + "\t".join([f"Force_{i+1}(N)" for i in range(len(temp_value_lst))])
            + "\n"
        )

        # 写入每一对 (t, val_lst) 数据
        for i, t in enumerate(normal_t_lst):
            # 将时间点 t 和对应的 force 值逐列写入文件
            f.write(
                f"{t:.5f}\t"
                + "\t".join([f"{force[i]:.5f}" for force in temp_value_lst])
                + "\n"
            )

    print(f"Data written to {file_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法: python script.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    main(config_file)
