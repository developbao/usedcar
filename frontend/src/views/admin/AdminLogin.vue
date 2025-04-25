<template>
  <div class="admin-login">
    <h2>管理员登录</h2>
    <form @submit.prevent="handleLogin">
      <input v-model="form.login_name" placeholder="用户名" required />
      <input
        v-model="form.passwd"
        type="password"
        placeholder="密码"
        required
      />
      <button class="submit-btn" type="submit">登录</button>
      <div class="admin-entry">
        <router-link to="/admin/register" class="admin-btn">
          没有账号？ 注册
        </router-link>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAdminStore } from "@/stores/admin"; // 导入store

const form = ref({
  login_name: "",
  passwd: "",
});

const router = useRouter();
const adminStore = useAdminStore();

const handleLogin = async () => {
  const success = await adminStore.login(form.value);
  if (success) {
    // 登录成功，跳转到管理后台
    console.log("登录成功，跳转到管理后台");
    // 你可以用 vue-router 跳转到管理员面板
    router.push("/admin");
  } else {
    console.log("登录失败");
  }
};

// 页面加载时检查登录状态
onMounted(() => {
  adminStore.checkLoginStatus();
});
</script>

<style scoped>
.admin-login {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}

input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.submit-btn {
  width: 100%;
  padding: 12px;
  background-color: #ff7d00;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
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
