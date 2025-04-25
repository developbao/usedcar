<template>
  <section class="banner">
    <div class="top-bar">
      <div class="left-buttons">
        <router-link to="/" class="top-button">首页</router-link>
        <router-link to="/search" class="explore-button">立即选购</router-link>
      </div>

      <h1 class="slogan">二手好车，放心选购</h1>

      <div class="right-buttons">
        <!-- 未登录状态 -->
        <template v-if="!userStore.isLoggedIn && !adminStore.isLoggedIn">
          <button class="top-button" @click="showLogin = true">用户登录</button>
          <router-link to="/admin/login" class="top-button">管理员</router-link>
        </template>

        <!-- 管理员登录状态 -->
        <template v-if="adminStore.isLoggedIn">
          <router-link to="/admin" class="top-button">后台管理</router-link>
          <button class="top-button" @click="handleLogoutAdmin">登出</button>
        </template>

        <!-- 用户登录状态 -->
        <template v-if="userStore.isLoggedIn">
          <router-link to="/addCar" class="top-button">发布</router-link>
          <router-link to="/personal" class="top-button">我的</router-link>
          <button class="top-button" @click="handleLogout">登出</button>
        </template>
      </div>
    </div>
  </section>

  <LoginModal v-if="showLogin" @close="showLogin = false" />

  <div id="app">
    <router-view />
  </div>

  <!-- 页脚 -->
  <footer class="footer">
    <p>© 2025 豹子二手车 | 联系方式：123-456-7890</p>
  </footer>
</template>

<script setup>
import { useUserStore } from "@/stores/user";
import { useAdminStore } from "@/stores/admin";
import { useRoute, useRouter } from "vue-router";
import { ref } from "vue";

import RecommendedCarList from "@/components/RecommendedCarList.vue";
import LoginModal from "@/components/LoginModal.vue";
import toyotaLogo from "@/assets/images/brands/toyota.png";
import BMW from "@/assets/images/brands/bmw.png";
import Honda from "@/assets/images/brands/honda.png";
import Mercedes from "@/assets/images/brands/benz.png";

const hotBrands = [
  { name: "Toyota", logo: toyotaLogo },
  { name: "BMW", logo: BMW },
  { name: "Honda", logo: Honda },
  { name: "Mercedes", logo: Mercedes },
];

const showLogin = ref(false);
const userStore = useUserStore();
const adminStore = useAdminStore();

const handleLogout = async () => {
  const success = await userStore.logout();
  if (success) location.reload();
};

const handleLogoutAdmin = () => {
  adminStore.logout();
};
</script>

<style>
.banner {
  width: 100%;
  background: linear-gradient(45deg, #3498db, #2c3e50);
  color: white;
  padding: 0;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 20px;
  height: 60px;
  position: relative;
}

/* 标语居中 */
.slogan {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  font-size: 18px;
  margin: 0;
  font-weight: bold;
  color: white;
  white-space: nowrap;
}

.top-button {
  background-color: rgba(255, 255, 255, 0.9);
  color: #3498db;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 14px;
  text-decoration: none;
  font-weight: bold;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.top-button:hover {
  background-color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 立即选购按钮样式 */
.explore-button {
  background-color: #ffffff;
  color: #3498db;
  padding: 6px 14px;
  border-radius: 20px;
  text-decoration: none;
  font-size: 14px;
  font-weight: bold;
  margin-right: 10px;
  transition: all 0.3s ease;
}

.explore-button:hover {
  background-color: #3498db;
  color: white;
}

.right-buttons,
.left-buttons {
  display: flex;
  align-items: center;
  gap: 10px;
}

/* 确保 html, body 和 #app 都具有 100% 高度 */
html,
body,
#app {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  overflow: auto;
}

/* 隐藏滚动条（WebKit 浏览器） */
::-webkit-scrollbar {
  width: 0px;
  height: 0px;
  display: none;
}

.footer {
  background: linear-gradient(45deg, #3498db, #2c3e50);
  text-align: center;
  padding: 30px 10px;
  background-color: #eee;
  color: #ffffff;
  margin-top: 40px;
}
</style>
