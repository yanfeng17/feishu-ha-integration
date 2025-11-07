# Feishu Gateway 集成安装指南

## 快速安装

### 步骤 1：找到您的 HA 配置目录

**常见位置：**
- Docker: `/config/`
- Home Assistant OS: `/config/`
- Core (venv): `~/.homeassistant/`
- Windows: `C:\Users\你的用户名\AppData\Roaming\.homeassistant\`
- Supervised: `/usr/share/hassio/homeassistant/`

### 步骤 2：复制集成文件

#### 选项 A：使用命令行（推荐）

**Windows PowerShell:**
```powershell
# 替换 <HA配置目录> 为您的实际路径
Copy-Item "C:\AI Coding\weixin\wechat-ha-integration\custom_components\feishu_gateway" -Destination "<HA配置目录>\custom_components\" -Recurse -Force
```

**示例：**
```powershell
# Docker (映射到本地)
Copy-Item "C:\AI Coding\weixin\wechat-ha-integration\custom_components\feishu_gateway" -Destination "C:\homeassistant\config\custom_components\" -Recurse -Force

# 直接安装
Copy-Item "C:\AI Coding\weixin\wechat-ha-integration\custom_components\feishu_gateway" -Destination "C:\Users\你的用户名\AppData\Roaming\.homeassistant\custom_components\" -Recurse -Force
```

**Linux/Mac:**
```bash
# 复制到配置目录
cp -r /path/to/wechat-ha-integration/custom_components/feishu_gateway /config/custom_components/

# 或者使用 scp 从本地复制到远程 HA
scp -r ./custom_components/feishu_gateway user@ha-server:/config/custom_components/
```

#### 选项 B：手动复制

1. 打开文件管理器
2. 导航到 `C:\AI Coding\weixin\wechat-ha-integration\custom_components\`
3. 复制 `feishu_gateway` 文件夹
4. 粘贴到您的 HA 配置目录的 `custom_components\` 文件夹中

### 步骤 3：验证文件结构

确保文件结构如下：

```
<HA配置目录>/
├── configuration.yaml
└── custom_components/
    └── feishu_gateway/
        ├── __init__.py
        ├── client.py
        ├── config_flow.py
        ├── const.py
        ├── manifest.json
        ├── notify.py
        ├── sensor.py
        ├── strings.json
        └── translations/
            ├── en.json
            └── zh-Hans.json
```

### 步骤 4：重启 Home Assistant

**方法 1：通过 UI**
1. 配置 → 系统 → 重启

**方法 2：通过命令行**
```bash
# Docker
docker restart homeassistant

# Supervised
ha core restart

# Core
sudo systemctl restart home-assistant@homeassistant
```

### 步骤 5：添加集成

1. 重启后，进入 **配置** → **设备与服务**
2. 点击右下角 **+ 添加集成**
3. 搜索 **"Feishu Gateway"**
4. 填写配置：
   - **Base URL**: `http://你的Gateway地址:8099`
   - **Access Token**: 留空（如果Gateway未设置token）
5. 点击 **提交**

### 步骤 6：验证安装

**检查实体：**
- 进入 **开发者工具** → **状态**
- 搜索 `sensor.feishu_gateway_last_message`
- 应该能看到这个实体

**检查服务：**
- 进入 **开发者工具** → **服务**
- 搜索 `notify.feishu_gateway`
- 应该能看到这个服务

## 常见问题

### Q1: 找不到集成

**解决方法：**
1. 确认文件复制到了正确位置
2. 检查文件夹名称是否为 `feishu_gateway`（不是 `wechat_gateway`）
3. 重启 Home Assistant
4. 清除浏览器缓存（Ctrl+F5）

### Q2: 提示 "Integration not found"

**原因：** manifest.json 文件损坏或缺失

**解决方法：**
```bash
# 检查文件是否存在
ls <HA配置目录>/custom_components/feishu_gateway/

# 应该看到所有必需文件
```

### Q3: 提示权限错误

**Linux 系统：**
```bash
# 设置正确的文件权限
sudo chown -R homeassistant:homeassistant /config/custom_components/feishu_gateway
sudo chmod -R 755 /config/custom_components/feishu_gateway
```

### Q4: 无法连接到 Gateway

**检查：**
1. Gateway 服务是否运行？
   ```bash
   curl http://gateway-ip:8099/health
   ```
2. HA 能否访问 Gateway？
3. 防火墙是否开放端口？

## 更新集成

当有新版本时：

1. 删除旧版本（如果存在）
   ```powershell
   Remove-Item "<HA配置目录>\custom_components\feishu_gateway" -Recurse -Force
   ```

2. 复制新版本
   ```powershell
   Copy-Item "C:\AI Coding\weixin\wechat-ha-integration\custom_components\feishu_gateway" -Destination "<HA配置目录>\custom_components\" -Recurse -Force
   ```

3. 重启 Home Assistant

## 卸载集成

1. 在 HA 中删除集成：
   - 配置 → 设备与服务
   - 找到 Feishu Gateway
   - 点击三个点 → 删除

2. 删除文件：
   ```powershell
   Remove-Item "<HA配置目录>\custom_components\feishu_gateway" -Recurse -Force
   ```

3. 重启 Home Assistant

## 获取帮助

- 查看 [README.md](./README.md) 了解使用方法
- 查看 [Gateway 文档](../wechat-ha-gateway/)
- 查看 HA 日志：配置 → 系统 → 日志

---

**安装完成后，请查看 [README.md](./README.md) 学习如何使用！** 🚀
