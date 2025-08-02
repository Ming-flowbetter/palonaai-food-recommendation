from typing import List, Dict, Any, Optional
from app.models.schemas import MenuItem, SearchRequest, SearchResponse
import json

class MenuService:
    def __init__(self):
        # 初始化示例菜品数据
        self.menu_items = self._load_sample_data()
    
    def _load_sample_data(self) -> List[MenuItem]:
        """加载示例菜品数据"""
        sample_data = [
            {
                "id": "1",
                "name": "宫保鸡丁",
                "description": "经典川菜，鸡肉嫩滑，花生香脆，甜辣适中",
                "price": 28.0,
                "category": "川菜",
                "ingredients": ["鸡肉", "花生", "干辣椒", "葱姜蒜"],
                "allergens": ["花生"],
                "image_url": "https://example.com/kungpao-chicken.jpg",
                "is_seasonal": False,
                "rating": 4.5
            },
            {
                "id": "2",
                "name": "麻婆豆腐",
                "description": "嫩滑豆腐配麻辣肉末，下饭神器",
                "price": 22.0,
                "category": "川菜",
                "ingredients": ["豆腐", "猪肉末", "豆瓣酱", "花椒"],
                "allergens": [],
                "image_url": "https://example.com/mapo-tofu.jpg",
                "is_seasonal": False,
                "rating": 4.3
            },
            {
                "id": "3",
                "name": "糖醋里脊",
                "description": "外酥内嫩，酸甜可口，经典鲁菜",
                "price": 32.0,
                "category": "鲁菜",
                "ingredients": ["里脊肉", "淀粉", "糖", "醋"],
                "allergens": [],
                "image_url": "https://example.com/sweet-sour-pork.jpg",
                "is_seasonal": False,
                "rating": 4.6
            },
            {
                "id": "4",
                "name": "清蒸鲈鱼",
                "description": "新鲜鲈鱼清蒸，保持原汁原味",
                "price": 68.0,
                "category": "粤菜",
                "ingredients": ["鲈鱼", "姜丝", "葱丝", "蒸鱼豉油"],
                "allergens": ["鱼类"],
                "image_url": "https://example.com/steamed-bass.jpg",
                "is_seasonal": True,
                "rating": 4.7
            },
            {
                "id": "5",
                "name": "红烧肉",
                "description": "肥而不腻，入口即化，经典本帮菜",
                "price": 45.0,
                "category": "本帮菜",
                "ingredients": ["五花肉", "酱油", "糖", "料酒"],
                "allergens": [],
                "image_url": "https://example.com/braised-pork.jpg",
                "is_seasonal": False,
                "rating": 4.8
            },
            {
                "id": "6",
                "name": "水煮鱼",
                "description": "鲜嫩鱼片配麻辣汤底，川菜经典",
                "price": 58.0,
                "category": "川菜",
                "ingredients": ["草鱼", "豆芽", "辣椒", "花椒"],
                "allergens": ["鱼类"],
                "image_url": "https://example.com/boiled-fish.jpg",
                "is_seasonal": False,
                "rating": 4.4
            },
            {
                "id": "7",
                "name": "北京烤鸭",
                "description": "皮酥肉嫩，配甜面酱和葱丝",
                "price": 128.0,
                "category": "京菜",
                "ingredients": ["鸭子", "甜面酱", "葱丝", "薄饼"],
                "allergens": [],
                "image_url": "https://example.com/beijing-duck.jpg",
                "is_seasonal": False,
                "rating": 4.9
            },
            {
                "id": "8",
                "name": "小笼包",
                "description": "皮薄馅多，汤汁丰富，上海名点",
                "price": 18.0,
                "category": "点心",
                "ingredients": ["猪肉", "面粉", "姜汁", "高汤"],
                "allergens": [],
                "image_url": "https://example.com/xiaolongbao.jpg",
                "is_seasonal": False,
                "rating": 4.6
            }
        ]
        
        return [MenuItem(**item) for item in sample_data]
    
    def get_all_menu_items(self) -> List[MenuItem]:
        """获取所有菜品"""
        return self.menu_items
    
    def get_menu_item_by_id(self, item_id: str) -> Optional[MenuItem]:
        """根据ID获取菜品"""
        for item in self.menu_items:
            if item.id == item_id:
                return item
        return None
    
    def search_menu_items(self, request: SearchRequest) -> SearchResponse:
        """搜索菜品"""
        query = request.query.lower()
        results = []
        
        for item in self.menu_items:
            # 搜索名称、描述、类别、配料
            if (query in item.name.lower() or 
                query in item.description.lower() or 
                query in item.category.lower() or
                any(query in ingredient.lower() for ingredient in item.ingredients)):
                results.append(item)
        
        # 应用过滤器
        if request.filters:
            results = self._apply_filters(results, request.filters)
        
        # 限制结果数量
        results = results[:request.limit]
        
        return SearchResponse(
            results=results,
            total_count=len(results),
            query=request.query
        )
    
    def _apply_filters(self, items: List[MenuItem], filters: Dict[str, Any]) -> List[MenuItem]:
        """应用过滤器"""
        filtered_items = items
        
        # 价格过滤
        if "max_price" in filters:
            filtered_items = [item for item in filtered_items if item.price <= filters["max_price"]]
        
        if "min_price" in filters:
            filtered_items = [item for item in filtered_items if item.price >= filters["min_price"]]
        
        # 类别过滤
        if "category" in filters:
            filtered_items = [item for item in filtered_items if item.category == filters["category"]]
        
        # 过敏原过滤
        if "exclude_allergens" in filters:
            exclude_allergens = filters["exclude_allergens"]
            filtered_items = [item for item in filtered_items 
                           if not any(allergen in exclude_allergens for allergen in item.allergens)]
        
        # 季节性过滤
        if "seasonal_only" in filters and filters["seasonal_only"]:
            filtered_items = [item for item in filtered_items if item.is_seasonal]
        
        # 评分过滤
        if "min_rating" in filters:
            filtered_items = [item for item in filtered_items if item.rating >= filters["min_rating"]]
        
        return filtered_items
    
    def get_categories(self) -> List[str]:
        """获取所有菜品类别"""
        categories = set(item.category for item in self.menu_items)
        return list(categories)
    
    def get_seasonal_items(self) -> List[MenuItem]:
        """获取季节性菜品"""
        return [item for item in self.menu_items if item.is_seasonal]
    
    def get_popular_items(self, limit: int = 5) -> List[MenuItem]:
        """获取热门菜品（按评分排序）"""
        sorted_items = sorted(self.menu_items, key=lambda x: x.rating, reverse=True)
        return sorted_items[:limit] 