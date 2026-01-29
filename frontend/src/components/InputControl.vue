<template>
  <el-card shadow="hover">
    <template #header>
      <div class="flex items-center gap-2">
        <el-icon><Pen /></el-icon>
        <span class="font-semibold">输入操作</span>
      </div>
    </template>
    
    <el-tabs v-model="activeTab">
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
            />
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
        <el-input
          v-model="textResourceId"
          placeholder="输入框的 resource-id"
          clearable
          class="mb-4"
        />
        <el-input
          v-model="textInput"
          placeholder="要输入的文本内容"
          clearable
          class="mb-4"
        />
        <div class="flex gap-2">
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
          <el-input
            v-model="locateValue"
            placeholder="输入定位值"
            clearable
          />
          <div class="flex gap-2">
            <el-select v-model="locateType" placeholder="选择定位方式" class="w-40">
              <el-option label="By ID" value="id" />
              <el-option label="By Text" value="text" />
              <el-option label="By Class" value="class" />
              <el-option label="By XPath" value="xpath" />
            </el-select>
            <el-button type="primary" :disabled="!locateValue || !locateType" @click="handleLocate">
              查找元素
            </el-button>
            <el-button v-if="locateType === 'class'" :disabled="!locateValue" @click="handleFindAll">
              查找全部
            </el-button>
          </div>
          <div v-if="locateResult" class="bg-gray-100 p-3 rounded text-sm max-h-60 overflow-auto">
            <pre>{{ JSON.stringify(locateResult, null, 2) }}</pre>
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
          <div v-if="elementInfo" class="bg-gray-100 p-3 rounded text-sm">
            <pre>{{ JSON.stringify(elementInfo, null, 2) }}</pre>
          </div>
        </div>
      </el-tab-pane>

      <el-tab-pane label="界面结构" name="hierarchy">
        <div class="space-y-4">
          <el-button type="primary" @click="handleGetHierarchy">
            获取当前界面 XML
          </el-button>
          <el-button @click="handleRefreshXml">
            刷新
          </el-button>
          <div v-if="hierarchyXml" class="bg-gray-100 p-3 rounded text-sm max-h-100 overflow-auto">
            <pre>{{ hierarchyXml }}</pre>
          </div>
        </div>
      </el-tab-pane>

      <el-tab-pane label="亮屏锁屏" name="screen">
        <div class="space-y-4">
          <div class="flex gap-2">
            <el-button type="primary" @click="handleScreenOn">
              亮屏
            </el-button>
            <el-button @click="handleScreenOff">
              锁屏
            </el-button>
          </div>
          <div class="flex gap-2">
            <el-button @click="handleUnlock">
              解锁
            </el-button>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
  </el-card>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { inputApi } from '@/api'
import { Pen } from '@vicons/fa'

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
  try {
    const result = await inputApi.getHierarchy()
    hierarchyXml.value = result.xml || ''
    ElMessage.success('获取界面结构成功')
  } catch (err) {
    ElMessage.error('获取界面结构失败')
    hierarchyXml.value = ''
  }
}

async function handleRefreshXml() {
  await handleGetHierarchy()
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
</script>
