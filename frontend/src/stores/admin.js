import { defineStore } from "pinia";
import axios from "axios";

export const useAdminStore = defineStore("admin", {
  state: () => ({
    adminId: null, // 存储管理员ID
    loginName: "", // 存储管理员登录名
    name: "", // 存储管理员真实姓名
    isLoggedIn: false, // 管理员是否登录状态
  }),

  actions: {
    // 注册管理员
    async register(formData) {
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/users/api/admin/register/",
          formData,
          {
            withCredentials: true,
          }
        );
        console.log("注册成功:", response.data);
        return true;
      } catch (error) {
        console.error("Register failed:", error);
        throw error; // 交由调用方处理错误信息
      }
    },

    // 登录管理员
    async login(formData) {
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/users/api/admin/login/",
          {
            login_name: formData.login_name,
            passwd: formData.passwd,
          },
          {
            withCredentials: true,
          }
        );
        this.adminId = response.data.admin_id;
        this.loginName = formData.login_name;
        this.isLoggedIn = true;
        localStorage.setItem("admin_id", this.adminId); // 存储登录状态
        localStorage.setItem("login_name", this.loginName); // 存储管理员名字
        return true;
      } catch (error) {
        console.error("Login failed:", error);
        return false;
      }
    },

    // 登出管理员
    logout() {
      this.adminId = null;
      this.loginName = "";
      this.isLoggedIn = false;
      localStorage.removeItem("admin_id"); // 清除登录状态
      localStorage.removeItem("login_name"); // 清除登录名
    },

    // 检查是否已登录
    checkLoginStatus() {
      const storedAdminId = localStorage.getItem("admin_id");
      const storedLoginName = localStorage.getItem("login_name");
      if (storedAdminId && storedLoginName) {
        this.adminId = storedAdminId;
        this.loginName = storedLoginName;
        this.isLoggedIn = true;
      }
    },
  },
  persist: true,
});
