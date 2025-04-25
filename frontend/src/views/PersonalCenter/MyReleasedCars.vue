<!-- src/views/PersonalCenter/MyReleasedCars.vue -->
<template>
  <div class="released-page">
    <h2>我的发布</h2>

    <div v-if="loading" class="status">加载中…</div>
    <div v-else-if="cars.length === 0" class="status">
      您还没有发布任何车辆。
    </div>

    <div class="cards">
      <div v-for="car in cars" :key="car.id" class="car-card">
        <img :src="getPhotoUrl(car.photo_url)" alt="车辆图片" />
        <div class="info">
          <h3>
            {{ car.brand }} <small>({{ car.year }})</small>
          </h3>
          <p>颜色：{{ car.color }}</p>
          <p>里程：{{ car.mileage }} 万公里</p>
          <p>价格：￥{{ car.price }} 万</p>
          <button @click="unrelease(car.id)" class="btn-unrelease">
            取消发布
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const cars = ref([]);
const loading = ref(true);

// 获取列表
const fetchReleased = async () => {
  loading.value = true;
  try {
    const res = await axios.get(
      "http://127.0.0.1:8000/users/api/my-released-cars/",
      { withCredentials: true }
    );
    cars.value = res.data;
  } catch (err) {
    console.error("拉取我的发布失败", err);
  } finally {
    loading.value = false;
  }
};

// 取消发布
const unrelease = async (carId) => {
  if (!confirm("确定要取消发布这辆车？")) return;
  try {
    await axios.delete("http://127.0.0.1:8000/users/api/my-released-cars/", {
      data: { car_id: carId },
      withCredentials: true,
    });
    cars.value = cars.value.filter((c) => c.id !== carId);
    alert("已取消发布");
  } catch (err) {
    console.error("取消发布失败", err);
    alert("取消发布失败");
  }
};

// 辅助：拼接图片 URL
const getPhotoUrl = (url) => `http://127.0.0.1:8000${url}`;

onMounted(fetchReleased);
</script>

<style scoped>
.released-page {
  padding: 20px;
}
.released-page h2 {
  margin-bottom: 16px;
  font-size: 24px;
}
.status {
  text-align: center;
  color: #888;
  margin: 40px 0;
}
.cards {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}
.car-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  width: 240px;
  display: flex;
  flex-direction: column;
}
.car-card img {
  width: 100%;
  height: 140px;
  object-fit: cover;
}
.info {
  padding: 12px;
  flex: 1;
  display: flex;
  flex-direction: column;
}
.info h3 {
  margin: 0 0 8px;
  font-size: 18px;
  font-weight: 600;
}
.info p {
  margin: 4px 0;
  font-size: 14px;
  color: #555;
  flex: 1;
}
.btn-unrelease {
  margin-top: 12px;
  padding: 8px;
  background: #e53e3e;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-unrelease:hover {
  background: #c53030;
}
</style>
