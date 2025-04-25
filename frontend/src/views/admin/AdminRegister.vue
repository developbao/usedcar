<template>
  <div class="admin-register">
    <h2>管理员注册</h2>
    <form @submit.prevent="handleRegister">
      <input v-model="form.login_name" placeholder="用户名" required />
      <input
        v-model="form.passwd"
        type="password"
        placeholder="密码"
        required
      />
      <input
        v-model="form.password2"
        type="password"
        placeholder="确认密码"
        required
      />
      <input v-model="form.name" placeholder="真实姓名" required />
      <input v-model="form.phone_num" placeholder="电话号码" required />
      <input v-model="form.admin_key" placeholder="管理员密钥" required />
      <button class="submit-btn" type="submit">注册</button>
      <p v-if="errorMsg" style="color: red">{{ errorMsg }}</p>
      <div class="admin-entry">
        <router-link to="/admin/login" class="admin-btn">
          已有账号？ 登录
        </router-link>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useAdminStore } from "@/stores/admin";
import { useRouter } from "vue-router";

const adminStore = useAdminStore();
const router = useRouter();

const form = ref({
  login_name: "",
  passwd: "",
  password2: "",
  name: "",
  phone_num: "",
  admin_key: "",
});

const errorMsg = ref("");

const handleRegister = async () => {
  errorMsg.value = "";
  try {
    const res = await adminStore.register(form.value);
    alert("注册成功，正在跳转登录页");
    router.push("/admin/login"); // 修改为你的路由路径
  } catch (error) {
    errorMsg.value =
      error.response?.data?.message || "注册失败，请检查表单内容";
  }
};
</script>

<style scoped>
.admin-register {
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
