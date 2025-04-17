from django import forms
from .models import User, Admin, CheckingCar
import requests


class UserCreationForm(forms.Form):
    login_name = forms.CharField(max_length=50, required=True, label="登录名")
    passwd = forms.CharField(max_length=50, widget=forms.PasswordInput, required=True, label="密码")
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput, required=True, label="确认密码")
    name = forms.CharField(max_length=50, required=True, label="姓名")
    phone_num = forms.CharField(max_length=50, required=True, label="电话号码")

    def clean_login_name(self):
        login_name = self.cleaned_data.get("login_name")
        if User.objects(login_name=login_name).first():
            raise forms.ValidationError("Login name already exists")
        return login_name

    def clean_password2(self):
        password1 = self.cleaned_data.get("passwd")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self):
        # 通过表单数据创建一个新的 User 对象并保存
        user = User(
            login_name=self.cleaned_data['login_name'],
            passwd=self.cleaned_data['passwd'],
            name=self.cleaned_data['name'],
            phone_num=self.cleaned_data['phone_num'],
            selling_cars=[],
            liked_cars=[],
            checking_cars=[],
            searched_cars=[],
        )
        user.save()
        return user


class UserLoginForm(forms.Form):
    login_name = forms.CharField(max_length=50, required=True, label="登录名")
    passwd = forms.CharField(max_length=50, widget=forms.PasswordInput, required=True, label="密码")


class CarSearchForm(forms.Form):
    brand = forms.CharField(max_length=50, required=False, label="品牌")
    year = forms.DateField(required=False, input_formats=['%Y-%m'], widget=forms.TextInput(attrs={'type': 'month'}),
                           label="年份")
    price_max = forms.DecimalField(max_digits=10, decimal_places=2, required=False, min_value=0.00, label="最高价格")
    price_min = forms.DecimalField(max_digits=10, decimal_places=2, required=False, min_value=0.00, label="最低价格")
    color = forms.CharField(max_length=50, required=False, label="颜色")
    mileage = forms.DecimalField(max_digits=10, decimal_places=2, required=False, min_value=0.00, label="里程")
    configuration = forms.CharField(max_length=200, required=False, label="配置")
    condition_description = forms.CharField(max_length=200, required=False, label="车况描述")

    def clean(self):
        cleaned_data = super().clean()
        price_min = cleaned_data.get("price_min")
        price_max = cleaned_data.get("price_max")

        if price_min is not None and price_max is not None:
            if price_min > price_max:
                raise forms.ValidationError("Minimum price cannot be greater than maximum price.")
        return cleaned_data


class AddCheckingCarForm(forms.Form):
    brand = forms.CharField(max_length=50, required=True, label="品牌")
    color = forms.CharField(max_length=50, required=True, label="颜色")
    year = forms.DateField(required=False, input_formats=['%Y-%m'], widget=forms.TextInput(attrs={'type': 'month'}), label="年份")
    mileage = forms.DecimalField(max_digits=10, decimal_places=2, required=False, min_value=0.00, label="里程")
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=False, min_value=0.00, label="价格")
    configuration = forms.CharField(max_length=200, required=True, label="配置")
    condition_description = forms.CharField(max_length=200, required=True, label="车况描述")
    photo = forms.ImageField(required=True, label="照片")

    def save(self):
        # 获取表单数据
        data = self.cleaned_data
        photo = data.pop('photo')

        # 创建并保存 CheckingCar 对象（不包含照片URL）
        checking_car = CheckingCar(
            Brand=data['brand'],
            Color=data['color'],
            Year=data['year'],
            Mileage=data['mileage'],
            Price=data['price'],
            Configuration=data['configuration'],
            ConditionDescription=data['condition_description']
        )
        checking_car.save()

        # 获取存入之后的 ObjectID
        object_id = checking_car.id

        # 将照片存入本地目录
        photo_path = f"./static/images/{object_id}.jpg"
        with open(photo_path, 'wb') as f:
            for chunk in photo.chunks():
                f.write(chunk)

        # 更新照片URL到数据库中
        PhotoUrl = f"/static/images/{object_id}.jpg"
        checking_car.PhotoUrl = PhotoUrl
        checking_car.save()

        return checking_car


class AdminCreationForm(forms.Form):
    login_name = forms.CharField(max_length=50, required=True, label="登录名")
    passwd = forms.CharField(max_length=50, widget=forms.PasswordInput, required=True, label="密码")
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput, required=True, label="确认密码")
    name = forms.CharField(max_length=50, required=True, label="姓名")
    phone_num = forms.CharField(max_length=50, required=True, label="电话号码")
    admin_key = forms.CharField(max_length=50, required=True, label="管理员密钥")

    def clean_login_name(self):
        login_name = self.cleaned_data.get("login_name")
        if Admin.objects(login_name=login_name).first():
            raise forms.ValidationError("Login name already exists")
        return login_name

    def clean_password2(self):
        password1 = self.cleaned_data.get("passwd")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_admin_key(self):
        admin_key = self.cleaned_data.get("admin_key")
        if admin_key != "2025":  # 检查管理员密钥是否正确
            raise forms.ValidationError("Invalid admin key")
        return admin_key

    def save(self):
        admin = Admin(
            login_name=self.cleaned_data['login_name'],
            passwd=self.cleaned_data['passwd'],
            name=self.cleaned_data['name'],
            phone_num=self.cleaned_data['phone_num']
        )
        admin.save()
        return admin


class AdminLoginForm(forms.Form):
    login_name = forms.CharField(max_length=50, required=True, label="登录名")
    passwd = forms.CharField(max_length=50, widget=forms.PasswordInput, required=True, label="密码")

    def clean(self):
        cleaned_data = super().clean()
        login_name = cleaned_data.get("login_name")
        passwd = cleaned_data.get("passwd")

        # 检查管理员账号
        try:
            admin = Admin.objects.get(login_name=login_name, passwd=passwd)
        except Admin.DoesNotExist:
            raise forms.ValidationError("Invalid login credentials or not an admin.")
        return cleaned_data



