# telegram_chat_bot
关键词匹配 自建回复模板的一个telegram 客服机器人，可本地，可vps搭建，有自己的数据库，可网页查看用户咨询信息。
#机器人工作逻辑
我要再telegram上搭建一个智能机器人  当作客服  工作逻辑大致这样  你是一个 Telegram 客服助手，能够根据用户的回复内容来判断其意图。请遵循以下指示进行响应：

1. **判断用户意图**：
   - 如果用户的消息包含以下关键词，则认为用户有合作推广的意图：
     - 视频合作、视频制作、制作一期视频、广告、商务、付费推广、推荐、机场推广、合作、机场合作、vpn推广、商务推广
   - 如果用户的消息包含以下关键词，则认为用户寻求帮助或询问代码问题：
     - 帮助、问题、教程、群、求救、远程、协助、求助、工具、帮忙、工具，请教、如何操作、设置、博客

2. **根据用户的意图提供相应的回复**：
   - **若判定为合作推广**，请回复以下内容（完全不删减）：
     
推广合作：

     **1、视频制作推广：
     **您可以通过回复“个人电报”来获取我的个人电报。**


   - **若判定为寻求帮助**，请回复以下内容（完全不删减）：
     
我的群组：

     您要的工具都在博客中，您可以访问 www.jdssl.top ,里面可以找到对应的文章内容，如果遇到问题可以进群请教其他朋友帮助：https://t.me/+qoHg0sYhHgkxM2Vl


3. **在用户回复“个人电报”时**：
   - **若用户之前被判定为合作推广**，则回复以下内容（完全不删减）：
     
个人电报：

     您好， 我的电报：https://t.me/ssrr_xxxx

   - **若用户之前被判定为寻求帮助**，则不回复个人电报模板的内容。

4. **注意事项**：
   - 只有在用户被判定为合作推广并回复“个人电报”时，才发送个人电报模板的内容。
   - 在其他情况下，不发送个人电报的内容。  我该如何实现
  

### 总体流程

1. **系统准备：更新和安装基础依赖**
2. **创建项目目录并配置Python环境**
3. **上传或克隆项目代码**
4. **安装Python依赖**
5. **配置并启动Supervisor管理服务**
6. **配置网络访问**
7. **验证部署**

### 一、系统准备

### 1. 更新系统和安装依赖

确保系统包是最新的：

```bash

sudo apt update && sudo apt upgrade -y

```

安装Python 3、`git`等工具：

```bash

sudo apt install -y python3 python3-venv git

```

> 注意: 若系统默认未安装Python 3，请确认安装，否则可能导致后续Python命令无法执行。
> 

### 二、创建项目目录并配置Python环境

### 1. 创建项目目录

在`root`或`home`目录中创建项目目录：

```bash

mkdir ~/project && cd ~/project

```

### 2. 创建Python虚拟环境

为了确保项目依赖环境的独立性，创建并激活虚拟环境：

```bash
python3 -m venv venv
source venv/bin/activate

```

> 注意: 每次重新连接服务器时，执行项目中的Python脚本前都需要重新激活虚拟环境，使用source venv/bin/activate。
> 

### 三、上传或克隆项目代码

若项目代码托管在GitHub上，可使用`git clone`命令：

```bash
git clone https://github.com/yourusername/your-repo.git .

```

> 注意: .号表示将文件直接下载到当前文件夹。如果是上传本地代码，请将app.py、bot.py、requirements.txt、supervisord.conf等文件传入project目录中。
> 

### 四、安装Python依赖

### 1. 准备`requirements.txt`文件

确保项目目录中有一个`requirements.txt`，文件内容如下：

```
Flask
pytz
python-telegram-bot
supervisor

```

### 2. 安装依赖

运行以下命令安装依赖库：

```bash
bash
复制代码
pip install -r requirements.txt

```

> 
> - **"externally-managed-environment" 错误**: 如果出现此问题，请确保虚拟环境已激活(`source venv/bin/activate`)。
> - **找不到模块错误**: 确保`requirements.txt`文件存在，并且内容完整。

### 五、配置Supervisor管理服务

Supervisor将帮助我们在后台管理和自动重启`app.py`和`bot.py`。

### 1. 创建并配置`supervisord.conf`

在项目根目录中创建一个名为`supervisord.conf`的文件，内容如下：

```
ini
复制代码
[supervisord]
nodaemon=true

[program:app]
command=/root/project/venv/bin/python /root/project/app.py
autostart=true
autorestart=true
stdout_logfile=/dev/stdout
stderr_logfile=/dev/stderr

[program:bot]
command=/root/project/venv/bin/python /root/project/bot.py
autostart=true
autorestart=true
stdout_logfile=/dev/stdout
stderr_logfile=/dev/stderr

```

