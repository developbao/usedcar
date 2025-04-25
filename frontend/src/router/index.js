// src/router/index.js
import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import AdminRegister from "../views/admin/AdminRegister.vue";

const routes = [
  { path: "/", name: "Home", component: HomeView },
  {
    path: "/car/:id",
    name: "CarDetail",
    component: () => import("@/views/CarDetailView.vue"),
  },
  {
    path: "/users/create_order/:carId/", // 添加这个路由
    name: "CreateOrder",
    component: () => import("@/views/CreateOrderView.vue"),
    props: true, // 将 URL 参数作为 prop 传递给组件
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("@/views/LoginView.vue"), // 有了模态框，这个登录路由其实已经可以删了
  },
  {
    path: "/register",
    name: "Register",
    component: () => import("@/views/RegisterView.vue"), // 这里也可以删掉，暂且保利一下，万一以后用得上
  },
  {
    path: "/search",
    name: "Search",
    component: () => import("@/views/SearchView.vue"),
  },
  {
    path: "/addCar",
    name: "AddCar",
    component: () => import("@/views/AddCarView.vue"),
  },
  {
    path: "/personal",
    name: "Personal",
    component: () => import("@/views/PersonalCenter/PersonalHome.vue"),
    redirect: "/personal/collection", // 默认我的主页加载我的收藏
    children: [
      {
        path: "collection",
        component: () => import("@/views/PersonalCenter/MyCollection.vue"),
      },
      {
        path: "released",
        component: () => import("@/views/PersonalCenter/MyReleasedCars.vue"),
      },
      {
        path: "pending",
        component: () => import("@/views/PersonalCenter/PendingCars.vue"),
      },
      {
        path: "orders",
        component: () => import("@/views/PersonalCenter/MyOrders.vue"),
      },
    ],
  },

  // 管理员部分
  {
    path: "/admin/login",
    name: "AdminLogin",
    component: () => import("@/views/admin/AdminLogin.vue"),
  },
  {
    path: "/admin/register",
    name: "AdminRegister",
    component: () => import("@/views/admin/AdminRegister.vue"),
  },
  {
    path: "/admin",
    name: "AdminDashboard",
    component: () => import("@/views/admin/AdminDashboard.vue"),
    redirect: "/admin/checking_cars",
    children: [
      {
        path: "checking_cars",
        name: "CheckingCars",
        component: () => import("@/views/admin/CheckingCars.vue"),
      },
      {
        path: "users",
        name: "AdminUserList",
        component: () => import("@/views/admin/AdminUserList.vue"),
        children: {
          path: "/:userId",
          name: "UserProfile",
          component: () => import("@/views/admin/UserProfile.vue"),
        },
      },
      {
        path: "data-analysis",
        name: "AdminDataAnalysis",
        component: () => import("@/views/admin/AdminDataAnalysis.vue"),
      },
    ],
  },
  { path: "/:pathMatch(.*)*", redirect: "/" },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
