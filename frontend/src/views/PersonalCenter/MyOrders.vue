<template>
  <div class="my-orders">
    <h2 class="page-title">我的订单</h2>

    <!-- 加载中 -->
    <div v-if="loading" class="loading">加载中...</div>

    <!-- 订单列表 -->
    <div v-else-if="orders.length">
      <div v-for="order in orders" :key="order.id" class="order-card">
        <img
          :src="getCarPhotoUrl(order.PhotoUrl)"
          alt="车辆图片"
          class="car-photo"
        />
        <div class="order-details">
          <h3 class="car-title">{{ order.Brand }} · {{ order.Color }}</h3>
          <div class="info-row">
            <span>年份：{{ order.Year }}</span>
            <span>里程：{{ order.Mileage }} km</span>
            <span>价格：¥{{ order.Price }}</span>
          </div>
          <p class="configuration">配置：{{ order.Configuration }}</p>
          <div class="buyer-info">
            <p>买家：{{ order.buyer_name }}</p>
            <p>电话：{{ order.phone_number }}</p>
            <p>地址：{{ order.delivery_address }}</p>
            <p>支付：{{ order.payment_method }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 无订单 -->
    <div v-else class="no-orders">暂无订单</div>

    <!-- 错误提示 -->
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const loading = ref(true);
const orders = ref([]);
const error = ref("");

const getCarPhotoUrl = (url) => `http://127.0.0.1:8000${url}`;

async function fetchOrders() {
  loading.value = true;
  error.value = "";
  try {
    const res = await axios.get("http://127.0.0.1:8000/users/api/my-orders/", {
      withCredentials: true,
    });
    orders.value = res.data.orders || [];
  } catch (err) {
    console.error(err);
    error.value = "加载订单失败，请重试";
  } finally {
    loading.value = false;
  }
}

onMounted(fetchOrders);
</script>

<style scoped>
.my-orders {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  font-family: "Helvetica Neue", sans-serif;
}

.page-title {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 30px;
  color: #2c3e50;
}

.loading,
.no-orders,
.error {
  text-align: center;
  font-size: 1.2rem;
  margin: 40px 0;
}

.error {
  color: #e74c3c;
}

.order-card {
  display: flex;
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
  margin-bottom: 20px;
  transition: transform 0.2s;
}

.order-card:hover {
  transform: translateY(-4px);
}

.car-photo {
  width: 240px;
  height: 160px;
  object-fit: cover;
}

.order-details {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.car-title {
  font-size: 1.4rem;
  margin: 0 0 10px;
  color: #34495e;
}

.info-row {
  display: flex;
  gap: 20px;
  font-size: 0.95rem;
  color: #555;
  margin-bottom: 10px;
}

.configuration {
  font-size: 0.95rem;
  color: #666;
  margin-bottom: 15px;
}

.buyer-info p {
  font-size: 0.9rem;
  color: #444;
  margin: 4px 0;
}
</style>
