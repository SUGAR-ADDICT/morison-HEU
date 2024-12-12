import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from src.Cylinder import Cylinder
from src.force_calculate import ForceCal
from src.Morison import Morsion
import raschii
import yaml
os.environ['TCL_LIBRARY'] = r'D:/Application/Python3.13.0/tcl/tcl8.6'


def parse_yaml_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)  # 使用 safe_load 来加载文件
    return config


def read_mesh(file_path, resolution):
    """Read the Mesh.cy file and create Cylinder objects."""
    cylinders = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            if line.startswith('#') or not line:  # Skip comments and empty lines
                continue
            elif line.strip():  # Skip empty lines
                start_x, start_y, start_z, end_x, end_y, end_z, diameter = map(
                    float, line.split())
                start = (start_x, start_y, start_z)
                end = (end_x, end_y, end_z)
                # Create Cylinder objects
                cylinders.append(Cylinder(diameter, start, end, resolution))
    return cylinders


def main(config_file_path, geo_file_path):
    config = parse_yaml_config('config.yaml')

    C_D = config['env']['C_D']
    C_M = config['env']['C_M']
    RHO = config['env']['RHO']

    WAVE_MODEL = config['wave']['WAVE_MODEL']
    WAVE_LENGTH = config['wave']['WAVE_LENGTH']
    WAVE_HEIGHT = config['wave']['WAVE_HEIGHT']
    WATER_DEPTH = config['wave']['WATER_DEPTH']

    MESH_RESOLUTION = config['solver']['MESH_RESOLUTION']
    TIME_RESOLUTION = config['solver']['TIME_RESOLUTION']

    print(f"Wave Model: {WAVE_MODEL}")
    print(f"Wave Length: {WAVE_LENGTH} m")
    print(f"Wave Height: {WAVE_HEIGHT} m")
    print(f"Water Depth: {WATER_DEPTH} m")

    # Initialize wave model
    wave_model, _ = raschii.get_wave_model(WAVE_MODEL)
    my_wave = wave_model(WAVE_HEIGHT, WATER_DEPTH, WAVE_LENGTH)
    period = my_wave.T
    t_lst = np.linspace(0, period, TIME_RESOLUTION)

    # Initialize Morison class
    my_morison = Morsion(C_D, C_M)

    # Read Mesh.cy file and create Cylinder objects
    cylinders = read_mesh(geo_file_path, MESH_RESOLUTION)

    val_lst = []
    # Loop through time points and calculate forces
    for t in t_lst:
        total_force = 0
        for my_cylinder in cylinders:
            my_force_cal = ForceCal(my_cylinder, my_wave, my_morison, RHO, t)
            force = my_force_cal.cal_force_x()
            total_force += force  # Accumulate the total force for all cylinders
        val_lst.append(total_force)

    # Plot the results
    # TODO 将结果写入文件
    plt.plot(t_lst, val_lst)
    plt.xlabel("Time (s)")
    plt.ylabel("Total Force (N)")
    plt.title("Total Force on Cylinders Over Time")
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法: python script.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    main(config_file, "Mesh.cy")
