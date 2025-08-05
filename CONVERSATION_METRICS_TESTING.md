# 对话指标监控测试指南

## 📊 概述

对话指标监控功能用于实时监控对话质量和用户满意度，包括以下核心指标：

- **用户满意度**: 基于用户反馈计算
- **响应时间**: 监控AI响应速度
- **意图识别准确率**: 评估意图识别准确性
- **情感识别准确率**: 评估情感分析准确性
- **对话长度**: 统计消息数量
- **交互次数**: 记录用户交互频率

## 🧪 测试方法

### 1. 自动化测试

#### 运行测试脚本
```bash
# 本地测试
python test_conversation_metrics.py

# 线上测试（修改脚本中的BASE_URL）
python test_conversation_metrics.py
```

#### 测试脚本功能
- ✅ 健康检查
- ✅ 基础对话指标测试
- ✅ 对话指标API测试
- ✅ 用户反馈影响测试
- ✅ 会话信息测试
- ✅ 多会话指标对比
- ✅ 实时监控测试

### 2. 手动测试

#### 2.1 健康检查
```bash
curl -X GET "https://palonaai-food-recommendation.onrender.com/api/health"
```

**预期结果**:
```json
{
  "status": "healthy",
  "service": "PalonaAI菜品推荐系统",
  "version": "2.0.0",
  "features": [
    "智能对话",
    "意图识别",
    "情感分析",
    "实体提取",
    "个性化推荐",
    "用户反馈"
  ]
}
```

#### 2.2 创建测试对话
```bash
curl -X POST "https://palonaai-food-recommendation.onrender.com/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "你好，我想吃辣的菜"}'
```

**预期结果**:
```json
{
  "response": "你好！根据您的偏好，我推荐...",
  "session_id": "uuid-string",
  "conversation_length": 2,
  "interaction_count": 1,
  "intent_scores": {"recommendation": 0.8, "preference": 0.6},
  "emotion_scores": {"neutral": 0.7},
  "entities": {"taste_preferences": ["spicy"]}
}
```

#### 2.3 获取对话指标
```bash
curl -X GET "https://palonaai-food-recommendation.onrender.com/api/conversation-metrics/{session_id}"
```

**预期结果**:
```json
{
  "session_id": "uuid-string",
  "total_messages": 4,
  "user_satisfaction_score": 0.85,
  "average_response_time": 1.23,
  "intent_accuracy": 0.92,
  "emotion_recognition_accuracy": 0.88,
  "created_at": "2024-01-01T10:00:00",
  "updated_at": "2024-01-01T10:05:00"
}
```

#### 2.4 提交用户反馈
```bash
curl -X POST "https://palonaai-food-recommendation.onrender.com/api/feedback" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "uuid-string",
    "message_id": "test_message",
    "rating": 5,
    "feedback_type": "positive",
    "comment": "推荐很准确！"
  }'
```

**预期结果**:
```json
{
  "message": "反馈已提交",
  "session_id": "uuid-string",
  "rating": 5,
  "feedback_type": "positive"
}
```

#### 2.5 获取会话信息
```bash
curl -X GET "https://palonaai-food-recommendation.onrender.com/api/session/{session_id}"
```

**预期结果**:
```json
{
  "session_id": "uuid-string",
  "conversation_length": 4,
  "interaction_count": 2,
  "user_preferences": {
    "taste_preferences": ["spicy"],
    "cuisine_preferences": ["chinese"]
  },
  "intent_history": [...],
  "emotion_history": [...],
  "created_at": "2024-01-01T10:00:00",
  "last_activity": "2024-01-01T10:05:00"
}
```

## 📈 指标说明

### 1. 用户满意度 (user_satisfaction_score)
- **计算方式**: 基于用户反馈评分计算
- **范围**: 0.0 - 1.0 (0% - 100%)
- **更新频率**: 每次提交反馈时更新
- **测试方法**: 提交不同评分的反馈，观察指标变化

### 2. 平均响应时间 (average_response_time)
- **计算方式**: 所有API调用的平均响应时间
- **单位**: 秒
- **更新频率**: 每次API调用时更新
- **测试方法**: 进行多次API调用，观察响应时间统计

