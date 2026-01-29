<template>
  <el-card shadow="hover">
    <template #header>
      <div class="flex items-center gap-2">
        <el-icon><Compass /></el-icon>
        <span class="font-semibold">导航控制</span>
      </div>
    </template>
    
    <div class="grid grid-cols-3 gap-3">
      <el-button @click="handleHome">
        <el-icon class="mr-1"><Home /></el-icon>
        Home
      </el-button>
      <el-button @click="handleBack">
        <el-icon class="mr-1"><ArrowLeft /></el-icon>
        返回
      </el-button>
      <el-button @click="handleMenu">
        <el-icon class="mr-1"><Cog /></el-icon>
        菜单
      </el-button>
      <el-button @click="handleGoHome">
        <el-icon class="mr-1"><Home /></el-icon>
        主页
      </el-button>
      <el-button @click="handleRecentApps">
        <el-icon class="mr-1"><Th /></el-icon>
        最近
      </el-button>
    </div>
  </el-card>
</template>

<script setup>
import { ElMessage } from 'element-plus'
import { navigationApi } from '@/api'
import { Compass, ArrowLeft, Home, Cog, Th } from '@vicons/fa'

async function handleHome() {
  try {
    await navigationApi.home()
    ElMessage.success('已按下 Home 键')
  } catch (err) {
    ElMessage.error('操作失败')
  }
}

async function handleBack() {
  try {
    await navigationApi.back()
    ElMessage.success('已按下返回键')
  } catch (err) {
    ElMessage.error('操作失败')
  }
}

async function handleMenu() {
  try {
    await navigationApi.menu()
    ElMessage.success('已打开菜单')
  } catch (err) {
    ElMessage.error('操作失败')
  }
}

async function handleGoHome() {
  try {
    await navigationApi.goHome()
    ElMessage.success('已返回主页')
  } catch (err) {
    ElMessage.error('操作失败')
  }
}

async function handleRecentApps() {
  try {
    await navigationApi.recentApps()
    ElMessage.success('已打开最近应用')
  } catch (err) {
    ElMessage.error('操作失败')
  }
}
</script>
