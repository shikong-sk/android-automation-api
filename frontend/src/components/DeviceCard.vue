<template>
  <el-card class="device-card" shadow="hover">
    <template #header>
      <div class="flex items-center justify-between">
        <span class="font-semibold">设备连接</span>
        <el-tag :type="connected ? 'success' : 'danger'">
          {{ connected ? '已连接' : '未连接' }}
        </el-tag>
      </div>
    </template>
    
    <div v-if="deviceInfo" class="space-y-2">
      <div class="flex items-center gap-2">
        <el-icon class="text-gray-500"><MobileAlt /></el-icon>
        <span class="text-sm">{{ deviceInfo.serial }}</span>
      </div>
      <div class="flex items-center gap-2">
        <el-icon class="text-gray-500"><Desktop /></el-icon>
        <span class="text-sm">{{ deviceInfo.product_name }}</span>
      </div>
      <div class="flex items-center gap-2">
        <el-icon class="text-gray-500"><Microchip /></el-icon>
        <span class="text-sm">API Level: {{ deviceInfo.api_level }}</span>
      </div>
      <div class="flex items-center gap-2">
        <el-icon class="text-gray-500"><BatteryFull /></el-icon>
        <span class="text-sm">电量: {{ deviceInfo.battery_level }}%</span>
      </div>
    </div>
    
    <div v-else class="space-y-4">
      <div class="text-gray-500 text-center py-2">
        <el-icon class="text-4xl mb-2"><MobileAlt /></el-icon>
        <p class="text-sm">暂无设备连接</p>
      </div>
      
      <el-input
        v-model="deviceSerial"
        placeholder="输入设备序列号或 IP 地址"
        clearable
        @keyup.enter="handleConnect"
      >
        <template #prepend>
          <el-icon><Plug /></el-icon>
        </template>
      </el-input>
      <p class="text-xs text-gray-400">
        留空自动选择设备，或输入 IP:端口 进行 WiFi 连接
      </p>
    </div>
    
    <template #footer>
      <div class="flex justify-end gap-2">
        <el-button 
          v-if="!connected"
          type="primary" 
          :loading="loading"
          @click="handleConnect"
        >
          连接设备
        </el-button>
        <template v-else>
          <el-button 
            type="primary"
            :loading="loading"
            @click="handleRefresh"
          >
            刷新状态
          </el-button>
          <el-button 
            type="danger" 
            :loading="loading"
            @click="handleDisconnect"
          >
            断开连接
          </el-button>
        </template>
      </div>
    </template>
  </el-card>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useDeviceStore } from '@/stores'
import { MobileAlt, Desktop, Microchip, BatteryFull, Plug } from '@vicons/fa'

const deviceStore = useDeviceStore()
const deviceSerial = ref('')

const connected = computed(() => deviceStore.connected)
const deviceInfo = computed(() => deviceStore.deviceInfo)
const loading = computed(() => deviceStore.loading)

// 页面加载时获取设备状态
onMounted(async () => {
  try {
    await deviceStore.fetchStatus()
  } catch (err) {
    // 忽略初始化错误
  }
})

async function handleConnect() {
  try {
    const serial = deviceSerial.value.trim() || null
    await deviceStore.connect(serial)
    ElMessage.success('设备连接成功')
    deviceSerial.value = ''
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '连接设备失败')
  }
}

async function handleDisconnect() {
  try {
    await deviceStore.disconnect()
    ElMessage.success('设备已断开')
  } catch (err) {
    ElMessage.error('断开连接失败')
  }
}

async function handleRefresh() {
  try {
    await deviceStore.fetchStatus()
    ElMessage.success('状态已刷新')
  } catch (err) {
    ElMessage.error('刷新状态失败')
  }
}
</script>

<style scoped>
.device-card {
  @apply w-full;
}
</style>
