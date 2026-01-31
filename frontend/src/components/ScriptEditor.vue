<template>
  <div class="space-y-4">
    <!-- 工具栏 -->
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <el-select v-model="currentScript" placeholder="选择脚本" style="width: 200px" @change="loadScript">
          <el-option v-for="s in scripts" :key="s.name" :label="s.name" :value="s.name" />
        </el-select>
        <el-button @click="newScript">新建</el-button>
        <el-button type="primary" @click="saveScript" :disabled="!scriptContent">保存</el-button>
        <el-button type="danger" @click="deleteScript" :disabled="!currentScript">删除</el-button>
      </div>
      <div class="flex items-center gap-2">
        <el-button @click="validateScript" :disabled="!scriptContent">验证语法</el-button>
        <el-button 
          type="success" 
          @click="executeScript" 
          :loading="executing" 
          :disabled="!scriptContent || executing"
        >
          {{ executing ? '执行中...' : '执行脚本' }}
        </el-button>
        <el-button 
          type="danger" 
          @click="stopScript" 
          :disabled="!executing"
          v-show="executing"
        >
          停止
        </el-button>
      </div>
    </div>

    <!-- 编辑器区域 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <!-- 脚本编辑器 -->
      <el-card shadow="hover">
        <template #header>
          <div class="flex items-center justify-between">
            <span class="font-semibold">脚本编辑器</span>
            <el-tag v-if="currentScript" size="small">{{ currentScript }}</el-tag>
          </div>
        </template>
        <el-input
          v-model="scriptContent"
          type="textarea"
          :rows="20"
          placeholder="在此输入脚本内容..."
          class="font-mono"
          style="font-family: monospace;"
        />
      </el-card>

      <!-- 执行日志 -->
      <el-card shadow="hover">
        <template #header>
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="font-semibold">执行日志</span>
              <el-tag v-if="executing" type="success" size="small" effect="dark">
                <span class="animate-pulse">实时</span>
              </el-tag>
            </div>
            <el-button size="small" @click="clearLogs" :disabled="executing">清空</el-button>
          </div>
        </template>
        <div 
          class="log-container bg-gray-900 text-green-400 p-4 rounded font-mono text-sm overflow-auto resize-y"
          style="min-height: 200px; height: 384px; max-height: 800px;"
        >
          <div v-if="logs.length === 0" class="text-gray-500">暂无日志</div>
          <div v-for="(log, index) in logs" :key="index" class="mb-1 whitespace-pre-wrap break-all">
            {{ log }}
          </div>
          <div v-if="executionError && !executing" class="text-red-400 mt-2">
            [ERROR] {{ executionError }}
          </div>
        </div>
      </el-card>
    </div>

    <!-- 语法帮助 -->
    <el-card shadow="hover">
      <template #header>
        <div class="flex items-center gap-2 cursor-pointer select-none hover:text-blue-600 transition-colors" @click="showHelp = !showHelp">
          <span class="font-semibold">DSL 语法参考</span>
          <span class="text-gray-500 text-xs">(点击{{ showHelp ? '收起' : '展开' }})</span>
          <el-icon class="transition-transform" :class="{ 'rotate-180': showHelp }">
            <ArrowDown />
          </el-icon>
        </div>
      </template>
      <div v-show="showHelp" class="text-sm space-y-4">
        <!-- 选择器类型说明 -->
        <div class="bg-blue-50 p-3 rounded border border-blue-200">
          <h4 class="font-semibold mb-2 text-blue-800">选择器类型</h4>
          <div class="text-xs text-blue-700 grid grid-cols-2 md:grid-cols-4 gap-2">
            <div><code class="bg-blue-100 px-1 rounded">id:"resource_id"</code> 资源ID</div>
            <div><code class="bg-blue-100 px-1 rounded">text:"文本"</code> 显示文本</div>
            <div><code class="bg-blue-100 px-1 rounded">xpath:"//..."</code> XPath表达式</div>
            <div><code class="bg-blue-100 px-1 rounded">class:"类名"</code> 类名</div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <!-- 基础命令 -->
          <div>
            <h4 class="font-semibold mb-2">点击命令</h4>
            <pre class="bg-gray-100 p-2 rounded text-xs"># 通过选择器点击
click id:"resource_id"
click text:"按钮文本"
click xpath:"//Button[@text='确定']"
click class:"android.widget.Button"

# 快捷点击
click_text "文本"
click_id "resource_id"</pre>
          </div>

          <div>
            <h4 class="font-semibold mb-2">输入命令</h4>
            <pre class="bg-gray-100 p-2 rounded text-xs"># 输入文本
input id:"input_id" "要输入的文本"
input text:"搜索" "关键词"

