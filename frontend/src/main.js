// src/main.js
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { createPinia } from "pinia"; // 漏了这一行
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";

import { useUserStore } from "@/stores/user";
import axios from "axios";

axios.defaults.withCredentials = true; // ✅ 关键：全局设置

const app = createApp(App);

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

app.use(pinia); // 应该先 app.use(pinia)
app.use(router); // 然后再 use(router)
app.mount("#app"); // 最后 mount

// 开发调试用：挂到 window 上
if (import.meta.env.DEV) {
  window.userStore = useUserStore(); // 用于在控制台直接用 window.userStore
}
