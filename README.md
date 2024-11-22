# Auto_St0ck_Tools

## env

python==3.12.7

### 安装 Anaconda

```Anaconda Debian
apt-get install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6
```

```Anaconda RedHat
yum install libXcomposite libXcursor libXi libXtst libXrandr alsa-lib mesa-libEGL libXdamage mesa-libGL libXScrnSaver
```

```Download the latest version of Anaconda Distribution
curl -O https://repo.anaconda.com/archive/Anaconda3-2024.10-1-Linux-x86_64.sh
```

```Install Anaconda Distribution
bash ~/Anaconda3-2024.10-1-Linux-x86_64.sh
```

```refresh the terminal
source ~/.bashrc
```

conda 命令

```conda
conda -V
```

```conda
conda env list
```

```conda
conda create -n 环境名
```

```conda
conda activate 环境名
```

Anaconda官方文档: [https://docs.anaconda.com/anaconda/install/](https://docs.anaconda.com/anaconda/install/ "点击跳转")

### 数据处理库 pandas

pandas==2.2.2

#### 安装 pandas

```pandas
conda install pandas
```

### 开源财经接口 [akshare](https://github.com/akfamily/akshare "GitHub地址")

#### akshare 国内安装-Anaconda

```akshare
pip install akshare --upgrade --user -i https://pypi.tuna.tsinghua.edu.cn/simple
```

akshare官方文档: [https://akshare.akfamily.xyz/installation.html](https://akshare.akfamily.xyz/installation.html "点击跳转")
