import os
import sys

# 添加backend目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# 导入FastAPI应用
from main import app

# 创建WSGI应用
application = app 