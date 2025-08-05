import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, RefreshCw, Info, ThumbsUp, ThumbsDown, MessageSquare, TrendingUp } from 'lucide-react';
import { chatWithAI, submitFeedback, getConversationMetrics } from '../services/api';
import AIAnalysis from '../components/AIAnalysis';

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
  intent_scores?: Record<string, number>;
  emotion_scores?: Record<string, number>;
  entities?: Record<string, any>;
  feedbackSubmitted?: boolean; // Added for feedback status
}

interface SessionInfo {
  session_id: string;
  user_preferences: Record<string, any>;
  conversation_length: number;
  interaction_count: number;
  intent_history?: Record<string, number>[];
  emotion_history?: Record<string, number>[];
  entity_history?: Record<string, any>[];
}

interface ConversationMetrics {
  session_id: string;
  total_messages: number;
  user_satisfaction_score: number;
  average_response_time: number;
  intent_accuracy: number;
  emotion_recognition_accuracy: number;
}

const Chat: React.FC = () => {
  // 从本地存储恢复会话ID
  const [sessionId, setSessionId] = useState<string>(() => {
    const savedSessionId = localStorage.getItem('chat_session_id');
    return savedSessionId || '';
  });

  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: '您好！我是您的PalonaAI菜品助手。请告诉我您喜欢的口味、菜品类型或者有什么特殊需求，我会为您推荐最适合的菜品。',
      isUser: false,
      timestamp: new Date()
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionInfo, setSessionInfo] = useState<SessionInfo | null>(null);
  const [showSessionInfo, setShowSessionInfo] = useState(false);
  const [showMetrics, setShowMetrics] = useState(false);
  const [metrics, setMetrics] = useState<ConversationMetrics | null>(null);
  const [selectedMessageId, setSelectedMessageId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 保存会话ID到本地存储
  useEffect(() => {
    if (sessionId) {
      localStorage.setItem('chat_session_id', sessionId);
    } else {
      localStorage.removeItem('chat_session_id');
    }
  }, [sessionId]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputText.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      isUser: true,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      // 传递当前的sessionId给API
      const response = await chatWithAI(inputText, sessionId);
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: response.response,
        isUser: false,
        timestamp: new Date(),
        intent_scores: response.intent_scores,
        emotion_scores: response.emotion_scores,
        entities: response.entities
      };

      setMessages(prev => [...prev, aiMessage]);
      
      // 更新会话信息
      if (response.session_id) {
        setSessionId(response.session_id);
        setSessionInfo({
          session_id: response.session_id,
          user_preferences: response.user_preferences || {},
          conversation_length: response.conversation_length || 0,
          interaction_count: response.interaction_count || 0,
          intent_history: sessionInfo?.intent_history || [],
          emotion_history: sessionInfo?.emotion_history || [],
          entity_history: sessionInfo?.entity_history || []
        });
      }
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: '抱歉，处理您的消息时出现了错误。请稍后再试。',
        isUser: false,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleNewSession = () => {
    setMessages([
      {
        id: '1',
        text: '您好！我是您的PalonaAI菜品助手。请告诉我您喜欢的口味、菜品类型或者有什么特殊需求，我会为您推荐最适合的菜品。',
        isUser: false,
        timestamp: new Date()
      }
    ]);
    setSessionId('');
    setSessionInfo(null);
    setMetrics(null);
    // 清除本地存储的会话ID
    localStorage.removeItem('chat_session_id');
  };

  const handleFeedback = async (messageId: string, rating: number, feedbackType: string) => {
    if (!sessionId) return;

    try {
      await submitFeedback({
        session_id: sessionId,
        message_id: messageId,
        rating,
        feedback_type: feedbackType
      });
      
      // 更新消息显示反馈状态
      setMessages(prev => prev.map(msg => 
        msg.id === messageId 
          ? { ...msg, feedbackSubmitted: true }
          : msg
      ));
    } catch (error) {
      console.error('提交反馈失败:', error);
    }
  };

  const loadMetrics = async () => {
    if (!sessionId) return;

    try {
      const metricsData = await getConversationMetrics(sessionId);
      setMetrics(metricsData);
    } catch (error) {
      console.error('获取对话指标失败:', error);
    }
  };

  const formatPreferences = (preferences: Record<string, any>) => {
    const preferenceMap: Record<string, any> = {
      taste_preference: {
        spicy: '重口味',
        mild: '清淡口味'
      },
      cuisine_preference: {
        chinese: '中餐',
        western: '西餐',
        japanese: '日料'
      },
      budget_preference: {
        low: '经济实惠',
        high: '高档精致'
      }
    };

    return Object.entries(preferences).map(([key, value]) => {
      const label = preferenceMap[key]?.[value as string] || value;
      return `${key.replace('_', ' ')}: ${label}`;
    }).join(', ');
  };



  return (
    <div className="max-w-4xl mx-auto">
      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-2">
            <Bot className="h-6 w-6 text-primary-500" />
            <h1 className="text-2xl font-bold text-gray-900">PalonaAI菜品助手</h1>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setShowMetrics(!showMetrics)}
              className="btn-secondary"
              title="对话指标"
            >
              <TrendingUp className="h-4 w-4" />
            </button>
            <button
              onClick={() => setShowSessionInfo(!showSessionInfo)}
              className="btn-secondary"
              title="会话信息"
            >
              <Info className="h-4 w-4" />
            </button>
            <button
              onClick={handleNewSession}
              className="btn-secondary"
              title="开始新对话"
            >
              <RefreshCw className="h-4 w-4" />
            </button>
          </div>
        </div>

        {/* 对话指标 */}
        {showMetrics && metrics && (
          <div className="mb-4 p-4 bg-purple-50 rounded-lg">
            <h3 className="font-semibold text-purple-900 mb-2">📊 对话指标</h3>
            <div className="text-sm text-purple-800 space-y-1">
              <p>总消息数: {metrics.total_messages}</p>
              <p>用户满意度: {(metrics.user_satisfaction_score * 100).toFixed(1)}%</p>
              <p>平均响应时间: {metrics.average_response_time.toFixed(2)}秒</p>
              <p>意图识别准确率: {(metrics.intent_accuracy * 100).toFixed(1)}%</p>
              <p>情感识别准确率: {(metrics.emotion_recognition_accuracy * 100).toFixed(1)}%</p>
            </div>
          </div>
        )}

        {/* Session Info */}
        {showSessionInfo && sessionInfo && (
          <div className="mb-4 p-4 bg-blue-50 rounded-lg">
            <h3 className="font-semibold text-blue-900 mb-2">📊 会话信息</h3>
            <div className="text-sm text-blue-800 space-y-1">
              <p>会话ID: {sessionInfo.session_id}</p>
              <p>对话轮数: {sessionInfo.conversation_length}</p>
              <p>交互次数: {sessionInfo.interaction_count}</p>
              {Object.keys(sessionInfo.user_preferences).length > 0 && (
                <p>用户偏好: {formatPreferences(sessionInfo.user_preferences)}</p>
              )}
            </div>
          </div>
        )}

        {/* 会话状态显示 */}
        {sessionId && (
          <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="flex items-center space-x-2">
              <Info className="h-4 w-4 text-blue-500" />
              <span className="text-sm text-blue-700">
                会话已连接 (ID: {sessionId.substring(0, 8)}...)
                {sessionInfo && ` • 对话长度: ${sessionInfo.conversation_length} • 交互次数: ${sessionInfo.interaction_count}`}
              </span>
            </div>
          </div>
        )}

        {/* Messages */}
        <div className="h-96 overflow-y-auto mb-6 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`flex items-start space-x-2 max-w-xs lg:max-w-md ${
                  message.isUser ? 'flex-row-reverse space-x-reverse' : ''
                }`}
              >
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center ${
                    message.isUser
                      ? 'bg-primary-500 text-white'
                      : 'bg-gray-200 text-gray-600'
                  }`}
                >
                  {message.isUser ? (
                    <User className="h-4 w-4" />
                  ) : (
                    <Bot className="h-4 w-4" />
                  )}
                </div>
                <div
                  className={`px-4 py-2 rounded-lg ${
                    message.isUser
                      ? 'bg-primary-500 text-white'
                      : 'bg-gray-100 text-gray-900'
                  }`}
                >
                  <p className="text-sm">{message.text}</p>
                  
                  {/* 使用AI分析组件 */}
                  {!message.isUser && (
                    <AIAnalysis
                      intent_scores={message.intent_scores}
                      emotion_scores={message.emotion_scores}
                      entities={message.entities}
                      showDetails={false}
                    />
                  )}
                  
                  <p
                    className={`text-xs mt-1 ${
                      message.isUser ? 'text-primary-100' : 'text-gray-500'
                    }`}
                  >
                    {message.timestamp.toLocaleTimeString()}
                  </p>
                  
                  {/* 反馈按钮 */}
                  {!message.isUser && !message.feedbackSubmitted && (
                    <div className="flex space-x-2 mt-2">
                      <button
                        onClick={() => handleFeedback(message.id, 5, 'positive')}
                        className="text-green-600 hover:text-green-800 text-xs"
                        title="好评"
                      >
                        <ThumbsUp className="h-3 w-3" />
                      </button>
                      <button
                        onClick={() => handleFeedback(message.id, 1, 'negative')}
                        className="text-red-600 hover:text-red-800 text-xs"
                        title="差评"
                      >
                        <ThumbsDown className="h-3 w-3" />
                      </button>
                    </div>
                  )}
                  
                  {message.feedbackSubmitted && (
                    <div className="text-xs text-green-600 mt-1">
                      ✓ 感谢您的反馈
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="flex justify-start">
              <div className="flex items-start space-x-2">
                <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center">
                  <Bot className="h-4 w-4 text-gray-600" />
                </div>
                <div className="bg-gray-100 px-4 py-2 rounded-lg">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="输入您的消息..."
            className="input-field flex-1"
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputText.trim() || isLoading}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="h-4 w-4" />
          </button>
        </div>

        {/* Tips */}
        <div className="mt-6 p-4 bg-blue-50 rounded-lg">
          <h3 className="font-semibold text-blue-900 mb-2">💡 对话提示</h3>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• "我喜欢辣的食物，有什么推荐吗？"</li>
            <li>• "我想尝试川菜，有什么特色菜？"</li>
            <li>• "我对海鲜过敏，有什么安全的选项？"</li>
            <li>• "今天有什么季节性推荐？"</li>
            <li>• "根据我之前的偏好，还有什么推荐？"</li>
            <li>• "这个菜的营养价值怎么样？"</li>
            <li>• "比较一下这两个菜的区别"</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Chat; 