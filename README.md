- 本人github的项目可能目前主要分为两大类，Frog系列为自动化扫描方向，Doge系列为免杀及内网渗透方向

- Frog-Submon为Frog系列第一个项目

# Frog-Submon
Frog-Submon子域名监控脚本，采用python3实现，使用subprocess加载三款golang子域名发现工具：

- [ksubdomain](https://github.com/knownsec/ksubdomain) 为知道创宇404团队开源的无状态子域名爆破工具
- [subfinder](https://github.com/projectdiscovery/subfinder) 子域名发现工具
- [xray](https://xray.cool/) 高级版的子域名发现功能(可选项)

xray和subfinder主要进行api相关的子域名发现，ksubdomain则进行大字典的爆破

```
- ksundomain爆破对网络影响较大。
```

在一轮扫描结束后进行三个工具结果的合并去重、子域名更新统计、微信Server酱提示、临时文件删除，并睡眠等待下次扫描

# Usage
若无高级版xray则可以使用submon_noxray.py, 仅调用两个工具
```
下载并更新[ksubdomain](https://github.com/knownsec/ksubdomain/releases/) 二进制文件。

下载并更新[subfinder] (https://github.com/projectdiscovery/subfinder/releases) 二进制文件。

下载并更新[xray](https://github.com/chaitin/xray/releases) 二进制文件。
```
在xray文件夹内放入xray-license.lic

若在linux下使用，请给对应的三个二进制文件执行权限

在linux下，还需要安装`libpcap-dev`,在Windows下需要安装`WinPcap`，mac下可以直接使用。

domain.txt内填上需要扫描的域名，一行一个。脚本内url1填写Server酱api

```
python3 submon.py
               ⣿⣿⣿⣿⣿⣿⢟⣡⣴⣶⣶⣦⣌⡛⠟⣋⣩⣬⣭⣭⡛⢿⣿⣿⣿⣿
               ⣿⣿⣿⣿⠋⢰⣿⣿⠿⣛⣛⣙⣛⠻⢆⢻⣿⠿⠿⠿⣿⡄⠻⣿⣿⣿
               ⣿⣿⣿⠃⢠⣿⣿⣶⣿⣿⡿⠿⢟⣛⣒⠐⠲⣶⡶⠿⠶⠶⠦⠄⠙⢿
               ⣿⠋⣠⠄⣿⣿⣿⠟⡛⢅⣠⡵⡐⠲⣶⣶⣥⡠⣤⣵⠆⠄⠰⣦⣤⡀
               ⠇⣰⣿⣼⣿⣿⣧⣤⡸⢿⣿⡀⠂⠁⣸⣿⣿⣿⣿⣇⠄⠈⢀⣿⣿⠿
               ⣰⣿⣿⣿⣿⣿⣿⣿⣷⣤⣈⣙⠶⢾⠭⢉⣁⣴⢯⣭⣵⣶⠾⠓⢀⣴
               ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣉⣤⣴⣾⣿⣿⣦⣄⣤⣤⣄⠄⢿⣿
               ⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠈⢿
               ⣿⣿⣿⣿⣿⣿⡟⣰⣞⣛⡒⢒⠤⠦⢬⣉⣉⣉⣉⣉⣉⣉⡥⠴⠂⢸
               ⠻⣿⣿⣿⣿⣏⠻⢌⣉⣉⣩⣉⡛⣛⠒⠶⠶⠶⠶⠶⠶⠶⠶⠂⣸⣿
               ⣥⣈⠙⡻⠿⠿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⠿⠛⢉⣠⣶⣶⣿⣿
         _          _           _            _
        /\ \       /\ \        /\ \         /\ \
       /  \ \     /  \ \      /  \ \       /  \ \
      / /\ \ \   / /\ \ \    / /\ \ \     / /\ \_\
     / / /\ \_\ / / /\ \_\  / / /\ \ \   / / /\/_/
    / /_/_ \/_// / /_/ / / / / /  \ \_\ / / / ______
   / /____/\  / / /__\/ / / / /   / / // / / /\_____\
  / /\____\/ / / /_____/ / / /   / / // / /  \/____ /
 / / /      / / /\ \ \  / / /___/ / // / /_____/ / /
/ / /      / / /  \ \ \/ / /____\/ // / /______\/ /
\/_/       \/_/    \_\/\/_________/ \/___________/


Usage:---------------------------------------
-----                                  ------
-----       submon.py linux            ------
-----        submon.py win             ------
-----                                  ------
---------------------------------------------
```
具体调用的参数也可在脚本内进行修改。

# 运行截图
### 运行

![image1](https://raw.githubusercontent.com/timwhitez/Frog-Submon/master/images/frogsubmon.jpg)

### 生成的更新文本

![image2](https://raw.githubusercontent.com/timwhitez/Frog-Submon/master/images/frogsubmon2.jpg)

### Server酱提醒

![image3](https://raw.githubusercontent.com/timwhitez/Frog-Submon/master/images/frogsubmon3.png)
