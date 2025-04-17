from django.db import models
import mongoengine
from myproject.settings import DATABASES

from gridfs import *


mongoengine.connect(
    db = DATABASES['mongodb']['DATABASE'],
    host = DATABASES['mongodb']['HOST'],    
    port = DATABASES['mongodb']['PORT'],
    alias='all_db'
)


# Create your models here.
class User(mongoengine.Document):
    login_name = mongoengine.StringField(max_length=50, required=True)
    passwd = mongoengine.StringField(max_length=50, required=True)
    name = mongoengine.StringField(max_length=50, required=True)
    phone_num = mongoengine.StringField(max_length=50, required=True)
    selling_cars = mongoengine.ListField(mongoengine.ObjectIdField())
    checking_cars = mongoengine.ListField(mongoengine.ObjectIdField())
    liked_cars = mongoengine.ListField(mongoengine.ObjectIdField())
    searched_cars = mongoengine.ListField(mongoengine.ObjectIdField())

    def __str__(self):
        return self.login_name

    meta = {
        'collection': 'user_collection',
        'db_alias': 'all_db'
    }


class UsedCar(mongoengine.Document):
    owner_id = mongoengine.ObjectIdField()
    Brand = mongoengine.StringField(max_length=50, required=True)
    Color = mongoengine.StringField(max_length=50, required=True)
    Year = mongoengine.DateTimeField()
    Mileage = mongoengine.DecimalField()
    Price = mongoengine.DecimalField()
    Configuration = mongoengine.StringField(max_length=200, required=True)
    ConditionDescription = mongoengine.StringField(max_length=200, required=True)
    PhotoUrl = mongoengine.StringField(max_length=200)

    def __str__(self):
        return f"{self.Brand} - {self.Year}"
    
    meta = {
        'collection': 'selling_car_collection',
        'db_alias': 'all_db'
    }


class CheckingCar(mongoengine.Document):
    owner_id = mongoengine.ObjectIdField()
    Brand = mongoengine.StringField(max_length=50, required=True)
    Color = mongoengine.StringField(max_length=50, required=True)
    Year = mongoengine.DateTimeField()
    Mileage = mongoengine.DecimalField()
    Price = mongoengine.DecimalField()
    Configuration = mongoengine.StringField(max_length=200, required=True)
    ConditionDescription = mongoengine.StringField(max_length=200, required=True)
    PhotoUrl = mongoengine.StringField(max_length=200)

    def __str__(self):
        return f"{self.Brand} - {self.Year}"
    
    meta = {
        'collection': 'checking_car_collection',
        'db_alias': 'all_db'
    }


class Admin(mongoengine.Document):
    login_name = mongoengine.StringField(max_length=50, required=True)
    passwd = mongoengine.StringField(max_length=50, required=True)
    name = mongoengine.StringField(max_length=50, required=True)
    phone_num = mongoengine.StringField(max_length=50, required=True)

    def __str__(self):
        return self.login_name

    meta = {
        'collection': 'admin_collection',
        'db_alias': 'all_db'
    }


class Order(mongoengine.Document):
    owner_id = mongoengine.ObjectIdField()
    Brand = mongoengine.StringField(max_length=50, required=True)
    Color = mongoengine.StringField(max_length=50, required=True)
    Year = mongoengine.DateTimeField()
    Mileage = mongoengine.DecimalField()
    Price = mongoengine.DecimalField()
    Configuration = mongoengine.StringField(max_length=200, required=True)
    PhotoUrl = mongoengine.StringField(max_length=200)
    buyer_name = mongoengine.StringField(max_length=50, required=True)
    phone_number = mongoengine.StringField(max_length=50, required=True)
    delivery_address = mongoengine.StringField(max_length=50, required=True)
    payment_method = mongoengine.StringField(max_length=50, required=True)

    def __str__(self):
        return f"{self.Brand} - {self.Year}"

    meta = {
        'collection': 'order_collection',
        'db_alias': 'all_db'
    }