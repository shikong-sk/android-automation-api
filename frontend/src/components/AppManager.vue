<template>
  <el-card shadow="hover">
    <template #header>
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <el-icon><Folder /></el-icon>
          <span class="font-semibold">应用管理</span>
        </div>
      </div>
    </template>
    
    <div class="space-y-4">
      <el-input
        v-model="packageName"
        placeholder="输入应用包名（如 com.example.app）"
        clearable
      />
      
      <div class="flex flex-wrap gap-2">
        <el-button type="primary" :disabled="!packageName" @click="handleStart">
          启动应用
        </el-button>
        <el-button type="warning" :disabled="!packageName" @click="handleStop">
          停止应用
        </el-button>
        <el-button type="danger" :disabled="!packageName" @click="handleClear">
          清除数据
        </el-button>
      </div>
      
      <el-divider />
      
      <div class="flex flex-wrap gap-2">
        <el-button :disabled="!packageName" @click="handleGetVersion">
          获取版本
        </el-button>
        <el-button :disabled="!packageName" @click="handleGetStatus">
          检查状态
        </el-button>
        <el-button type="success" @click="handleGetCurrent">
          获取当前应用
        </el-button>
      </div>
      
      <div v-if="appInfo" class="bg-gray-100 p-3 rounded text-sm">
        <pre>{{ JSON.stringify(appInfo, null, 2) }}</pre>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { appApi } from '@/api'
import { Folder } from '@vicons/fa'

const packageName = ref('')
const appInfo = ref(null)

async function handleStart() {
  try {
    await appApi.start(packageName.value)
    ElMessage.success(`应用已启动: ${packageName.value}`)
  } catch (err) {
    ElMessage.error('启动应用失败')
  }
}

async function handleStop() {
  try {
    await appApi.stop(packageName.value)
    ElMessage.success(`应用已停止: ${packageName.value}`)
  } catch (err) {
    ElMessage.error('停止应用失败')
  }
}

async function handleClear() {
  try {
    await appApi.clear(packageName.value)
    ElMessage.success(`应用数据已清除: ${packageName.value}`)
  } catch (err) {
    ElMessage.error('清除数据失败')
  }
}

async function handleGetVersion() {
  try {
    const result = await appApi.getVersion(packageName.value)
    appInfo.value = result
  } catch (err) {
    ElMessage.error('获取版本失败')
  }
}

async function handleGetStatus() {
  try {
    const result = await appApi.getStatus(packageName.value)
    appInfo.value = result
    ElMessage.success(`应用${result.running ? '正在运行' : '未运行'}`)
  } catch (err) {
    ElMessage.error('获取状态失败')
  }
}

async function handleGetCurrent() {
  try {
    const result = await appApi.getCurrent()
    appInfo.value = result
    ElMessage.success(`当前应用: ${result.package}`)
  } catch (err) {
    ElMessage.error('获取当前应用失败')
  }
}
</script>
