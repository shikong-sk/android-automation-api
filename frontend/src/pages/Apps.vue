<template>
  <div class="apps-page">
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-800">应用管理</h2>
      <p class="text-gray-500 mt-1">管理设备上的应用程序</p>
    </div>
    
    <AppManager />
  </div>
</template>

<script setup>
import AppManager from '@/components/AppManager.vue'
</script>
