<template>
  <div class="add-checking-car">
    <div class="form-card">
      <h2>发布车辆</h2>
      <form @submit.prevent="submitCar" class="car-form">
        <div class="input-group">
          <input v-model="brand" type="text" placeholder="品牌" required />
        </div>
        <div class="input-group">
          <input v-model="color" type="text" placeholder="颜色" required />
        </div>
        <div class="input-group">
          <input v-model="year" type="month" placeholder="年份" required />
        </div>
        <div class="input-group">
          <input v-model="mileage" type="number" placeholder="里程" required />
        </div>
        <div class="input-group">
          <input v-model="price" type="number" placeholder="价格" required />
        </div>
        <div class="input-group">
          <input
            v-model="configuration"
            type="text"
            placeholder="配置"
            required
          />
        </div>
        <div class="input-group">
          <textarea
            v-model="conditionDescription"
            placeholder="车况描述"
            required
          ></textarea>
        </div>
        <div class="input-group">
          <input type="file" @change="handleFileChange" required />
        </div>
        <div class="submit-group">
          <button type="submit">发布车辆</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const router = useRouter();

// 表单数据
const brand = ref("");
const color = ref("");
const year = ref("");
const mileage = ref("");
const price = ref("");
const configuration = ref("");
const conditionDescription = ref("");
const photo = ref(null);

// 文件上传处理
const handleFileChange = (event) => {
  photo.value = event.target.files[0];
};

const submitCar = async () => {
  const formData = new FormData();
  formData.append("brand", brand.value);
  formData.append("color", color.value);

  const [y, m] = year.value.split("-");
  const dt = new Date(Date.UTC(Number(y), Number(m) - 1, 1, 0, 0, 0));
  formData.append("Year", dt.toISOString());

  formData.append("mileage", parseFloat(mileage.value));
  formData.append("price", parseFloat(price.value));
  formData.append("configuration", configuration.value);
  formData.append("condition_description", conditionDescription.value);
  formData.append("photo", photo.value); // 上传的文件

  try {
    const response = await axios.post(
      "http://127.0.0.1:8000/users/api/add_checking_car/", // 后端接口
      formData,
      {
        withCredentials: true, // 判断用户是否已登录，确保带上 cookies
        headers: {
          "Content-Type": "multipart/form-data", // 上传文件时设置正确的 Content-Type
          "X-CSRFToken": getCsrfTokenFromCookie(), // CSRF token
        },
      }
    );
    alert("车辆发布成功");
    router.push("/search"); // 跳转到车辆搜索页面
  } catch (error) {
    console.error("发布车辆失败", error.response.data);
    alert("发布车辆失败：" + JSON.stringify(error.response.data));
  }
};

// 从 Cookie 中获取 CSRF Token
function getCsrfTokenFromCookie() {
  const matches = document.cookie.match(/csrftoken=([^;]+)/);
  return matches ? matches[1] : "";
}
</script>

<style scoped>
.add-checking-car {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f9f9f9;
  padding: 3rem;
}

.form-card {
  background: white;
  padding: 3rem;
  border-radius: 10px;
  width: 100%;
  max-width: 600px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
}

.car-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.input-group input,
.input-group textarea {
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 1rem;
  width: 100%;
  box-sizing: border-box;
}

.input-group textarea {
  resize: vertical;
  min-height: 120px;
}

.input-group input[type="file"] {
  background: #f0f0f0;
  padding: 0.75rem;
}

.submit-group {
  display: flex;
  justify-content: center;
}

.submit-group button {
  padding: 1rem;
  border: none;
  border-radius: 8px;
  background: #007bff;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  width: 100%;
  max-width: 200px;
  transition: background 0.3s ease;
}

.submit-group button:hover {
  background: #0056b3;
}

.submit-group button:active {
  background: #004085;
}
</style>
