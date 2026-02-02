<template>
  <el-container class="h-screen">
    <el-aside
      :width="isCollapsed ? '64px' : '240px'"
      class="bg-white border-r border-gray-200 transition-all duration-300"
    >
      <div class="flex items-center justify-between p-3 border-b border-gray-200" :class="{ 'justify-center': isCollapsed }">
        <transition name="fade">
          <h1 v-if="!isCollapsed" class="text-lg font-bold text-gray-800 flex items-center gap-2">
            <el-icon class="text-blue-500"><Magic /></el-icon>
            Android 自动化
          </h1>
        </transition>
        <el-button
          :icon="isCollapsed ? 'ArrowRight' : 'ArrowLeft'"
          :title="isCollapsed ? '展开' : '收起'"
          circle
          size="small"
          @click="toggleCollapse"
        />
      </div>
      <el-menu
        :default-active="activeMenu"
        router
        :collapse="isCollapsed"
        class="border-r-0"
      >
        <el-menu-item index="/">
          <el-icon><TachometerAlt /></el-icon>
          <template #title>控制台</template>
        </el-menu-item>
        <el-menu-item index="/device">
          <el-icon><Plug /></el-icon>
          <template #title>设备管理</template>
        </el-menu-item>
        <el-menu-item index="/input">
          <el-icon><Pen /></el-icon>
          <template #title>输入控制</template>
        </el-menu-item>
        <el-menu-item index="/navigation">
          <el-icon><Compass /></el-icon>
          <template #title>导航控制</template>
        </el-menu-item>
        <el-menu-item index="/apps">
          <el-icon><Folder /></el-icon>
          <template #title>应用管理</template>
        </el-menu-item>
        <el-menu-item index="/adb">
          <el-icon><Terminal /></el-icon>
          <template #title>ADB 工具</template>
        </el-menu-item>
        <el-menu-item index="/script">
          <el-icon><Code /></el-icon>
          <template #title>自动化脚本</template>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-main class="bg-gray-50 p-6 overflow-auto">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { Magic, TachometerAlt, Plug, Pen, Compass, Folder, Terminal, Code } from '@vicons/fa'

const isCollapsed = ref(false)

function toggleCollapse() {
  isCollapsed.value = !isCollapsed.value
}

const route = useRoute()
const activeMenu = computed(() => route.path)
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
