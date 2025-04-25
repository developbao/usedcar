<template>
  <div class="base">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="!car" class="not-found">车辆信息未找到</div>
    <div v-else class="container">
      <h2 class="title">{{ car.Brand }} {{ car.Model }}</h2>

      <img :src="getPhotoUrl(car.PhotoUrl)" alt="车辆图片" class="car-image" />

      <div class="car-details">
        <p><strong>品牌:</strong> {{ car.Brand }}</p>
        <p><strong>年份:</strong> {{ car.Year }}</p>
        <p><strong>价格:</strong> {{ car.Price }} 万</p>
        <p><strong>颜色:</strong> {{ car.Color }}</p>
        <p><strong>里程:</strong> {{ car.Mileage }} 公里</p>
        <p><strong>配置:</strong> {{ car.Configuration }}</p>
        <p><strong>描述:</strong> {{ car.ConditionDescription }}</p>
      </div>

      <div class="button-group">
        <button
          @click="toggleLike"
          class="like-button"
          :class="{ liked: isLiked }"
        >
          {{ isLiked ? "已收藏" : "收藏" }}
        </button>

        <button @click="buyCar" class="buy-button">立即购买</button>
      </div>
    </div>
  </div>
  <LoginModal v-if="showLogin" @close="showLogin = false" />
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import { useUserStore } from "@/stores/user";
import LoginModal from "@/components/LoginModal.vue";

const userStore = useUserStore();
const showLogin = ref(false);

const route = useRoute();
const router = useRouter();
const carId = route.params.id;
// console.log(carId);
// const url = `http://127.0.0.1:8000/users/api/car/detail/${carId}/`;
// console.log("请求的 URL：", url);

const car = ref(null);
const isLiked = ref(false);
const loading = ref(true);

const fetchCarDetail = async () => {
  try {
    const res = await axios.get(
      `http://127.0.0.1:8000/users/api/car/detail/${carId}/`,
      {
        withCredentials: userStore.isLoggedIn,
      }
    );
    console.log(res);
    car.value = res.data.car;
    console.log(car.value);
    isLiked.value = res.data.is_liked;
  } catch (err) {
    console.error("加载车辆详情失败", err);
  } finally {
    loading.value = false;
  }
};

const toggleLike = async () => {
  if (!userStore.isLoggedIn) {
    showLogin.value = true;
    return;
  }
  try {
    const res = await axios.post(
      `http://127.0.0.1:8000/users/api/car/detail/${carId}/`,
      { action: "like" },
      {
        withCredentials: userStore.isLoggedIn,
      }
    );
    isLiked.value = res.data.is_liked;
  } catch (err) {
    console.error("收藏失败", err);
  }
};

const buyCar = async () => {
  if (!userStore.isLoggedIn) {
    showLogin.value = true;
    return;
  }
  try {
    const res = await axios.post(
      `http://127.0.0.1:8000/users/api/car/detail/${carId}/`,
      { action: "buy" },
      {
        withCredentials: userStore.isLoggedIn,
      }
    );
    if (res.data.redirect_url) {
      router.push(res.data.redirect_url);
    }
  } catch (err) {
    console.error("购买失败", err);
  }
};

function getPhotoUrl(url) {
  return `http://127.0.0.1:8000/${url}/`;
}

onMounted(() => {
  fetchCarDetail();
});
</script>

<style scoped>
.base {
  font-family: "Helvetica Neue", Arial, sans-serif;
  background-color: #f9fafb;
  min-height: 100vh;
  padding: 40px 20px;
}

.loading,
.not-found {
  text-align: center;
  font-size: 18px;
  color: #888;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  background-color: #ffffff;
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.title {
  text-align: center;
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}

.car-image {
  display: block;
  margin: 0 auto 30px;
  max-width: 100%;
  height: auto;
  border-radius: 16px;
  object-fit: cover;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
}

.car-details {
  font-size: 16px;
  line-height: 1.6;
  color: #444;
  padding: 0 10px;
}

.car-details p {
  margin-bottom: 10px;
}

.car-details strong {
  color: #222;
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
}

.like-button,
.buy-button {
  padding: 12px 28px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: all 0.3s ease;
}

.like-button {
  background-color: #e5e7eb;
  color: #333;
}

.like-button:hover {
  background-color: #f3f4f6;
}

.like-button.liked {
  background-color: #ef4444;
  color: white;
}

.buy-button {
  background-color: #10b981;
  color: white;
}

.buy-button:hover {
  background-color: #059669;
}
</style>
