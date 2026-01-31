<template>
  <div class="space-y-6">
    <!-- 输入操作卡片 -->
    <el-card shadow="hover">
      <template #header>
        <div class="flex items-center gap-2">
          <el-icon><Pen /></el-icon>
          <span class="font-semibold">输入操作</span>
        </div>
      </template>
      
      <el-tabs v-model="activeTab" class="input-tabs">
        <el-tab-pane label="点击元素" name="click">
          <div class="space-y-4">
            <div class="flex gap-2">
              <el-select v-model="clickLocateType" placeholder="查找方式" class="w-32">
                <el-option label="By ID" value="id" />
                <el-option label="By Text" value="text" />
                <el-option label="By Class" value="class" />
                <el-option label="By XPath" value="xpath" />
              </el-select>
              <el-input
                v-model="clickLocateValue"
                :placeholder="clickPlaceholder"
                clearable
                class="flex-1"
              >
                <template #append v-if="clickLocateType === 'xpath'">
                  <el-button @click="openXPathGenerator('click')">
                    生成
                  </el-button>
                </template>
              </el-input>
            </div>
            <div class="flex gap-2">
              <el-button type="primary" :disabled="!clickLocateValue" @click="handleClick">
                点击元素
              </el-button>
              <el-button :disabled="!clickLocateValue" @click="handleExists">
                检查存在
              </el-button>
            </div>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="输入文本" name="text">
          <div class="space-y-4">
            <el-input
              v-model="textResourceId"
              placeholder="输入框的 resource-id"
              clearable
            />
            <el-input
              v-model="textInput"
              placeholder="要输入的文本内容"
              clearable
            />
            <div class="flex gap-2 flex-wrap">
              <el-button type="primary" :disabled="!textResourceId || !textInput" @click="handleSetText">
                输入文本
              </el-button>
              <el-button :disabled="!textResourceId" @click="handleClearText">
                清除文本
              </el-button>
              <el-button :disabled="!textResourceId" @click="handleSendAction">
                完成 (Send Action)
              </el-button>
            </div>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="滑动屏幕" name="swipe">
          <div class="space-y-4">
            <div>
              <p class="text-sm text-gray-500 mb-2">滑动方向</p>
              <el-radio-group v-model="swipeDirection">
                <el-radio-button value="up">向上</el-radio-button>
                <el-radio-button value="down">向下</el-radio-button>
                <el-radio-button value="left">向左</el-radio-button>
                <el-radio-button value="right">向右</el-radio-button>
              </el-radio-group>
            </div>
            <div>
              <p class="text-sm text-gray-500 mb-2">滑动比例: {{ swipePercent }}</p>
              <el-slider v-model="swipePercent" :min="0.1" :max="0.9" :step="0.1" />
            </div>
            <div class="flex justify-end">
              <el-button type="primary" @click="handleSwipe">滑动</el-button>
            </div>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="元素定位" name="locate">
          <div class="space-y-4">
            <div class="flex gap-2">
              <el-select v-model="locateType" placeholder="选择定位方式" class="w-32">
                <el-option label="By ID" value="id" />
                <el-option label="By Text" value="text" />
                <el-option label="By Class" value="class" />
                <el-option label="By XPath" value="xpath" />
              </el-select>
              <el-input
                v-model="locateValue"
                placeholder="输入定位值"
                clearable
                class="flex-1"
              >
                <template #append v-if="locateType === 'xpath'">
                  <el-button @click="openXPathGenerator('locate')">
                    生成
                  </el-button>
                </template>
              </el-input>
            </div>
            <div class="flex gap-2">
              <el-button type="primary" :disabled="!locateValue || !locateType" @click="handleLocate">
                查找元素
              </el-button>
              <el-button v-if="locateType === 'class'" :disabled="!locateValue" @click="handleFindAll">
                查找全部
              </el-button>
            </div>
            <div 
              v-if="locateResult" 
              class="bg-gray-100 p-3 rounded text-sm overflow-auto resize-y"
              style="min-height: 100px; height: 200px; max-height: 400px;"
            >
              <pre class="whitespace-pre-wrap">{{ JSON.stringify(locateResult, null, 2) }}</pre>
            </div>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="等待元素" name="wait">
          <div class="space-y-4">
            <el-input
              v-model="waitResourceId"
              placeholder="输入元素的 resource-id"
              clearable
            />
            <div>
              <p class="text-sm text-gray-500 mb-2">等待时间（秒）: {{ waitTimeout }}</p>
              <el-slider v-model="waitTimeout" :min="1" :max="30" :step="1" />
            </div>
            <div class="flex gap-2">
              <el-button type="primary" :disabled="!waitResourceId" @click="handleWaitAppear">
                等待出现
              </el-button>
              <el-button :disabled="!waitResourceId" @click="handleWaitGone">
                等待消失
              </el-button>
            </div>
          </div>
        </el-tab-pane>

        <el-tab-pane label="元素信息" name="info">
          <div class="space-y-4">
            <el-input
              v-model="infoResourceId"
              placeholder="输入元素的 resource-id"
              clearable
            />
            <div class="flex gap-2">
              <el-button type="primary" :disabled="!infoResourceId" @click="handleGetText">
                获取文本
              </el-button>
              <el-button :disabled="!infoResourceId" @click="handleGetBounds">
                获取边界
              </el-button>
            </div>
            <div 
              v-if="elementInfo" 
              class="bg-gray-100 p-3 rounded text-sm overflow-auto resize-y"
              style="min-height: 80px; height: 120px; max-height: 300px;"
            >
              <pre class="whitespace-pre-wrap">{{ JSON.stringify(elementInfo, null, 2) }}</pre>
            </div>
          </div>
        </el-tab-pane>

        <el-tab-pane label="屏幕控制" name="screen">
          <div class="space-y-4">
            <p class="text-sm text-gray-500">控制设备屏幕状态</p>
            <div class="flex gap-2 flex-wrap">
              <el-button type="primary" @click="handleScreenOn">
                亮屏
              </el-button>
              <el-button @click="handleScreenOff">
                锁屏
              </el-button>
              <el-button type="success" @click="handleUnlock">
                解锁
              </el-button>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 界面结构卡片 -->
    <el-card shadow="hover">
      <template #header>
        <div class="flex items-center gap-2">
          <el-icon><Code /></el-icon>
          <span class="font-semibold">界面结构</span>
        </div>
      </template>
      
      <div class="space-y-4">
        <!-- 操作按钮 -->
        <div class="flex gap-2 flex-wrap">
          <el-button type="primary" @click="handleGetHierarchy" :loading="loadingHierarchy">
            获取当前界面 XML
          </el-button>
          <el-button @click="handleRefreshXml" :loading="loadingHierarchy">
            刷新
          </el-button>
          <el-button v-if="hierarchyXml" @click="copyHierarchy">
            复制
          </el-button>
          <el-button type="success" @click="showXPathGenerator = true">
            XPath 生成器
          </el-button>
        </div>
        
        <!-- 搜索功能区 -->
        <div v-if="hierarchyXml" class="space-y-3">
          <div class="flex gap-2 flex-wrap items-center">
            <el-select v-model="searchFilterType" placeholder="过滤属性" class="w-36">
              <el-option label="全部内容" value="all" />
              <el-option label="resource-id" value="resource-id" />
              <el-option label="text" value="text" />
              <el-option label="class" value="class" />
              <el-option label="content-desc" value="content-desc" />
              <el-option label="bounds" value="bounds" />
            </el-select>
            <el-input
              v-model="searchKeyword"
              placeholder="输入搜索关键词..."
              clearable
              class="flex-1"
              @input="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </div>
          
          <!-- 搜索结果导航 -->
          <div v-if="searchKeyword && searchMatches.length > 0" class="flex items-center gap-3">
            <span class="text-sm text-gray-500">
              找到 <span class="text-blue-600 font-semibold">{{ searchMatches.length }}</span> 个匹配
              <span v-if="currentMatchIndex >= 0" class="ml-1">
                ({{ currentMatchIndex + 1 }}/{{ searchMatches.length }})
              </span>
            </span>
            <div class="flex gap-1">
              <el-button size="small" :disabled="searchMatches.length === 0" @click="goToPrevMatch">
                <el-icon><ArrowUp /></el-icon>
                上一个
              </el-button>
              <el-button size="small" :disabled="searchMatches.length === 0" @click="goToNextMatch">
                下一个
                <el-icon><ArrowDown /></el-icon>
              </el-button>
            </div>
          </div>
          <div v-else-if="searchKeyword && searchMatches.length === 0" class="text-sm text-gray-400">
            未找到匹配内容
          </div>
        </div>
        
        <!-- XML 展示区 -->
        <div 
          v-if="hierarchyXml" 
          ref="xmlContainerRef"
          class="bg-gray-900 text-green-400 p-3 rounded text-xs font-mono overflow-auto resize-y"
          style="min-height: 200px; height: 400px; max-height: 700px;"
        >
          <pre class="whitespace-pre-wrap" v-html="highlightedXml"></pre>
        </div>
      </div>
    </el-card>

    <!-- XPath 生成器弹窗 -->
    <XPathGenerator
      v-model="showXPathGenerator"
      @insert="handleXPathInsert"
    />
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { inputApi } from '@/api'
import { Pen, Code, Search, ArrowUp, ArrowDown } from '@vicons/fa'
import XPathGenerator from './XPathGenerator.vue'

