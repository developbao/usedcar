<template>
  <div class="my-collection-page">
    <h2>我的收藏</h2>
    <div v-if="loading" class="status-text">加载中…</div>
    <div v-else-if="error" class="status-text error">{{ error }}</div>
    <div v-else-if="cars.length === 0" class="status-text">
      您还没有收藏任何车辆
    </div>
    <div class="car-grid">
      <CarCard v-for="car in cars" :key="car.id" :car="car" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import CarCard from "@/components/CarCard.vue";

const router = useRouter();
const cars = ref([]);
const loading = ref(true);
const error = ref("");

const fetchCollection = async () => {
  loading.value = true;
  error.value = "";
  try {
    const res = await axios.get(
      "http://127.0.0.1:8000/users/api/my-collection/",
      { withCredentials: true }
    );
    cars.value = res.data.available_cars;
  } catch (err) {
    if (err.response?.status === 401) {
      error.value = "请先登录";
      // 2 秒后跳转到登录页
      setTimeout(() => router.push("/login"), 2000);
    } else {
      error.value = "获取收藏失败，请稍后重试";
      console.error(err);
    }
  } finally {
    loading.value = false;
  }
};

onMounted(fetchCollection);
</script>

<style scoped>
.my-collection-page {
  padding: 20px;
}
h2 {
  font-size: 24px;
  margin-bottom: 16px;
  color: #333;
}
.status-text {
  text-align: center;
  color: #888;
  margin: 40px 0;
}
.status-text.error {
  color: #e74c3c;
}
.car-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: left;
}
</style>
