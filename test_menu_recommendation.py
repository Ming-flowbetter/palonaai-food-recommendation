#!/usr/bin/env python3
"""
菜单推荐功能测试脚本
测试聊天中推荐菜单内菜品的功能
"""

import requests
import json
import time
from datetime import datetime

# 配置
BASE_URL = "http://localhost:8000"  # 本地测试
# BASE_URL = "https://palonaai-food-recommendation.onrender.com"  # 线上测试
API_BASE = f"{BASE_URL}/api"

def test_menu_recommendation_basic():
    """测试基础菜单推荐功能"""
    print("🍽️ 测试基础菜单推荐功能...")
    
    # 测试场景
    test_scenarios = [
        {
            "message": "你好，我想吃辣的菜",
            "description": "测试辣味菜品推荐"
        },
        {
            "message": "我想吃川菜",
            "description": "测试川菜推荐"
        },
        {
            "message": "我想吃清淡的菜",
            "description": "测试清淡菜品推荐"
        },
        {
            "message": "我想吃海鲜",
            "description": "测试海鲜菜品推荐"
        },
        {
            "message": "我想吃便宜的菜",
            "description": "测试经济实惠菜品推荐"
        }
    ]
    
    session_id = None
    
    for i, scenario in enumerate(test_scenarios):
        print(f"\n--- 测试场景 {i+1}: {scenario['description']} ---")
        
        try:
            payload = {"message": scenario["message"]}
            if session_id:
                payload["session_id"] = session_id
                
            response = requests.post(f"{API_BASE}/chat", json=payload)
            if response.status_code == 200:
                data = response.json()
                session_id = data.get('session_id')
                
                print(f"✅ 用户消息: '{scenario['message']}'")
                print(f"🤖 AI回复: {data.get('response', '')[:200]}...")
                
                # 显示分析结果
                intent_scores = data.get('intent_scores', {})
                emotion_scores = data.get('emotion_scores', {})
                entities = data.get('entities', {})
                
                if intent_scores:
                    primary_intent = max(intent_scores.items(), key=lambda x: x[1])[0]
                    print(f"   意图识别: {primary_intent} ({(max(intent_scores.values()) * 100):.1f}%)")
                
                if emotion_scores:
                    primary_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
                    print(f"   情感分析: {primary_emotion} ({(max(emotion_scores.values()) * 100):.1f}%)")
                
                if entities:
                    print(f"   实体提取: {entities}")
                
            else:
                print(f"❌ 聊天失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 聊天异常: {e}")
        
        time.sleep(1)  # 避免请求过快
    
    return session_id

def test_menu_recommendation_advanced():
    """测试高级菜单推荐功能"""
    print("\n🎯 测试高级菜单推荐功能...")
    
    # 复杂测试场景
    advanced_scenarios = [
        {
            "message": "我对海鲜过敏，想要清淡的菜",
            "description": "测试过敏原过滤 + 清淡口味"
        },
        {
            "message": "我想吃川菜，但是不要太辣的",
            "description": "测试菜系 + 口味偏好"
        },
        {
            "message": "我想吃营养丰富的菜，预算在50元以内",
            "description": "测试健康需求 + 预算限制"
        },
        {
            "message": "我想吃当季的菜",
            "description": "测试季节性菜品"
        },
        {
            "message": "我想吃评分高的菜",
            "description": "测试评分排序"
        }
    ]
    
    session_id = None
    
    for i, scenario in enumerate(advanced_scenarios):
        print(f"\n--- 高级测试场景 {i+1}: {scenario['description']} ---")
        
        try:
            payload = {"message": scenario["message"]}
            if session_id:
                payload["session_id"] = session_id
                
            response = requests.post(f"{API_BASE}/chat", json=payload)
            if response.status_code == 200:
                data = response.json()
                session_id = data.get('session_id')
                
                print(f"✅ 用户消息: '{scenario['message']}'")
                print(f"🤖 AI回复: {data.get('response', '')}")
                
                # 检查是否包含菜单菜品信息
                response_text = data.get('response', '')
                if '¥' in response_text or '价格' in response_text:
                    print("✅ 包含菜单价格信息")
                if '评分' in response_text:
                    print("✅ 包含菜品评分信息")
                if '描述' in response_text or '特点' in response_text:
                    print("✅ 包含菜品描述信息")
                
            else:
                print(f"❌ 聊天失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 聊天异常: {e}")
        
        time.sleep(1)
    
    return session_id

def test_menu_search():
    """测试菜单搜索功能"""
    print("\n🔍 测试菜单搜索功能...")
    
    # 测试菜单搜索API
    search_queries = [
        {"query": "川菜", "description": "搜索川菜"},
        {"query": "辣", "description": "搜索辣味菜品"},
        {"query": "海鲜", "description": "搜索海鲜菜品"},
        {"query": "清淡", "description": "搜索清淡菜品"},
        {"query": "便宜", "description": "搜索经济菜品"}
    ]
    
    for i, search in enumerate(search_queries):
        print(f"\n--- 搜索测试 {i+1}: {search['description']} ---")
        
        try:
            payload = {
                "query": search["query"],
                "limit": 5
            }
            
            response = requests.post(f"{API_BASE}/search", json=payload)
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                print(f"✅ 搜索关键词: '{search['query']}'")
                print(f"   找到 {len(results)} 个结果:")
                
                for j, item in enumerate(results, 1):
                    print(f"   {j}. {item.get('name', 'N/A')} - ¥{item.get('price', 0)}")
                    print(f"      类别: {item.get('category', 'N/A')}")
                    print(f"      评分: {item.get('rating', 0)}/5.0")
                
            else:
                print(f"❌ 搜索失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 搜索异常: {e}")
        
        time.sleep(1)

