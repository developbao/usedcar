import os

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

# 定义函数从数据库获取二手车信息
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


def index(request):
    user_id = request.session.get('user_id')
    user = None
    recommended_cars = []

    if user_id:
        try:
            user = User.objects.using('all_db').get(id=user_id)

            # 确保用户存在并且有收藏或搜索的车辆
            if user.searched_cars or user.liked_cars:
                response = recommend_cars(request, user.id)  # 获取推荐的车辆的 JsonResponse
                # 解析 JsonResponse 内容
                recommended_cars_ids = json.loads(response.content).get('recommendations', [])
                print(f"推荐的车辆 ID 数量: {len(recommended_cars_ids)}")  # Debug: 打印推荐车辆 ID 数量

                # 从数据库获取完整的车辆对象，跳过不存在的车辆
                for car_id in recommended_cars_ids:
                    try:
                        car = UsedCar.objects.using('all_db').get(id=car_id)
                        recommended_cars.append(car)
                    except UsedCar.DoesNotExist:
                        print(f"车辆 ID {car_id} 不存在，跳过该车辆。")
                print(f"最终推荐的车辆数量: {len(recommended_cars)}")  # Debug: 打印最终推荐车辆数量
            else:
                recommended_cars = list(UsedCar.objects.using('all_db').all()[:20])  # 默认展示前20辆
        except User.DoesNotExist:
            # 用户不存在时展示默认车辆
            recommended_cars = list(UsedCar.objects.using('all_db').all()[:20])
    else:
        # 用户未登录时展示默认车辆
        recommended_cars = list(UsedCar.objects.using('all_db').all()[:20])

    paginator = Paginator(recommended_cars, 20)
    page_number = request.GET.get('page')  # 获取当前页码
    page_obj = paginator.get_page(page_number)

    print(f"推荐车辆: {recommended_cars}")  # Debug: 打印推荐的车辆
    return render(request, 'users/index.html', {'user': user, 'recommended_cars': recommended_cars, 'page_obj': page_obj})


# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            request.session['user_id'] = str(user.id)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    user_id = request.session.get('user_id')
    if user_id:
        # 用户已经登录，提示用户已登录
        return render(request, 'users/already_logged_in.html')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            login_name = form.cleaned_data['login_name']
            passwd = form.cleaned_data['passwd']
            try:
                user = User.objects.get(login_name=login_name, passwd=passwd)
                # 手动登录用户
                request.session['user_id'] = str(user.id)
                return redirect('/')
            except User.DoesNotExist:
                form.add_error(None, "Invalid login credentials")
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    request.session.flush()
    return redirect('/')


def search_cars(request):
    form = CarSearchForm(request.GET)
    cars = UsedCar.objects.using('all_db')  # 默认不查询所有车辆

    brand = request.GET.get('brand')  # 获取品牌参数
    if brand:
        cars = cars.filter(Brand__icontains=brand)

    # 如果没有任何查询条件，返回空列表或适当的提示
    if not form.is_valid() or not any(form.cleaned_data.values()):
        cars = cars.none()  # 这样就不会返回所有的车辆

    # 如果没有任何查询条件，返回空列表或适当的提示
    if not form.is_valid() or not any(form.cleaned_data.values()):
        cars = cars.none()  # 这样就不会返回所有的车辆

    if form.is_valid():
        if form.cleaned_data['brand']:
            cars = cars.filter(Brand__icontains=form.cleaned_data['brand'])

        if form.cleaned_data['year']:
            search_year = form.cleaned_data['year']
            cars = cars.filter(Year__gt=search_year)

        if form.cleaned_data['price_min']:
            price_min = form.cleaned_data['price_min']
            cars = cars.filter(Price__gte=price_min)

        if form.cleaned_data['price_max']:
            price_max = form.cleaned_data['price_max']
            cars = cars.filter(Price__lte=price_max)

        if form.cleaned_data['color']:
            cars = cars.filter(Color__icontains=form.cleaned_data['color'])

        if form.cleaned_data['mileage']:
            mileage = form.cleaned_data['mileage']
            cars = cars.filter(Mileage__lte=mileage)

        if form.cleaned_data['configuration']:
            cars = cars.filter(Configuration__icontains=form.cleaned_data['configuration'])

        if form.cleaned_data['condition_description']:
            cars = cars.filter(ConditionDescription__icontains=form.cleaned_data['condition_description'])

    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.using('all_db').get(id=user_id)
        search_cars_ids = [car.id for car in cars]
        user.searched_cars.extend(search_cars_ids)
        user.save()

    paginator = Paginator(cars, 20)
    page_number = request.GET.get('page')  # 获取当前页码
    page_obj = paginator.get_page(page_number)

    return render(request, 'users/search_results.html', {'form': form, 'cars': cars, 'page_obj': page_obj})


