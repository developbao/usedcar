<!-- src/views/HomeView.vue -->
<template>
  <div class="home">
    <!-- 顶部横幅 -->

    <!-- 热门品牌 -->
    <section class="section brands">
      <div class="container">
        <h2 class="section-title">热门品牌</h2>
        <div class="brand-grid">
          <div
            v-for="brand in hotBrands"
            :key="brand.name"
            class="brand-card"
            @click="goToBrandSearch(brand.name)"
          >
            <img :src="brand.logo" :alt="brand.name" />
            <span>{{ brand.name }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- 推荐车辆 -->
    <section class="section">
      <div class="container">
        <h2 class="section-title">推荐车辆</h2>
        <RecommendedCarList :shouldRefresh="refreshRecommended" />
      </div>
    </section>
  </div>
</template>

<script setup>
import { useUserStore } from "../stores/user";
import { useRoute, useRouter } from "vue-router";
import { ref, watch, onMounted } from "vue";

import RecommendedCarList from "@/components/RecommendedCarList.vue";
import toyotaLogo from "@/assets/images/brands/toyota.png";
import BMW from "@/assets/images/brands/bmw.png";
import Honda from "@/assets/images/brands/honda.png";
import Mercedes from "@/assets/images/brands/benz.png";

const hotBrands = [
  { name: "丰田", logo: toyotaLogo },
  { name: "宝马", logo: BMW },
  { name: "本田", logo: Honda },
  { name: "奔驰", logo: Mercedes },
];

const showLogin = ref(false);
const userStore = useUserStore();
const router = useRouter();

const goToBrandSearch = (brandName) => {
  router.push({
    path: "/search",
    query: { brand: brandName },
  });
};
const handleLogout = async () => {
  const success = await userStore.logout();
  if (success) location.reload();
};

const refreshRecommended = ref(0);

watch(
  [() => userStore.justLoggedIn, () => userStore.justLoggedOut],
  ([justLoggedIn, justLoggedOut]) => {
    if (justLoggedIn || justLoggedOut) {
      refreshRecommended.value++;

      // 清除标志位
      if (justLoggedIn) userStore.clearLoginFlag();
      if (justLoggedOut) userStore.clearLogoutFlag();
    }
  }
);
</script>

<style scoped>
.home {
  font-family: "Helvetica Neue", sans-serif;
  background-color: #f9f9f9;
  color: #333;
}

.section {
  width: 100%;
  margin: 40px 0;
  padding: 0 20px;
  box-sizing: border-box;
}

.section-title {
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 20px;
  color: #222;
}

.container {
  width: 100%;
  margin: 0 auto;
}

.brand-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 60px;
  justify-content: center;
}

.brand-card {
  background-color: white;
  padding: 16px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
  width: 20%;
  text-align: center;
  transition: transform 0.3s;
}

.brand-card img {
  height: 120px;
  width: 100%;
  object-fit: cover;
  margin-bottom: 8px;
}

.brand-card:hover {
  transform: translateY(-4px);
}
</style>
