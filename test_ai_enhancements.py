#!/usr/bin/env python3
"""
AI对话能力增强测试脚本
测试意图识别、情感分析、实体提取等新功能
"""

import requests
import json
import time

# 配置
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def test_health_check():
    """测试健康检查"""
    print("🔍 测试健康检查...")
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 健康检查通过")
            print(f"   版本: {data.get('version', 'N/A')}")
            print(f"   功能: {', '.join(data.get('features', []))}")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {e}")
        return False

def test_intent_analysis():
    """测试意图分析"""
    print("\n🧠 测试意图分析...")
    
    test_messages = [
        "我想吃辣的菜",
        "这个菜的营养价值怎么样？",
        "比较一下川菜和粤菜的区别",
        "我喜欢清淡的口味",
        "我对海鲜过敏",
        "今天有什么季节性推荐？",
        "预算在100元以内"
    ]
    
    for message in test_messages:
        try:
            response = requests.post(f"{API_BASE}/analyze-intent", json={"message": message})
            if response.status_code == 200:
                data = response.json()
                primary_intent = data.get('primary_intent', 'unknown')
                print(f"✅ '{message}' -> 主要意图: {primary_intent}")
            else:
                print(f"❌ 意图分析失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 意图分析异常: {e}")

def test_emotion_analysis():
    """测试情感分析"""
    print("\n💖 测试情感分析...")
    
    test_messages = [
        "这个推荐太棒了！",
        "我不喜欢这个菜",
        "还可以吧",
        "太兴奋了，迫不及待想尝试！",
        "我有点担心这个菜太辣"
    ]
    
    for message in test_messages:
        try:
            response = requests.post(f"{API_BASE}/analyze-emotion", json={"message": message})
            if response.status_code == 200:
                data = response.json()
                primary_emotion = data.get('primary_emotion', 'unknown')
                print(f"✅ '{message}' -> 主要情感: {primary_emotion}")
            else:
                print(f"❌ 情感分析失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 情感分析异常: {e}")

def test_entity_extraction():
    """测试实体提取"""
    print("\n🏷️ 测试实体提取...")
    
    test_messages = [
        "我想吃中餐，喜欢辣的口味",
        "我对海鲜过敏，想要清淡的菜",
        "预算在200元以内，想要高档的意大利菜",
        "3个人用餐，想要川菜"
    ]
    
    for message in test_messages:
        try:
            response = requests.post(f"{API_BASE}/extract-entities", json={"message": message})
            if response.status_code == 200:
                data = response.json()
                entities = data.get('entities', {})
                print(f"✅ '{message}'")
                for entity_type, value in entities.items():
                    if value:
                        print(f"   {entity_type}: {value}")
            else:
                print(f"❌ 实体提取失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 实体提取异常: {e}")

def test_enhanced_chat():
    """测试增强的聊天功能"""
    print("\n💬 测试增强的聊天功能...")
    
    test_messages = [
        "你好",
        "我想吃辣的菜",
        "这个推荐怎么样？",
        "我对海鲜过敏"
    ]
    
    session_id = None
    
    for i, message in enumerate(test_messages):
        try:
            payload = {"message": message}
            if session_id:
                payload["session_id"] = session_id
                
            response = requests.post(f"{API_BASE}/chat", json=payload)
            if response.status_code == 200:
                data = response.json()
                session_id = data.get('session_id')
                
                print(f"✅ 消息 {i+1}: '{message}'")
                print(f"   AI回复: {data.get('response', '')[:100]}...")
                
                # 显示分析结果
                intent_scores = data.get('intent_scores', {})
                emotion_scores = data.get('emotion_scores', {})
                entities = data.get('entities', {})
                
                if intent_scores:
                    primary_intent = max(intent_scores.items(), key=lambda x: x[1])[0]
                    print(f"   意图: {primary_intent} ({(max(intent_scores.values()) * 100):.1f}%)")
                
                if emotion_scores:
                    primary_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
                    print(f"   情感: {primary_emotion} ({(max(emotion_scores.values()) * 100):.1f}%)")
                
                if entities:
                    print(f"   实体: {entities}")
                
            else:
                print(f"❌ 聊天失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 聊天异常: {e}")
        
        time.sleep(1)  # 避免请求过快

def test_feedback_system():
    """测试反馈系统"""
    print("\n📝 测试反馈系统...")
    
    # 先进行一个对话
    try:
        response = requests.post(f"{API_BASE}/chat", json={"message": "我想吃川菜"})
        if response.status_code == 200:
            data = response.json()
            session_id = data.get('session_id')
            message_id = "test_message_id"
            
            # 提交正面反馈
            feedback_payload = {
                "session_id": session_id,
                "message_id": message_id,
                "rating": 5,
                "feedback_type": "positive",
                "comment": "推荐很准确"
            }
            
            feedback_response = requests.post(f"{API_BASE}/feedback", json=feedback_payload)
            if feedback_response.status_code == 200:
                print("✅ 反馈提交成功")
            else:
                print(f"❌ 反馈提交失败: {feedback_response.status_code}")
        else:
            print("❌ 无法创建测试对话")
    except Exception as e:
        print(f"❌ 反馈测试异常: {e}")

def test_conversation_metrics():
    """测试对话指标"""
    print("\n📊 测试对话指标...")
    
    # 先进行一个对话
    try:
        response = requests.post(f"{API_BASE}/chat", json={"message": "你好"})
        if response.status_code == 200:
            data = response.json()
            session_id = data.get('session_id')
            
            # 获取对话指标
            metrics_response = requests.get(f"{API_BASE}/conversation-metrics/{session_id}")
            if metrics_response.status_code == 200:
                metrics = metrics_response.json()
                print("✅ 对话指标获取成功")
                print(f"   总消息数: {metrics.get('total_messages', 0)}")
                print(f"   用户满意度: {metrics.get('user_satisfaction_score', 0):.2f}")
                print(f"   平均响应时间: {metrics.get('average_response_time', 0):.2f}秒")
            else:
                print(f"❌ 获取对话指标失败: {metrics_response.status_code}")
        else:
            print("❌ 无法创建测试对话")
    except Exception as e:
        print(f"❌ 对话指标测试异常: {e}")

def main():
    """主测试函数"""
    print("🚀 开始AI对话能力增强测试")
    print("=" * 50)
    
    # 测试健康检查
    if not test_health_check():
        print("❌ 健康检查失败，请确保后端服务正在运行")
        return
    
    # 测试各项功能
    test_intent_analysis()
    test_emotion_analysis()
    test_entity_extraction()
    test_enhanced_chat()
    test_feedback_system()
    test_conversation_metrics()
    
    print("\n" + "=" * 50)
    print("🎉 AI对话能力增强测试完成！")
    print("💡 如果所有测试都通过，说明新功能已成功部署")

if __name__ == "__main__":
    main() 