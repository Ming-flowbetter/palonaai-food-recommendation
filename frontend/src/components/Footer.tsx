import React from 'react';
import { Utensils } from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Brand */}
          <div className="flex items-center space-x-2">
            <Utensils className="h-6 w-6 text-primary-400" />
            <span className="text-lg font-bold">PalonaAI菜品推荐</span>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4">快速链接</h3>
            <ul className="space-y-2">
              <li>
                <a href="/" className="text-gray-300 hover:text-white transition-colors">
                  首页
                </a>
              </li>
              <li>
                <a href="/menu" className="text-gray-300 hover:text-white transition-colors">
                  菜单
                </a>
              </li>
              <li>
                <a href="/chat" className="text-gray-300 hover:text-white transition-colors">
                  AI助手
                </a>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="text-lg font-semibold mb-4">联系我们</h3>
            <div className="space-y-2 text-gray-300">
              <p>邮箱: ming@flowbetter.io</p>
              <p>电话: +1 408-768-0315</p>
              <p>地址: San Jose, California, USA</p>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2024 PalonaAI菜品推荐. 保留所有权利.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 