const activeTab = ref('click')
const clickLocateType = ref('id')
const clickLocateValue = ref('')
const textResourceId = ref('')
const textInput = ref('')
const swipeDirection = ref('up')
const swipePercent = ref(0.5)
const locateValue = ref('')
const locateType = ref('id')
const locateResult = ref(null)
const waitResourceId = ref('')
const waitTimeout = ref(10)
const infoResourceId = ref('')
const elementInfo = ref(null)
const hierarchyXml = ref('')
const loadingHierarchy = ref(false)

// 搜索相关状态
const searchKeyword = ref('')
const searchFilterType = ref('all')
const searchMatches = ref([])
const currentMatchIndex = ref(-1)
const xmlContainerRef = ref(null)

// XPath 生成器相关
const showXPathGenerator = ref(false)
const xpathInsertTarget = ref('') // 'click' 或 'locate'

function openXPathGenerator(target) {
  xpathInsertTarget.value = target
  showXPathGenerator.value = true
}

function handleXPathInsert(xpath) {
  if (xpathInsertTarget.value === 'click') {
    clickLocateValue.value = xpath
    clickLocateType.value = 'xpath'
  } else if (xpathInsertTarget.value === 'locate') {
    locateValue.value = xpath
    locateType.value = 'xpath'
  }
  ElMessage.success('XPath 已插入')
}

