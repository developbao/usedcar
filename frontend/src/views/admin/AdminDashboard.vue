<template>
  <div class="admin-dashboard">
    <aside class="sidebar">
      <ul class="nav-list">
        <li>
          <RouterLink
            to="/admin/checking_cars"
            class="nav-button"
            active-class="active"
          >
            待审核车辆
          </RouterLink>
        </li>
        <li>
          <RouterLink
            to="/admin/users"
            class="nav-button"
            active-class="active"
          >
            用户管理
          </RouterLink>
        </li>
        <li>
          <RouterLink
            to="/admin/data-analysis"
            class="nav-button"
            active-class="active"
          >
            数据分析
          </RouterLink>
        </li>
        <li>
          <button @click="logout" class="nav-button" active-class="active">
            退出登录
          </button>
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
import { useRouter } from "vue-router";
import { useAdminStore } from "../../stores/admin";

const adminStore = useAdminStore();
const router = useRouter();

const logout = () => {
  adminStore.logout();
  router.push("/");
};
</script>

<style scoped>
.admin-dashboard {
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

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-list li + li {
  margin-top: 12px;
}

/* 基本导航按钮样式 */
.nav-button {
  display: block;
  padding: 10px 16px;
  border-radius: 6px;
  color: #555;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s;
  background-color: #ffffff; /* 为按钮提供一个统一背景 */
  border: 1px solid transparent; /* 去掉默认边框 */
}

/* 鼠标悬停时效果 */
.nav-button:hover {
  background-color: #f5f7fa;
  color: #3498db;
}

/* 激活状态样式 */
.nav-button.active {
  background: linear-gradient(90deg, #3498db, #2c3e50);
  color: #fff !important;
  box-shadow: 0 2px 6px rgba(78, 84, 200, 0.3);
}

/* 按钮样式 - 针对 <button> 元素 */
.nav-button:focus {
  outline: none; /* 去掉聚焦时的轮廓线 */
  box-shadow: none; /* 去掉按钮点击时的默认阴影 */
}

.nav-list li button {
  display: block;
  width: 100%; /* 让按钮宽度和其他链接一致 */
  background-color: #ffffff;
  padding: 10px 16px;
  border-radius: 6px;
  color: #555;
  font-weight: bolder;
  text-align: left;
  cursor: pointer;
  border: 1px solid transparent; /* 去掉默认边框 */
  transition: all 0.2s;
}

/* 退出按钮的悬停效果 */
.nav-list li button:hover {
  background-color: #f5f7fa;
  color: #3498db;
}

/* 退出按钮的激活效果 */
.nav-list li button.active {
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
