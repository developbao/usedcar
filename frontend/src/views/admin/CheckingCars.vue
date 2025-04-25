<template>
  <div class="checking-cars-page">
    <h2 class="page-title">待审核车辆</h2>
    <div class="car-list">
      <div v-for="car in cars" :key="car.id" class="car-card">
        <img
          :src="getCarPhotoUrl(car.PhotoUrl)"
          alt="车辆照片"
          class="car-image"
        />
        <div class="car-info">
          <h3>{{ car.Brand }} - {{ car.Year }}</h3>
          <p>颜色：{{ car.Color }}</p>
          <p>里程：{{ car.Mileage }} km</p>
          <p>价格：¥{{ car.Price }}</p>
          <p>配置：{{ car.Configuration }}</p>
          <p>描述：{{ car.ConditionDescription }}</p>

          <div class="action-buttons">
            <button class="approve-btn" @click="approveCar(car.id)">
              通过
            </button>
            <button class="reject-btn" @click="rejectCar(car.id)">
              不通过
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { ElMessage } from "element-plus";

const cars = ref([]);

const getCarPhotoUrl = (photoUrl) => {
  return `http://127.0.0.1:8000/${photoUrl}`;
};

const fetchCheckingCars = async () => {
  try {
    const res = await axios.get(
      "http://127.0.0.1:8000/users/api/admin_dashboard/",
      {},
      {
        withCredentials: true,
      }
    );
    cars.value = res.data;
  } catch (err) {
    ElMessage.error("加载待审核车辆失败");
  }
};

const approveCar = async (carId) => {
  try {
    await axios.post(
      `http://127.0.0.1:8000/users/api/checking_car/${carId}/approve/`,
      {},
      {
        withCredentials: true,
      }
    );
    ElMessage.success("审核通过");
    cars.value = cars.value.filter((car) => car.id !== carId);
  } catch (err) {
    ElMessage.error("审核通过失败");
  }
};

const rejectCar = async (carId) => {
  try {
    await axios.delete(
      `http://127.0.0.1:8000/users/api/checking_car/${carId}/reject/`,
      {},
      {
        withCredentials: true,
      }
    );
    ElMessage.success("车辆已拒绝");
    cars.value = cars.value.filter((car) => car.id !== carId);
  } catch (err) {
    ElMessage.error("操作失败");
  }
};

onMounted(() => {
  fetchCheckingCars();
});
</script>

<style scoped>
.checking-cars-page {
  padding: 20px;
}

.page-title {
  font-size: 1.6rem;
  margin-bottom: 20px;
}

.car-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.car-card {
  width: 300px;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
}

.car-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.car-info {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.action-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 12px;
}

.approve-btn {
  background-color: #4caf50;
  color: #fff;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.2s;
}

.reject-btn {
  background-color: #f44336;
  color: #fff;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.2s;
}

.approve-btn:hover {
  background-color: #43a047;
}

.reject-btn:hover {
  background-color: #e53935;
}
</style>
