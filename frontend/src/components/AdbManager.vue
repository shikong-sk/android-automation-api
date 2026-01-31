<template>
  <div class="space-y-6">
    <!-- 设备信息卡片 -->
    <el-card shadow="hover">
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <el-icon><Mobile /></el-icon>
            <span class="font-semibold">设备信息</span>
          </div>
          <el-button type="primary" size="small" @click="loadDeviceInfo" :loading="loading.deviceInfo">
            刷新
          </el-button>
        </div>
      </template>
      
      <div v-if="deviceInfo" class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="bg-gray-50 p-3 rounded">
          <div class="text-xs text-gray-500">型号</div>
          <div class="font-medium">{{ deviceInfo.model }}</div>
        </div>
        <div class="bg-gray-50 p-3 rounded">
          <div class="text-xs text-gray-500">品牌</div>
          <div class="font-medium">{{ deviceInfo.brand }}</div>
        </div>
        <div class="bg-gray-50 p-3 rounded">
          <div class="text-xs text-gray-500">Android 版本</div>
          <div class="font-medium">{{ deviceInfo.android_version }}</div>
        </div>
        <div class="bg-gray-50 p-3 rounded">
          <div class="text-xs text-gray-500">SDK 版本</div>
          <div class="font-medium">{{ deviceInfo.sdk_version }}</div>
        </div>
      </div>
      <el-empty v-else description="点击刷新获取设备信息" />
    </el-card>

    <!-- 电池和屏幕信息 -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <el-card shadow="hover">
        <template #header>
          <div class="flex items-center gap-2">
            <el-icon><BatteryFull /></el-icon>
            <span class="font-semibold">电池信息</span>
          </div>
        </template>
        <div v-if="batteryInfo" class="space-y-2">
          <div class="flex justify-between">
            <span class="text-gray-500">电量</span>
            <span class="font-medium">{{ batteryInfo.level }}%</span>
          </div>
          <el-progress :percentage="batteryInfo.level || 0" :status="batteryInfo.level < 20 ? 'exception' : ''" />
          <div class="flex justify-between text-sm">
            <span class="text-gray-500">状态</span>
            <el-tag :type="batteryInfo.usb_powered || batteryInfo.ac_powered ? 'success' : 'info'" size="small">
              {{ batteryInfo.usb_powered || batteryInfo.ac_powered ? '充电中' : '未充电' }}
            </el-tag>
          </div>
        </div>
        <el-button v-else type="primary" size="small" @click="loadBatteryInfo" :loading="loading.battery">
          获取电池信息
        </el-button>
      </el-card>

      <el-card shadow="hover">
        <template #header>
          <div class="flex items-center gap-2">
            <el-icon><Desktop /></el-icon>
            <span class="font-semibold">屏幕信息</span>
          </div>
        </template>
        <div v-if="screenInfo" class="space-y-2">
          <div class="flex justify-between">
            <span class="text-gray-500">分辨率</span>
            <span class="font-medium">{{ screenInfo.width }} x {{ screenInfo.height }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-500">密度</span>
            <span class="font-medium">{{ screenInfo.density }} dpi</span>
          </div>
        </div>
        <el-button v-else type="primary" size="small" @click="loadScreenInfo" :loading="loading.screen">
          获取屏幕信息
        </el-button>
      </el-card>
    </div>

    <!-- 应用列表 -->
    <el-card shadow="hover">
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <el-icon><Th /></el-icon>
            <span class="font-semibold">已安装应用</span>
            <el-tag v-if="packages.length" size="small">{{ packages.length }} 个</el-tag>
          </div>
          <div class="flex items-center gap-2">
            <el-select v-model="filterType" placeholder="筛选类型" size="small" style="width: 140px" @change="loadPackages">
              <el-option label="全部应用" value="" />
              <el-option label="第三方应用" value="third_party" />
              <el-option label="系统应用" value="system" />
            </el-select>
            <el-button type="primary" size="small" @click="loadPackages" :loading="loading.packages">
              刷新
            </el-button>
          </div>
        </div>
      </template>
      
      <div class="mb-4">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索应用包名..."
          clearable
          prefix-icon="Search"
        />
      </div>
      
      <el-table :data="filteredPackages" max-height="400" v-loading="loading.packages">
        <el-table-column prop="name" label="包名" min-width="300">
          <template #default="{ row }">
            <span class="font-mono text-sm">{{ row }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button-group size="small">
              <el-button @click="viewPackageInfo(row)">详情</el-button>
              <el-button type="danger" @click="handleUninstall(row)">卸载</el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- Shell 命令 -->
    <el-card shadow="hover">
      <template #header>
        <div class="flex items-center gap-2">
          <el-icon><Terminal /></el-icon>
          <span class="font-semibold">Shell 命令</span>
        </div>
      </template>
      
      <div class="space-y-4">
        <el-input
          v-model="shellCommand"
          placeholder="输入 shell 命令（如 ls /sdcard）"
          @keyup.enter="executeShell"
        >
          <template #append>
            <el-button @click="executeShell" :loading="loading.shell">执行</el-button>
          </template>
        </el-input>
        
        <div v-if="shellOutput !== null" class="bg-gray-900 text-green-400 p-4 rounded font-mono text-sm overflow-auto max-h-64">
          <pre>{{ shellOutput }}</pre>
        </div>
      </div>
    </el-card>

    <!-- 应用详情对话框 -->
    <el-dialog v-model="showPackageDialog" title="应用详情" width="500px">
      <div v-if="selectedPackageInfo" class="space-y-3">
        <div class="flex justify-between py-2 border-b">
          <span class="text-gray-500">包名</span>
          <span class="font-mono">{{ selectedPackageInfo.package_name }}</span>
        </div>
        <div class="flex justify-between py-2 border-b">
          <span class="text-gray-500">版本名称</span>
          <span>{{ selectedPackageInfo.version_name || '-' }}</span>
        </div>
        <div class="flex justify-between py-2 border-b">
          <span class="text-gray-500">版本号</span>
          <span>{{ selectedPackageInfo.version_code || '-' }}</span>
        </div>
        <div class="flex justify-between py-2 border-b">
          <span class="text-gray-500">目标 SDK</span>
          <span>{{ selectedPackageInfo.target_sdk || '-' }}</span>
        </div>
        <div class="flex justify-between py-2 border-b">
          <span class="text-gray-500">最低 SDK</span>
          <span>{{ selectedPackageInfo.min_sdk || '-' }}</span>
        </div>
        <div class="flex justify-between py-2 border-b">
          <span class="text-gray-500">首次安装</span>
          <span class="text-sm">{{ selectedPackageInfo.first_install_time || '-' }}</span>
        </div>
        <div class="flex justify-between py-2">
          <span class="text-gray-500">最后更新</span>
          <span class="text-sm">{{ selectedPackageInfo.last_update_time || '-' }}</span>
        </div>
      </div>
      <div v-else class="text-center py-8">
        <el-icon class="is-loading" :size="24"><Spinner /></el-icon>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { adbApi } from '@/api'
import { Mobile, BatteryFull, Desktop, Th, Terminal, Spinner } from '@vicons/fa'

// 状态
const loading = ref({
  deviceInfo: false,
  battery: false,
  screen: false,
  packages: false,
  shell: false
})

const deviceInfo = ref(null)
const batteryInfo = ref(null)
const screenInfo = ref(null)
const packages = ref([])
const filterType = ref('')
const searchKeyword = ref('')
const shellCommand = ref('')
const shellOutput = ref(null)
const showPackageDialog = ref(false)
const selectedPackageInfo = ref(null)

// 计算属性
const filteredPackages = computed(() => {
  if (!searchKeyword.value) return packages.value
  const keyword = searchKeyword.value.toLowerCase()
  return packages.value.filter(pkg => pkg.toLowerCase().includes(keyword))
})

// 方法
async function loadDeviceInfo() {
  loading.value.deviceInfo = true
  try {
    deviceInfo.value = await adbApi.getDeviceInfo()
  } catch (err) {
    ElMessage.error('获取设备信息失败')
  } finally {
    loading.value.deviceInfo = false
  }
}

async function loadBatteryInfo() {
  loading.value.battery = true
  try {
    batteryInfo.value = await adbApi.getBatteryInfo()
  } catch (err) {
    ElMessage.error('获取电池信息失败')
  } finally {
    loading.value.battery = false
  }
}

async function loadScreenInfo() {
  loading.value.screen = true
  try {
    const [resolution, density] = await Promise.all([
      adbApi.getScreenResolution(),
      adbApi.getScreenDensity()
    ])
    screenInfo.value = {
      ...resolution,
      density: density.density
    }
  } catch (err) {
    ElMessage.error('获取屏幕信息失败')
  } finally {
    loading.value.screen = false
  }
}

async function loadPackages() {
  loading.value.packages = true
  try {
    const result = await adbApi.listPackages(filterType.value || null)
    packages.value = result.packages
  } catch (err) {
    ElMessage.error('获取应用列表失败')
  } finally {
    loading.value.packages = false
  }
}

async function viewPackageInfo(packageName) {
  showPackageDialog.value = true
  selectedPackageInfo.value = null
  try {
    selectedPackageInfo.value = await adbApi.getPackageInfo(packageName)
  } catch (err) {
    ElMessage.error('获取应用详情失败')
    showPackageDialog.value = false
  }
}

async function handleUninstall(packageName) {
  try {
    await ElMessageBox.confirm(
      `确定要卸载应用 ${packageName} 吗？`,
      '确认卸载',
      { type: 'warning' }
    )
    await adbApi.uninstallPackage(packageName)
    ElMessage.success('应用已卸载')
    loadPackages()
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error('卸载失败')
    }
  }
}

async function executeShell() {
  if (!shellCommand.value.trim()) return
  loading.value.shell = true
  try {
    const result = await adbApi.executeShell(shellCommand.value)
    shellOutput.value = result.output
  } catch (err) {
    ElMessage.error('执行命令失败')
  } finally {
    loading.value.shell = false
  }
}

// 初始化
onMounted(() => {
  loadDeviceInfo()
  loadBatteryInfo()
  loadScreenInfo()
  loadPackages()
})
</script>