const clickPlaceholder = computed(() => {
  const placeholders = {
    id: '输入元素的 resource-id（如 com.example:id/button）',
    text: '输入元素的文本内容（如 确定）',
    class: '输入元素的类名（如 android.widget.Button）',
    xpath: '输入 XPath 表达式（如 //android.widget.Button[@text="确定"]）'
  }
  return placeholders[clickLocateType.value] || '输入定位值'
})

async function handleClick() {
  try {
    let response
    switch (clickLocateType.value) {
      case 'id':
        response = await inputApi.click(clickLocateValue.value)
        break
      case 'text':
        response = await inputApi.clickByText(clickLocateValue.value)
        break
      case 'class':
        response = await inputApi.clickByClass(clickLocateValue.value)
        break
      case 'xpath':
        response = await inputApi.clickByXpath(clickLocateValue.value)
        break
    }
    if (response.success) {
      ElMessage.success('点击成功')
    } else {
      ElMessage.warning('元素不存在，无法点击')
    }
  } catch (err) {
    ElMessage.error('点击失败')
  }
}

async function handleExists() {
  try {
    let response
    switch (clickLocateType.value) {
      case 'id':
        response = await inputApi.exists(clickLocateValue.value)
        break
      case 'text':
        response = await inputApi.existsByText(clickLocateValue.value)
        break
      case 'class':
        response = await inputApi.existsByClass(clickLocateValue.value)
        break
      case 'xpath':
        response = await inputApi.existsByXpath(clickLocateValue.value)
        break
    }
    const exists = response.result?.exists ?? response.exists
    if (exists) {
      ElMessage.success('元素存在')
    } else {
      ElMessage.warning('元素不存在')
    }
  } catch (err) {
    ElMessage.error('检查失败')
  }
}