### 3. 意图识别准确率 (intent_accuracy)
- **计算方式**: 基于历史对话的意图识别准确性
- **范围**: 0.0 - 1.0 (0% - 100%)
- **更新频率**: 每次对话时更新
- **测试方法**: 发送不同类型的消息，观察意图识别准确性

### 4. 情感识别准确率 (emotion_recognition_accuracy)
- **计算方式**: 基于历史对话的情感分析准确性
- **范围**: 0.0 - 1.0 (0% - 100%)
- **更新频率**: 每次对话时更新
- **测试方法**: 发送不同情感色彩的消息，观察情感识别准确性

## 🔍 测试场景

### 场景1: 基础对话指标测试
1. 创建新会话
2. 发送多条消息
3. 检查对话长度和交互次数
4. 验证指标计算正确性

### 场景2: 用户反馈影响测试
1. 提交正面反馈 (rating: 5)
2. 提交负面反馈 (rating: 1)
3. 提交中性反馈 (rating: 3)
4. 观察满意度指标变化

### 场景3: 实时监控测试
1. 模拟真实对话流程
2. 记录每次响应时间
3. 观察指标实时更新
4. 验证监控准确性

### 场景4: 多会话对比测试
1. 创建多个测试会话
2. 进行不同的对话内容
3. 提交不同的反馈
4. 对比各会话的指标差异

## 🐛 常见问题排查

### 1. 指标不更新
**可能原因**:
- 会话ID不正确
- 反馈提交失败
- 数据库连接问题

**排查方法**:
```bash
# 检查会话是否存在
curl -X GET "https://palonaai-food-recommendation.onrender.com/api/session/{session_id}"

# 检查反馈是否提交成功
curl -X POST "https://palonaai-food-recommendation.onrender.com/api/feedback" \
  -H "Content-Type: application/json" \
  -d '{"session_id": "test", "message_id": "test", "rating": 5, "feedback_type": "positive"}'
```

### 2. 响应时间异常
**可能原因**:
- 网络延迟
- 服务器负载高
- AI服务响应慢

**排查方法**:
```bash
# 测试健康检查响应时间
time curl -X GET "https://palonaai-food-recommendation.onrender.com/api/health"

# 测试聊天API响应时间
time curl -X POST "https://palonaai-food-recommendation.onrender.com/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "测试消息"}'
```

### 3. 准确率计算错误
**可能原因**:
- 意图识别算法问题
- 情感分析模型问题
- 数据预处理错误

**排查方法**:
```bash
# 测试意图分析
curl -X POST "https://palonaai-food-recommendation.onrender.com/api/analyze-intent" \
  -H "Content-Type: application/json" \
  -d '{"message": "我想吃辣的菜"}'

# 测试情感分析
curl -X POST "https://palonaai-food-recommendation.onrender.com/api/analyze-emotion" \
  -H "Content-Type: application/json" \
  -d '{"message": "这个推荐太棒了！"}'
```

## 📊 性能基准

### 预期性能指标
- **响应时间**: < 3秒 (95%的请求)
- **用户满意度**: > 80%
- **意图识别准确率**: > 85%
- **情感识别准确率**: > 80%
- **API可用性**: > 99%

### 监控建议
1. **定期测试**: 建议每天运行一次完整测试
2. **性能监控**: 监控响应时间和错误率
3. **用户反馈**: 收集真实用户反馈数据
4. **指标趋势**: 观察指标变化趋势，及时发现问题

## ✅ 测试检查清单

### 基础功能测试
- [ ] 健康检查正常
- [ ] 对话创建成功
- [ ] 指标API可访问
- [ ] 反馈提交成功
- [ ] 会话信息获取正常

### 指标准确性测试
- [ ] 用户满意度计算正确
- [ ] 响应时间统计准确
- [ ] 意图识别准确率合理
- [ ] 情感识别准确率合理
- [ ] 对话长度统计正确

### 实时监控测试
- [ ] 指标实时更新
- [ ] 多会话指标独立
- [ ] 反馈影响指标变化
- [ ] 性能指标稳定

### 异常情况测试
- [ ] 无效会话ID处理
- [ ] 网络错误处理
- [ ] 服务异常恢复
- [ ] 数据一致性检查

---

**测试工具**: `test_conversation_metrics.py`  
**测试环境**: 本地/线上  
**测试频率**: 建议每日一次  
**维护人员**: 开发团队 