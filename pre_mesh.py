
import re
import sys
import yaml


def parse_yaml_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)  # 使用 safe_load 来加载文件
    return config


def main(config_file):
    output_mesh_file = "Mesh.cy"
    config = parse_yaml_config('config.yaml')

    WATER_DEPTH = config['wave']['WATER_DEPTH']

    GEO_FILE = config['geo']['GEO_FILE']

    # 节点和截面信息存储
    nodes = []  # 存储节点信息: [(id, x, y, z), ...]
    pbarl = {}
    # 存储截面信息: [(x_start, y_start, z_start, x_end, y_end, z_end), ...]
    sections = []

    # 读取几何文件并提取信息
    with open(GEO_FILE, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        line = line.strip()

        # 提取节点 (GRID 数据)
        if line.startswith("GRID"):
            parts = re.split(r"\s+", line)
            node_id = int(parts[1])
            x, y, z = float(parts[2]), float(parts[3]), float(parts[4])
            nodes.append((node_id, x, y, z))

        # 提取杆单元 (CBAR 数据)
        elif line.startswith("CBAR"):
            parts = re.split(r"\s+", line)
            cbar_prop_id = int(parts[2])
            node_id_start = int(parts[3])
            node_id_end = int(parts[4])

            # 查找节点坐标
            start_coords = next((x, y, z) for n_id, x, y,
                                z in nodes if n_id == node_id_start)
            end_coords = next((x, y, z)
                              for n_id, x, y, z in nodes if n_id == node_id_end)

            sections.append((*start_coords, *end_coords, cbar_prop_id))
        # 提取PBARL数据
        elif line.startswith("PBARL"):  # 找到以 PBARL 开头的行
            parts = re.split(r"\s+", line)
            pbarl_id = int(parts[1])

            next_line = lines[i + 1]  # 获取下一行
            parts = re.split(r"\s+", next_line)
            pbarl_radius = parts[1]

            pbarl[rf'{pbarl_id}'] = pbarl_radius  # 把属性id和截面半径存入字典

    # 写入输出文件
    with open(output_mesh_file, "w") as f:
        # 写入截面信息
        f.write("# START(x,y,z) END(x,y,z) DIAMETER\n")
        for section in sections:
            diameter = float(pbarl[f'{section[6]}'])*2
            f.write(f"{section[0]} {section[1]} {
                    section[2]+WATER_DEPTH} {section[3]} {section[4]} {section[5]+WATER_DEPTH} {diameter}\n")

    print(f"Mesh 文件已生成: {output_mesh_file}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法: python script.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    main(config_file)