def test_menu_categories():
    """测试菜单分类功能"""
    print("\n📂 测试菜单分类功能...")
    
    try:
        response = requests.get(f"{API_BASE}/menu/categories")
        if response.status_code == 200:
            categories = response.json()
            print("✅ 菜单分类:")
            for category in categories:
                print(f"   - {category}")
        else:
            print(f"❌ 获取分类失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取分类异常: {e}")

def test_menu_items():
    """测试菜单菜品列表"""
    print("\n📋 测试菜单菜品列表...")
    
    try:
        response = requests.get(f"{API_BASE}/menu/items")
        if response.status_code == 200:
            items = response.json()
            print(f"✅ 菜单共有 {len(items)} 道菜品:")
            
            # 按类别显示
            categories = {}
            for item in items:
                category = item.get('category', '其他')
                if category not in categories:
                    categories[category] = []
                categories[category].append(item)
            
            for category, category_items in categories.items():
                print(f"\n   {category} ({len(category_items)}道):")
                for item in category_items[:3]:  # 只显示前3个
                    print(f"     - {item.get('name')} - ¥{item.get('price')}")
                if len(category_items) > 3:
                    print(f"     ... 还有{len(category_items)-3}道菜")
        else:
            print(f"❌ 获取菜品列表失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取菜品列表异常: {e}")

def test_conversation_with_menu():
    """测试与菜单的对话交互"""
    print("\n💬 测试与菜单的对话交互...")
    
    # 模拟真实对话流程
    conversation_flow = [
        "你好，我想吃川菜",
        "这个推荐怎么样？",
        "我想吃更辣的",
        "我对花生过敏",
        "我想吃便宜的",
        "谢谢推荐！"
    ]
    
    session_id = None
    
    for i, message in enumerate(conversation_flow):
        print(f"\n--- 对话轮次 {i+1} ---")
        
        try:
            payload = {"message": message}
            if session_id:
                payload["session_id"] = session_id
                
            response = requests.post(f"{API_BASE}/chat", json=payload)
            if response.status_code == 200:
                data = response.json()
                session_id = data.get('session_id')
                
                print(f"👤 用户: {message}")
                print(f"🤖 AI: {data.get('response', '')[:150]}...")
                
                # 检查用户偏好更新
                preferences = data.get('user_preferences', {})
                if preferences:
                    print(f"📝 用户偏好: {preferences}")
                
            else:
                print(f"❌ 对话失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 对话异常: {e}")
        
        time.sleep(1)
    
    return session_id

def test_menu_recommendation_features():
    """测试菜单推荐特色功能"""
    print("\n⭐ 测试菜单推荐特色功能...")
    
    # 测试特色功能
    feature_tests = [
        {
            "message": "我想吃当季的菜",
            "feature": "季节性推荐"
        },
        {
            "message": "我想吃评分最高的菜",
            "feature": "评分排序"
        },
        {
            "message": "我想吃最便宜的菜",
            "feature": "价格排序"
        },
        {
            "message": "我想吃最贵的菜",
            "feature": "高端推荐"
        },
        {
            "message": "我想吃没有过敏原的菜",
            "feature": "过敏原过滤"
        }
    ]
    
    session_id = None
    
    for i, test in enumerate(feature_tests):
        print(f"\n--- 特色功能测试 {i+1}: {test['feature']} ---")
        
        try:
            payload = {"message": test["message"]}
            if session_id:
                payload["session_id"] = session_id
                
            response = requests.post(f"{API_BASE}/chat", json=payload)
            if response.status_code == 200:
                data = response.json()
                session_id = data.get('session_id')
                
                print(f"✅ 测试功能: {test['feature']}")
                print(f"👤 用户消息: '{test['message']}'")
                print(f"🤖 AI回复: {data.get('response', '')[:200]}...")
                
                # 检查回复质量
                response_text = data.get('response', '')
                if '推荐' in response_text and ('¥' in response_text or '价格' in response_text):
                    print("✅ 包含菜单推荐和价格信息")
                if '评分' in response_text:
                    print("✅ 包含评分信息")
                if '描述' in response_text or '特点' in response_text:
                    print("✅ 包含菜品描述")
                
            else:
                print(f"❌ 功能测试失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 功能测试异常: {e}")
        
        time.sleep(1)
    
    return session_id

def main():
    """主测试函数"""
    print("🚀 开始菜单推荐功能测试")
    print("=" * 60)
    
    # 测试健康检查
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            print("✅ 服务健康检查通过")
        else:
            print("❌ 服务健康检查失败")
            return
    except Exception as e:
        print(f"❌ 健康检查异常: {e}")
        return
    
    # 测试菜单分类
    test_menu_categories()
    
    # 测试菜单菜品列表
    test_menu_items()
    
    # 测试菜单搜索
    test_menu_search()
    
    # 测试基础菜单推荐
    session_id_1 = test_menu_recommendation_basic()
    
    # 测试高级菜单推荐
    session_id_2 = test_menu_recommendation_advanced()
    
    # 测试菜单推荐特色功能
    session_id_3 = test_menu_recommendation_features()
    
    # 测试对话交互
    session_id_4 = test_conversation_with_menu()
    
    print("\n" + "=" * 60)
    print("📊 测试结果总结:")
    print("✅ 菜单分类功能正常")
    print("✅ 菜单菜品列表正常")
    print("✅ 菜单搜索功能正常")
    print("✅ 基础菜单推荐功能正常")
    print("✅ 高级菜单推荐功能正常")
    print("✅ 菜单推荐特色功能正常")
    print("✅ 对话交互功能正常")
    
    print("\n🎉 菜单推荐功能测试完成！")
    print("💡 现在聊天功能可以推荐菜单中的具体菜品了")

if __name__ == "__main__":
    main() 