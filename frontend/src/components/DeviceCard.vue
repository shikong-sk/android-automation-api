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
    
    <div v-else class="text-gray-500 text-center py-4">
      <el-icon class="text-4xl mb-2"><MobileAlt /></el-icon>
      <p class="text-sm">暂无设备连接</p>
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
        <el-button 
          v-else
          type="danger" 
          :loading="loading"
          @click="handleDisconnect"
        >
          断开连接
        </el-button>
      </div>
    </template>
  </el-card>
</template>

<script setup>
import { computed } from 'vue'
import { useDeviceStore } from '@/stores'
import { MobileAlt, Desktop, Microchip, BatteryFull } from '@vicons/fa'

const deviceStore = useDeviceStore()

const connected = computed(() => deviceStore.connected)
const deviceInfo = computed(() => deviceStore.deviceInfo)
const loading = computed(() => deviceStore.loading)

async function handleConnect() {
  try {
    await deviceStore.connect()
  } catch (err) {
    console.error('连接失败:', err)
  }
}

async function handleDisconnect() {
  try {
    await deviceStore.disconnect()
  } catch (err) {
    console.error('断开连接失败:', err)
  }
}
</script>

<style scoped>
.device-card {
  @apply w-full max-w-sm;
}
</style>
