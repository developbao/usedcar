<template>
  <div class="pending-cars">
    <h2>待审核车辆</h2>

    <!-- 加载中 -->
    <div v-if="loading" class="loading">加载中...</div>

    <!-- 错误信息 -->
    <div v-else-if="error" class="error">{{ error }}</div>

    <!-- 车辆列表 -->
    <div v-else-if="cars.length > 0" class="cars-list">
      <div v-for="car in cars" :key="car.id" class="car-card">
        <img
          :src="getCarPhotoUrl(car.photo_url)"
          alt="Car Photo"
          class="car-photo"
        />
        <div class="car-details">
          <h3>{{ car.brand }} – {{ car.color }}</h3>
          <p>年份: {{ car.year }}</p>
          <p>里程: {{ car.mileage }} km</p>
          <p>价格: ¥{{ car.price }}</p>
          <p>{{ car.condition_description }}</p>
        </div>
      </div>
    </div>

    <!-- 无待审核车辆 -->
    <div v-else class="no-cars">暂无待审核车辆</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

// 状态
const loading = ref(true);
const error = ref("");
const cars = ref([]);

// 工具函数：拼接图片 URL
const getCarPhotoUrl = (url) => `http://127.0.0.1:8000${url}`;

// 拉取数据
async function fetchPendingCars() {
  loading.value = true;
  error.value = "";
  try {
    const res = await axios.get(
      "http://127.0.0.1:8000/users/api/pending-cars/",
      { withCredentials: true }
    );
    cars.value = res.data.checking_cars || [];
  } catch (e) {
    console.error(e);
    error.value = "加载失败，请稍后重试";
  } finally {
    loading.value = false;
  }
}

// 组件挂载后执行
onMounted(fetchPendingCars);
</script>

<style scoped>
.pending-cars {
  padding: 24px;
  font-family: "Helvetica Neue", Arial, sans-serif;
}

.loading,
.error,
.no-cars {
  text-align: center;
  font-size: 16px;
  color: #555;
  margin-top: 20px;
}

.error {
  color: #e74c3c;
}

.cars-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 16px;
}

.car-card {
  display: flex;
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.car-photo {
  width: 160px;
  height: 120px;
  object-fit: cover;
  flex-shrink: 0;
}

.car-details {
  padding: 12px 16px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.car-details h3 {
  margin: 0 0 8px;
  font-size: 18px;
  color: #333;
}

.car-details p {
  margin: 4px 0;
  font-size: 14px;
  color: #666;
}
</style>
