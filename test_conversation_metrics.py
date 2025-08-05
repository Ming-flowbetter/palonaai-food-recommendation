#!/usr/bin/env python3
"""
对话指标监控测试脚本
测试实时监控对话质量和用户满意度功能
"""

import requests
import json
import time
from datetime import datetime

# 配置
BASE_URL = "http://localhost:8000"  # 本地测试
# BASE_URL = "https://palonaai-food-recommendation.onrender.com"  # 线上测试
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

def test_conversation_metrics_basic():
    """测试基础对话指标"""
    print("\n📊 测试基础对话指标...")
    
    # 创建测试对话
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
                print(f"   会话ID: {session_id}")
                print(f"   对话长度: {data.get('conversation_length', 0)}")
                print(f"   交互次数: {data.get('interaction_count', 0)}")
                
                # 显示分析结果
                intent_scores = data.get('intent_scores', {})
                emotion_scores = data.get('emotion_scores', {})
                
                if intent_scores:
                    primary_intent = max(intent_scores.items(), key=lambda x: x[1])[0]
                    print(f"   主要意图: {primary_intent} ({(max(intent_scores.values()) * 100):.1f}%)")
                
                if emotion_scores:
                    primary_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
                    print(f"   主要情感: {primary_emotion} ({(max(emotion_scores.values()) * 100):.1f}%)")
                
            else:
                print(f"❌ 聊天失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 聊天异常: {e}")
        
        time.sleep(1)  # 避免请求过快
    
    return session_id

def test_conversation_metrics_api(session_id):
    """测试对话指标API"""
    print(f"\n📈 测试对话指标API (会话ID: {session_id})...")
    
    try:
        response = requests.get(f"{API_BASE}/conversation-metrics/{session_id}")
        if response.status_code == 200:
            metrics = response.json()
            print("✅ 对话指标获取成功")
            print(f"   会话ID: {metrics.get('session_id')}")
            print(f"   总消息数: {metrics.get('total_messages', 0)}")
            print(f"   用户满意度: {(metrics.get('user_satisfaction_score', 0) * 100):.1f}%")
            print(f"   平均响应时间: {metrics.get('average_response_time', 0):.2f}秒")
            print(f"   意图识别准确率: {(metrics.get('intent_accuracy', 0) * 100):.1f}%")
            print(f"   情感识别准确率: {(metrics.get('emotion_recognition_accuracy', 0) * 100):.1f}%")
            print(f"   创建时间: {metrics.get('created_at')}")
            print(f"   更新时间: {metrics.get('updated_at')}")
            return metrics
        else:
            print(f"❌ 获取对话指标失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 对话指标API异常: {e}")
        return None

def test_user_feedback_impact(session_id):
    """测试用户反馈对指标的影响"""
    print(f"\n💬 测试用户反馈对指标的影响...")
    
    # 提交正面反馈
    try:
        feedback_payload = {
            "session_id": session_id,
            "message_id": "test_positive_feedback",
            "rating": 5,
            "feedback_type": "positive",
            "comment": "推荐很准确，非常满意！"
        }
        
        response = requests.post(f"{API_BASE}/feedback", json=feedback_payload)
        if response.status_code == 200:
            print("✅ 正面反馈提交成功")
        else:
            print(f"❌ 正面反馈提交失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 正面反馈异常: {e}")
    
    # 提交负面反馈
    try:
        feedback_payload = {
            "session_id": session_id,
            "message_id": "test_negative_feedback",
            "rating": 2,
            "feedback_type": "negative",
            "comment": "推荐不够准确"
        }
        
        response = requests.post(f"{API_BASE}/feedback", json=feedback_payload)
        if response.status_code == 200:
            print("✅ 负面反馈提交成功")
        else:
            print(f"❌ 负面反馈提交失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 负面反馈异常: {e}")
    
    # 再次获取指标，查看变化
    time.sleep(2)  # 等待指标更新
    updated_metrics = test_conversation_metrics_api(session_id)
    return updated_metrics

def test_session_info(session_id):
    """测试会话信息"""
    print(f"\n📋 测试会话信息 (会话ID: {session_id})...")
    
    try:
        response = requests.get(f"{API_BASE}/session/{session_id}")
        if response.status_code == 200:
            session_info = response.json()
            print("✅ 会话信息获取成功")
            print(f"   会话ID: {session_info.get('session_id')}")
            print(f"   对话长度: {session_info.get('conversation_length', 0)}")
            print(f"   交互次数: {session_info.get('interaction_count', 0)}")
            print(f"   创建时间: {session_info.get('created_at')}")
            print(f"   最后活动: {session_info.get('last_activity')}")
            
            # 显示用户偏好
            preferences = session_info.get('user_preferences', {})
            if preferences:
                print("   用户偏好:")
                for key, value in preferences.items():
                    print(f"     {key}: {value}")
            
            # 显示意图历史
            intent_history = session_info.get('intent_history', [])
            if intent_history:
                print(f"   意图历史: {len(intent_history)} 条记录")
            
            # 显示情感历史
            emotion_history = session_info.get('emotion_history', [])
            if emotion_history:
                print(f"   情感历史: {len(emotion_history)} 条记录")
            
            return session_info
        else:
            print(f"❌ 获取会话信息失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 会话信息异常: {e}")
        return None

