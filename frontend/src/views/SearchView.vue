<template>
  <div class="search-page">
    <button class="toggle-btn" @click="toggleFilters">
      {{ showFilters ? "收起搜索框 ⬆" : "展开搜索框 ⬇" }}
    </button>
    <!-- 筛选条件表单 -->
    <transition name="fade">
      <div v-show="showFilters" class="full-width-container">
        <div class="search-bar">
          <h2>搜索车辆</h2>
          <form class="filter-form" @submit.prevent="handleSearch">
            <input v-model="filters.brand" placeholder="品牌" />
            <input
              v-model="filters.year"
              type="number"
              placeholder="年份之后"
            />
            <input
              v-model="filters.price_min"
              type="number"
              placeholder="最低价格"
            />
            <input
              v-model="filters.price_max"
              type="number"
              placeholder="最高价格"
            />
            <input v-model="filters.color" placeholder="颜色" />
            <input
              v-model="filters.mileage"
              type="number"
              placeholder="最大里程"
            />
            <input v-model="filters.configuration" placeholder="配置" />
            <input
              v-model="filters.condition_description"
              placeholder="车况描述"
            />
            <button type="submit" :disabled="loading">搜索</button>
          </form>
        </div>
      </div>
    </transition>
    <!-- 搜索结果 -->
    <div v-if="loading">加载中...</div>
    <div v-else-if="searched && cars.length === 0" class="no-results">
      没有符合条件的车辆
    </div>

    <div class="results-grid">
      <CarCard v-for="car in cars" :key="car.id" :car="car" />
    </div>

    <!-- 分页控制 -->
    <div class="pagination" v-if="totalPages > 1">
      <button
        @click="changePage(currentPage - 1)"
        :disabled="currentPage === 1"
      >
        上一页
      </button>
      <span>第 {{ currentPage }} / {{ totalPages }} 页</span>
      <button
        @click="changePage(currentPage + 1)"
        :disabled="currentPage === totalPages"
      >
        下一页
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from "vue";
import axios from "axios";
import CarCard from "@/components/CarCard.vue";
import { useRoute } from "vue-router";
const route = useRoute();

const filters = ref({
  brand: "",
  year: "",
  price_min: "",
  price_max: "",
  color: "",
  mileage: "",
  configuration: "",
  condition_description: "",
});

const cars = ref([]);
const loading = ref(false);
const currentPage = ref(1);
const totalPages = ref(1);
const searched = ref(false);

const showFilters = ref(true);

const toggleFilters = () => {
  showFilters.value = !showFilters.value;
};

const fetchCars = async () => {
  loading.value = true;
  cars.value = []; // 清空搜索结果
  try {
    const params = {
      ...filters.value,
      page: currentPage.value,
    };

    const res = await axios.get(
      "http://127.0.0.1:8000/users/api/search-cars/",
      {
        params,
        withCredentials: true,
      }
    );

    cars.value = res.data.results;

    totalPages.value = res.data.total_pages;
  } catch (err) {
    console.error("搜索失败", err);
  } finally {
    loading.value = false;
  }
};

const handleSearch = () => {
  currentPage.value = 1;
  searched.value = true;
  fetchCars();
};

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
    fetchCars();
  }
};

onMounted(async () => {
  if (route.query.brand) {
    await nextTick(); // 确保 DOM 和响应式系统都准备好了
    filters.value.brand = route.query.brand;
    handleSearch();
  }
});

watch(
  () => route.query.brand,
  (newBrand) => {
    if (newBrand) {
      filters.value.brand = newBrand;
      handleSearch();
    }
  }
);
</script>

<style scoped>
.search-page {
  padding: 20px;
  width: 100%;
  margin: auto;
}

.toggle-btn {
  background: none;
  border: none;
  font-size: 14px;
  color: #2980b9;
  cursor: pointer;
  transition: color 0.3s ease;
  padding: 6px 12px;
  margin-bottom: 15px;
  border-radius: 8px;
}

.toggle-btn:hover {
  color: #1c5980;
  background-color: #ecf0f1;
}

/* 收起/展开动画 */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: scaleY(0.95);
  transform-origin: top;
}

.full-width-container {
  width: 100%;
  padding: 60px 20px;
  background: linear-gradient(to right, #f1f3f8, #e8ecf4);
}

.search-bar {
  max-width: 1200px;
  margin: auto;
  background: #ffffff;
  border-radius: 20px;
  padding: 40px 30px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease-in-out;
}

.search-bar:hover {
  box-shadow: 0 25px 45px rgba(0, 0, 0, 0.15);
}

.search-bar h2 {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 30px;
  text-align: center;
  color: #2c3e50;
}

.filter-form {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(20%, 1fr));
  gap: 20px;
}

.filter-form input {
  padding: 12px 16px;
  border: 2px solid #dfe4ea;
  border-radius: 12px;
  font-size: 14px;
  background-color: #fafbfc;
  transition: all 0.3s ease;
}

.filter-form input:focus {
  border-color: #3498db;
  background-color: #fff;
  outline: none;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.2);
}

.filter-form button {
  grid-column: 1 / -1;
  padding: 14px;
  background: linear-gradient(to right, #3498db, #2980b9);
  color: #fff;
  font-size: 16px;
  font-weight: bold;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: background 0.3s ease, transform 0.2s ease;
}

.filter-form button:hover {
  background: linear-gradient(to right, #2980b9, #2471a3);
  transform: translateY(-1px);
}

.filter-form button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.no-results {
  text-align: center;
  color: #888;
  font-size: 16px;
  margin: 40px 0;
}

.results-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-top: 40px;
  font-size: 16px;
}

.pagination button {
  padding: 10px 18px;
  background: linear-gradient(to right, #2b5876, #4e4376);
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.3s ease, transform 0.2s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.pagination button:hover {
  background: linear-gradient(to right, #34495e, #5d478b);
  transform: translateY(-2px);
}

.pagination button:disabled {
  background: #ccc;
  color: #666;
  cursor: not-allowed;
  box-shadow: none;
}

.pagination span {
  font-size: 15px;
  color: #2c3e50;
  font-weight: 500;
}
</style>
