// src/stores/user.js
import { defineStore } from "pinia";
import axios from "axios";

export const useUserStore = defineStore("user", {
  state: () => ({
    user: null,
    isLoggedIn: false,
    justLoggedIn: false,
    justloggedOut: false,
  }),
  actions: {
    async login(userData) {
      try {
        const res = await axios.post(
          "http://127.0.0.1:8000/users/api/login/",
          {
            login_name: userData.login_name,
            passwd: userData.passwd,
          },
          {
            withCredentials: true,
          }
        );
        this.user = res.data.user || { login_name: userData.login_name };
        this.isLoggedIn = true;
        this.justLoggedIn = true;
        console.log("yes");
        return { success: true };
      } catch (error) {
        console.log("no", error.response.data);
        return {
          success: false,
          message: error.response?.data?.error || "登录失败",
        };
      }
    },

    clearLoginFlag() {
      this.justLoggedIn = false; // ✅ 清除刷新标志
    },

    async register(userData) {
      try {
        const res = await axios.post(
          "http://127.0.0.1:8000/users/api/register/",
          {
            login_name: userData.login_name,
            passwd: userData.passwd,
            name: userData.name,
            phone_num: userData.phone_num,
          }
        );
        if (res.data.message === "注册成功") {
          //router.push("/login");
          console.log("注册成功", res.data);
          return true;
        } else {
          console.error("注册失败", res.data);
          return false;
        }
      } catch (error) {
        console.log("注册失败", error.response.data);
        return {
          success: false,
          message: error.response?.data?.error || "注册失败",
        };
      }
    },

    async logout() {
      const res = await axios.post("http://127.0.0.1:8000/users/api/logout/");
      this.user = null;
      this.isLoggedIn = false;
      this.justLoggedOut = true;
    },

    clearLogoutFlag() {
      this.justLoggedOut = false; // ✅ 清除刷新标志
    },
  },
  persist: true, // 需要 pinia-plugin-persistedstate 支持
});
