# 环境
我本地环境 Python 3.10.6

# 安装
```shell
pip install -r requirements.txt
```

# 运行
```shell
python main.py
```

# 打包
```shell
pyinstaller -n Yupoo-detect --onefile main.py
```

# 用途
检测Yupoo相册是否存在侵权内容的小工具，并将检测结果保存到CSV文件中。