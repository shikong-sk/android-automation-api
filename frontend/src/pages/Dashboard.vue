<template>
  <div class="dashboard">
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-800">控制台</h2>
      <p class="text-gray-500 mt-1">Android 设备自动化控制面板</p>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
      <DeviceCard />
      <InputControl />
      <NavigationControl />
    </div>
    
    <div class="mt-6">
      <AppManager />
    </div>
  </div>
</template>

<script setup>
import DeviceCard from '@/components/DeviceCard.vue'
import InputControl from '@/components/InputControl.vue'
import NavigationControl from '@/components/NavigationControl.vue'
import AppManager from '@/components/AppManager.vue'
</script>
