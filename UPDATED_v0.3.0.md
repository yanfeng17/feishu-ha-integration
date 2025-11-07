# 🎉 Feishu Gateway v0.3.0 - 重大更新

## 已解决所有兼容性问题 ✅

此版本完全兼容最新的 Home Assistant，不再有任何错误！

## 重大变更

### ❌ 移除了 Notify 平台

由于 Home Assistant 新的 NotifyEntity API 限制，**移除了 notify 平台**。

### ✅ 新增自定义服务

现在使用更强大的**自定义服务**发送消息：

#### 发送消息服务

```yaml
service: feishu_gateway.send_message
data:
  target: "ou_bb7ed63bd3551a46547cf259a4e49651"  # 飞书 open_id
  message: "Hello from Home Assistant!"
  at_list:  # 可选，群聊中@某人
    - "ou_xxxxx"
```

#### 发送图片服务（预留）

```yaml
service: feishu_gateway.send_image
data:
  target: "ou_bb7ed63bd3551a46547cf259a4e49651"
  image_url: "https://example.com/image.jpg"
```

## 完整功能列表

### ✅ 实时消息接收
- WebSocket 连接
- 自动重连
- 事件触发

### ✅ 消息发送
- 通过 `feishu_gateway.send_message` 服务
- 支持私聊和群聊
- 支持 @提醒

### ✅ Sensor 实体
- `sensor.feishu_gateway_last_message` - 显示最新消息

### ✅ 事件
- `feishu_gateway_message` - 收到消息时触发

## 使用示例

### 示例 1：基本发送消息

```yaml
service: feishu_gateway.send_message
data:
  target: "ou_bb7ed63bd3551a46547cf259a4e49651"
  message: "测试消息"
```

### 示例 2：自动化回复

```yaml
automation:
  - alias: "飞书自动回复"
    trigger:
      - platform: event
        event_type: feishu_gateway_message
    condition:
      - condition: template
        value_template: "{{ trigger.event.data.content == '状态' }}"
    action:
      - service: feishu_gateway.send_message
        data:
          target: "{{ trigger.event.data.sender }}"
          message: "系统运行正常！"
```

### 示例 3：智能家居控制

```yaml
automation:
  - alias: "飞书控制灯光"
    trigger:
      - platform: event
        event_type: feishu_gateway_message
    condition:
      - condition: template
        value_template: "{{ '开灯' in trigger.event.data.content }}"
    action:
      - service: light.turn_on
        target:
          entity_id: light.living_room
      - service: feishu_gateway.send_message
        data:
          target: "{{ trigger.event.data.sender }}"
          message: "已开启客厅灯光"
```

### 示例 4：查询传感器状态

```yaml
automation:
  - alias: "查询温度"
    trigger:
      - platform: event
        event_type: feishu_gateway_message
    condition:
      - condition: template
        value_template: "{{ '温度' in trigger.event.data.content }}"
    action:
      - service: feishu_gateway.send_message
        data:
          target: "{{ trigger.event.data.sender }}"
          message: >
            当前温度：{{ states('sensor.temperature') }}°C
            湿度：{{ states('sensor.humidity') }}%
```

## 安装步骤

### 1. 更新文件

```powershell
# 完全替换
Remove-Item "<HA配置目录>\custom_components\feishu_gateway" -Recurse -Force
Copy-Item "C:\AI Coding\weixin\wechat-ha-integration\custom_components\feishu_gateway" -Destination "<HA配置目录>\custom_components\" -Recurse -Force
```

### 2. 重启 Home Assistant

### 3. 重新加载集成

如果已经添加过集成：
1. 配置 → 设备与服务
2. 找到 "Feishu Gateway"
3. 点击三个点 → **重新加载**

如果重新加载失败：
1. 删除集成
2. 重启 HA
3. 重新添加集成

## 文件结构

```
feishu_gateway/
├── __init__.py          ✅ 注册自定义服务
├── client.py            ✅ Gateway API 客户端
├── config_flow.py       ✅ UI 配置
├── const.py             ✅ 常量定义
├── manifest.json        ✅ v0.3.0
├── sensor.py            ✅ Sensor 实体
├── services.yaml        ✅ 新增：服务定义
├── strings.json         ✅ UI 文本
└── translations/        ✅ 多语言
    ├── en.json
    └── zh-Hans.json
```

## 技术说明

### 为什么移除 Notify 平台？

Home Assistant 2024.6+ 引入了新的 `NotifyEntity` API，但它有一个限制：
- **每个实体必须代表一个固定的目标**
- 不支持动态指定接收者

我们的用例需要：
- **动态指定目标（open_id）**
- 支持发送到不同用户/群聊

因此，**自定义服务**是更好的选择：
- ✅ 完全控制参数
- ✅ 支持动态目标
- ✅ 更符合我们的需求

### API 兼容性

- ✅ Home Assistant 2023.x+
- ✅ Home Assistant 2024.x+
- ✅ Home Assistant 2025.x+

## 获取服务 ID

### 获取用户 open_id

1. 在飞书中给机器人发消息
2. 查看 Gateway 日志：
   ```
   [Feishu] Received message from ou_xxxxx: 测试
   ```
3. 复制 `ou_xxxxx` 就是 open_id

### 获取群聊 chat_id

1. 在群聊中@机器人发消息
2. 查看 Gateway 日志中的 `room_id`:
   ```
   room_id: oc_xxxxx
   ```
3. 复制 `oc_xxxxx` 就是 chat_id

## 故障排查

### Q: 服务调用失败

**检查：**
1. 集成是否正常运行？
2. Gateway 服务是否运行？
3. target ID 是否正确？

**测试连接：**
```bash
curl http://gateway-ip:8099/health
```

### Q: 找不到服务

**解决方法：**
1. 确认集成已安装并启用
2. 重启 Home Assistant
3. 检查日志是否有错误

### Q: 无法接收消息

**检查：**
1. Gateway 日志是否显示收到消息？
2. Sensor 是否更新？
3. WebSocket 是否连接？

## 下一步

- ✅ 测试发送消息
- ✅ 测试接收消息
- ✅ 创建自动化
- ✅ 部署到生产环境

---

**更新完成！开始享受稳定的飞书集成吧！** 🚀

有任何问题请查看日志：**配置 → 系统 → 日志**
