# users/api_views.py
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework_mongoengine.viewsets import ModelViewSet
from sklearn.feature_extraction.text import TfidfVectorizer
from .models import User, UsedCar, CheckingCar, Admin, Order
from .serializers import UserSerializer, UsedCarSerializer, CheckingCarSerializer, AdminSerializer, OrderSerializer, AdminCreationSerializer, AdminLoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import os
import hashlib
from django.contrib.auth.hashers import make_password, check_password
import mongoengine
import requests
from django.core.paginator import Paginator
from django.http import HttpResponse
from .forms import UserCreationForm
from .forms import UserLoginForm
from .forms import CarSearchForm
from .forms import AddCheckingCarForm
from .forms import AdminCreationForm
from .forms import AdminLoginForm
from .models import User
from .models import Admin
from .models import UsedCar
from .models import CheckingCar
from .models import Order
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import BallTree
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
import os
from django.conf import settings
from django.http import JsonResponse
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from bson import ObjectId
from django.http import HttpRequest
import datetime
from collections import Counter

# 资源型
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UsedCarViewSet(ModelViewSet):
    queryset = UsedCar.objects.all()
    serializer_class = UsedCarSerializer


class CheckingCarViewSet(ModelViewSet):
    queryset = CheckingCar.objects.all()
    serializer_class = CheckingCarSerializer


