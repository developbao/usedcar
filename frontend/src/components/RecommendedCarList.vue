<!-- src/components/RecommendedCars.vue -->
<template>
  <section class="recommended-section">
    <div v-if="loading" class="loading-text">加载中...</div>
    <div v-else-if="cars.length === 0" class="empty-text">暂无推荐车辆</div>

    <div class="car-list">
      <CarCard v-for="car in cars" :key="car.id" :car="car" />
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import axios from "axios";
import { useUserStore } from "@/stores/user";
import CarCard from "@/components/CarCard.vue";

const props = defineProps({
  shouldRefresh: Number,
});

const cars = ref([]);
const loading = ref(true);
const userStore = useUserStore();

const fetchRecommendations = async () => {
  loading.value = true;
  try {
    const res = await axios.get(
      "http://127.0.0.1:8000/users/api/recommend-cars/",
      {
        withCredentials: userStore.isLoggedIn,
      }
    );
    cars.value = res.data.data || [];
  } catch (error) {
    console.error("获取推荐车辆失败", error);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchRecommendations);

watch(
  () => props.shouldRefresh,
  () => {
    fetchRecommendations();
  }
);
</script>

<style scoped>
.recommended-section {
  background-color: #f7f9fc;
  min-height: 100vh;
  width: 100%;
}

.loading-text,
.empty-text {
  text-align: center;
  color: #888;
  font-size: 18px;
  margin-top: 100px;
}

.car-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: space-around;
}
</style>
