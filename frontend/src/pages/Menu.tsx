import React, { useState, useEffect } from 'react';
import { Search, Filter, Star, Clock } from 'lucide-react';
import { getMenuItems, searchMenuItems } from '../services/api';

interface MenuItem {
  id: string;
  name: string;
  description: string;
  price: number;
  category: string;
  ingredients: string[];
  allergens: string[];
  image_url?: string;
  is_seasonal: boolean;
  rating: number;
}

const Menu: React.FC = () => {
  const [menuItems, setMenuItems] = useState<MenuItem[]>([]);
  const [filteredItems, setFilteredItems] = useState<MenuItem[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [categories, setCategories] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadMenuItems();
  }, []);

  useEffect(() => {
    filterItems();
  }, [menuItems, searchQuery, selectedCategory]);

  const loadMenuItems = async () => {
    try {
      setIsLoading(true);
      const items = await getMenuItems();
      setMenuItems(items);
      
      // 提取所有类别
      const allCategories = [...new Set(items.map((item: MenuItem) => item.category))] as string[];
      setCategories(allCategories);
    } catch (error) {
      console.error('加载菜单失败:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const filterItems = () => {
    let filtered = menuItems;

    // 按搜索查询过滤
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(item =>
        item.name.toLowerCase().includes(query) ||
        item.description.toLowerCase().includes(query) ||
        item.category.toLowerCase().includes(query) ||
        item.ingredients.some(ingredient => ingredient.toLowerCase().includes(query))
      );
    }

    // 按类别过滤
    if (selectedCategory) {
      filtered = filtered.filter(item => item.category === selectedCategory);
    }

    setFilteredItems(filtered);
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      loadMenuItems();
      return;
    }

    try {
      setIsLoading(true);
      const results = await searchMenuItems(searchQuery);
      setFilteredItems(results.results);
    } catch (error) {
      console.error('搜索失败:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const clearFilters = () => {
    setSearchQuery('');
    setSelectedCategory('');
    setFilteredItems(menuItems);
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">菜单浏览</h1>
        <p className="text-gray-600">探索我们的精选菜品，找到您的最爱</p>
      </div>

      {/* Search and Filters */}
      <div className="card mb-8">
        <div className="flex flex-col md:flex-row gap-4">
          {/* Search */}
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                placeholder="搜索菜品、配料或类别..."
                className="input-field pl-10"
              />
            </div>
          </div>

          {/* Category Filter */}
          <div className="md:w-48">
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="input-field"
            >
              <option value="">所有类别</option>
              {categories.map(category => (
                <option key={category} value={category}>{category}</option>
              ))}
            </select>
          </div>

          {/* Buttons */}
          <div className="flex gap-2">
            <button
              onClick={handleSearch}
              className="btn-primary flex items-center space-x-1"
            >
              <Search className="h-4 w-4" />
              <span>搜索</span>
            </button>
            <button
              onClick={clearFilters}
              className="btn-secondary flex items-center space-x-1"
            >
              <Filter className="h-4 w-4" />
              <span>清除</span>
            </button>
          </div>
        </div>
      </div>

      {/* Results Count */}
      <div className="mb-6">
        <p className="text-gray-600">
          找到 {filteredItems.length} 道菜品
          {searchQuery && ` (搜索: "${searchQuery}")`}
          {selectedCategory && ` (类别: ${selectedCategory})`}
        </p>
      </div>

      {/* Menu Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredItems.map((item) => (
          <div key={item.id} className="card hover:shadow-md transition-shadow">
            {/* Image Placeholder */}
            <div className="w-full h-48 bg-gray-200 rounded-lg mb-4 flex items-center justify-center">
              <span className="text-gray-500 text-sm">菜品图片</span>
            </div>

            {/* Content */}
            <div className="space-y-3">
              <div className="flex justify-between items-start">
                <h3 className="text-lg font-semibold text-gray-900">{item.name}</h3>
                <span className="text-lg font-bold text-primary-600">¥{item.price}</span>
              </div>

              <p className="text-gray-600 text-sm">{item.description}</p>

              {/* Rating and Seasonal */}
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-1">
                  <Star className="h-4 w-4 text-yellow-400 fill-current" />
                  <span className="text-sm text-gray-600">{item.rating}</span>
                </div>
                {item.is_seasonal && (
                  <div className="flex items-center space-x-1 text-green-600">
                    <Clock className="h-4 w-4" />
                    <span className="text-sm">季节性</span>
                  </div>
                )}
              </div>

              {/* Category */}
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                  {item.category}
                </span>
                {item.allergens.length > 0 && (
                  <span className="text-xs text-red-500">
                    过敏原: {item.allergens.join(', ')}
                  </span>
                )}
              </div>

              {/* Ingredients */}
              <div>
                <p className="text-xs text-gray-500 mb-1">主要配料:</p>
                <div className="flex flex-wrap gap-1">
                  {item.ingredients.slice(0, 3).map((ingredient, index) => (
                    <span
                      key={index}
                      className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded"
                    >
                      {ingredient}
                    </span>
                  ))}
                  {item.ingredients.length > 3 && (
                    <span className="text-xs text-gray-400">+{item.ingredients.length - 3} 更多</span>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* No Results */}
      {filteredItems.length === 0 && !isLoading && (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <Search className="h-12 w-12 mx-auto" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">没有找到匹配的菜品</h3>
          <p className="text-gray-600">尝试调整搜索条件或清除过滤器</p>
        </div>
      )}
    </div>
  );
};

export default Menu; 