def test_metrics_comparison():
    """测试多个会话的指标对比"""
    print(f"\n📊 测试多个会话的指标对比...")
    
    sessions = []
    
    # 创建多个测试会话
    test_scenarios = [
        ["你好", "我想吃川菜", "这个推荐很棒！"],
        ["你好", "我想吃清淡的菜", "还可以吧"],
        ["你好", "我对海鲜过敏", "谢谢推荐"]
    ]
    
    for i, messages in enumerate(test_scenarios):
        print(f"\n--- 测试会话 {i+1} ---")
        session_id = None
        
        for message in messages:
            try:
                payload = {"message": message}
                if session_id:
                    payload["session_id"] = session_id
                    
                response = requests.post(f"{API_BASE}/chat", json=payload)
                if response.status_code == 200:
                    data = response.json()
                    session_id = data.get('session_id')
                    
                    # 提交反馈
                    feedback_type = "positive" if "很棒" in message else "neutral"
                    rating = 5 if "很棒" in message else 3
                    
                    feedback_payload = {
                        "session_id": session_id,
                        "message_id": f"test_{i}_{len(messages)}",
                        "rating": rating,
                        "feedback_type": feedback_type
                    }
                    
                    requests.post(f"{API_BASE}/feedback", json=feedback_payload)
                    
            except Exception as e:
                print(f"❌ 会话 {i+1} 异常: {e}")
        
        if session_id:
            sessions.append(session_id)
            time.sleep(1)
    
    # 对比所有会话的指标
    print(f"\n📈 会话指标对比:")
    for i, session_id in enumerate(sessions):
        try:
            response = requests.get(f"{API_BASE}/conversation-metrics/{session_id}")
            if response.status_code == 200:
                metrics = response.json()
                print(f"\n会话 {i+1}:")
                print(f"   总消息数: {metrics.get('total_messages', 0)}")
                print(f"   用户满意度: {(metrics.get('user_satisfaction_score', 0) * 100):.1f}%")
                print(f"   平均响应时间: {metrics.get('average_response_time', 0):.2f}秒")
        except Exception as e:
            print(f"❌ 获取会话 {i+1} 指标失败: {e}")

def test_real_time_monitoring():
    """测试实时监控功能"""
    print(f"\n⏱️ 测试实时监控功能...")
    
    session_id = None
    
    # 模拟实时对话
    real_time_messages = [
        "你好，我想吃辣的菜",
        "这个推荐怎么样？",
        "我对海鲜过敏",
        "谢谢推荐！"
    ]
    
    start_time = time.time()
    
    for i, message in enumerate(real_time_messages):
        try:
            payload = {"message": message}
            if session_id:
                payload["session_id"] = session_id
                
            response = requests.post(f"{API_BASE}/chat", json=payload)
            if response.status_code == 200:
                data = response.json()
                session_id = data.get('session_id')
                
                # 计算响应时间
                response_time = time.time() - start_time
                
                print(f"✅ 消息 {i+1} (响应时间: {response_time:.2f}秒):")
                print(f"   '{message}'")
                print(f"   会话ID: {session_id}")
                print(f"   对话长度: {data.get('conversation_length', 0)}")
                
                # 显示实时分析结果
                intent_scores = data.get('intent_scores', {})
                emotion_scores = data.get('emotion_scores', {})
                
                if intent_scores:
                    primary_intent = max(intent_scores.items(), key=lambda x: x[1])[0]
                    confidence = max(intent_scores.values()) * 100
                    print(f"   意图: {primary_intent} ({confidence:.1f}%)")
                
                if emotion_scores:
                    primary_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
                    intensity = max(emotion_scores.values()) * 100
                    print(f"   情感: {primary_emotion} ({intensity:.1f}%)")
                
                # 提交反馈
                if "谢谢" in message:
                    feedback_payload = {
                        "session_id": session_id,
                        "message_id": f"realtime_{i}",
                        "rating": 5,
                        "feedback_type": "positive"
                    }
                    requests.post(f"{API_BASE}/feedback", json=feedback_payload)
                    print("   ✅ 提交正面反馈")
                
            else:
                print(f"❌ 实时消息失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 实时消息异常: {e}")
        
        time.sleep(1)  # 模拟真实对话间隔
    
    # 获取最终指标
    if session_id:
        final_metrics = test_conversation_metrics_api(session_id)
        return final_metrics
    
    return None

def main():
    """主测试函数"""
    print("🚀 开始对话指标监控测试")
    print("=" * 60)
    
    # 测试健康检查
    if not test_health_check():
        print("❌ 健康检查失败，请确保服务正在运行")
        return
    
    # 测试基础对话指标
    session_id = test_conversation_metrics_basic()
    if not session_id:
        print("❌ 无法创建测试会话")
        return
    
    # 测试对话指标API
    initial_metrics = test_conversation_metrics_api(session_id)
    
    # 测试用户反馈影响
    updated_metrics = test_user_feedback_impact(session_id)
    
    # 测试会话信息
    session_info = test_session_info(session_id)
    
    # 测试多个会话对比
    test_metrics_comparison()
    
    # 测试实时监控
    real_time_metrics = test_real_time_monitoring()
    
    print("\n" + "=" * 60)
    print("📊 测试结果总结:")
    
    if initial_metrics:
        print(f"✅ 初始指标: 消息数={initial_metrics.get('total_messages', 0)}, "
              f"满意度={(initial_metrics.get('user_satisfaction_score', 0) * 100):.1f}%")
    
    if updated_metrics:
        print(f"✅ 更新后指标: 消息数={updated_metrics.get('total_messages', 0)}, "
              f"满意度={(updated_metrics.get('user_satisfaction_score', 0) * 100):.1f}%")
    
    if real_time_metrics:
        print(f"✅ 实时监控指标: 消息数={real_time_metrics.get('total_messages', 0)}, "
              f"满意度={(real_time_metrics.get('user_satisfaction_score', 0) * 100):.1f}%")
    
    print("\n🎉 对话指标监控测试完成！")
    print("💡 如果所有测试都通过，说明监控功能正常工作")

if __name__ == "__main__":
    main() 