<template>
  <div class="device-page">
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-800">设备管理</h2>
      <p class="text-gray-500 mt-1">管理 Android 设备连接状态</p>
    </div>
    
    <DeviceCard />
  </div>
</template>

<script setup>
import DeviceCard from '@/components/DeviceCard.vue'
</script>
