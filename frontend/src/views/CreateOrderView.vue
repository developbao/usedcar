<template>
  <div class="create-order-container">
    <div class="order-card">
      <h2>创建订单</h2>
      <p class="car-id">车辆 ID: {{ carId }}</p>

      <form @submit.prevent="submitOrder" class="order-form">
        <input v-model="buyerName" placeholder="买家姓名" required />
        <input v-model="phoneNumber" placeholder="电话" required />
        <input v-model="deliveryAddress" placeholder="送货地址" required />
        <select v-model="paymentMethod" required>
          <option value="credit_card">信用卡</option>
          <option value="paypal">PayPal</option>
        </select>
        <button type="submit">提交订单</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import { useUserStore } from "../stores/user";

const userStore = useUserStore();
const route = useRoute();
const router = useRouter();
const carId = route.params.carId;

const buyerName = ref("");
const phoneNumber = ref("");
const deliveryAddress = ref("");
const paymentMethod = ref("credit_card");

const submitOrder = async () => {
  try {
    const response = await axios.post(
      `http://127.0.0.1:8000/users/api/create_order/${carId}/`,
      {
        buyer_name: buyerName.value,
        phone_number: phoneNumber.value,
        delivery_address: deliveryAddress.value,
        payment_method: paymentMethod.value,
      },
      {
        withCredentials: userStore.isLoggedIn,
        headers: {
          "X-CSRFToken": getCsrfTokenFromCookie(),
        },
      }
    );
    alert("订单创建成功！");
    router.push("/");
  } catch (error) {
    console.error("订单创建失败", error);
  }
};

function getCsrfTokenFromCookie() {
  const matches = document.cookie.match(/csrftoken=([^;]+)/);
  return matches ? matches[1] : "";
}
</script>

<style scoped>
.create-order-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 3rem 1rem;
  background-color: #f4f7fa;
  min-height: 100vh;
}

.order-card {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500px;
}

.order-card h2 {
  font-size: 1.8rem;
  margin-bottom: 1rem;
  color: #333;
  text-align: center;
}

.car-id {
  font-size: 0.9rem;
  color: #888;
  margin-bottom: 1.5rem;
  text-align: center;
}

.order-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.order-form input,
.order-form select {
  padding: 0.75rem 1rem;
  border: 1px solid #ccc;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: border-color 0.2s ease;
}

.order-form input:focus,
.order-form select:focus {
  outline: none;
  border-color: #007bff;
}

.order-form button {
  background-color: #007bff;
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.order-form button:hover {
  background-color: #0056b3;
}
</style>