class AdminViewSet(ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


# recommend api
class RecommendCarsAPI(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.using('all_db').get(id=user_id)
            liked_cars = user.liked_cars

            all_cars = UsedCar.objects.using('all_db').all()

            if not liked_cars:
                recent_cars = all_cars.order_by('-id')[:50]
                return Response({
                    'status': 'success',
                    'recommendations': [str(car.id) for car in recent_cars]
                })

            content_based_recs = get_content_based_recommendations(liked_cars, all_cars)
            collaborative_recs = get_collaborative_recommendations(user_id, liked_cars)
            final_recommendations = merge_recommendations(content_based_recs, collaborative_recs)

            return Response({
                'status': 'success',
                'recommendations': final_recommendations
            })

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

def recommend_cars(request, user_id):
    try:
        user = User.objects.using('all_db').get(id=user_id)
        liked_cars = user.liked_cars

        all_cars = UsedCar.objects.using('all_db').all()

        # 如果用户没有喜欢的车辆，返回最新上架的车辆
        if not liked_cars:
            recent_cars = all_cars.order_by('-id')[:50]
            return JsonResponse({
                'status': 'success',
                'recommendations': [str(car.id) for car in recent_cars]  # 将 ObjectId 转换为字符串
            })

        content_based_recs = get_content_based_recommendations(liked_cars, all_cars)
        collaborative_recs = get_collaborative_recommendations(user_id, liked_cars)
        # 合并两种推荐结果
        final_recommendations = merge_recommendations(content_based_recs, collaborative_recs)

        return JsonResponse({
            'status': 'success',
            'recommendations': [str(car_id) for car_id in final_recommendations]  # 将推荐的车辆 ID 转换为字符串
        })

    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)


def get_content_based_recommendations(liked_cars, all_cars, limit=25):
    """基于内容的推荐算法"""
    if not liked_cars:
        return []
    car_features = []
    car_ids = []
    for car in all_cars:
        feature_text = f"{car.Brand} {car.Color} {car.Configuration}"
        car_features.append(feature_text)
        car_ids.append(str(car.id))
    tfidf = TfidfVectorizer(stop_words='english')
    feature_matrix = tfidf.fit_transform(car_features)
    similarity_matrix = cosine_similarity(feature_matrix)
    liked_indices = [car_ids.index(str(car_id)) for car_id in liked_cars if str(car_id) in car_ids]
    if not liked_indices:
        return []
    mean_similarities = np.mean([similarity_matrix[idx] for idx in liked_indices], axis=0)
    # 获取推荐（排除已喜欢的车辆）
    recommended_indices = np.argsort(mean_similarities)[::-1]
    recommendations = []
    for idx in recommended_indices:
        car_id = car_ids[idx]
        if car_id not in [str(x) for x in liked_cars]:
            recommendations.append(car_id)
            if len(recommendations) >= limit:
                break
    return recommendations


def get_collaborative_recommendations(user_id, liked_cars, limit=25):
    """基于用户的协同过滤推荐算法"""
    all_users = User.objects.using('all_db').all()
    user_car_matrix = {}
    all_cars = set()
    for user in all_users:
        user_car_matrix[str(user.id)] = set(user.liked_cars)
        all_cars.update(user.liked_cars)
    current_user_cars = set(liked_cars)
    user_similarities = {}
    for other_user_id, other_user_cars in user_car_matrix.items():
        if other_user_id != str(user_id):
            intersection = len(current_user_cars & other_user_cars)
            union = len(current_user_cars | other_user_cars)
            similarity = intersection / union if union > 0 else 0
            user_similarities[other_user_id] = similarity
    similar_users = sorted(user_similarities.items(),
                           key=lambda x: x[1],
                           reverse=True)[:5]
    recommended_cars = set()
    for similar_user_id, _ in similar_users:
        recommended_cars.update(user_car_matrix[similar_user_id])
    # 排除当前用户已喜欢的车辆
    recommended_cars = list(recommended_cars - set(liked_cars))
    return recommended_cars[:limit]


def merge_recommendations(content_recs, collaborative_recs):
    weighted_scores = {}
    for i, car_id in enumerate(content_recs):
        weighted_scores[car_id] = 0.5 * (1 - i / len(content_recs))
    for i, car_id in enumerate(collaborative_recs):
        if car_id in weighted_scores:
            weighted_scores[car_id] += 0.5 * (1 - i / len(collaborative_recs))
        else:
            weighted_scores[car_id] = 0.5 * (1 - i / len(collaborative_recs))
    # 按得分排序并返回推荐
    sorted_recs = sorted(weighted_scores.items(), key=lambda x: x[1], reverse=True)
    return [car_id for car_id, _ in sorted_recs[:50]]


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            request.session['user_id'] = str(user.id)
            return Response({'message': '注册成功'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        login_name = request.data.get('login_name')
        passwd = request.data.get('passwd')

        if not login_name or not passwd:
            return Response({'error': '用户名和密码不能为空'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(login_name=login_name)
            if check_password(passwd, user.passwd):
                request.session['user_id'] = str(user.id)
                return Response({'message': '登录成功'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': '密码错误'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'error': '用户名不存在'}, status=status.HTTP_404_NOT_FOUND)


class LogoutAPIView(APIView):
    def post(self, request):
        request.session.flush()
        return Response({'message': '已退出登录'}, status=status.HTTP_200_OK)


class MeAPIView(APIView):
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({'error': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user)
            return Response({'user': serializer.data})
        except User.DoesNotExist:
            return Response({'error': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)


class SearchCarsAPIView(APIView):
    def get(self, request):
        cars = UsedCar.objects.using('all_db')
        params = request.GET

        # 筛选条件
        brand = params.get('brand')
        year = params.get('year')
        price_min = params.get('price_min')
        price_max = params.get('price_max')
        color = params.get('color')
        mileage = params.get('mileage')
        configuration = params.get('configuration')
        condition_description = params.get('condition_description')

        if brand:
            cars = cars.filter(Brand__icontains=brand)
        if year:
            try:
                cars = cars.filter(Year__gt=int(year))
            except ValueError:
                pass
        if price_min:
            try:
                cars = cars.filter(Price__gte=float(price_min))
            except ValueError:
                pass
        if price_max:
            try:
                cars = cars.filter(Price__lte=float(price_max))
            except ValueError:
                pass
        if color:
            cars = cars.filter(Color__icontains=color)
        if mileage:
            try:
                cars = cars.filter(Mileage__lte=int(mileage))
            except ValueError:
                pass
        if configuration:
            cars = cars.filter(Configuration__icontains=configuration)
        if condition_description:
            cars = cars.filter(ConditionDescription__icontains=condition_description)

        # 保存搜索记录
        user_id = request.session.get('user_id')
        if user_id:
            try:
                user = User.objects.using('all_db').get(id=user_id)
                search_ids = [car.id for car in cars]
                user.searched_cars.extend(search_ids)
                user.save()
            except User.DoesNotExist:
                pass

        # 分页
        paginator = Paginator(cars, 20)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        serialized_data = UsedCarSerializer(page_obj.object_list, many=True).data

        return Response({
            'results': serialized_data,
            'page': page_obj.number,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count,
        }, status=status.HTTP_200_OK)


class CarPhotoAPIView(APIView):
    def get(self, request, car_id):
        try:
            car = UsedCar.objects.using('all_db').get(id=car_id)
            if car.PhotoUrl:
                photo_path = os.path.join(settings.MEDIA_ROOT, car.PhotoUrl)
                with open(photo_path, 'rb') as photo_file:
                    return HttpResponse(photo_file.read(), content_type='image/jpg')
            else:
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        except UsedCar.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)


class CarDetailAPIView(APIView):
    def get(self, request, car_id):
        try:
            car = UsedCar.objects.using('all_db').get(id=car_id)
            serialized_car = UsedCarSerializer(car).data
            user_id = request.session.get('user_id')
            is_liked = False
            if user_id:
                user = User.objects.using('all_db').get(id=user_id)
                if car.id in user.liked_cars:
                    is_liked = True
            return Response({
                'car': serialized_car,
                'is_liked': is_liked
            }, status=status.HTTP_200_OK)
        except UsedCar.DoesNotExist:
            return Response({'detail': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, car_id):
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({'detail': 'User not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            car = UsedCar.objects.using('all_db').get(id=car_id)
            user = User.objects.using('all_db').get(id=user_id)
            action = request.data.get('action')

            if action == 'like':
                if car.id not in user.liked_cars:
                    user.liked_cars.append(car.id)
                    user.save()
                    return Response({'is_liked': True}, status=status.HTTP_200_OK)
                else:
                    user.liked_cars.remove(car.id)
                    user.save()
                    return Response({'is_liked': False}, status=status.HTTP_200_OK)

            elif action == 'buy':
                return Response({
                    'redirect_url': f'/users/create_order/{car.id}/'
                }, status=status.HTTP_200_OK)

            return Response({'detail': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        except UsedCar.DoesNotExist:
            return Response({'detail': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)


class CreateOrderAPIView(APIView):
    def post(self, request, car_id):
        # 获取车辆信息
        car = UsedCar.objects.using('all_db').filter(id=car_id).first()
        if not car:
            return Response({'detail': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)

        user_id = request.session.get('user_id')
        if not user_id:
            return Response({'detail': 'User not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.using('all_db').filter(id=user_id).first()
        if not user:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # 获取请求数据
        buyer_name = request.data.get('buyer_name', '').strip()
        phone_number = request.data.get('phone_number', '').strip()
        delivery_address = request.data.get('delivery_address', '').strip()
        payment_method = request.data.get('payment_method', '').strip()

        required_fields = [buyer_name, phone_number, delivery_address, payment_method]
        if any(not field for field in required_fields):
            return Response({'detail': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        # 创建订单
        order = Order(
            owner_id=user.id,
            Brand=car.Brand,
            Color=car.Color,
            Year=car.Year,
            Mileage=car.Mileage,
            Price=car.Price,
            Configuration=car.Configuration,
            PhotoUrl=car.PhotoUrl,
            buyer_name=buyer_name,
            phone_number=phone_number,
            delivery_address=delivery_address,
            payment_method=payment_method
        )
        order.save(using='all_db')

        # 更新车辆主人的 selling_cars 字段
        owner_id = car.owner_id
        owner = User.objects.using('all_db').filter(id=owner_id).first()
        if owner and car.id in owner.selling_cars:
            owner.selling_cars.remove(car.id)
            owner.save()

        # 删除车辆记录
        car.delete()

        # 返回成功响应
        return Response({'detail': 'Order created successfully'}, status=status.HTTP_201_CREATED)


class AddCheckingCarAPIView(APIView):
    def post(self, request):
        # 判断用户是否登录
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({'detail': 'User not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.using('all_db').get(id=user_id)

        # 获取请求数据
        form_data = request.data
        form_files = request.FILES

        # 序列化检查车数据
        serializer = CheckingCarSerializer(data=form_data, files=form_files)
        if serializer.is_valid():
            checking_car = serializer.save()
            checking_car.owner_id = user.id
            checking_car.save()

            # 将车辆ID添加到用户的 checking_cars 列表中
            user.checking_cars.append(checking_car.id)
            user.save()

            return Response({'detail': 'Checking car added successfully'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminCreationAPIView(APIView):
    def post(self, request):
        serializer = AdminCreationSerializer(data=request.data)
        if serializer.is_valid():
            admin = serializer.save()
            return Response({'message': 'Admin registered successfully', 'admin_id': str(admin.id)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminLoginAPIView(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            login_name = serializer.validated_data['login_name']
            passwd = serializer.validated_data['passwd']

            admin = authenticate(request, username=login_name, password=passwd)

            if admin is not None:
                # 登录成功，返回会话或认证令牌
                request.session['admin_id'] = str(admin.id)  # 将管理员ID存入session
                return Response({'message': 'Login successful', 'admin_id': str(admin.id)}, status=status.HTTP_200_OK)
            return Response({'message': 'Invalid login credentials or not an admin.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminDashboardAPIView(APIView):
    def get(self, request):
        # 获取 session 中的管理员 ID
        admin_id = request.session.get('admin_id')
        if not admin_id:
            return Response({'detail': 'Not logged in as admin'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # 验证管理员身份
            admin = Admin.objects.using('all_db').get(id=admin_id)
        except Admin.DoesNotExist:
            return Response({'detail': 'Invalid admin session'}, status=status.HTTP_401_UNAUTHORIZED)

        # 获取所有待审核的车辆
        checking_cars = CheckingCar.objects.using('all_db').all()
        serializer = CheckingCarSerializer(checking_cars, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CheckingCarDetailAPIView(APIView):
    def get(self, request, car_id):
        admin_id = request.session.get('admin_id')
        if not admin_id:
            return Response({'detail': 'Admin not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

        car = get_object_or_404(CheckingCar.objects.using('all_db'), id=car_id)
        serializer = CheckingCarSerializer(car)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApproveCarAPIView(APIView):
    def post(self, request, car_id):
        admin_id = request.session.get('admin_id')
        if not admin_id:
            return Response({'detail': 'Admin not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            car = CheckingCar.objects.using('all_db').get(id=car_id)
        except CheckingCar.DoesNotExist:
            return Response({'detail': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)

        used_car = UsedCar(
            owner_id=car.owner_id,
            Brand=car.Brand,
            Color=car.Color,
            Year=car.Year,
            Mileage=car.Mileage,
            Price=car.Price,
            Configuration=car.Configuration,
            ConditionDescription=car.ConditionDescription,
            PhotoUrl=car.PhotoUrl
        )
        used_car.save(using='all_db')
        car.delete()

        return Response({'detail': 'Car approved successfully'}, status=status.HTTP_200_OK)


class RejectCarAPIView(APIView):
    def delete(self, request, car_id):
        admin_id = request.session.get('admin_id')
        if not admin_id:
            return Response({'detail': 'Admin not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            car = CheckingCar.objects.using('all_db').get(id=car_id)
        except CheckingCar.DoesNotExist:
            return Response({'detail': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)

        car.delete()
        return Response({'detail': 'Car rejected and deleted'}, status=status.HTTP_200_OK)



class AdminUserListAPIView(APIView):
    def get(self, request):
        admin_id = request.session.get('admin_id')
        if not admin_id:
            return Response({'detail': 'Admin not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

        users = User.objects.using('all_db').all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfileAPIView(APIView):
    def get(self, request, user_id):
        user = User.objects.using('all_db').filter(id=user_id).first()
        if not user:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        orders = Order.objects.using('all_db').filter(owner_id=user.id)
        if not orders:
            profile = {"message": "该用户暂无订单数据"}
        else:
            brands = [order.Brand for order in orders]
            colors = [order.Color for order in orders]
            configs = [order.Configuration for order in orders]
            prices = [float(order.Price) for order in orders if order.Price]

            profile = {
                "preferred_brands": Counter(brands).most_common(3),
                "preferred_colors": Counter(colors).most_common(3),
                "preferred_configurations": Counter(configs).most_common(3),
                "average_price": round(sum(prices) / len(prices), 2) if prices else "无",
                "purchase_count": len(orders),
            }

        return Response({
            "user": {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
            },
            "profile": profile
        }, status=status.HTTP_200_OK)


class DeleteUserAPIView(APIView):
    def delete(self, request, user_id):
        admin_id = request.session.get('admin_id')
        if not admin_id:
            return Response({'detail': 'Admin not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.using('all_db').filter(id=user_id).first()
        if not user:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({'detail': 'User deleted successfully'}, status=status.HTTP_200_OK)


class AdminDataAnalysisAPIView(APIView):
    def get(self, request):
        admin_id = request.session.get('admin_id')
        if not admin_id:
            return Response({'detail': 'Admin not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

        if not Admin.objects.filter(id=admin_id).first():
            return Response({'detail': 'Admin not found'}, status=status.HTTP_401_UNAUTHORIZED)

        brands = {
            '奥迪': ['奥迪'], '宝马': ['宝马'], '奔驰': ['奔驰'],
            '雷克萨斯': ['雷克萨斯'], '特斯拉': ['特斯拉'],
            '比亚迪': ['比亚迪'], '吉利': ['吉利'], '其它': []
        }

        def aggregate_brand_counts(source, field_name):
            pipeline = [
                {"$unwind": f"${field_name}"},
                {"$lookup": {
                    "from": "selling_car_collection",
                    "localField": field_name,
                    "foreignField": "_id",
                    "as": "car_details"
                }},
                {"$unwind": "$car_details"},
                {"$addFields": {
                    "brand_category": {
                        "$switch": {
                            "branches": [
                                {"case": {"$regexMatch": {"input": "$car_details.Brand", "regex": b}}, "then": b}
                                for b in brands if b != "其它"
                            ],
                            "default": "其它"
                        }
                    }
                }},
                {"$group": {"_id": "$brand_category", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
            ]
            result = User.objects.aggregate(*pipeline)
            return {item['_id']: item['count'] for item in result}

        # 购买车辆品牌统计
        purchased_cars = UsedCar.objects.aggregate(
            {"$addFields": {
                "brand_category": {
                    "$switch": {
                        "branches": [
                            {"case": {"$regexMatch": {"input": "$Brand", "regex": b}}, "then": b}
                            for b in brands if b != "其它"
                        ],
                        "default": "其它"
                    }
                }
            }},
            {"$group": {"_id": "$brand_category", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        )
        purchased_car_counts = {b: 0 for b in brands}
        for item in purchased_cars:
            purchased_car_counts[item['_id']] = item['count']

        searched_car_counts = aggregate_brand_counts(User, "searched_cars")
        liked_car_counts = aggregate_brand_counts(User, "liked_cars")

        # 车龄分析
        current_year = datetime.datetime.now().year
        age_ranges = {"0-2年": 0, "3-5年": 0, "6-10年": 0, "10年以上": 0}

        all_cars = UsedCar.objects.all()
        for car in all_cars:
            if car.Year:
                try:
                    car_year = int(car.Year) if isinstance(car.Year, str) else car.Year.year
                    car_age = current_year - car_year
                    if car_age <= 2:
                        age_ranges["0-2年"] += 1
                    elif 3 <= car_age <= 5:
                        age_ranges["3-5年"] += 1
                    elif 6 <= car_age <= 10:
                        age_ranges["6-10年"] += 1
                    else:
                        age_ranges["10年以上"] += 1
                except:
                    continue

        return Response({
            'purchased_car_counts': purchased_car_counts,
            'searched_car_counts': searched_car_counts,
            'liked_car_counts': liked_car_counts,
            'age_ranges': age_ranges,
        }, status=status.HTTP_200_OK)


class MyCollectionAPIView(APIView):
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({'detail': '请先登录'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'detail': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)

        available_cars = []
        removed_ids = []

        for car_id in user.liked_cars[:]:  # 复制一份用于安全移除
            try:
                car = UsedCar.objects.get(id=car_id)
                available_cars.append(car)
            except UsedCar.DoesNotExist:
                user.liked_cars.remove(car_id)
                removed_ids.append(str(car_id))

        if removed_ids:
            user.save()

        serialized = UsedCarSerializer(available_cars, many=True)
        return Response({
            'available_cars': serialized.data,
            'removed_ids': removed_ids  # 可选返回：哪些已被删除
        }, status=status.HTTP_200_OK)


class MyReleasedCarsAPIView(APIView):
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({'detail': '请先登录'}, status=status.HTTP_401_UNAUTHORIZED)

        cars = UsedCar.objects.filter(owner_id=user_id)
        serializer = UsedCarSerializer(cars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({'detail': '请先登录'}, status=status.HTTP_401_UNAUTHORIZED)

        car_id = request.data.get('car_id')
        if not car_id:
            return Response({'detail': '缺少参数 car_id'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            car = UsedCar.objects.get(id=car_id)
            if str(car.owner_id) != user_id:
                return Response({'detail': '无权限取消该车辆'}, status=status.HTTP_403_FORBIDDEN)
            car.delete()
            return Response({'detail': f'车辆 {car.Brand} 已取消发布'}, status=status.HTTP_200_OK)
        except UsedCar.DoesNotExist:
            return Response({'detail': '车辆不存在'}, status=status.HTTP_404_NOT_FOUND)


class PendingCarsAPIView(APIView):
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({'detail': '请先登录'}, status=status.HTTP_401_UNAUTHORIZED)

        checking_cars = CheckingCar.objects(owner_id=user_id)

        serializer = CheckingCarSerializer(checking_cars, many=True)

        if not checking_cars:
            return Response({
                'checking_cars': [],
                'message': '暂无待审核车辆'
            }, status=status.HTTP_200_OK)

        return Response({
            'checking_cars': serializer.data
        }, status=status.HTTP_200_OK)


class MyOrdersAPIView(APIView):
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({'detail': '请先登录'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user_object_id = ObjectId(user_id)
            orders = Order.objects(owner_id=user_object_id).all()
            serializer = OrderSerializer(orders, many=True)
            return Response({'orders': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"查询订单时出错: {e}")
            return Response({'orders': [], 'detail': '查询订单出错'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)























