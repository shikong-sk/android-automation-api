<template>
  <div class="screen-preview">
    <el-card shadow="hover" class="h-full">
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <el-icon><Mobile /></el-icon>
            <span class="font-semibold">屏幕预览</span>
          </div>
          <div class="flex gap-2">
            <el-button size="small" :loading="loading" @click="refreshScreenshot">
              <el-icon class="mr-1"><Sync /></el-icon>
              刷新
            </el-button>
            <el-switch
              v-model="autoRefresh"
              active-text="自动"
              inactive-text=""
              size="small"
            />
          </div>
        </div>
      </template>

      <div class="screen-container">
        <div v-if="loading && !screenshotData" class="loading-placeholder">
          <el-icon class="is-loading" :size="40"><Spinner /></el-icon>
          <p class="mt-2 text-gray-500">正在获取截图...</p>
        </div>

        <div v-else-if="error" class="error-placeholder">
          <el-icon :size="40" class="text-red-400"><ExclamationTriangle /></el-icon>
          <p class="mt-2 text-red-500">{{ error }}</p>
          <el-button size="small" class="mt-2" @click="refreshScreenshot">重试</el-button>
        </div>

        <div 
          v-else-if="screenshotData"
          ref="imageContainerRef"
          class="image-container"
          @click="handleImageClick"
          @mousemove="handleMouseMove"
          @mouseleave="handleMouseLeave"
        >
          <img 
            ref="imageRef"
            :src="screenshotData" 
            alt="设备截图"
            class="screenshot-image"
            @load="handleImageLoad"
          />
          
          <div 
            v-if="showCrosshair && mousePosition"
            class="crosshair"
            :style="crosshairStyle"
          >
            <div class="crosshair-h"></div>
            <div class="crosshair-v"></div>
          </div>

          <div 
            v-for="(marker, index) in clickMarkers"
            :key="index"
            class="click-marker"
            :class="marker.type"
            :style="getMarkerStyle(marker)"
          >
            <div class="marker-dot"></div>
            <div class="marker-ripple"></div>
          </div>

           <svg 
             v-if="dragPreview && dragPreview.show && imageDisplayWidth && imageDisplayHeight"
             class="drag-preview-svg"
             :viewBox="`0 0 ${imageDisplayWidth} ${imageDisplayHeight}`"
             preserveAspectRatio="none"
           >
             <!-- 轨迹路径 -->
             <path
               :d="dragPreview.path"
               fill="none"
               :stroke="getTrajectoryColor(dragPreview.trajectoryType)"
               stroke-width="3"
               stroke-dasharray="8,4"
             />
             
             <!-- 起点标记 -->
             <circle
               :cx="dragPreview.startX"
               :cy="dragPreview.startY"
               r="10"
               fill="#67C23A"
               stroke="white"
               stroke-width="3"
               class="marker-pulse"
             />
             <text
               :x="dragPreview.startX"
               :y="dragPreview.startY + 25"
               text-anchor="middle"
               fill="#67C23A"
               font-size="12"
               font-weight="bold"
             >起点</text>
             
             <!-- 终点标记 -->
             <circle
               :cx="dragPreview.endX"
               :cy="dragPreview.endY"
               r="10"
               fill="#F56C6C"
               stroke="white"
               stroke-width="3"
               class="marker-pulse"
             />
             <text
               :x="dragPreview.endX"
               :y="dragPreview.endY + 25"
               text-anchor="middle"
               fill="#F56C6C"
               font-size="12"
               font-weight="bold"
             >终点</text>
             
             <!-- 移动的手指/圆点 -->
             <g v-if="dragPreview.currentPoint" class="drag-finger">
               <circle
                 :cx="dragPreview.currentPoint.x"
                 :cy="dragPreview.currentPoint.y"
                 r="12" 
                 fill="#409EFF"
                 stroke="white"
                 stroke-width="2"
                 class="finger-shadow"
               />
               <circle
                 :cx="dragPreview.currentPoint.x"
                 :cy="dragPreview.currentPoint.y"
                 r="6"
                 fill="white"
               />
             </g>
             
             <!-- 进度条 -->
             <rect
               :x="10"
               :y="imageDisplayHeight - 20"
               :width="(imageDisplayWidth - 20) * (dragPreview.progress || 0)"
               height="6"
               rx="3"
               fill="#409EFF"
             />
           </svg>

          <div v-if="loading" class="refresh-overlay">
            <el-icon class="is-loading" :size="24"><Spinner /></el-icon>
          </div>
        </div>

        <div v-else class="empty-placeholder">
          <el-icon :size="40" class="text-gray-300"><Image /></el-icon>
          <p class="mt-2 text-gray-400">点击刷新获取截图</p>
          <el-button size="small" class="mt-2" @click="refreshScreenshot">获取截图</el-button>
        </div>
      </div>

      <div class="coordinate-info mt-3">
        <div class="flex items-center justify-between text-sm">
          <div class="flex gap-4">
            <span class="text-gray-500">
              屏幕: <span class="text-gray-700 font-mono">{{ screenWidth }} × {{ screenHeight }}</span>
            </span>
            <span v-if="currentCoordinate" class="text-gray-500">
              坐标: <span class="text-blue-600 font-mono font-semibold">{{ currentCoordinate.x }}, {{ currentCoordinate.y }}</span>
            </span>
          </div>
          <div v-if="lastClickCoordinate" class="text-gray-500">
            已选: <span class="text-green-600 font-mono font-semibold">{{ lastClickCoordinate.x }}, {{ lastClickCoordinate.y }}</span>
            <el-button size="small" link type="primary" class="ml-2" @click="copyCoordinate">
              复制
            </el-button>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { adbApi } from '@/api'
