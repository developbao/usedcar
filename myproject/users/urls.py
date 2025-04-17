from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_cars, name='search_cars'),
    path('car_photo/<str:car_id>/', views.get_car_photo, name='get_car_photo'),
    path('car/<str:car_id>/', views.car_detail, name='car_detail'),
    path('add_checking_car/', views.add_checking_car, name='add_checking_car'),
    path('admin_register/', views.admin_register, name='admin_register'),
    path('admin_login/', views.admin_login_view, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),  # 管理员审核页面
    path('admin_user_list/', views.admin_user_list, name='admin_user_list'),  # 管理员审核用户页面
    path('admin/delete_user/<str:user_id>/', views.delete_user, name='delete_user'),  # 删除用户
    path('approve_car/<str:car_id>/', views.approve_car, name='approve_car'),  # 审核通过
    path('reject_car/<str:car_id>/', views.reject_car, name='reject_car'),  # 审核不通过
    path('user_homepage/', views.personal_homepage, name='user_homepage'),
    path('my_collection/', views.my_collection, name='my_collection'),
    path('my_released_cars/', views.my_released_cars, name='my_released_cars'),
    path('pending_cars/', views.pending_cars, name='pending_cars'),
    # path('create_order/?car_id=<str:car_id>/', views.create_order, name='create_order'),
    # urls.py
    path('create_order/<str:car_id>/', views.create_order, name='create_order'),
    path('admin_data_analysis/', views.admin_data_analysis, name='admin_data_analysis'),
    path('my_orders', views.my_orders, name='my_orders'),
    path('checking_car_detail/<str:car_id>/', views.checking_car_detail, name='checking_car_detail'),
    path('user/<str:user_id>/profile/', views.user_profile_view, name='user_profile')
]



