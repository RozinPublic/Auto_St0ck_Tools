# Auto_St0ck_Tools

To ensure app dependencies are ported from your virtual environment/host machine into your container, run 'pip freeze > requirements.txt' in the terminal to overwrite this file

## env

python==3.12.3

conda==24.1.2

### 数据处理库 pandas

pandas==2.2.1

#### pandas安装

```pandas
conda install pandas
```

### 开源财经接口 akshare

[akshare安装指导]('https://akshare.akfamily.xyz/installation.html')

[github地址]('https://github.com/akfamily/akshare')

#### akshare 国内安装-Anaconda

```akshare
pip install akshare --upgrade --user -i https://pypi.tuna.tsinghua.edu.cn/simple
```
