# Feishu Gateway - Home Assistant 集成

Home Assistant 自定义集成，用于连接飞书（Feishu/Lark）Gateway 服务。

## 版本

- **版本**: 0.2.1
- **兼容**: Home Assistant 2023.x+
- **Gateway 版本**: 0.2.0+

## 功能特性

- ✅ **实时消息接收** - 通过 WebSocket 接收飞书消息
- ✅ **消息发送** - 通过 Notify 服务发送消息
- ✅ **Sensor 实体** - 显示最新收到的消息
- ✅ **事件触发** - 消息触发 HA 自动化
- ✅ **私聊和群聊** - 支持私聊和群组消息

## 安装

### 手动安装

1. **复制集成文件**

   将 `custom_components/feishu_gateway` 目录复制到您的 Home Assistant 配置目录：

   ```
   <config_dir>/custom_components/feishu_gateway/
   ```

2. **重启 Home Assistant**

   配置 → 开发者工具 → YAML → 重启 Home Assistant

## 配置

### 通过 UI 配置（推荐）

1. 进入 **配置** → **设备与服务**
2. 点击右下角 **+ 添加集成**
3. 搜索 **"Feishu Gateway"**
4. 填写配置：
   - **Base URL**: Gateway 服务地址（例如：`http://192.168.1.100:8099`）
   - **Access Token**: 可选，如果 Gateway 配置了 `GATEWAY_TOKEN`，在此填入

5. 点击 **提交**

## 使用

### Notify 服务

发送消息到飞书：

```yaml
service: notify.feishu_gateway
data:
  message: "Hello from Home Assistant!"
  target: "ou_xxxxxxxxxxxxx"  # 用户的 open_id
```

**发送群消息：**

```yaml
service: notify.feishu_gateway
data:
  message: "群聊消息"
  target: "oc_xxxxxxxxxxxxx"  # 群聊的 chat_id
```

### Sensor 实体

**实体 ID**: `sensor.feishu_gateway_last_message`

**属性：**
- `state`: 最新消息内容
- `sender`: 发送者 open_id
- `sender_name`: 发送者名称
- `room_id`: 群聊 chat_id（如果是群消息）
- `room_name`: 群聊名称
- `timestamp`: 消息时间戳
- `received_at`: HA 接收时间

### 事件

**事件类型**: `feishu_gateway_message`

**事件数据：**
```json
{
  "msg_id": "消息ID",
  "sender": "ou_xxxxx",
  "sender_name": "发送者名称",
  "content": "消息内容",
  "is_group": false,
  "timestamp": 1699999999,
  "room_id": null,
  "room_name": null
}
```

## 自动化示例

### 示例 1：收到特定消息时回复

```yaml
automation:
  - alias: "飞书消息自动回复"
    trigger:
      - platform: event
        event_type: feishu_gateway_message
    condition:
      - condition: template
        value_template: "{{ trigger.event.data.content == '状态' }}"
    action:
      - service: notify.feishu_gateway
        data:
          message: "系统运行正常！"
          target: "{{ trigger.event.data.sender }}"
```

### 示例 2：智能家居控制

```yaml
automation:
  - alias: "通过飞书控制灯光"
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
      - service: notify.feishu_gateway
        data:
          message: "已开启客厅灯光"
          target: "{{ trigger.event.data.sender }}"
```

### 示例 3：传感器状态查询

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
      - service: notify.feishu_gateway
        data:
          message: >
            当前温度：{{ states('sensor.temperature') }}°C
            湿度：{{ states('sensor.humidity') }}%
          target: "{{ trigger.event.data.sender }}"
```

## 故障排查

### 无法连接到 Gateway

**检查：**
1. Gateway 服务是否运行？
2. Base URL 是否正确？
3. 防火墙是否开放 8099 端口？

**测试连接：**
```bash
curl http://your-gateway-ip:8099/health
# 应该返回: {"status":"ok"}
```

### 收不到消息

**检查：**
1. Gateway 日志是否显示收到消息？
2. WebSocket 连接是否正常？
3. 飞书事件订阅是否配置正确？

### 发送消息失败

**检查：**
1. `target` ID 是否正确？
   - 飞书用户：`ou_xxxxx`
   - 飞书群聊：`oc_xxxxx`
2. Gateway 权限是否正确配置？

## 更新日志

### v0.2.1 - 2025-11-07
- ✅ 重命名为 Feishu Gateway
- ✅ 修复 aiohttp_client 导入问题
- ✅ 优化代码结构

### v0.2.0 - 2025-11-07
- ✅ 支持飞书 Gateway v0.2.0
- ✅ 完整的消息收发功能

## 许可证

MIT License

---

**享受您的智能家居飞书集成！** 🏠📱
