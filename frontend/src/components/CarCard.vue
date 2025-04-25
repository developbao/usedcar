<!-- src/components/CarCard.vue -->
<template>
  <div class="car-card" @click="goToDetail(car.id)">
    <img
      :src="getCarPhotoUrl(car.photo_url)"
      alt="车辆图片"
      class="car-image"
    />
    <div class="car-info">
      <h3>{{ car.brand }} - {{ car.year.split("-")[0] }}</h3>
      <p><strong>价格：</strong>￥{{ car.price?.toLocaleString() }}万元</p>
      <p><strong>里程：</strong>{{ car.mileage }}</p>
      <p><strong>配置：</strong>{{ car.configuration }}</p>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
const props = defineProps({
  car: Object,
});
const router = useRouter();

const goToDetail = (id) => {
  console.log("即将跳转的车辆 ID：", id);
  router.push(`/car/${id}`);
};

const getCarPhotoUrl = (photoUrl) => {
  return `http://127.0.0.1:8000/${photoUrl}`;
};
</script>

<style scoped>
.text-primary {
  color: #f97316;
}

.car-card {
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
  width: 300px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease-in-out;
}

.car-card:hover {
  transform: translateY(-10px);
}

.car-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.car-info {
  padding: 15px;
  text-align: center;
}

.car-info h3 {
  font-size: 20px;
  margin-bottom: 10px;
}

.car-info p {
  font-size: 14px;
  margin: 5px 0;
  color: #555;
}
</style>
