# 准备工作
首先创建虚拟环境，然后将工程从github上克隆下来，
安装必要的依赖。
```
pip install -r requirement.txt
```

然后克隆[raschii_modidy](https://github.com/SUGAR-ADDICT/raschii_modidy)到任意位置，复制所有内容覆盖虚拟环境文件夹下的`\Lib\site-packages\raschii`中的所有文件

# 使用方法
1. 将bdf文件放入根目录
2. 在config.YAML内设置计算参数
3. 将bdf文件处理成.cy后缀的计算文件
```
py pre_mesh.py config.YAML
```
4. 根据设置求解
```
py solver.py config.YAML
```
5. 对计算结果进行后处理，找出每一个算例中的最大值
```
py postProc.py
```

# config.YAML 模板
```
# 环境设置
env:
  C_D: 1.0
  C_M: 2.0
  RHO: 1000

# 几何设置
geo:
  GEO_FILE: "d90_scale.bdf"

# 波浪设置
wave:
  WAVE_MODEL: "Fenton" #The available wave models {"Airy": AiryWave, "Fenton": FentonWave, "Stokes": StokesWave}
  WAVE_ORDER: 5
  WAVE_LENGTH:
    start: 0.852
    end: 5.852
    step: 1.1
  WAVE_HEIGHT:
    start: 0.08
    end: 0.08
    step: 1
  WATER_DEPTH:
    start: 1.2
    end: 1.2
    step: 1

# 求解设置
solver:
  MESH_RESOLUTION: 50
  TIME_RESOLUTION: 20
```
