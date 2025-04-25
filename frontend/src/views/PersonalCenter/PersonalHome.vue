<template>
  <div class="personal-page">
    <aside class="sidebar">
      <ul class="nav-list">
        <li>
          <RouterLink
            to="/personal/collection"
            class="nav-button"
            active-class="active"
            >我的收藏</RouterLink
          >
        </li>
        <li>
          <RouterLink
            to="/personal/released"
            class="nav-button"
            active-class="active"
            >我的发布</RouterLink
          >
        </li>
        <li>
          <RouterLink
            to="/personal/pending"
            class="nav-button"
            active-class="active"
            >待审核车辆</RouterLink
          >
        </li>
        <li>
          <RouterLink
            to="/personal/orders"
            class="nav-button"
            active-class="active"
            >我的订单</RouterLink
          >
        </li>
      </ul>
    </aside>

    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";
</script>

<style scoped>
.personal-page {
  display: flex;
  height: 100vh;
  font-family: "PingFang SC", "Helvetica Neue", Arial, sans-serif;
  background: #f0f2f5;
}

/* 侧边栏 */
.sidebar {
  width: 12%;
  background-color: #ffffff;
  border-right: 1px solid #e0e0e0;
  padding: 24px;
  box-sizing: border-box;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.03);
}

.logo {
  font-size: 1.4rem;
  font-weight: bold;
  color: #3498db;
  margin-bottom: 24px;
  text-align: center;
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-list li + li {
  margin-top: 12px;
}

.nav-button {
  display: block;
  padding: 10px 16px;
  border-radius: 6px;
  color: #555;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s;
}

.nav-button:hover {
  background-color: #f5f7fa;
  color: #3498db;
}

.nav-button.active {
  background: linear-gradient(90deg, #3498db, #2c3e50);
  color: #fff !important;
  box-shadow: 0 2px 6px rgba(78, 84, 200, 0.3);
}

/* 内容区 */
.content {
  flex: 1;
  padding: 32px;
  overflow-y: auto;
  background: #f0f2f5;
}

/* 给滚动条加个清淡样式 */
.content::-webkit-scrollbar {
  width: 8px;
}
.content::-webkit-scrollbar-track {
  background: #f0f2f5;
}
.content::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}
</style>