def get_car_photo(request, car_id):
    try:
        car = UsedCar.objects.using('all_db').get(id=car_id)
        if car.PhotoUrl:
            photo_path = '..' + os.path.join(settings.MEDIA_ROOT, car.PhotoUrl)
            with open(photo_path, 'rb') as photo_file:
                return HttpResponse(photo_file.read(), content_type='images/jpg')
        else:
            return HttpResponse(status=404)
    except UsedCar.DoesNotExist:
        return HttpResponse(status=404)


def car_detail(request, car_id):
    car = get_object_or_404(UsedCar.objects.using('all_db'), id=car_id)
    user_id = request.session.get('user_id')
    user = User.objects.using('all_db').get(id=user_id) if user_id else None
    is_liked = False

    if request.method == 'POST':
        if not user:
            return redirect('/users/login/')  # 用户未登录时重定向到登录页面

        action = request.POST.get('action')
        if action == 'like' and user:
            if car.id not in user.liked_cars:
                user.liked_cars.append(car.id)
                user.save()
                is_liked = True
            else:
                user.liked_cars.remove(car.id)
                user.save()
                is_liked = False
        elif action == 'buy' and user:
            if car.id not in user.selling_cars:
                # 进入下单页面，传递车辆信息
                return redirect('/users/create_order/{}/'.format(car.id))  # 修改此行

    if user and car.id in user.liked_cars:
        is_liked = True

    return render(request, 'users/car_detail.html', {'car': car, 'user': user, 'is_liked': is_liked})