# 清除文本
clear id:"input_id"
clear text:"搜索框"</pre>
          </div>

          <div>
            <h4 class="font-semibold mb-2">滑动命令</h4>
            <pre class="bg-gray-100 p-2 rounded text-xs"># 方向滑动（可选距离比例）
swipe up 0.5      # 向上滑动 50%
swipe down 0.3    # 向下滑动 30%
swipe left        # 向左滑动
swipe right       # 向右滑动</pre>
          </div>

          <div>
            <h4 class="font-semibold mb-2">等待命令</h4>
            <pre class="bg-gray-100 p-2 rounded text-xs"># 固定等待
wait 2            # 等待 2 秒
wait 0.5          # 等待 0.5 秒

# 等待元素出现
wait_element id:"loading" 10

# 等待元素消失
wait_gone id:"loading" 10</pre>
          </div>

          <div>
            <h4 class="font-semibold mb-2">导航命令</h4>
            <pre class="bg-gray-100 p-2 rounded text-xs">back      # 返回键
home      # 主页键
menu      # 菜单键
recent    # 最近应用</pre>
          </div>

          <div>
            <h4 class="font-semibold mb-2">应用命令</h4>
            <pre class="bg-gray-100 p-2 rounded text-xs"># 启动应用
start_app "com.example.app"

# 停止应用
stop_app "com.example.app"

# 清除应用数据
clear_app "com.example.app"</pre>
          </div>

          <div>
            <h4 class="font-semibold mb-2">屏幕控制</h4>
            <pre class="bg-gray-100 p-2 rounded text-xs">screen_on     # 亮屏
screen_off    # 锁屏
unlock        # 解锁屏幕</pre>
          </div>

          <div>
            <h4 class="font-semibold mb-2">变量操作</h4>
            <pre class="bg-gray-100 p-2 rounded text-xs"># 设置变量
set $name = "value"
set $count = 10

# 获取元素文本
set $text = get_text id:"title"

# 检查元素是否存在
set $found = exists id:"button"

# 使用变量
click text:$name
input id:"input" $text</pre>
          </div>

          <div>
            <h4 class="font-semibold mb-2">条件判断</h4>
            <pre class="bg-gray-100 p-2 rounded text-xs">if exists id:"button"
    click id:"button"
elif not exists id:"loading"
    log "加载完成"
elif $var == "value"
    log "变量匹配"
else
    log "未找到"
end

# 条件表达式:
# exists id:"xxx"     元素存在
# not exists id:"xxx" 元素不存在
# $var == "value"     变量等于
# $var != "value"     变量不等于</pre>
          </div>

          <div>
            <h4 class="font-semibold mb-2">循环控制</h4>
            <pre class="bg-gray-100 p-2 rounded text-xs"># 固定次数循环
loop 5
    click id:"button"
    wait 1
end

# 条件循环
while exists id:"loading"
    wait 1
end

# 循环控制
loop 10
    if exists id:"done"
        break     # 跳出循环
    end
    click id:"next"
    continue      # 继续下一次
end</pre>
          </div>

          <div>
            <h4 class="font-semibold mb-2">错误处理</h4>
            <pre class="bg-gray-100 p-2 rounded text-xs">try
    click id:"maybe_not_exist"
    wait 1
catch
    log "元素不存在，跳过"
end</pre>
          </div>

          <div>
            <h4 class="font-semibold mb-2">其他命令</h4>
            <pre class="bg-gray-100 p-2 rounded text-xs"># 输出日志
log "日志消息"
log $variable

# 执行 Shell 命令
shell "ls /sdcard"
shell "pm list packages"

# 调用其他脚本
call "other_script.script"

# 注释（以 # 开头）
# 这是一行注释</pre>
          </div>
        </div>

        <!-- 完整示例 -->
        <div class="mt-4">
          <h4 class="font-semibold mb-2">完整脚本示例</h4>
          <pre class="bg-gray-100 p-3 rounded text-xs overflow-x-auto"># 自动打开设置并滑动
start_app "com.android.settings"
wait 2

# 等待界面加载
wait_element id:"android:id/title" 10

# 查找并点击 WLAN
if exists text:"WLAN"
    click text:"WLAN"
    wait 1
else
    log "未找到 WLAN"
end

# 滑动 3 次
loop 3
    swipe up 0.3
    wait 0.5
end

# 返回主页
home
log "完成"</pre>
        </div>
      </div>
    </el-card>

    <!-- 新建脚本对话框 -->
    <el-dialog v-model="showNewDialog" title="新建脚本" width="400px">
      <el-input v-model="newScriptName" placeholder="输入脚本名称" />
      <template #footer>
        <el-button @click="showNewDialog = false">取消</el-button>
        <el-button type="primary" @click="createScript">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowDown } from '@element-plus/icons-vue'
import { scriptApi } from '@/api'

