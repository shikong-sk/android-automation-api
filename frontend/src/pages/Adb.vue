<template>
  <div class="adb-page">
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-800">ADB 工具</h2>
      <p class="text-gray-500 mt-1">通过 ADB 命令管理设备和应用</p>
    </div>
    
    <AdbManager />
  </div>
</template>

<script setup>
import AdbManager from '@/components/AdbManager.vue'
</script>