def create_order(request: HttpRequest, car_id):
    # 使用 get_object_or_404 获取车辆信息
    car = get_object_or_404(UsedCar.objects.using('all_db'), id=car_id)

    user_id = request.session.get('user_id')
    user = User.objects.using('all_db').get(id=user_id) if user_id else None

    if request.method == 'POST':
        if not user:
            return redirect('/users/login/')
        # 获取当前用户
        buyer_name = request.POST.get('buyer_name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        delivery_address = request.POST.get('delivery_address', '').strip()
        payment_method = request.POST.get('payment_method', '').strip()

        required_fields = [buyer_name, phone_number, delivery_address, payment_method]
        if any(not field for field in required_fields):
            return render(request, 'users/order.html', {
                'car': car,
                'error': '所有字段均为必填项'
            })

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
        order.save(using='all_db')  # 保存订单到 MongoDB

        # 更新车辆主人的 selling_cars 字段
        owner_id = car.owner_id
        try:
            owner = User.objects.using('all_db').get(id=owner_id)
            if car.id in owner.selling_cars:
                owner.selling_cars.remove(car.id)
                owner.save()
        except User.DoesNotExist:
            pass  # 如果主人不存在，则不操作

        # 删除车辆记录
        car.delete()

        # 提示买车成功并跳转到首页
        return redirect('/')  # 或者跳转到你希望的页面

    return render(request, 'users/order.html', {'car': car})


def add_checking_car(request):
    # 判断用户是否登录
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/users/login/')

    user = User.objects.using('all_db').get(id=user_id)

    if request.method == 'POST':
        form = AddCheckingCarForm(request.POST, request.FILES)
        if form.is_valid():
            checking_car = form.save()
            checking_car.owner_id = user.id
            checking_car.save()
            # 将车辆ID添加到用户的 checking_cars 列表中
            user.checking_cars.append(checking_car.id)
            user.save()

            return redirect('/users/search/')
    else:
        form = AddCheckingCarForm()

    return render(request, 'users/add_checking_car.html', {'form': form})


# 管理员注册
def admin_register(request):
    if request.method == 'POST':
        form = AdminCreationForm(request.POST)
        if form.is_valid():
            # 密钥验证通过，保存管理员信息
            form.save()
            return redirect('/users/admin_login/')
    else:
        form = AdminCreationForm()
    return render(request, 'users/admin_register.html', {'form': form})


def admin_login_view(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            login_name = form.cleaned_data['login_name']
            passwd = form.cleaned_data['passwd']
            try:
                admin = Admin.objects.get(login_name=login_name, passwd=passwd)
                request.session['admin_id'] = str(admin.id)  # 将管理员的ID存入session
                return redirect('/users/admin_dashboard/')  # 登录成功后重定向到 admin_dashboard
            except Admin.DoesNotExist:
                form.add_error(None, "Invalid login credentials or not an admin.")
    else:
        form = AdminLoginForm()
    return render(request, 'users/admin_login.html', {'form': form})


def admin_dashboard(request):
    # 获取 session 中存储的管理员ID
    user_id = request.session.get('admin_id')

    # 检查是否登录，如果没有登录则重定向到登录页面
    if not user_id:
        return redirect('/users/admin_login/')  # 未登录时跳转到管理员登录页面

    try:
        # 根据 session 中的 user_id 获取管理员用户
        admin = Admin.objects.get(id=user_id)
    except Admin.DoesNotExist:
        return redirect('/users/admin_login/')  # 如果没有找到对应的管理员用户，重定向到登录页面

    # 获取所有待审核的车辆
    checking_cars = CheckingCar.objects.all()

    # 渲染模板并传递待审核车辆数据
    return render(request, 'users/admin_dashboard.html', {'checking_cars': checking_cars})


def checking_car_detail(request, car_id):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('users/admin_login')

    car = get_object_or_404(CheckingCar.objects.using('all_db'), id=car_id)

    return render(request, 'users/checking_car_detail.html', {'car': car})


def approve_car(request, car_id):
    # 获取 session 中存储的管理员ID
    admin_id = request.session.get('admin_id')

    # 检查是否登录，如果没有登录则重定向到登录页面
    if not admin_id:
        return redirect('/users/admin_login/')  # 未登录时跳转到管理员登录页面
    
    # 获取待审核车辆
    try:
        car = CheckingCar.objects.using('all_db').get(id=car_id)
    except CheckingCar.DoesNotExist:
        return HttpResponse("Car not found", status=404)

    # 创建一个新的 UsedCar 对象
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
    used_car.save()  # 将车辆保存到 UsedCar 集合

    # 删除该车辆从待审核集合中
    car.delete()

    return redirect('/users/admin_dashboard/')


def reject_car(request, car_id):
    # 获取 session 中存储的管理员ID
    admin_id = request.session.get('admin_id')

    # 检查是否登录，如果没有登录则重定向到登录页面
    if not admin_id:
        return redirect('/users/admin_login/')  # 未登录时跳转到管理员登录页面
    
    # 获取待审核车辆
    try:
        car = CheckingCar.objects.using('all_db').get(id=car_id)
    except CheckingCar.DoesNotExist:
        return HttpResponse("Car not found", status=404)

    # 删除该车辆从待审核集合中
    car.delete()

    return redirect('/users/admin_dashboard/')


def admin_user_list(request):
    # 检查是否是管理员（可以根据 session 中的管理员信息判断）
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('/users/admin_login/')  # 如果没有管理员登录，重定向到登录页面

    # 获取所有用户
    users = User.objects.all()

    return render(request, 'users/admin_user_list.html', {'users': users})


def user_profile_view(request, user_id):
    # 用 MongoEngine 的查询方法代替 Django 的 get_object_or_404
    user = User.objects(id=user_id).first()
    if not user:
        return render(request, "admin/user_profile.html", {
            "error": "用户不存在"
        })

    orders = Order.objects(owner_id=user.id)

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

    return render(request, "user_profile.html", {
        "user": user,
        "profile": profile
    })

# 删除用户
def delete_user(request, user_id):
    # 检查是否是管理员
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('/users/admin_login/')  # 如果没有管理员登录，重定向到登录页面

    try:
        # 获取用户对象
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponse("User not found", status=404)

    # 删除用户
    user.delete()

    return redirect('/users/admin_user_list/')  # 删除后重定向到用户列表页面


def admin_data_analysis(request):
    # 获取 session 中存储的管理员ID
    admin_id = request.session.get('admin_id')

    # 检查是否登录，如果没有登录则重定向到登录页面
    if not admin_id:
        return redirect('/users/admin_login/')  # 未登录时跳转到管理员登录页面

    try:
        # 根据 session 中的 admin_id 获取管理员用户
        Admin.objects.get(id=admin_id)
    except Admin.DoesNotExist:
        return redirect('/users/admin_login/')  # 如果没有找到对应的管理员用户，重定向到登录页面

    # 定义品牌分类
    brands = {
        '奥迪': ['奥迪'],
        '宝马': ['宝马'],
        '奔驰': ['奔驰'],
        '雷克萨斯': ['雷克萨斯'],
        '特斯拉': ['特斯拉'],
        '比亚迪': ['比亚迪'],
        '吉利': ['吉利'],
        '其它': []
    }

    # 初始化统计结果
    purchased_car_counts = {brand: 0 for brand in brands}
    searched_car_counts = {brand: 0 for brand in brands}
    liked_car_counts = {brand: 0 for brand in brands}

    # 新旧程度分析结果初始化
    age_ranges = {"0-2年": 0, "3-5年": 0, "6-10年": 0, "10年以上": 0}

    # 分析购买车辆的占比
    purchased_cars = UsedCar.objects.aggregate(
        {"$addFields": {
            "brand_category": {
                "$switch": {
                    "branches": [
                        {"case": {"$regexMatch": {"input": "$Brand", "regex": "奥迪"}}, "then": "奥迪"},
                        {"case": {"$regexMatch": {"input": "$Brand", "regex": "宝马"}}, "then": "宝马"},
                        {"case": {"$regexMatch": {"input": "$Brand", "regex": "奔驰"}}, "then": "奔驰"},
                        {"case": {"$regexMatch": {"input": "$Brand", "regex": "雷克萨斯"}}, "then": "雷克萨斯"},
                        {"case": {"$regexMatch": {"input": "$Brand", "regex": "特斯拉"}}, "then": "特斯拉"},
                        {"case": {"$regexMatch": {"input": "$Brand", "regex": "比亚迪"}}, "then": "比亚迪"},
                        {"case": {"$regexMatch": {"input": "$Brand", "regex": "吉利"}}, "then": "吉利"},
                    ],
                    "default": "其它"
                }
            }
        }},
        {"$group": {"_id": "$brand_category", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    )
    for car in purchased_cars:
        purchased_car_counts[car['_id']] = car['count']

    # 分析搜索最多和最少的车辆
    searched_cars = User.objects.aggregate(
        {"$unwind": "$searched_cars"},
        {"$lookup": {
            "from": "selling_car_collection",
            "localField": "searched_cars",
            "foreignField": "_id",
            "as": "searched_car_details"
        }},
        {"$unwind": "$searched_car_details"},
        {"$addFields": {
            "brand_category": {
                "$switch": {
                    "branches": [
                        {"case": {"$regexMatch": {"input": "$searched_car_details.Brand", "regex": "奥迪"}},
                         "then": "奥迪"},
                        {"case": {"$regexMatch": {"input": "$searched_car_details.Brand", "regex": "宝马"}},
                         "then": "宝马"},
                        {"case": {"$regexMatch": {"input": "$searched_car_details.Brand", "regex": "奔驰"}},
                         "then": "奔驰"},
                        {"case": {"$regexMatch": {"input": "$searched_car_details.Brand", "regex": "雷克萨斯"}},
                         "then": "雷克萨斯"},
                        {"case": {"$regexMatch": {"input": "$searched_car_details.Brand", "regex": "特斯拉"}},
                         "then": "特斯拉"},
                        {"case": {"$regexMatch": {"input": "$searched_car_details.Brand", "regex": "比亚迪"}},
                         "then": "比亚迪"},
                        {"case": {"$regexMatch": {"input": "$searched_car_details.Brand", "regex": "吉利"}},
                         "then": "吉利"},
                    ],
                    "default": "其它"
                }
            }
        }},
        {"$group": {"_id": "$brand_category", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    )
    for car in searched_cars:
        searched_car_counts[car['_id']] = car['count']

    # 分析收藏车辆的占比
    liked_cars = User.objects.aggregate(
        {"$unwind": "$liked_cars"},
        {"$lookup": {
            "from": "selling_car_collection",
            "localField": "liked_cars",
            "foreignField": "_id",
            "as": "liked_car_details"
        }},
        {"$unwind": "$liked_car_details"},
        {"$addFields": {
            "brand_category": {
                "$switch": {
                    "branches": [
                        {"case": {"$regexMatch": {"input": "$liked_car_details.Brand", "regex": "奥迪"}},
                         "then": "奥迪"},
                        {"case": {"$regexMatch": {"input": "$liked_car_details.Brand", "regex": "宝马"}},
                         "then": "宝马"},
                        {"case": {"$regexMatch": {"input": "$liked_car_details.Brand", "regex": "奔驰"}},
                         "then": "奔驰"},
                        {"case": {"$regexMatch": {"input": "$liked_car_details.Brand", "regex": "雷克萨斯"}},
                         "then": "雷克萨斯"},
                        {"case": {"$regexMatch": {"input": "$liked_car_details.Brand", "regex": "特斯拉"}},
                         "then": "特斯拉"},
                        {"case": {"$regexMatch": {"input": "$liked_car_details.Brand", "regex": "比亚迪"}},
                         "then": "比亚迪"},
                        {"case": {"$regexMatch": {"input": "$liked_car_details.Brand", "regex": "吉利"}},
                         "then": "吉利"},
                    ],
                    "default": "其它"
                }
            }
        }},
        {"$group": {"_id": "$brand_category", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    )
    for car in liked_cars:
        liked_car_counts[car['_id']] = car['count']

        # 当前年份
    current_year = datetime.datetime.now().year

    # 车龄分类字典
    age_ranges = {
        "0-2年": 0,
        "3-5年": 0,
        "6-10年": 0,
        "10年以上": 0
    }

    # 获取所有车辆信息
    all_cars = UsedCar.objects.all()

    # 遍历所有车辆
    for car in all_cars:
        if car.Year:
            try:
                # 如果 car.Year 是字符串，将其转换为整数
                if isinstance(car.Year, str):
                    car_year = int(car.Year)
                else:
                    car_year = car.Year.year  # 如果已经是 datetime 对象，则直接获取年份
            except ValueError:
                continue  # 如果无法转换为整数，跳过该条记录

            # 计算车龄
            car_age = current_year - car_year

            if car_age <= 2:
                age_ranges["0-2年"] += 1
            elif 3 <= car_age <= 5:
                age_ranges["3-5年"] += 1
            elif 6 <= car_age <= 10:
                age_ranges["6-10年"] += 1
            else:
                age_ranges["10年以上"] += 1

    # 输出最终的统计结果
    print("Age ranges distribution:", age_ranges)
    context = {
        'purchased_car_counts': purchased_car_counts,
        'searched_car_counts': searched_car_counts,
        'liked_car_counts': liked_car_counts,
        'age_ranges': age_ranges,  # 新旧程度分析结果
    }

    return render(request, 'users/admin_data_analysis.html', context)


def homepage(request):
    return redirect('/users/search/')


def personal_homepage(request):
    return render(request, 'users/personal_page.html')


def my_collection(request):
    # 获取当前登录用户的ID
    user_id = request.session.get('user_id')
    user = User.objects.using('all_db').get(id=user_id) if user_id else None

    if not user:
        return redirect('/users/login/')  # 如果用户未登录，重定向到登录页面

    liked_cars = user.liked_cars
    available_cars = []

    # 检查每辆用户喜欢的车是否仍然在出售
    for car_id in liked_cars:
        try:
            car = UsedCar.objects.using('all_db').get(id=car_id)
            available_cars.append(car)
        except UsedCar.DoesNotExist:
            # 如果这辆车已不再出售，则从用户的收藏中删除
            user.liked_cars.remove(car_id)
            user.save()
            messages.info(request, f"车辆 {car_id} 已被买走，已从您的收藏中移除。")

    return render(request, 'users/my_collection.html', {'available_cars': available_cars})


def my_released_cars(request):
    # 获取当前登录用户的ID
    user_id = request.session.get('user_id')
    user = User.objects.using('all_db').get(id=user_id) if user_id else None

    if not user:
        return redirect('/users/login/')  # 如果用户未登录，重定向到登录页面

    # 获取用户发布的所有车辆
    posted_cars = UsedCar.objects.using('all_db').filter(owner_id=user.id)

    if request.method == 'POST':
        # 处理取消发布的操作
        car_id = request.POST.get('car_id')
        if car_id:
            try:
                car_to_remove = UsedCar.objects.using('all_db').get(id=car_id)
                if car_to_remove.owner_id == user.id:
                    car_to_remove.delete()  # 删除已发布的车
                    messages.success(request, f"车辆 {car_to_remove.Brand} 已取消发布。")
                else:
                    messages.error(request, "无法取消发布该车，因为该车不是您的。")
            except UsedCar.DoesNotExist:
                messages.error(request, "未找到该车辆，取消发布失败。")

            return redirect('my_released_cars')  # 操作完成后重定向回我的发布页面

    return render(request, 'users/my_released_cars.html', {'posted_cars': posted_cars})


def pending_cars(request):
    # 通过 session 获取当前用户 ID
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('/users/login/')  # 如果没有登录，跳转到登录页面

    # 查询待审核车辆，筛选出所有属于当前用户的车辆
    checking_cars = CheckingCar.objects(owner_id=user_id)

    # 如果没有待审核车辆，返回一个提示信息
    if not checking_cars:
        message = "No pending cars found."
    else:
        message = None

    # 渲染页面并传递查询到的待审核车辆
    return render(request, 'users/pending_cars.html', {
        'checking_cars': checking_cars,
        'message': message,
    })


def my_orders(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('/users/login/')

    try:
        user_id = ObjectId(user_id)  # 确保 ID 是 ObjectId 类型
        orders = Order.objects(owner_id=user_id).all()
    except Exception as e:
        print(f"查询订单时出错: {e}")
        orders = []

    return render(request, 'users/my_orders.html', {'orders': orders})