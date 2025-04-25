# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import api_views  # 新建的视图文件，用于 API
from .api_views import (
    RecommendCarsAPI,
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    MeAPIView,
    SearchCarsAPIView,
    CarPhotoAPIView,
    CarDetailAPIView,
    CreateOrderAPIView,
    AddCheckingCarAPIView,
    AdminLoginAPIView,
    AdminCreationAPIView,
    AdminDashboardAPIView,
    CheckingCarDetailAPIView,
    ApproveCarAPIView,
    RejectCarAPIView,
    AdminUserListAPIView,
    UserProfileAPIView,
    DeleteUserAPIView,
    AdminDataAnalysisAPIView,
    MyCollectionAPIView,
    MyReleasedCarsAPIView,
    PendingCarsAPIView,
    MyOrdersAPIView
)

# 注册 API 路由
router = DefaultRouter()
router.register(r'api/users', api_views.UserViewSet, basename='user')
router.register(r'api/cars', api_views.UsedCarViewSet, basename='car')
router.register(r'api/checking_cars', api_views.CheckingCarViewSet, basename='checking car')
router.register(r'api/admins', api_views.AdminViewSet, basename='admin')
router.register(r'api/orders', api_views.OrderViewSet, basename='order')


urlpatterns = [
    # 原有路由
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_cars, name='search_cars'),
    path('car_photo/<str:car_id>/', views.get_car_photo, name='get_car_photo'),
    path('car/<str:car_id>/', views.car_detail, name='car_detail'),
    path('add_checking_car/', views.add_checking_car, name='add_checking_car'),
    path('admin_register/', views.admin_register, name='admin_register'),
    path('admin_login/', views.admin_login_view, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_user_list/', views.admin_user_list, name='admin_user_list'),
    path('admin/delete_user/<str:user_id>/', views.delete_user, name='delete_user'),
    path('approve_car/<str:car_id>/', views.approve_car, name='approve_car'),
    path('reject_car/<str:car_id>/', views.reject_car, name='reject_car'),
    path('user_homepage/', views.personal_homepage, name='user_homepage'),
    path('my_collection/', views.my_collection, name='my_collection'),
    path('my_released_cars/', views.my_released_cars, name='my_released_cars'),
    path('pending_cars/', views.pending_cars, name='pending_cars'),
    path('create_order/<str:car_id>/', views.create_order, name='create_order'),
    path('admin_data_analysis/', views.admin_data_analysis, name='admin_data_analysis'),
    path('my_orders', views.my_orders, name='my_orders'),
    path('checking_car_detail/<str:car_id>/', views.checking_car_detail, name='checking_car_detail'),
    path('user/<str:user_id>/profile/', views.user_profile_view, name='user_profile'),

    # 新增 API 路由
    path('', include(router.urls)),
    path('api/recommend-cars/', RecommendCarsAPI.as_view(), name='recommend_cars'),
    path('api/register/', RegisterAPIView.as_view()),
    path('api/login/', LoginAPIView.as_view()),
    path('api/logout/', LogoutAPIView.as_view()),
    path('api/me/', MeAPIView.as_view()),
    path('api/search-cars/', SearchCarsAPIView.as_view()),
    path('api/car/photo/<int:car_id>/', CarPhotoAPIView.as_view(), name='car_photo'),
    path('api/car/detail/<str:car_id>/', CarDetailAPIView.as_view(), name='car_detail'),
    path('api/create_order/<str:car_id>/', CreateOrderAPIView.as_view(), name='create_order'),
    path('api/add_checking_car/', AddCheckingCarAPIView.as_view(), name='add_checking_car'),
    path('api/admin/login/', AdminLoginAPIView.as_view(), name='admin_login'),
    path('api/admin/register/', AdminCreationAPIView.as_view(), name='admin_register'),
    path('api/admin_dashboard/', AdminDashboardAPIView.as_view(), name='admin_dashboard_api'),
    path('api/checking_car/<str:car_id>/', CheckingCarDetailAPIView.as_view(), name='checking_car_detail'),
    path('api/checking_car/<str:car_id>/approve/', ApproveCarAPIView.as_view(), name='approve_car'),
    path('api/checking_car/<str:car_id>/reject/', RejectCarAPIView.as_view(), name='reject_car'),
    path('api/admin/users/', AdminUserListAPIView.as_view(), name='admin_user_list'),
    path('api/admin/users/<str:user_id>/', UserProfileAPIView.as_view(), name='user_profile'),
    path('api/admin/users/<str:user_id>/delete/', DeleteUserAPIView.as_view(), name='delete_user'),
    path('api/admin/data-analysis/', AdminDataAnalysisAPIView.as_view(), name='admin_data_analysis'),
    path('api/my-collection/', MyCollectionAPIView.as_view(), name='api_my_collection'),
    path('api/my-released-cars/', MyReleasedCarsAPIView.as_view(), name='api_my_released_cars'),
    path('api/pending-cars/', PendingCarsAPIView.as_view(), name='api_pending_cars'),
    path('api/my-orders/', MyOrdersAPIView.as_view(), name='api_my_orders'),
]