async function handleSetText() {
  try {
    await inputApi.setText(textResourceId.value, textInput.value)
    ElMessage.success('文本输入成功')
  } catch (err) {
    ElMessage.error('输入文本失败')
  }
}

async function handleClearText() {
  try {
    await inputApi.clearText(textResourceId.value)
    ElMessage.success('清除文本成功')
  } catch (err) {
    ElMessage.error('清除文本失败')
  }
}

async function handleSendAction() {
  try {
    await inputApi.sendAction(textResourceId.value)
    ElMessage.success('发送完成动作成功')
  } catch (err) {
    ElMessage.error('发送完成动作失败')
  }
}

async function handleSwipe() {
  try {
    await inputApi.swipe(swipeDirection.value, swipePercent.value)
    ElMessage.success('滑动成功')
  } catch (err) {
    ElMessage.error('滑动失败')
  }
}

async function handleLocate() {
  try {
    let result
    switch (locateType.value) {
      case 'id':
        result = await inputApi.findById(locateValue.value)
        break
      case 'text':
        result = await inputApi.findByText(locateValue.value)
        break
      case 'class':
        result = await inputApi.findByClass(locateValue.value)
        break
      case 'xpath':
        result = await inputApi.findByXpath(locateValue.value)
        break
    }
    locateResult.value = result
    ElMessage.success('查找完成')
  } catch (err) {
    ElMessage.error('查找失败')
    locateResult.value = null
  }
}

async function handleFindAll() {
  try {
    const result = await inputApi.findElementsByClass(locateValue.value)
    locateResult.value = result
    ElMessage.success(`找到 ${result.elements?.length || result.count || 0} 个元素`)
  } catch (err) {
    ElMessage.error('查找失败')
    locateResult.value = null
  }
}

async function handleWaitAppear() {
  try {
    const result = await inputApi.waitAppear(waitResourceId.value, waitTimeout.value)
    if (result.appeared) {
      ElMessage.success('元素已出现')
    } else {
      ElMessage.warning('等待超时，元素未出现')
    }
  } catch (err) {
    ElMessage.error('等待失败')
  }
}

async function handleWaitGone() {
  try {
    const result = await inputApi.waitGone(waitResourceId.value, waitTimeout.value)
    if (result.gone) {
      ElMessage.success('元素已消失')
    } else {
      ElMessage.warning('等待超时，元素仍在')
    }
  } catch (err) {
    ElMessage.error('等待失败')
  }
}

async function handleGetText() {
  try {
    const result = await inputApi.getElementText(infoResourceId.value)
    elementInfo.value = result
    ElMessage.success('获取文本成功')
  } catch (err) {
    ElMessage.error('获取文本失败')
    elementInfo.value = null
  }
}

async function handleGetBounds() {
  try {
    const result = await inputApi.getElementBounds(infoResourceId.value)
    elementInfo.value = result
    ElMessage.success('获取边界成功')
  } catch (err) {
    ElMessage.error('获取边界失败')
    elementInfo.value = null
  }
}

async function handleGetHierarchy() {
  loadingHierarchy.value = true
  try {
    const result = await inputApi.getHierarchy()
    hierarchyXml.value = result.xml || ''
    ElMessage.success('获取界面结构成功')
  } catch (err) {
    ElMessage.error('获取界面结构失败')
    hierarchyXml.value = ''
  } finally {
    loadingHierarchy.value = false
  }
}

async function handleRefreshXml() {
  await handleGetHierarchy()
}

function copyHierarchy() {
  navigator.clipboard.writeText(hierarchyXml.value)
  ElMessage.success('已复制到剪贴板')
}

async function handleScreenOn() {
  try {
    await inputApi.screenOn()
    ElMessage.success('亮屏成功')
  } catch (err) {
    ElMessage.error('亮屏失败')
  }
}

async function handleScreenOff() {
  try {
    await inputApi.screenOff()
    ElMessage.success('锁屏成功')
  } catch (err) {
    ElMessage.error('锁屏失败')
  }
}

async function handleUnlock() {
  try {
    await inputApi.unlock()
    ElMessage.success('解锁成功')
  } catch (err) {
    ElMessage.error('解锁失败')
  }
}

