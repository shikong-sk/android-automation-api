<template>
  <el-container class="h-screen">
    <el-aside width="240px" class="bg-white border-r border-gray-200">
      <div class="p-4 border-b border-gray-200">
        <h1 class="text-lg font-bold text-gray-800 flex items-center gap-2">
          <el-icon class="text-blue-500"><Magic /></el-icon>
          Android 自动化
        </h1>
      </div>
      <el-menu
        :default-active="activeMenu"
        router
        class="border-r-0"
      >
        <el-menu-item index="/">
          <el-icon><TachometerAlt /></el-icon>
          <span>控制台</span>
        </el-menu-item>
        <el-menu-item index="/device">
          <el-icon><Plug /></el-icon>
          <span>设备管理</span>
        </el-menu-item>
        <el-menu-item index="/input">
          <el-icon><Pen /></el-icon>
          <span>输入控制</span>
        </el-menu-item>
        <el-menu-item index="/navigation">
          <el-icon><Compass /></el-icon>
          <span>导航控制</span>
        </el-menu-item>
        <el-menu-item index="/apps">
          <el-icon><Folder /></el-icon>
          <span>应用管理</span>
        </el-menu-item>
        <el-menu-item index="/adb">
          <el-icon><Terminal /></el-icon>
          <span>ADB 工具</span>
        </el-menu-item>
        <el-menu-item index="/script">
          <el-icon><Code /></el-icon>
          <span>自动化脚本</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    
    <el-main class="bg-gray-50 p-6 overflow-auto">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { Magic, TachometerAlt, Plug, Pen, Compass, Folder, Terminal, Code } from '@vicons/fa'

const route = useRoute()
const activeMenu = computed(() => route.path)
</script>
