<template>
  <div class="dashboard">
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-800">控制台</h2>
      <p class="text-gray-500 mt-1">Android 设备自动化控制面板</p>
    </div>
    
    <!-- 设备和导航 -->
    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 mb-6">
      <DeviceCard />
      <NavigationControl />
      <AppManager />
    </div>
    
    <!-- 输入控制 - 单独一行，全宽 -->
    <div class="mb-6">
      <InputControl />
    </div>
  </div>
</template>

<script setup>
import DeviceCard from '@/components/DeviceCard.vue'
import InputControl from '@/components/InputControl.vue'
import NavigationControl from '@/components/NavigationControl.vue'
import AppManager from '@/components/AppManager.vue'
</script>
