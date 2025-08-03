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
            # 川菜系列
            {
                "id": "1",
                "name": "宫保鸡丁",
                "description": "经典川菜，选用新鲜鸡胸肉，配以花生、干辣椒爆炒，鸡肉嫩滑，花生香脆，甜辣适中，是川菜的代表作之一",
                "price": 38.0,
                "category": "川菜",
                "ingredients": ["鸡胸肉", "花生", "干辣椒", "葱姜蒜", "生抽", "老抽", "糖", "醋"],
                "allergens": ["花生"],
                "image_url": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=300&fit=crop&crop=entropy",
                "is_seasonal": False,
                "rating": 4.8
            },
            {
                "id": "2",
                "name": "麻婆豆腐",
                "description": "嫩滑豆腐配麻辣肉末，使用正宗郫县豆瓣酱，麻辣鲜香，下饭神器，是川菜中的经典家常菜",
                "price": 28.0,
                "category": "川菜",
                "ingredients": ["嫩豆腐", "猪肉末", "郫县豆瓣酱", "花椒", "辣椒", "蒜末", "葱花"],
                "allergens": [],
                "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop&crop=entropy",
                "is_seasonal": False,
                "rating": 4.6
            },
            {
                "id": "3",
                "name": "水煮鱼",
                "description": "鲜嫩鱼片配麻辣汤底，选用新鲜草鱼，配以豆芽、辣椒、花椒，麻辣鲜香，是川菜中的经典名菜",
                "price": 68.0,
                "category": "川菜",
                "ingredients": ["草鱼", "豆芽", "辣椒", "花椒", "蒜末", "葱花", "香菜"],
                "allergens": ["鱼类"],
                "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop&crop=entropy",
                "is_seasonal": False,
                "rating": 4.7
            },
            {
                "id": "4",
                "name": "回锅肉",
                "description": "肥而不腻，入口即化，选用五花肉，配以青椒、蒜苗爆炒，是川菜中的经典家常菜",
                "price": 42.0,
                "category": "川菜",
                "ingredients": ["五花肉", "青椒", "蒜苗", "豆瓣酱", "生抽", "老抽"],
                "allergens": [],
                "image_url": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=300&fit=crop&crop=entropy",
                "is_seasonal": False,
                "rating": 4.5
            },
            
            # 粤菜系列
            {
                "id": "5",
                "name": "清蒸鲈鱼",
                "description": "新鲜鲈鱼清蒸，保持原汁原味，配以姜丝、葱丝、蒸鱼豉油，鱼肉鲜嫩，汤汁鲜美",
                "price": 88.0,
                "category": "粤菜",
                "ingredients": ["鲈鱼", "姜丝", "葱丝", "蒸鱼豉油", "料酒", "盐"],
                "allergens": ["鱼类"],
                "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop&crop=entropy",
                "is_seasonal": True,
                "rating": 4.9
            },
            {
                "id": "6",
                "name": "白切鸡",
                "description": "选用三黄鸡，配以姜葱酱，鸡肉嫩滑，皮爽肉嫩，是粤菜中的经典名菜",
                "price": 58.0,
                "category": "粤菜",
                "ingredients": ["三黄鸡", "姜丝", "葱丝", "生抽", "香油", "盐"],
                "allergens": [],
                "image_url": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=300&fit=crop&crop=entropy",
                "is_seasonal": False,
                "rating": 4.7
            },
            {
                "id": "7",
                "name": "叉烧肉",
                "description": "选用五花肉，配以叉烧酱腌制，烤制而成，甜咸适中，肉质鲜嫩",
                "price": 48.0,
                "category": "粤菜",
                "ingredients": ["五花肉", "叉烧酱", "蜂蜜", "生抽", "老抽", "料酒"],
                "allergens": [],
                "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop&crop=entropy",
                "is_seasonal": False,
                "rating": 4.6
            },
            {
                "id": "8",
                "name": "虾仁炒蛋",
                "description": "新鲜虾仁配以嫩滑鸡蛋，简单美味，营养丰富，是粤菜中的经典家常菜",
                "price": 32.0,
                "category": "粤菜",
                "ingredients": ["虾仁", "鸡蛋", "葱花", "盐", "料酒", "生抽"],
                "allergens": ["虾类", "鸡蛋"],
                "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop&crop=entropy",
                "is_seasonal": False,
                "rating": 4.4
            },
            
            # 鲁菜系列
            {
                "id": "9",
                "name": "糖醋里脊",
                "description": "外酥内嫩，酸甜可口，选用里脊肉，配以糖醋汁，是鲁菜中的经典名菜",
                "price": 42.0,
                "category": "鲁菜",
                "ingredients": ["里脊肉", "淀粉", "糖", "醋", "番茄酱", "生抽"],
                "allergens": [],
                "image_url": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=300&fit=crop&crop=entropy",
                "is_seasonal": False,
                "rating": 4.8
            },
            {
                "id": "10",
                "name": "九转大肠",
                "description": "选用猪大肠，经过九道工序制作，口感独特，是鲁菜中的经典名菜",
                "price": 58.0,
                "category": "鲁菜",
                "ingredients": ["猪大肠", "葱姜蒜", "八角", "桂皮", "生抽", "老抽"],
                "allergens": [],
                "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop&crop=entropy",
                "is_seasonal": False,
                "rating": 4.3
            },
            
            # 本帮菜系列
            {
                "id": "11",
                "name": "红烧肉",
                "description": "肥而不腻，入口即化，选用五花肉，配以酱油、糖、料酒，是上海本帮菜的代表作",
                "price": 52.0,
                "category": "本帮菜",
                "ingredients": ["五花肉", "酱油", "糖", "料酒", "葱姜蒜", "八角"],
                "allergens": [],
                "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop&crop=entropy",
                "is_seasonal": False,
                "rating": 4.9
            },
            {
                "id": "12",
                "name": "小笼包",
                "description": "皮薄馅多，汤汁丰富，选用猪肉馅，配以姜汁、高汤，是上海名点",
                "price": 22.0,
                "category": "点心",
                "ingredients": ["猪肉", "面粉", "姜汁", "高汤", "葱花", "盐"],
                "allergens": [],
                "image_url": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=300&fit=crop&crop=entropy",
                "is_seasonal": False,
                "rating": 4.7
            },
            {
                "id": "13",
                "name": "生煎包",
                "description": "底部酥脆，顶部松软，选用猪肉馅，配以葱花，是上海经典早点",
                "price": 18.0,
                "category": "点心",
                "ingredients": ["猪肉", "面粉", "葱花", "盐", "生抽", "料酒"],
                "allergens": [],
                "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop&crop=entropy",
                "is_seasonal": False,
                "rating": 4.6
            },
            
            # 京菜系列
            {
                "id": "14",
                "name": "北京烤鸭",
                "description": "皮酥肉嫩，配甜面酱和葱丝，选用北京填鸭，经过特殊工艺烤制，是北京名菜",
                "price": 158.0,
                "category": "京菜",
                "ingredients": ["北京填鸭", "甜面酱", "葱丝", "薄饼", "黄瓜丝"],
                "allergens": [],
                "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop&crop=entropy",
                "is_seasonal": False,
                "rating": 4.9
            },
            {
                "id": "15",
                "name": "炸酱面",
                "description": "选用手工面条，配以炸酱、黄瓜丝、豆芽，是北京经典面食",
                "price": 28.0,
                "category": "面食",
                "ingredients": ["手工面条", "炸酱", "黄瓜丝", "豆芽", "葱花"],
                "allergens": [],
                "image_url": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=300&fit=crop&crop=entropy",
                "is_seasonal": False,
                "rating": 4.5
            },
            
            # 湘菜系列
            {
                "id": "16",
                "name": "剁椒鱼头",
                "description": "选用新鲜鱼头，配以剁椒、蒜末，麻辣鲜香，是湘菜中的经典名菜",
                "price": 78.0,
                "category": "湘菜",
                "ingredients": ["鱼头", "剁椒", "蒜末", "姜丝", "葱花", "生抽"],
                "allergens": ["鱼类"],
                "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop&crop=entropy",
                "is_seasonal": False,
                "rating": 4.7
            },
            {
                "id": "17",
                "name": "农家小炒肉",
                "description": "选用五花肉，配以青椒、蒜苗爆炒，香辣可口，是湘菜中的经典家常菜",
                "price": 38.0,
                "category": "湘菜",
                "ingredients": ["五花肉", "青椒", "蒜苗", "辣椒", "生抽", "老抽"],
                "allergens": [],
                "image_url": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=300&fit=crop&crop=entropy",
                "is_seasonal": False,
                "rating": 4.6
            },
            
            # 苏菜系列
            {
                "id": "18",
                "name": "松鼠桂鱼",
                "description": "选用桂鱼，经过特殊刀工处理，炸制而成，形似松鼠，酸甜可口",
                "price": 98.0,
                "category": "苏菜",
                "ingredients": ["桂鱼", "淀粉", "糖", "醋", "番茄酱", "生抽"],
                "allergens": ["鱼类"],
                "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop&crop=entropy",
                "is_seasonal": False,
                "rating": 4.8
            },
            {
                "id": "19",
                "name": "清炒时蔬",
                "description": "选用当季新鲜蔬菜，清炒而成，营养丰富，口感清爽",
                "price": 18.0,
                "category": "素菜",
                "ingredients": ["时令蔬菜", "蒜末", "盐", "生抽", "香油"],
                "allergens": [],
                "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop&crop=entropy",
                "is_seasonal": True,
                "rating": 4.3
            },
            
            # 汤品系列
            {
                "id": "20",
                "name": "酸菜鱼汤",
                "description": "选用新鲜鱼片，配以酸菜、辣椒，酸辣开胃，是川菜中的经典汤品",
                "price": 48.0,
                "category": "汤品",
                "ingredients": ["鱼片", "酸菜", "辣椒", "蒜末", "葱花", "香菜"],
                "allergens": ["鱼类"],
                "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop&crop=entropy",
                "is_seasonal": False,
                "rating": 4.6
            },
            {
                "id": "21",
                "name": "紫菜蛋花汤",
                "description": "选用紫菜、鸡蛋，简单美味，营养丰富，是经典家常汤品",
                "price": 12.0,
                "category": "汤品",
                "ingredients": ["紫菜", "鸡蛋", "葱花", "盐", "香油"],
                "allergens": ["鸡蛋"],
                "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop&crop=entropy",
                "is_seasonal": False,
                "rating": 4.2
            },
            
            # 甜点系列
            {
                "id": "22",
                "name": "红豆沙汤圆",
                "description": "选用糯米粉制作，配以红豆沙馅，甜而不腻，是经典甜点",
                "price": 16.0,
                "category": "甜点",
                "ingredients": ["糯米粉", "红豆沙", "糖", "水"],
                "allergens": [],
                "image_url": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=300&fit=crop&crop=entropy",
                "is_seasonal": False,
                "rating": 4.5
            },
            {
                "id": "23",
                "name": "杨枝甘露",
                "description": "选用芒果、西米露，配以椰奶，清爽可口，是港式经典甜点",
                "price": 22.0,
                "category": "甜点",
                "ingredients": ["芒果", "西米露", "椰奶", "糖", "水"],
                "allergens": [],
                "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop&crop=entropy",
                "is_seasonal": True,
                "rating": 4.7
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