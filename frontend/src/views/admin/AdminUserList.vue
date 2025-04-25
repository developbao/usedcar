<template>
  <div class="container">
    <h2 class="title">用户列表</h2>
    <table class="user-table">
      <thead>
        <tr>
          <th>登录名</th>
          <th>姓名</th>
          <th>手机号</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.login_name }}</td>
          <td>{{ user.name }}</td>
          <td>{{ user.phone_num }}</td>
          <td>
            <button @click="viewUserProfile(user.id)">查看画像</button>
            <button @click="deleteUser(user.id)" class="delete-button">
              删除用户
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <UserProfileDialog
      v-if="dialogVisible"
      :userProfile="userProfile"
      @close="dialogVisible = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import UserProfileDialog from "@/views/admin/UserProfile.vue";

const users = ref([]);
const dialogVisible = ref(false);
const userProfile = ref(null);

const fetchUsers = async () => {
  try {
    const res = await axios.get(
      "http://127.0.0.1:8000/users/api/admin/users/",
      {
        withCredentials: true,
      }
    );
    users.value = res.data;
  } catch (err) {
    alert("加载用户列表失败");
  }
};

const deleteUser = async (userId) => {
  try {
    await axios.delete(
      `http://127.0.0.1:8000/users/api/admin/users/${userId}/delete/`,
      {
        withCredentials: true,
      }
    );
    alert("用户已删除");
    users.value = users.value.filter((user) => user.id !== userId);
  } catch (err) {
    alert("删除失败");
  }
};

const viewUserProfile = async (userId) => {
  try {
    const res = await axios.get(
      `http://127.0.0.1:8000/users/api/admin/users/${userId}/`,
      {
        withCredentials: true,
      }
    );
    userProfile.value = res.data;
    // console.log(userProfile);
    dialogVisible.value = true;
  } catch (err) {
    alert("加载画像失败");
  }
};

onMounted(fetchUsers);
</script>

<style scoped>
.container {
  padding: 24px;
  width: 90%;
  margin: 0 auto;
  background-color: #f9fafb;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
}

.title {
  font-size: 28px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 24px;
  text-align: center;
}

.user-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 10px;
}

.user-table th {
  background-color: #e5e7eb;
  padding: 14px;
  text-align: center;
  font-weight: 600;
  color: #374151;
  border-radius: 8px 8px 0 0;
}

.user-table td {
  background-color: #ffffff;
  padding: 16px;
  text-align: center;
  color: #4b5563;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);
  border-radius: 0;
}

.user-table tr {
  border-radius: 8px;
  overflow: hidden;
}

.user-table tr td:first-child {
  border-radius: 8px 0 0 8px;
}

.user-table tr td:last-child {
  border-radius: 0 8px 8px 0;
}

button {
  padding: 8px 14px;
  margin: 4px;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

button:hover {
  transform: translateY(-1px);
  opacity: 0.9;
}

button:active {
  transform: scale(0.98);
}

button:not(.delete-button) {
  background-color: #3b82f6;
  color: white;
}

.delete-button {
  background-color: #ef4444;
  color: white;
}
</style>