const scripts = ref([])
const currentScript = ref('')
const scriptContent = ref('')
const logs = ref([])
const executionError = ref('')
const executing = ref(false)
const showHelp = ref(true)
const showNewDialog = ref(false)
const newScriptName = ref('')

// SSE 执行相关
const currentSessionId = ref('')
const executionController = ref(null)
const logContainer = ref(null)

async function loadScripts() {
  try {
    scripts.value = await scriptApi.list()
  } catch (err) {
    ElMessage.error('加载脚本列表失败')
  }
}

async function loadScript(name) {
  if (!name) return
  try {
    const result = await scriptApi.get(name)
    scriptContent.value = result.content
  } catch (err) {
    ElMessage.error('加载脚本失败')
  }
}

function newScript() {
  newScriptName.value = ''
  showNewDialog.value = true
}

function createScript() {
  if (!newScriptName.value.trim()) {
    ElMessage.warning('请输入脚本名称')
    return
  }
  currentScript.value = newScriptName.value.endsWith('.script') 
    ? newScriptName.value 
    : newScriptName.value + '.script'
  scriptContent.value = '# ' + currentScript.value + '\n\n'
  showNewDialog.value = false
}

async function saveScript() {
  if (!scriptContent.value) return
  
  const name = currentScript.value || 'untitled.script'
  try {
    await scriptApi.save(name, scriptContent.value)
    ElMessage.success('脚本已保存')
    if (!currentScript.value) {
      currentScript.value = name
    }
    loadScripts()
  } catch (err) {
    ElMessage.error('保存脚本失败')
  }
}

async function deleteScript() {
  if (!currentScript.value) return
  
  try {
    await ElMessageBox.confirm(`确定要删除脚本 ${currentScript.value} 吗？`, '确认删除', { type: 'warning' })
    await scriptApi.delete(currentScript.value)
    ElMessage.success('脚本已删除')
    currentScript.value = ''
    scriptContent.value = ''
    loadScripts()
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error('删除脚本失败')
    }
  }
}

async function validateScript() {
  if (!scriptContent.value) return
  
  try {
    const result = await scriptApi.validate(scriptContent.value)
    if (result.valid) {
      ElMessage.success(`语法正确，共 ${result.statements} 条语句`)
    } else {
      ElMessage.error(`语法错误: ${result.error}`)
    }
  } catch (err) {
    ElMessage.error('验证失败')
  }
}

// 自动滚动到日志底部
function scrollToBottom() {
  nextTick(() => {
    const container = document.querySelector('.log-container')
    if (container) {
      container.scrollTop = container.scrollHeight
    }
  })
}

// 使用 SSE 实时执行脚本
function executeScript() {
  if (!scriptContent.value) return
  
  executing.value = true
  logs.value = []
  executionError.value = ''
  currentSessionId.value = ''

  // 添加开始执行的日志
  const startTime = new Date().toLocaleTimeString()
  logs.value.push(`[${startTime}] 开始执行脚本...`)
  scrollToBottom()

  executionController.value = scriptApi.executeStream(
    scriptContent.value,
    null,
    {
      onSession: (sessionId) => {
        currentSessionId.value = sessionId
      },
      onLog: (message) => {
        logs.value.push(message)
        scrollToBottom()
      },
      onResult: (result) => {
        if (!result.success) {
          executionError.value = result.error || '执行失败'
        }
      },
      onError: (error) => {
        executionError.value = error
        logs.value.push(`[ERROR] ${error}`)
        scrollToBottom()
      },
      onEnd: () => {
        executing.value = false
        executionController.value = null
        currentSessionId.value = ''
        
        const endTime = new Date().toLocaleTimeString()
        if (executionError.value) {
          logs.value.push(`[${endTime}] 脚本执行失败: ${executionError.value}`)
          ElMessage.error('脚本执行失败')
        } else {
          logs.value.push(`[${endTime}] 脚本执行完成`)
          ElMessage.success('脚本执行完成')
        }
        scrollToBottom()
      }
    }
  )
}

// 停止脚本执行
async function stopScript() {
  if (!executing.value) return

  try {
    // 先尝试通过 API 停止
    if (currentSessionId.value) {
      await scriptApi.stop(currentSessionId.value)
    }
    // 同时中止 SSE 连接
    if (executionController.value) {
      executionController.value.abort()
    }
    
    logs.value.push(`[${new Date().toLocaleTimeString()}] 用户停止执行`)
    scrollToBottom()
    ElMessage.warning('脚本已停止')
  } catch (err) {
    console.error('停止脚本失败:', err)
  } finally {
    executing.value = false
    executionController.value = null
    currentSessionId.value = ''
  }
}

function clearLogs() {
  logs.value = []
  executionError.value = ''
}

// 组件卸载时清理
onUnmounted(() => {
  if (executionController.value) {
    executionController.value.abort()
  }
})

onMounted(() => {
  loadScripts()
})
</script>