// 搜索功能：高亮显示的 XML
const highlightedXml = computed(() => {
  if (!hierarchyXml.value) return ''
  if (!searchKeyword.value) {
    return escapeHtml(hierarchyXml.value)
  }
  
  const keyword = searchKeyword.value
  let xmlContent = hierarchyXml.value
  
  // 根据过滤类型构建搜索内容
  if (searchFilterType.value !== 'all') {
    // 只在特定属性中搜索
    const attrPattern = new RegExp(
      `(${searchFilterType.value}="[^"]*)(${escapeRegExp(keyword)})([^"]*")`,
      'gi'
    )
    return escapeHtml(xmlContent).replace(
      new RegExp(`(${escapeRegExp(searchFilterType.value)}=&quot;[^&]*)(${escapeRegExp(escapeHtml(keyword))})([^&]*&quot;)`, 'gi'),
      (match, before, kw, after, offset) => {
        return `${before}<mark class="search-highlight" data-match-index="${offset}">${kw}</mark>${after}`
      }
    )
  }
  
  // 全局搜索并高亮
  const escapedXml = escapeHtml(xmlContent)
  const escapedKeyword = escapeHtml(keyword)
  const regex = new RegExp(`(${escapeRegExp(escapedKeyword)})`, 'gi')
  
  let matchIndex = 0
  return escapedXml.replace(regex, (match) => {
    return `<mark class="search-highlight" data-match-index="${matchIndex++}">${match}</mark>`
  })
})

// 搜索处理函数
function handleSearch() {
  if (!searchKeyword.value || !hierarchyXml.value) {
    searchMatches.value = []
    currentMatchIndex.value = -1
    return
  }
  
  const keyword = searchKeyword.value
  let content = hierarchyXml.value
  
  // 根据过滤类型搜索
  if (searchFilterType.value !== 'all') {
    // 只在特定属性中搜索
    const attrRegex = new RegExp(`${searchFilterType.value}="[^"]*${escapeRegExp(keyword)}[^"]*"`, 'gi')
    const matches = content.match(attrRegex) || []
    searchMatches.value = matches
  } else {
    // 全局搜索
    const regex = new RegExp(escapeRegExp(keyword), 'gi')
    const matches = content.match(regex) || []
    searchMatches.value = matches
  }
  
  // 如果有匹配，自动跳转到第一个
  if (searchMatches.value.length > 0) {
    currentMatchIndex.value = 0
    nextTick(() => scrollToMatch(0))
  } else {
    currentMatchIndex.value = -1
  }
}

// 跳转到上一个匹配
function goToPrevMatch() {
  if (searchMatches.value.length === 0) return
  
  currentMatchIndex.value = currentMatchIndex.value <= 0 
    ? searchMatches.value.length - 1 
    : currentMatchIndex.value - 1
  
  nextTick(() => scrollToMatch(currentMatchIndex.value))
}

// 跳转到下一个匹配
function goToNextMatch() {
  if (searchMatches.value.length === 0) return
  
  currentMatchIndex.value = currentMatchIndex.value >= searchMatches.value.length - 1 
    ? 0 
    : currentMatchIndex.value + 1
  
  nextTick(() => scrollToMatch(currentMatchIndex.value))
}

// 滚动到指定匹配位置
function scrollToMatch(index) {
  if (!xmlContainerRef.value) return
  
  const marks = xmlContainerRef.value.querySelectorAll('mark.search-highlight')
  
  // 移除所有当前高亮
  marks.forEach(mark => mark.classList.remove('current-match'))
  
  if (marks[index]) {
    marks[index].classList.add('current-match')
    marks[index].scrollIntoView({ behavior: 'smooth', block: 'center' })
  }
}

// 辅助函数：转义 HTML
function escapeHtml(text) {
  const div = document.createElement('div')
  div.textContent = text
  return div.innerHTML
}

// 辅助函数：转义正则表达式特殊字符
function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}
</script>

<style scoped>
.input-tabs :deep(.el-tabs__content) {
  padding: 16px 0;
}

/* 搜索高亮样式 */
:deep(.search-highlight) {
  background-color: #fbbf24;
  color: #1f2937;
  padding: 1px 2px;
  border-radius: 2px;
}

:deep(.search-highlight.current-match) {
  background-color: #f97316;
  color: white;
  box-shadow: 0 0 0 2px #f97316;
}
</style>