> 说明:
> 
> - `command` 路径确保指向虚拟环境内的Python解释器。
> - `nodaemon=true` 让Supervisor运行在前台，方便查看运行状态。
> - `autostart` 和 `autorestart` 确保脚本自动启动及在失败后重启。

### 2. 启动Supervisor

进入`project`目录并启动Supervisor：

```bash

supervisord -c ~/project/supervisord.conf

```

查看Supervisor是否启动成功：

```bash

ps aux | grep supervisord

```

> 注意: 若未看到supervisord进程，请检查配置路径是否正确，或者使用绝对路径。
> 

### 3. 检查Supervisor日志

Supervisor会将日志存放在默认路径中，可以查看日志以了解错误原因：

```bash

tail -f /var/log/supervisor/supervisord.log

```

### 六、配置网络访问

### 1. 确保Flask监听所有接口

在`app.py`的最后一行，确保Flask监听所有接口：

```python

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

```

### 2. 开放防火墙端口

开放VPS端口5001以允许外部访问：

```bash

sudo ufw allow 5001

```

> 注意: 确保服务器提供商（如阿里云、AWS）的控制面板中也开放了该端口。
> 

### 七、验证部署

1. **查看服务状态**
确保Supervisor正在运行`app.py`和`bot.py`。可使用以下命令检查：
    
    ```bash
  
    supervisorctl status
    
    ```
    
2. **访问应用**
使用浏览器访问`http://VPS_IP:5001`，应看到应用的页面。如果无法访问，请检查以下项：
    - Flask监听的接口和端口是否正确。
    - VPS防火墙端口是否开放。


### 1. 启动应用

确保进入项目目录，激活虚拟环境后启动Supervisor来运行`app.py`和`bot.py`。

```bash

# 进入项目目录
cd ~/project

# 启动 Supervisor 服务
supervisord -c ~/project/supervisord.conf

```

**运行后验证**：
您可以通过以下命令查看Supervisor是否启动成功：

```bash

ps aux | grep supervisord

```

**查看运行状态**：
查看应用是否正常运行以及日志输出。

```bash

tail -f /var/log/supervisor/supervisord.log

```

---

### 2. 重启应用

若需要重启应用，例如在更新代码或配置后，可以通过以下命令重启Supervisor管理的进程：

```bash

# 使用 supervisorctl 重新启动所有进程
supervisorctl reload

# 或者单独重启 app.py 和 bot.py 进程
supervisorctl restart app
supervisorctl restart bot

```

> 说明: supervisorctl reload 将重启所有配置的进程。使用 restart app 和 restart bot 可分别单独重启。
> 

---

### 3. 关闭应用

要停止Supervisor管理的所有进程，可使用以下命令：

```bash

# 停止所有Supervisor进程
supervisorctl stop all

# 若要彻底关闭Supervisor服务
pkill supervisord

```

> 提示: pkill supervisord 将完全关闭Supervisor服务，确保没有其他与Supervisor相关的进程在运行。
> 

---

### 常见问题及解决

1. **端口占用**：如果遇到端口被占用，可以用以下命令查找并结束相关进程。
    
    ```bash
   
    lsof -i :5001
    kill -9 <PID>
    
    ```
    
2. **检查服务状态**：如遇到启动或重启失败，可以使用以下命令检查各个进程的状态：
    
    ```bash
  
    supervisorctl status
    
    ```
    

---

### 4. 测试应用

在应用正常启动后，可以通过浏览器访问应用页面来测试：

```

http://<VPS_IP>:5001

```

---

这些命令涵盖了应用的运行、重启、停止以及常见问题的排查，可以帮助确保您的应用在Debian VPS上顺利运行。



执行 `supervisord -c /path/to/project/supervisord.conf` 命令后，即使关闭VPS窗口，Supervisor仍会继续运行并管理您的 `app.py` 和 `bot.py` 进程。

### 验证后台运行

可以用以下命令查看 `supervisord` 是否在后台运行：

```bash

ps aux | grep supervisord

```

### 如果需要在后台关闭或重启 Supervisor 进程

- **重启所有进程**：`supervisorctl reload`
- **停止所有进程**：`supervisorctl stop all`
- **彻底关闭Supervisor服务**：`pkill supervisord`

这样Supervisor将继续在后台监控并确保 `app.py` 和 `bot.py` 正常运行，即使关闭VPS窗口，服务依然保持在线。
