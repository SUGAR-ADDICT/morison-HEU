import yaml
from numpy import linspace

def frange(start, end, step):
    while start <= end:
        yield round(start, 8)  # 避免浮点数累积误差
        start += step


def parse_yaml_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)  # 使用 safe_load 来加载文件

    # 处理配置中的 start, end, step 为列表的逻辑
    for key in config['wave']:
        if isinstance(config['wave'][key], dict) and 'start' in config['wave'][key]:
            start = config['wave'][key]['start']
            end = config['wave'][key]['end']
            n = config['wave'][key].get('n', 1)  # 默认为1
            config['wave'][key] =  linspace(start,end,n)
    return config
