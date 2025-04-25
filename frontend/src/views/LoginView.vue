<template>
  <div class="login-box">
    <h2>登录</h2>
    <input v-model="username" placeholder="用户名" />
    <input v-model="password" type="password" placeholder="密码" />
    <button @click="handleLogin">登录</button>
    <p class="switch-link" @click="router.push('/register')">
      还没有账号？注册
    </p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "@/stores/user";

const username = ref("");
const password = ref("");
const router = useRouter();
const userStore = useUserStore();

const handleLogin = async () => {
  const success = await userStore.login(username.value, password.value);
  if (success) {
    router.push("/");
  } else {
    console.log("登录失败，请检查用户名或密码");
    console.log(username.value, password.value);
  }
};
</script>

<style scoped>
.login-box {
  max-width: 400px;
  margin: 100px auto;
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
input {
  display: block;
  width: 100%;
  margin: 10px 0;
  padding: 10px;
}
button {
  width: 100%;
  padding: 10px;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
}
.switch-link {
  color: #3b82f6;
  margin-top: 12px;
  text-align: center;
  cursor: pointer;
}
</style>
