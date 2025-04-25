<template>
  <div class="dialog-overlay" @click.self="close">
    <div class="dialog">
      <h3 class="dialog-title">用户画像</h3>
      <div v-if="userProfile">
        <p><strong>用户 ID：</strong>{{ userProfile.user.id }}</p>
        <p><strong>用户名：</strong>{{ userProfile.user.login_name }}</p>
        <p><strong>姓名：</strong>{{ userProfile.user.name || "无" }}</p>
        <p><strong>手机号：</strong>{{ userProfile.user.phone_num || "无" }}</p>

        <h4 class="section-title">画像信息</h4>
        <p v-if="userProfile.profile.message">
          {{ userProfile.profile.message }}
        </p>
        <div v-else>
          <p>
            <strong>购车次数：</strong>{{ userProfile.profile.purchase_count }}
          </p>
          <p>
            <strong>平均购车价格：</strong
            >{{ userProfile.profile.average_price }} 万
          </p>

          <p>
            <strong>偏好品牌：</strong>
            <span
              v-for="(item, index) in userProfile.profile.preferred_brands"
              :key="index"
            >
              {{ item[0] }} ({{ item[1] }}次)
            </span>
          </p>
          <p>
            <strong>偏好颜色：</strong>
            <span
              v-for="(item, index) in userProfile.profile.preferred_colors"
              :key="index"
            >
              {{ item[0] }} ({{ item[1] }}次)
            </span>
          </p>
          <p>
            <strong>偏好配置：</strong>
            <span
              v-for="(item, index) in userProfile.profile
                .preferred_configurations"
              :key="index"
            >
              {{ item[0] }} ({{ item[1] }}次)
            </span>
          </p>
        </div>
      </div>
      <button class="close-btn" @click="close">关闭</button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  visible: Boolean,
  userProfile: Object,
});

const emit = defineEmits(); // 用于触发事件

const close = () => {
  emit("close"); // 使用 emit() 来触发事件
};
</script>

<style scoped>
.dialog-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(2px);
  animation: fadeIn 0.3s ease-in-out;
}

.dialog {
  background: #ffffff;
  padding: 32px 24px;
  width: 480px;
  max-width: 90vw;
  border-radius: 16px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
  animation: slideIn 0.3s ease;
}

.dialog-title {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 20px;
  text-align: center;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 12px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #374151;
  margin: 20px 0 10px;
  border-left: 4px solid #3b82f6;
  padding-left: 8px;
}

p {
  margin: 8px 0;
  color: #4b5563;
  font-size: 15px;
  line-height: 1.6;
}

strong {
  color: #1f2937;
}

span {
  display: inline-block;
  margin: 4px 6px 0 0;
  padding: 4px 8px;
  background-color: #e0f2fe;
  color: #0369a1;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 500;
}

button {
  margin-top: 24px;
  padding: 10px;
  width: 100%;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 16px;
  transition: all 0.2s ease-in-out;
  cursor: pointer;
}

button:hover {
  opacity: 0.95;
  transform: translateY(-1px);
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideIn {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
</style>