import { Mobile, Sync, Spinner, ExclamationTriangle, Image } from '@vicons/fa'

const props = defineProps({
  autoRefreshInterval: {
    type: Number,
    default: 3000
  }
})

const emit = defineEmits(['coordinate-click', 'coordinate-update'])

const loading = ref(false)
const error = ref('')
const screenshotData = ref('')
const screenWidth = ref(0)
const screenHeight = ref(0)
const autoRefresh = ref(false)
const imageRef = ref(null)
const imageContainerRef = ref(null)
const imageLoaded = ref(false)
const imageDisplayWidth = ref(0)
const imageDisplayHeight = ref(0)

const mousePosition = ref(null)
const showCrosshair = ref(true)
const currentCoordinate = ref(null)
const lastClickCoordinate = ref(null)
const clickMarkers = ref([])
const dragPreview = ref(null)

let autoRefreshTimer = null

const crosshairStyle = computed(() => {
  if (!mousePosition.value) return {}
  return {
    left: `${mousePosition.value.displayX}px`,
    top: `${mousePosition.value.displayY}px`
  }
})

function getMarkerStyle(marker) {
  if (!imageLoaded.value || !imageDisplayWidth.value) return { display: 'none' }
  
  const scaleX = imageDisplayWidth.value / screenWidth.value
  const scaleY = imageDisplayHeight.value / screenHeight.value
  
  return {
    left: `${marker.x * scaleX}px`,
    top: `${marker.y * scaleY}px`
  }
}

async function refreshScreenshot() {
  loading.value = true
  error.value = ''
  
  try {
    const result = await adbApi.takeScreenshotBase64()
    if (result.image) {
      screenshotData.value = result.image
      screenWidth.value = result.width || 0
      screenHeight.value = result.height || 0
    } else if (result.error) {
      error.value = result.error
    }
  } catch (err) {
    error.value = err.message || '获取截图失败'
  } finally {
    loading.value = false
  }
}

function handleImageLoad() {
  imageLoaded.value = true
  updateImageDisplaySize()
}

function updateImageDisplaySize() {
  if (imageRef.value) {
    imageDisplayWidth.value = imageRef.value.clientWidth || imageRef.value.offsetWidth
    imageDisplayHeight.value = imageRef.value.clientHeight || imageRef.value.offsetHeight
  }
}

function handleMouseMove(event) {
  if (!imageLoaded.value || !imageRef.value) return
  
  const rect = imageRef.value.getBoundingClientRect()
  const displayX = event.clientX - rect.left
  const displayY = event.clientY - rect.top
  
  if (displayX < 0 || displayY < 0 || displayX > rect.width || displayY > rect.height) {
    mousePosition.value = null
    currentCoordinate.value = null
    return
  }
  
  const scaleX = screenWidth.value / rect.width
  const scaleY = screenHeight.value / rect.height
  
  const realX = Math.round(displayX * scaleX)
  const realY = Math.round(displayY * scaleY)
  
  mousePosition.value = { displayX, displayY }
  currentCoordinate.value = { x: realX, y: realY }
  
  emit('coordinate-update', currentCoordinate.value)
}

function handleMouseLeave() {
  mousePosition.value = null
  currentCoordinate.value = null
}

function handleImageClick(event) {
  if (!currentCoordinate.value) return
  
  lastClickCoordinate.value = { ...currentCoordinate.value }
  
  addClickMarker(lastClickCoordinate.value.x, lastClickCoordinate.value.y, 'click')
  
  emit('coordinate-click', lastClickCoordinate.value)
  
  ElMessage.success(`已选择坐标: (${lastClickCoordinate.value.x}, ${lastClickCoordinate.value.y})`)
}

function addClickMarker(x, y, type = 'click') {
  const marker = { x, y, type, id: Date.now() }
  clickMarkers.value.push(marker)
  
  setTimeout(() => {
    const index = clickMarkers.value.findIndex(m => m.id === marker.id)
    if (index > -1) {
      clickMarkers.value.splice(index, 1)
    }
  }, 2000)
}

