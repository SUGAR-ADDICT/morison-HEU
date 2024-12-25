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
3. 依次运行
```
py pre_mesh.py config.YAML
```
预处理网格文件
```
py morison_solver.py config.YAML
```
开始计算

```
py postProc.py
```
对计算结果进行后处理，找出每一个算例中的最大值