# Django项目前后端分离系统设计日志

------

## 初步策略

### 改视图为 JSON API 接口

```python
# views.py
def car_detail(request, car_id):
    car = Car.objects.get(id=car_id)
    return render(request, 'users/car_detail.html', {'car': car})
```

 **改成 JSON API 形式：**

```python
from django.http import JsonResponse
from .models import Car

def car_detail_api(request, car_id):
    try:
        car = Car.objects.get(id=car_id)
        return JsonResponse({
            "id": car.id,
            "brand": car.brand,
            "model": car.model,
            "price": car.price,
            "image": car.image.url if car.image else None,
            "description": car.description,
        })
    except Car.DoesNotExist:
        return JsonResponse({"error": "Car not found"}, status=404)
```

------

开启跨域支持（CORS）

如果你前端用 Vite 跑在 `localhost:5173`，而 Django 是 `localhost:8000`，那么需要开启跨域支持。

安装 CORS 组件：

```bash
pip install django-cors-headers
```

修改 `settings.py`：

```python
INSTALLED_APPS = [
    ...
    'cors headers',
]

MIDDLEWARE = [
    'cors headers.middleware.CorsMiddleware',
    ...
]

# 开放所有域名跨域（开发环境用）
CORS_ALLOW_ALL_ORIGINS = True

# 生产环境建议只允许特定前端域名：
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:5173",
#     "https://your-frontend-domain.com",
# ]
```

------

### 使用 Django REST framework 暴露接口

有多个模型和复杂接口，建议使用 **DRF（Django REST framework）**：

1. 安装：

```bash
pip install djangorestframework
```

2. 注册到 `settings.py`

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

------

3. 写一个序列化器（Serializer）

```python
# users/serializers.py
from rest_framework import serializers
from .models import Car

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'
```

------

4. 写 API 视图（基于类）

```python
# users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Car
from .serializers import CarSerializer

class CarDetailAPIView(APIView):
    def get(self, request, car_id):
        try:
            car = Car.objects.get(id=car_id)
            serializer = CarSerializer(car)
            return Response(serializer.data)
        except Car.DoesNotExist:
            return Response({"error": "Car not found"}, status=status.HTTP_404_NOT_FOUND)
```

------

5. 添加到 `urls.py`

```python
# users/urls.py
from django.urls import path
from .views import CarDetailAPIView

urlpatterns = [
    path('api/cars/<int:car_id>/', CarDetailAPIView.as_view(), name='car-detail-api'),
]
```

前端现在可以通过 `http://localhost:8000/api/cars/1/` 访问车辆详情接口。

------

###  其他可选做法

- 批量列表接口也可以写一个 `ListAPIView`
- 用 `ViewSet` 自动生成增删改查接口（后期可以教你）
- 用户登录也可以写成 DRF 的 API（比如 `api/login/`）

------

## 序列化器

序列化器（Serializer）是计算机编程中用于**将复杂数据结构（如对象、数组、字典等）转换为可存储或传输格式（如字符串、字节流）**的工具，同时支持反向操作（反序列化）。以下是核心要点：

---

### **1. 核心功能**
• **序列化**：将内存中的对象转换为JSON、XML等格式，便于网络传输或持久化存储。
• **反序列化**：将接收的数据（如JSON）还原为程序可操作的对象或数据结构。
• **数据校验**：验证输入数据的合法性（如字段长度、类型等）。

---

### **2. 主要特性**
• **跨平台性**：支持不同编程语言和系统间的数据交换（如JSON、Protocol Buffers）。
• **性能优化**：高效处理大量数据（如Protocol Buffers二进制格式）。
• **安全性**：防止恶意数据注入（如JWT的签名加密）。

---

### **3. 应用场景**
• **Web API开发**：如Django REST框架中，序列化器将模型（Model）转换为JSON响应。
• **数据存储**：将对象序列化后保存到数据库或文件。
• **微服务通信**：服务间通过序列化格式传输数据。

---

### **4. 示例（Django REST框架）**
```python
from rest_framework import serializers

class BookSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=32)
    price = serializers.DecimalField(max_digits=5, decimal_places=2)
```
• **序列化**：`BookSerializer(instance=book).data` → 输出JSON。
• **反序列化**：`BookSerializer(data=request.data)` → 验证并保存数据。

---

### **5. 常见格式**
• **文本格式**：JSON（可读性强）、XML。
• **二进制格式**：Protocol Buffers（高效）、MessagePack（紧凑）。

序列化器是现代软件开发中数据交互的核心组件，尤其在分布式系统和高性能服务中不可或缺。

## 设计序列化器

```
# 安装Django REST框架的MongoDB支持
pip install django-rest-framework-mongoengine -i https://pypi.tuna.tsinghua.edu.cn/simple
```

users/serializers.py

```
# 写一个序列化器
# users/serializers.py
from rest_framework_mongoengine import serializers
from .models import User, UsedCar, CheckingCar, Admin, Order


class UserSerializer(serializers.DocumentSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UsedCarSerializer(serializers.DocumentSerializer):
    class Meta:
        model = UsedCar
        fields = '__all__'


class CheckingCarSerializer(serializers.DocumentSerializer):
    class Meta:
        model = CheckingCar
        fields = '__all__'


class AdminSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Admin
        fields = '__all__'


class OrderSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Order
        fields = '__all__'

```

## api设置

### 碰到的问题

Django REST Framework（DRF）标准的 `ModelViewSet` 和 `router.register` 是为 **Django ORM 的模型** 设计的。而现在用的是 **MongoEngine + rest_framework_mongoengine**。

因此：

```
router.register(r'api/users', api_views.UserViewSet)
```

这行会调用 `get_default_basename(viewset)`，进而访问：

```
queryset.model._meta.object_name.lower()
```

但 **MongoEngine 的 queryset 没有 `.model` 属性**，所以报错：

```
AttributeError: 'QuerySet' object has no attribute 'model'
```

------

解决方案

你只需要 **手动添加 `basename` 参数**，告诉 DRF 这个视图集的名字是什么：

修改路由注册如下：

```
python复制编辑router.register(r'api/users', api_views.UserViewSet, basename='user')
router.register(r'api/cars', api_views.UsedCarViewSet, basename='car')
router.register(r'api/checking_cars', api_views.CheckingCarViewSet, basename='checkingcar')
router.register(r'api/admins', api_views.AdminViewSet, basename='admin')
router.register(r'api/orders', api_views.OrderViewSet, basename='order')
```

这样就绕过了 `queryset.model._meta.object_name` 的推断过程，DRF 不再试图访问不存在的 `.model` 属性。

------

小提示

- **MongoEngine 不兼容 Django ORM 的一些内部结构**，所以很多地方都需要手动调整。
- `basename` 是 DRF 内部为生成路由名称（如 `user-list`, `user-detail`）所需的别名。

## 前端基本架构设计

采用vite搭建前端的基本结构

```
npm create vite@latest my-vue-app --template vue
cd my-vue-app
npm install

my-vue-app/
├── node_modules/
├── public/
│   └── index.html
├── src/
│   ├── assets/
│   ├── components/
│   ├── App.vue
│   ├── main.js
│   └── styles/
├── index.html
├── package.json
├── vite.config.js
└── README.md

npm run dev

npm install vue-router

```



# 后端api设计以及对应的前端

