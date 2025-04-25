<template>
  <div class="register-container">
    <form class="register-form" @submit.prevent="handleRegister">
      <h2 class="title">用户注册</h2>

      <input v-model="form.login_name" placeholder="用户名" required />
      <input
        v-model="form.passwd"
        placeholder="密码"
        type="password"
        required
      />
      <input v-model="form.name" placeholder="真实姓名" required />
      <input v-model="form.phone_num" placeholder="手机号" required />

      <button type="submit">注册</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";

const userStore = useUserStore();
const router = useRouter();

const form = ref({
  login_name: "",
  passwd: "",
  name: "",
  phone_num: "",
});

const handleRegister = async () => {
  const success = await userStore.register(form.value);
  if (success) {
    alert("注册成功！");
    router.push("/login");
  } else {
    alert("注册失败，请检查信息！");
  }
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(to right, #2b5876, #4e4376);
}

.register-form {
  background-color: white;
  padding: 40px 30px;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
}

.title {
  text-align: center;
  margin-bottom: 24px;
  color: #2b5876;
  font-size: 1.8rem;
}

.register-form input {
  padding: 10px 14px;
  margin-bottom: 16px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.register-form input:focus {
  outline: none;
  border-color: #2b5876;
}

.register-form button {
  background-color: #2b5876;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.register-form button:hover {
  background-color: #1d3f5e;
}
</style>
