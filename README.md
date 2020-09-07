- 本人github的项目可能目前主要分为两大类，🐸Frog系列为自动化扫描方向，🐶Doge系列为免杀及内网渗透方向

- 本系列命名为Frog可能是因为这种生物的寿命长 🐸 🤓 +1s 

- Frog-Submon为Frog系列第一个项目🐸

# 🐸Frog-Submon
```
2020/9/7更新：修复部分bug，
支持json格式输入，
加入http请求。
```
json格式仅支持[public-bugbounty-programs](https://github.com/projectdiscovery/public-bugbounty-programs)对应格式

Frog-Submon子域名监控脚本，采用python3实现，使用subprocess加载三款golang子域名发现工具：

- [ksubdomain](https://github.com/knownsec/ksubdomain) 为知道创宇404团队开源的无状态子域名爆破工具
- [subfinder](https://github.com/projectdiscovery/subfinder) 子域名发现工具
- [xray](https://xray.cool/) 高级版的子域名发现功能(可选项)

以及一款http请求工具：

- [httpx](https://github.com/projectdiscovery/httpx) fast and multi-purpose HTTP toolkit

xray和subfinder主要进行api相关的子域名发现，ksubdomain则进行大字典的爆破，

在爆破后使用httpx对更新的子域名进行请求，并获取相关返回值。

返回的子域名数据存储在output文件夹内，对于更新的子域名进行请求的数据存储在http-output文件夹内

为了扫描速度考虑采用内置字典

```
- ksundomain爆破对网络影响较大。

- 使用前请确定ksubdomain对应的网卡序号。
```

在一轮扫描结束后进行三个工具结果的合并去重、子域名更新统计、http(s)请求、微信Server酱提示、临时文件删除，并睡眠等待下次扫描

默认睡眠时间为50000s，可自行修改

# 常用命令
```
python3 submon.py linux
```
```
python3 submon.py win 
```
```
python3 submon.py linux -json test.json
```
```
python3 submon.py win -json test.json
```

# Usage
若无高级版xray则可以使用submon_noxray.py, 仅调用三个工具
```
下载并更新[ksubdomain](https://github.com/knownsec/ksubdomain/releases/) 二进制文件。(默认无需更新)

下载并更新[subfinder] (https://github.com/projectdiscovery/subfinder/releases) 二进制文件。(默认无需更新)

下载并更新[xray](https://github.com/chaitin/xray/releases) 二进制文件。放置于xray文件夹内命名为xray_win.exe与xray_linux

下载并更新[httpx](https://github.com/projectdiscovery/httpx/releases) 二进制文件。(默认无需更新)
```
在xray文件夹内放入xray-license.lic

若在linux下使用，请给对应的二进制文件执行权限

在linux下，还需要安装`libpcap-dev`,在Windows下需要安装`WinPcap`，mac下可以直接使用。

采用两种输入模式，json输入或txt输入，默认domain.txt输入

json格式仅支持[public-bugbounty-programs](https://github.com/projectdiscovery/public-bugbounty-programs)对应格式

txt输入模式下，domain.txt内填上需要扫描的域名，一行一个。py脚本内url1填写Server酱api

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


Usage:-------------------------------------------
-----                                      ------
-----       python3 submon.py -h           ------
-----                                      ------
-------------------------------------------------
usage: submon.py [-h] [-json JSON] os

positional arguments:
  os          win/linux

optional arguments:
  -h, --help  show this help message and exit
  -json JSON  json file name
```
具体subprocess调用的参数可在脚本内进行修改。

# 运行截图
### 运行

![image1](https://raw.githubusercontent.com/timwhitez/Frog-Submon/master/images/frogsubmon.jpg)

### 生成的更新文本

![image2](https://raw.githubusercontent.com/timwhitez/Frog-Submon/master/images/frogsubmon2.jpg)

### Server酱提醒

![image3](https://raw.githubusercontent.com/timwhitez/Frog-Submon/master/images/frogsubmon3.png)

# todo list
- [x] ~~按域名分类存储~~
- [x] ~~对更新域名进行请求~~
- [x] ~~解析json格式domain输入文件~~
- [ ] 加入扫描进度临时文件，重启扫描器读取进度文件
