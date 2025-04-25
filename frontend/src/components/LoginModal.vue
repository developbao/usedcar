<template>
  <div class="modal-overlay" @click.self="close">
    <div class="modal">
      <div class="modal-header">
        <div class="tabs">
          <span :class="{ active: isLogin }" @click="isLogin = true">登录</span>
          <span :class="{ active: !isLogin }" @click="isLogin = false"
            >注册</span
          >
        </div>
        <button class="close-btn" @click="close">✖</button>
      </div>

      <form @submit.prevent="isLogin ? handleLogin() : handleRegister()">
        <input v-model="form.login_name" placeholder="用户名" required />
        <input
          v-model="form.passwd"
          type="password"
          placeholder="密码"
          required
        />

        <template v-if="!isLogin">
          <input v-model="form.name" placeholder="真实姓名" required />
          <input v-model="form.phone_num" placeholder="手机号" required />
        </template>

        <button class="submit-btn" type="submit">
          {{ isLogin ? "登录" : "注册" }}
        </button>
      </form>
      <div class="admin-entry">
        <router-link to="/admin/login" class="admin-btn" @click.native="close">
          管理员入口
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useUserStore } from "@/stores/user";

const emit = defineEmits(["close"]);
const userStore = useUserStore();
const isLogin = ref(true);
const form = ref({
  login_name: "",
  passwd: "",
  name: "",
  phone_num: "",
});

const close = () => emit("close");

const handleLogin = async () => {
  const success = await userStore.login(form.value);
  if (success) {
    close();
    console.log("登录成功：", form.value);
  } else {
    console.log("登录失败：", form.value);
  }
};

const handleRegister = async () => {
  const success = await userStore.register(form.value);
  if (success) close();
  else console.log("failed to register!");
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: #fff;
  border-radius: 16px;
  width: 400px;
  padding: 30px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
  position: relative;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.tabs {
  display: flex;
  gap: 20px;
}

.tabs span {
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  color: #888;
  padding-bottom: 4px;
  transition: all 0.2s ease;
}

.tabs .active {
  color: #2b5876;
  border-bottom: 2px solid #2b5876;
}

.close-btn {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #888;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #333;
}

form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

input {
  padding: 10px 14px;
  border-radius: 8px;
  border: 1px solid #ccc;
  outline: none;
  font-size: 14px;
  transition: border-color 0.3s;
}

input:focus {
  border-color: #2b5876;
}

.submit-btn {
  background-color: #ff7d00;
  color: white;
  padding: 12px;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-btn:hover {
  background-color: #e46d00;
}

.admin-entry {
  text-align: center;
  margin-top: 12px;
}

.admin-btn {
  display: inline-block;
  padding: 6px 12px;
  background: rgba(0, 0, 0, 0.1);
  color: #666;
  border-radius: 4px;
  font-size: 13px;
  text-decoration: none;
  transition: background 0.2s, color 0.2s;
}
.admin-btn:hover {
  background: rgba(0, 0, 0, 0.15);
  color: #444;
}
</style>