function showDragPreview(startX, startY, endX, endY, options = {}) {
  console.log('[ScreenPreview] showDragPreview called:', { startX, startY, endX, endY, options })
  
  if (!imageLoaded.value) {
    console.log('[ScreenPreview] image not loaded, exiting')
    return
  }
  
  // 先更新图片显示尺寸（确保正确）
  updateImageDisplaySize()
  
  if (!imageDisplayWidth.value || !imageDisplayHeight.value) {
    console.log('[ScreenPreview] image size not available:', { imageDisplayWidth: imageDisplayWidth.value, imageDisplayHeight: imageDisplayHeight.value })
    return
  }

  const {
    trajectoryType = 'bezier',
    duration = 1000,
    speedMode = 'ease_in_out',
    numPoints = 50
  } = options

  const scaleX = imageDisplayWidth.value / screenWidth.value
  const scaleY = imageDisplayHeight.value / screenHeight.value

  const displayStartX = startX * scaleX
  const displayStartY = startY * scaleY
  const displayEndX = endX * scaleX
  const displayEndY = endY * scaleY

  // 生成轨迹路径和采样点
  let path = ''
  let points = []

  if (trajectoryType === 'bezier') {
    // 贝塞尔曲线
    const midX = (displayStartX + displayEndX) / 2
    const midY = (displayStartY + displayEndY) / 2
    const ctrlX = midX + (Math.random() - 0.5) * 50
    const ctrlY = midY + (Math.random() - 0.5) * 50

    path = `M ${displayStartX} ${displayStartY} Q ${ctrlX} ${ctrlY} ${displayEndX} ${displayEndY}`

    // 生成采样点用于动画
    for (let i = 0; i <= numPoints; i++) {
      const t = i / numPoints
      const pointT = applySpeedMode(t, speedMode)
      const x = Math.pow(1 - pointT, 2) * displayStartX + 2 * (1 - pointT) * pointT * ctrlX + Math.pow(pointT, 2) * displayEndX
      const y = Math.pow(1 - pointT, 2) * displayStartY + 2 * (1 - pointT) * pointT * ctrlY + Math.pow(pointT, 2) * displayEndY
      points.push({ x, y })
    }
  } else {
    // 直线 + 抖动
    const jitter = 5
    const jitterY = (Math.random() - 0.5) * jitter * scaleY

    path = `M ${displayStartX} ${displayStartY} L ${displayEndX} ${displayEndY}`

    for (let i = 0; i <= numPoints; i++) {
      const t = i / numPoints
      const pointT = applySpeedMode(t, speedMode)
      const x = displayStartX + (displayEndX - displayStartX) * pointT
      const jitterOffset = Math.sin(t * Math.PI * 2) * jitter * scaleY * (1 - t)
      const y = displayStartY + (displayEndY - displayStartY) * pointT + jitterOffset
      points.push({ x, y })
    }
  }

  // 显示预览并播放动画
  dragPreview.value = {
    show: true,
    startX: displayStartX,
    startY: displayStartY,
    endX: displayEndX,
    endY: displayEndY,
    path: path,
    trajectoryType,
    duration,
    progress: 0,
    currentPoint: null
  }
  
  console.log('[ScreenPreview] dragPreview.value set:', dragPreview.value)
  console.log('[ScreenPreview] imageDisplayWidth/Height:', { width: imageDisplayWidth.value, height: imageDisplayHeight.value })

  // 播放动画
  console.log('[ScreenPreview] Calling playDragAnimation with', { pointsLength: points.length, duration })
  
  // 确保 Vue 响应式系统触发视图更新后再播放动画
  setTimeout(() => {
    console.log('[ScreenPreview] Starting animation after 100ms delay')
    playDragAnimation(points, duration)
  }, 100)

  // 3秒后清除
  setTimeout(() => {
    dragPreview.value = null
  }, duration + 500 + 100)
}

function getTrajectoryColor(trajectoryType) {
  return trajectoryType === 'bezier' ? '#409EFF' : '#E6A23C'
}

function applySpeedMode(t, speedMode) {
  // 速度模式转换
  switch (speedMode) {
    case 'ease_in':
      return t * t
    case 'ease_out':
      return t * (2 - t)
    case 'linear':
      return t
    case 'random':
      // 随机速度，稍微不均匀
      return t + (Math.random() - 0.5) * 0.1 * Math.sin(t * Math.PI)
    case 'ease_in_out':
    default:
      return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t
  }
}

