import React from 'react';
import { Link } from 'react-router-dom';
import { MessageCircle, Menu as MenuIcon, Star, Clock, Users } from 'lucide-react';

const Home: React.FC = () => {
  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="text-center py-16">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            PalonaAI
            <span className="text-primary-500"> 菜品推荐</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            基于您的喜好和偏好，为您推荐最适合的菜品。体验个性化的美食推荐服务。
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/chat"
              className="btn-primary text-lg px-8 py-3 flex items-center justify-center space-x-2"
            >
              <MessageCircle className="h-5 w-5" />
              <span>开始对话</span>
            </Link>
            <Link
              to="/menu"
              className="btn-secondary text-lg px-8 py-3 flex items-center justify-center space-x-2"
            >
              <MenuIcon className="h-5 w-5" />
              <span>浏览菜单</span>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            为什么选择PalonaAI
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="card text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <MessageCircle className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">智能对话</h3>
              <p className="text-gray-600">
                与PalonaAI助手自然对话，描述您的喜好，获得个性化推荐
              </p>
            </div>
            
            <div className="card text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Star className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">精准推荐</h3>
              <p className="text-gray-600">
                基于您的偏好和季节性因素，推荐最适合的菜品
              </p>
            </div>
            
            <div className="card text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Clock className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">即时响应</h3>
              <p className="text-gray-600">
                快速获取推荐结果，无需等待，提升用餐体验
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-16 bg-white">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            如何使用
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="w-12 h-12 bg-primary-500 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                1
              </div>
              <h3 className="text-lg font-semibold mb-2">描述喜好</h3>
              <p className="text-gray-600">告诉PalonaAI您喜欢的口味、菜品类型等</p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-primary-500 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                2
              </div>
              <h3 className="text-lg font-semibold mb-2">获得推荐</h3>
              <p className="text-gray-600">AI分析您的偏好，提供个性化推荐</p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-primary-500 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                3
              </div>
              <h3 className="text-lg font-semibold mb-2">浏览菜单</h3>
              <p className="text-gray-600">查看详细菜单信息和菜品详情</p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-primary-500 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                4
              </div>
              <h3 className="text-lg font-semibold mb-2">享受美食</h3>
              <p className="text-gray-600">根据推荐选择心仪的菜品</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-primary-50">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            准备开始您的美食之旅？
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            立即体验AI智能推荐，发现更多美味
          </p>
          <Link
            to="/chat"
            className="btn-primary text-lg px-8 py-3 inline-flex items-center space-x-2"
          >
            <MessageCircle className="h-5 w-5" />
            <span>开始对话</span>
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Home; 