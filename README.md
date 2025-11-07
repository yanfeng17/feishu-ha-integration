# Feishu Gateway - Home Assistant 集成

Home Assistant 自定义集成，用于连接飞书（Feishu/Lark）Gateway 服务。

## ✨ 特性

- ✅ **实时消息接收** - 通过 WebSocket 接收飞书消息
- ✅ **消息发送** - 通过自定义服务发送消息
- ✅ **Sensor 实体** - 显示最新收到的消息
- ✅ **事件触发** - 消息触发 HA 自动化
- ✅ **高性能** - 优化的异步架构，延迟 < 100ms
- ✅ **私聊和群聊** - 支持私聊和群组消息

## 📋 版本

**当前版本：v0.3.1**

### 性能优化
- 纯异步 Sensor 更新机制（减少 20-50ms）
- 智能 WebSocket 重连策略（指数退避）
- 完善的错误处理和诊断日志
- 端到端延迟降低 40-50%

## 🚀 快速开始

### 1. 安装

将 `custom_components/feishu_gateway` 目录复制到您的 Home Assistant 配置目录：

```
<config_dir>/custom_components/feishu_gateway/
```

### 2. 重启 Home Assistant

### 3. 添加集成

1. **配置** → **设备与服务** → **添加集成**
2. 搜索 **"Feishu Gateway"**
3. 填写配置：
   - **Base URL**: Gateway 服务地址（如：`http://192.168.1.100:8099`）
   - **Access Token**: 可选，如果 Gateway 配置了令牌

### 4. 使用服务发送消息

```yaml
service: feishu_gateway.send_message
data:
  target: "ou_xxxxx"  # 飞书 open_id
  message: "Hello from Home Assistant!"
```

## 📖 文档

- [安装指南](./INSTALL.md)
- [v0.3.0 更新说明](./UPDATED_v0.3.0.md) - 服务架构变更
- [v0.3.1 性能优化](./PERFORMANCE_v0.3.1.md) - 性能优化详情

## 🎯 使用示例

### 发送消息

```yaml
service: feishu_gateway.send_message
data:
  target: "ou_bb7ed63bd3551a46547cf259a4e49651"
  message: "测试消息"
```

### 自动化回复

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

### 智能家居控制

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

## 🔌 可用服务

### `feishu_gateway.send_message`

发送文本消息到飞书用户或群组。

**参数：**
- `target` (必填): 目标 open_id 或 chat_id
- `message` (必填): 消息内容
- `at_list` (可选): 群聊中@的用户列表

### `feishu_gateway.send_image`

发送图片消息（暂未实现）。

## 📊 实体

### Sensor

- `sensor.feishu_gateway_last_message` - 最新收到的消息

**属性：**
- `sender`: 发送者 open_id
- `sender_name`: 发送者名称
- `room_id`: 群聊 chat_id（如果适用）
- `timestamp`: 消息时间戳
- `received_at`: HA 接收时间

### 事件

- `feishu_gateway_message` - 收到新消息时触发

**事件数据：**
```json
{
  "msg_id": "消息ID",
  "sender": "ou_xxxxx",
  "sender_name": "发送者",
  "content": "消息内容",
  "is_group": false,
  "timestamp": 1699999999
}
```

## 🏗️ 架构

```
飞书 ←→ Gateway ←→ HA 集成
                    ├─ WebSocket 连接（消息接收）
                    ├─ REST API（消息发送）
                    ├─ Sensor 实体
                    ├─ 事件触发
                    └─ 自定义服务
```

## 📊 性能

- **消息接收延迟**: 50-100ms
- **事件触发延迟**: 80-150ms  
- **Sensor 更新延迟**: 20-50ms
- **WebSocket 重连**: 智能指数退避（1s-60s）

## 🔧 调试

启用详细日志：

```yaml
# configuration.yaml
logger:
  default: info
  logs:
    custom_components.feishu_gateway: debug
```

## 🤝 配套项目

- [feishu-ha-gateway](https://github.com/yanfeng17/feishu-ha-gateway) - Gateway 服务

## ⚙️ 要求

- Home Assistant 2023.x 或更高版本
- Python 3.11+
- [feishu-ha-gateway](https://github.com/yanfeng17/feishu-ha-gateway) 服务运行中

## 📝 许可证

MIT License

## 🙏 致谢

感谢 Home Assistant 社区和开源贡献者。

---

**享受您的智能家居飞书集成！** 🏠📱