function playDragAnimation(points, duration) {
  if (!dragPreview.value || points.length === 0) return

  const intervalTime = duration / points.length // 每个点的间隔时间
  let currentIndex = 0

  // 立即显示第一个点
  dragPreview.value.currentPoint = points[0]
  dragPreview.value.progress = 0
  currentIndex++

  // 使用 setInterval 逐步更新动画
  const animateInterval = setInterval(() => {
    if (currentIndex >= points.length || !dragPreview.value) {
      clearInterval(animateInterval)
      return
    }

    dragPreview.value.currentPoint = points[currentIndex]
    dragPreview.value.progress = currentIndex / points.length

    currentIndex++
  }, intervalTime)

  // 动画结束后清除定时器
  setTimeout(() => {
    clearInterval(animateInterval)
  }, duration)
}

function clearDragPreview() {
  dragPreview.value = null
}

function copyCoordinate() {
  if (!lastClickCoordinate.value) return
  
  const text = `${lastClickCoordinate.value.x}, ${lastClickCoordinate.value.y}`
  navigator.clipboard.writeText(text)
  ElMessage.success('坐标已复制到剪贴板')
}

function startAutoRefresh() {
  stopAutoRefresh()
  autoRefreshTimer = setInterval(() => {
    if (!loading.value) {
      refreshScreenshot()
    }
  }, props.autoRefreshInterval)
}

function stopAutoRefresh() {
  if (autoRefreshTimer) {
    clearInterval(autoRefreshTimer)
    autoRefreshTimer = null
  }
}

watch(autoRefresh, (val) => {
  if (val) {
    startAutoRefresh()
  } else {
    stopAutoRefresh()
  }
})

onMounted(() => {
  refreshScreenshot()
})

onUnmounted(() => {
  stopAutoRefresh()
})

defineExpose({
  refreshScreenshot,
  addClickMarker,
  showDragPreview,
  clearDragPreview,
  lastClickCoordinate
})
</script>

<style scoped>
.screen-preview {
  height: 100%;
}

.screen-container {
  position: relative;
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  border-radius: 8px;
  overflow: hidden;
}

.loading-placeholder,
.error-placeholder,
.empty-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.image-container {
  position: relative;
  cursor: crosshair;
  max-width: 100%;
  max-height: 600px;
  overflow: hidden;
}

.screenshot-image {
  display: block;
  max-width: 100%;
  max-height: 600px;
  object-fit: contain;
  border-radius: 4px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.crosshair {
  position: absolute;
  pointer-events: none;
  z-index: 10;
}

.crosshair-h,
.crosshair-v {
  position: absolute;
  background: rgba(64, 158, 255, 0.8);
}

.crosshair-h {
  width: 20px;
  height: 1px;
  left: -10px;
  top: 0;
}

.crosshair-v {
  width: 1px;
  height: 20px;
  left: 0;
  top: -10px;
}

.click-marker {
  position: absolute;
  transform: translate(-50%, -50%);
  pointer-events: none;
  z-index: 20;
}

.marker-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #67C23A;
  border: 2px solid white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.click-marker.click .marker-dot {
  background: #67C23A;
}

.click-marker.double-click .marker-dot {
  background: #E6A23C;
}

.click-marker.long-press .marker-dot {
  background: #F56C6C;
}

.marker-ripple {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 2px solid #67C23A;
  animation: ripple 1s ease-out forwards;
}

.click-marker.double-click .marker-ripple {
  border-color: #E6A23C;
}

.click-marker.long-press .marker-ripple {
  border-color: #F56C6C;
}

@keyframes ripple {
  0% {
    width: 12px;
    height: 12px;
    opacity: 1;
  }
  100% {
    width: 50px;
    height: 50px;
    opacity: 0;
  }
}

.refresh-overlay {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  padding: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.coordinate-info {
  padding-top: 12px;
  border-top: 1px solid #ebeef5;
}

.drag-preview-svg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 20;
}

/* 拖拽动画样式 - 注释掉，使用 JavaScript 动画控制
.trajectory-path {
  animation: drawPath 1s ease-in-out forwards;
}

@keyframes drawPath {
  from {
    stroke-dashoffset: 1000;
  }
  to {
    stroke-dashoffset: 0;
  }
}
*/

.marker-pulse {
  animation: markerPulse 1.5s ease-in-out infinite;
  transform-origin: center;
}

@keyframes markerPulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.8;
  }
}

/* 限制 .drag-finger 动画只作用于移动手指组 */
.drag-finger > circle {
  animation: fingerBounce 0.3s ease-in-out infinite;
}

@keyframes fingerBounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-3px);
  }
}

.finger-shadow {
  filter: drop-shadow(0 2px 4px rgba(64, 158, 255, 0.4));
}

.progress-bar {
  animation: progressFill 1s ease-in-out forwards;
}

@keyframes progressFill {
  from {
    width: 0;
  }
  to {
    width: var(--target-width, 100%);
  }
}
</style>
