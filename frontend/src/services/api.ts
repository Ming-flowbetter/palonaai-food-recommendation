import axios from 'axios';

// 在生产环境中使用相对路径，在开发环境中使用localhost
const API_BASE_URL = process.env.NODE_ENV === 'production' ? '' : 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 聊天API（增强版）
export const chatWithAI = async (message: string, sessionId?: string) => {
  try {
    const response = await api.post('/api/chat', {
      message,
      session_id: sessionId,
    });
    return response.data;
  } catch (error) {
    console.error('聊天API错误:', error);
    throw error;
  }
};

// 分析用户意图
export const analyzeIntent = async (message: string) => {
  try {
    const response = await api.post('/api/analyze-intent', { message });
    return response.data;
  } catch (error) {
    console.error('意图分析错误:', error);
    throw error;
  }
};

// 分析用户情感
export const analyzeEmotion = async (message: string) => {
  try {
    const response = await api.post('/api/analyze-emotion', { message });
    return response.data;
  } catch (error) {
    console.error('情感分析错误:', error);
    throw error;
  }
};

// 提取实体信息
export const extractEntities = async (message: string) => {
  try {
    const response = await api.post('/api/extract-entities', { message });
    return response.data;
  } catch (error) {
    console.error('实体提取错误:', error);
    throw error;
  }
};

// 提交用户反馈
export const submitFeedback = async (feedback: {
  session_id: string;
  message_id: string;
  rating: number;
  feedback_type: string;
  comment?: string;
}) => {
  try {
    const response = await api.post('/api/feedback', feedback);
    return response.data;
  } catch (error) {
    console.error('提交反馈错误:', error);
    throw error;
  }
};

// 获取对话指标
export const getConversationMetrics = async (sessionId: string) => {
  try {
    const response = await api.get(`/api/conversation-metrics/${sessionId}`);
    return response.data;
  } catch (error) {
    console.error('获取对话指标错误:', error);
    throw error;
  }
};

// 获取会话信息（增强版）
export const getSessionInfo = async (sessionId: string) => {
  try {
    const response = await api.get(`/api/session/${sessionId}`);
    return response.data;
  } catch (error) {
    console.error('获取会话信息错误:', error);
    throw error;
  }
};

// 清除会话
export const clearSession = async (sessionId: string) => {
  try {
    const response = await api.delete(`/api/session/${sessionId}`);
    return response.data;
  } catch (error) {
    console.error('清除会话错误:', error);
    throw error;
  }
};

// 获取菜单
export const getMenuItems = async () => {
  try {
    const response = await api.get('/api/menu');
    return response.data;
  } catch (error) {
    console.error('获取菜单错误:', error);
    throw error;
  }
};

// 搜索菜单
export const searchMenuItems = async (query: string, filters?: any) => {
  try {
    const response = await api.post('/api/search', {
      query,
      filters,
      limit: 20,
    });
    return response.data;
  } catch (error) {
    console.error('搜索菜单错误:', error);
    throw error;
  }
};

// 获取菜品详情
export const getMenuItem = async (id: string) => {
  try {
    const response = await api.get(`/api/menu/${id}`);
    return response.data;
  } catch (error) {
    console.error('获取菜品详情错误:', error);
    throw error;
  }
};

// 获取类别
export const getCategories = async () => {
  try {
    const response = await api.get('/api/categories');
    return response.data.categories;
  } catch (error) {
    console.error('获取类别错误:', error);
    throw error;
  }
};

// 获取季节性菜品
export const getSeasonalItems = async () => {
  try {
    const response = await api.get('/api/seasonal');
    return response.data.items;
  } catch (error) {
    console.error('获取季节性菜品错误:', error);
    throw error;
  }
};

// 获取热门菜品
export const getPopularItems = async (limit: number = 5) => {
  try {
    const response = await api.get(`/api/popular?limit=${limit}`);
    return response.data.items;
  } catch (error) {
    console.error('获取热门菜品错误:', error);
    throw error;
  }
};

// 获取推荐（增强版）
export const getRecommendations = async (userPreferences: any) => {
  try {
    const response = await api.post('/api/recommendations', {
      user_preferences: userPreferences,
    });
    return response.data;
  } catch (error) {
    console.error('获取推荐错误:', error);
    throw error;
  }
};

// 健康检查
export const healthCheck = async () => {
  try {
    const response = await api.get('/api/health');
    return response.data;
  } catch (error) {
    console.error('健康检查错误:', error);
    throw error;
  }
}; 