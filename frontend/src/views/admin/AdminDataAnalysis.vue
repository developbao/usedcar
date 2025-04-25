<template>
  <div>
    <h2>数据分析</h2>
    <div class="chart-container">
      <div class="chart-item" v-if="purchasedCarData">
        <h3>购买车辆品牌（折线图）</h3>
        <Line :data="purchasedCarData" :options="chartOptions" />
      </div>

      <div class="chart-item" v-if="searchedCarData">
        <h3>搜索车辆品牌（条形图）</h3>
        <Bar :data="searchedCarData" :options="chartOptions" />
      </div>

      <div class="chart-item" v-if="likedCarData">
        <h3>喜欢车辆品牌（饼图）</h3>
        <Pie :data="likedCarData" :options="chartOptions" />
      </div>

      <div class="chart-item" v-if="ageRangeData">
        <h3>车龄分布（雷达图）</h3>
        <Radar :data="ageRangeData" :options="chartOptions" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { Bar, Pie, Line, Radar } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  BarElement,
  ArcElement,
  RadarController,
  RadialLinearScale,
  CategoryScale,
  LinearScale,
} from "chart.js";

// 注册图表组件
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  BarElement,
  ArcElement,
  RadarController,
  RadialLinearScale,
  CategoryScale,
  LinearScale
);

// 数据
const purchasedCarData = ref(null);
const searchedCarData = ref(null);
const likedCarData = ref(null);
const ageRangeData = ref(null);

// 配置项
const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: "bottom",
    },
  },
};

const fetchData = async () => {
  try {
    const response = await axios.get(
      "http://127.0.0.1:8000/users/api/admin/data-analysis/",
      { withCredentials: true }
    );
    const data = response.data;

    // 折线图 - 购买
    purchasedCarData.value = {
      labels: Object.keys(data.purchased_car_counts),
      datasets: [
        {
          label: "购买车辆品牌",
          data: Object.values(data.purchased_car_counts),
          borderColor: "#42a5f5",
          backgroundColor: "rgba(66, 165, 245, 0.2)",
          fill: true,
          tension: 0.3,
        },
      ],
    };

    // 条形图 - 搜索
    searchedCarData.value = {
      labels: Object.keys(data.searched_car_counts),
      datasets: [
        {
          label: "搜索车辆品牌",
          data: Object.values(data.searched_car_counts),
          backgroundColor: "#66bb6a",
        },
      ],
    };

    // 饼图 - 喜欢
    likedCarData.value = {
      labels: Object.keys(data.liked_car_counts),
      datasets: [
        {
          label: "喜欢车辆品牌",
          data: Object.values(data.liked_car_counts),
          backgroundColor: [
            "#ff6384",
            "#36a2eb",
            "#ffcd56",
            "#4bc0c0",
            "#9966ff",
          ],
        },
      ],
    };

    // 雷达图 - 年龄段
    ageRangeData.value = {
      labels: Object.keys(data.age_ranges),
      datasets: [
        {
          label: "车龄分布",
          data: Object.values(data.age_ranges),
          backgroundColor: "rgba(255, 99, 132, 0.2)",
          borderColor: "#ff6384",
          pointBackgroundColor: "#ff6384",
        },
      ],
    };
  } catch (err) {
    console.error("获取数据失败:", err);
  }
};

onMounted(fetchData);
</script>

<style scoped>
h2 {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

h3 {
  font-size: 18px;
  margin: 10px 0;
  text-align: center;
}

.chart-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.chart-item {
  flex: 1 1 calc(50% - 20px); /* 每项占一半，减去间距 */
  min-width: 300px; /* 防止太小 */
  height: 400px;
  background: #f9f9f9;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  box-sizing: border-box;
}

@media (max-width: 768px) {
  .chart-item {
    flex: 1 1 100%;
  }
}
</style>
