import React from 'react';
import { Brain, Heart, Tag } from 'lucide-react';

interface AIAnalysisProps {
  intent_scores?: Record<string, number>;
  emotion_scores?: Record<string, number>;
  entities?: Record<string, any>;
  showDetails?: boolean;
}

const AIAnalysis: React.FC<AIAnalysisProps> = ({
  intent_scores,
  emotion_scores,
  entities,
  showDetails = false
}) => {
  const getIntentColor = (intent: string) => {
    const colors: Record<string, string> = {
      recommendation: 'bg-blue-100 text-blue-800 border-blue-200',
      information: 'bg-green-100 text-green-800 border-green-200',
      comparison: 'bg-purple-100 text-purple-800 border-purple-200',
      preference: 'bg-yellow-100 text-yellow-800 border-yellow-200',
      health: 'bg-red-100 text-red-800 border-red-200',
      allergy: 'bg-orange-100 text-orange-800 border-orange-200',
      seasonal: 'bg-teal-100 text-teal-800 border-teal-200',
      budget: 'bg-indigo-100 text-indigo-800 border-indigo-200'
    };
    return colors[intent] || 'bg-gray-100 text-gray-800 border-gray-200';
  };

  const getEmotionColor = (emotion: string) => {
    const colors: Record<string, string> = {
      positive: 'bg-green-100 text-green-800 border-green-200',
      negative: 'bg-red-100 text-red-800 border-red-200',
      neutral: 'bg-gray-100 text-gray-800 border-gray-200',
      excited: 'bg-yellow-100 text-yellow-800 border-yellow-200',
      worried: 'bg-orange-100 text-orange-800 border-orange-200'
    };
    return colors[emotion] || 'bg-gray-100 text-gray-800 border-gray-200';
  };

  const getEntityColor = (entityType: string) => {
    const colors: Record<string, string> = {
      cuisine_types: 'bg-purple-100 text-purple-800 border-purple-200',
      taste_preferences: 'bg-pink-100 text-pink-800 border-pink-200',
      dietary_restrictions: 'bg-red-100 text-red-800 border-red-200',
      budget_range: 'bg-indigo-100 text-indigo-800 border-indigo-200',
      meal_type: 'bg-teal-100 text-teal-800 border-teal-200',
      cooking_method: 'bg-orange-100 text-orange-800 border-orange-200'
    };
    return colors[entityType] || 'bg-gray-100 text-gray-800 border-gray-200';
  };

  const formatEntityValue = (value: any): string => {
    if (Array.isArray(value)) {
      return value.join(', ');
    }
    if (typeof value === 'object' && value !== null) {
      return Object.entries(value)
        .map(([k, v]) => `${k}: ${v}`)
        .join(', ');
    }
    return String(value);
  };

  if (!intent_scores && !emotion_scores && !entities) {
    return null;
  }

  return (
    <div className="mt-3 space-y-2">
      {/* 意图分析 */}
      {intent_scores && Object.keys(intent_scores).length > 0 && (
        <div className="flex items-center space-x-2">
          <Brain className="h-4 w-4 text-blue-600" />
          <div className="flex flex-wrap gap-1">
            {Object.entries(intent_scores)
              .filter(([_, score]) => score > 0.1)
              .sort(([_, a], [__, b]) => b - a)
              .map(([intent, score]) => (
                <span
                  key={intent}
                  className={`px-2 py-1 rounded-full text-xs border ${getIntentColor(intent)}`}
                  title={`意图: ${intent}, 置信度: ${(score * 100).toFixed(1)}%`}
                >
                  {intent}: {(score * 100).toFixed(0)}%
                </span>
              ))}
          </div>
        </div>
      )}

      {/* 情感分析 */}
      {emotion_scores && Object.keys(emotion_scores).length > 0 && (
        <div className="flex items-center space-x-2">
          <Heart className="h-4 w-4 text-red-600" />
          <div className="flex flex-wrap gap-1">
            {Object.entries(emotion_scores)
              .filter(([_, score]) => score > 0.1)
              .sort(([_, a], [__, b]) => b - a)
              .map(([emotion, score]) => (
                <span
                  key={emotion}
                  className={`px-2 py-1 rounded-full text-xs border ${getEmotionColor(emotion)}`}
                  title={`情感: ${emotion}, 强度: ${(score * 100).toFixed(1)}%`}
                >
                  {emotion}: {(score * 100).toFixed(0)}%
                </span>
              ))}
          </div>
        </div>
      )}

      {/* 实体提取 */}
      {entities && Object.keys(entities).length > 0 && showDetails && (
        <div className="flex items-start space-x-2">
          <Tag className="h-4 w-4 text-green-600 mt-1" />
          <div className="flex flex-wrap gap-1">
            {Object.entries(entities)
              .filter(([_, value]) => value && (Array.isArray(value) ? value.length > 0 : true))
              .map(([entityType, value]) => (
                <span
                  key={entityType}
                  className={`px-2 py-1 rounded-full text-xs border ${getEntityColor(entityType)}`}
                  title={`实体类型: ${entityType}`}
                >
                  {entityType}: {formatEntityValue(value)}
                </span>
              ))}
          </div>
        </div>
      )}

      {/* 详细分析结果 */}
      {showDetails && (intent_scores || emotion_scores || entities) && (
        <div className="mt-3 p-3 bg-gray-50 rounded-lg">
          <h4 className="text-sm font-semibold text-gray-700 mb-2">详细分析</h4>
          
          {intent_scores && (
            <div className="mb-2">
              <h5 className="text-xs font-medium text-gray-600 mb-1">意图分析</h5>
              <div className="space-y-1">
                {Object.entries(intent_scores)
                  .sort(([_, a], [__, b]) => b - a)
                  .map(([intent, score]) => (
                    <div key={intent} className="flex justify-between text-xs">
                      <span className="capitalize">{intent}</span>
                      <span className="text-gray-500">{(score * 100).toFixed(1)}%</span>
                    </div>
                  ))}
              </div>
            </div>
          )}

          {emotion_scores && (
            <div className="mb-2">
              <h5 className="text-xs font-medium text-gray-600 mb-1">情感分析</h5>
              <div className="space-y-1">
                {Object.entries(emotion_scores)
                  .sort(([_, a], [__, b]) => b - a)
                  .map(([emotion, score]) => (
                    <div key={emotion} className="flex justify-between text-xs">
                      <span className="capitalize">{emotion}</span>
                      <span className="text-gray-500">{(score * 100).toFixed(1)}%</span>
                    </div>
                  ))}
              </div>
            </div>
          )}

          {entities && (
            <div>
              <h5 className="text-xs font-medium text-gray-600 mb-1">实体提取</h5>
              <div className="space-y-1">
                {Object.entries(entities)
                  .filter(([_, value]) => value && (Array.isArray(value) ? value.length > 0 : true))
                  .map(([entityType, value]) => (
                    <div key={entityType} className="flex justify-between text-xs">
                      <span className="capitalize">{entityType}</span>
                      <span className="text-gray-500">{formatEntityValue(value)}</span>
                    </div>
                  ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default AIAnalysis; 