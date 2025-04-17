from django.shortcuts import render
from django.http import JsonResponse
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from users.models import User, UsedCar
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder
from datetime import datetime
from bson import ObjectId
from sklearn.neighbors import BallTree





