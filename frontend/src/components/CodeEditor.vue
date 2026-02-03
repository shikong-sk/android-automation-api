<template>
  <div class="code-editor" ref="editorContainer">
    <div class="editor-wrapper" :style="{ height: `${currentHeight}px` }">
      <!-- 行号区域 -->
      <div class="line-numbers" ref="lineNumbersRef">
        <div v-for="line in lineCount" :key="line" class="line-number">{{ line }}</div>
      </div>
      
      <!-- 文本编辑区域 -->
      <textarea
        ref="textareaRef"
        v-model="editorContent"
        :placeholder="placeholder"
        class="editor-textarea"
        :style="{ fontFamily: fontFamily, fontSize: fontSize, lineHeight: lineHeight }"
        @keydown="handleKeydown"
        @scroll="handleScroll"
        @input="handleInput"
      />
    </div>
    
    <!-- 拖拽调整大小手柄 -->
    <div class="resize-handle" @mousedown="startResize" title="拖拽调整大小">
      <div class="resize-icon">⋮</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'

const MAX_HISTORY = 50

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: '在此输入内容...'
  },
  height: {
    type: Number,
    default: 400
  },
  minHeight: {
    type: Number,
    default: 200
  },
  maxHeight: {
    type: Number,
    default: 800
  },
  fontFamily: {
    type: String,
    default: 'monospace'
  },
  fontSize: {
    type: String,
    default: '14px'
  },
  lineHeight: {
    type: String,
    default: '1.5'
  },
  tabSize: {
    type: Number,
    default: 2
  },
  showLineNumbers: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

// Refs
const textareaRef = ref(null)
const lineNumbersRef = ref(null)
const editorContent = ref(props.modelValue)
const currentHeight = ref(props.height)

// 撤销/重做历史
const history = ref([])
const historyIndex = ref(-1)

// 拖拽调整大小相关
const isResizing = ref(false)
const startY = ref(0)
const startHeight = ref(0)

// 计算行数
const lineCount = computed(() => {
  return editorContent.value ? editorContent.value.split('\n').length : 1
})

// 监听内容变化
watch(() => props.modelValue, (newValue) => {
  if (newValue !== editorContent.value) {
    editorContent.value = newValue
    nextTick(() => {
      updateLineNumbersHeight()
    })
  }
})

watch(editorContent, (newValue) => {
  emit('update:modelValue', newValue)
  emit('change', newValue)
  nextTick(() => {
    updateLineNumbersHeight()
  })
})

// 保存当前状态到历史记录
function saveHistory() {
  const textarea = textareaRef.value
  if (!textarea) return
  
  const state = {
    content: editorContent.value,
    selectionStart: textarea.selectionStart,
    selectionEnd: textarea.selectionEnd
  }
  
  // 移除当前索引之后的历史记录（如果有重做记录）
  history.value = history.value.slice(0, historyIndex.value + 1)
  
  // 添加新状态
  history.value.push(state)
  
  // 限制历史记录数量
  if (history.value.length > MAX_HISTORY) {
    history.value.shift() // 移除最旧的状态
  } else {
    historyIndex.value++
  }
}

// 撤销
function undo() {
  if (historyIndex.value <= 0) return
  
  historyIndex.value--
  const state = history.value[historyIndex.value]
  
  editorContent.value = state.content
  
  nextTick(() => {
    restoreState(state)
  })
}

// 重做
function redo() {
  if (historyIndex.value >= history.value.length - 1) return
  
  historyIndex.value++
  const state = history.value[historyIndex.value]
  
  editorContent.value = state.content
  
  nextTick(() => {
    restoreState(state)
  })
}

// 恢复状态（内容和光标位置）
function restoreState(state) {
  const textarea = textareaRef.value
  if (!textarea) return
  
  textarea.value = state.content
  textarea.setSelectionRange(state.selectionStart, state.selectionEnd)
  textarea.focus()
}

// 拖拽调整大小
function startResize(event) {
  isResizing.value = true
  startY.value = event.clientY
  startHeight.value = currentHeight.value
  
  document.addEventListener('mousemove', handleResize)
  document.addEventListener('mouseup', stopResize)
  
  // 阻止文本选择
  event.preventDefault()
  document.body.style.userSelect = 'none'
  document.body.style.cursor = 'row-resize'
}

function handleResize(event) {
  if (!isResizing.value) return
  
  const deltaY = event.clientY - startY.value
  const newHeight = startHeight.value + deltaY
  
  // 限制最小和最大高度
  currentHeight.value = Math.max(
    props.minHeight,
    Math.min(props.maxHeight, newHeight)
  )
}

function stopResize() {
  isResizing.value = false
  
  document.removeEventListener('mousemove', handleResize)
  document.removeEventListener('mouseup', stopResize)
  
  document.body.style.userSelect = ''
  document.body.style.cursor = ''
}

// 处理键盘事件
function handleKeydown(event) {
  // Tab 缩进
  if (event.key === 'Tab') {
    event.preventDefault()
    insertTab()
    return
  }
  
  // Ctrl+Z 撤销
  if (event.ctrlKey && event.key === 'z') {
    event.preventDefault()
    undo()
    return
  }
  
  // Ctrl+Y 重做
  if (event.ctrlKey && event.key === 'y') {
    event.preventDefault()
    redo()
    return
  }
}

// 插入 Tab
function insertTab() {
  const textarea = textareaRef.value
  if (!textarea) return

  const start = textarea.selectionStart
  const end = textarea.selectionEnd
  const tab = ' '.repeat(props.tabSize)
  
  // 如果有文本选中，对每一行都缩进
  if (start !== end) {
    // 获取选中文本
    const selectedText = editorContent.value.substring(start, end)
    const lines = selectedText.split('\n')
    
    // 对每一行添加缩进
    const indentedLines = lines.map(line => tab + line)
    const newText = indentedLines.join('\n')
    
    // 更新内容
    editorContent.value = editorContent.value.substring(0, start) + newText + editorContent.value.substring(end)
    
    // 更新光标位置（选中所有已缩进的行）
    nextTick(() => {
      textarea.selectionStart = start
      textarea.selectionEnd = start + newText.length
      textarea.focus()
    })
  } else {
    // 没有选中内容，直接插入 Tab
    editorContent.value = editorContent.value.substring(0, start) + tab + editorContent.value.substring(end)
    
    // 更新光标位置
    nextTick(() => {
      textarea.selectionStart = textarea.selectionEnd = start + tab.length
      textarea.focus()
    })
  }
}

// 处理滚动事件，同步行号滚动
function handleScroll() {
  if (!lineNumbersRef.value || !textareaRef.value) return
  lineNumbersRef.value.scrollTop = textareaRef.value.scrollTop
}

// 处理输入事件
function handleInput() {
  // 保存到历史记录
  saveHistory()
  
  // 输入时自动更新行号
  nextTick(() => {
    updateLineNumbersHeight()
  })
}

// 更新行号区域高度
function updateLineNumbersHeight() {
  if (!lineNumbersRef.value || !textareaRef.value) return
  
  const lineHeight = parseFloat(props.lineHeight)
  const fontSize = parseFloat(props.fontSize)
  const lineHeightPx = fontSize * lineHeight
  
  // 设置行号高度与文本区域一致
  lineNumbersRef.value.style.lineHeight = `${lineHeightPx}px`
}

// 暴露方法给父组件
defineExpose({
  focus: () => textareaRef.value?.focus(),
  getTextarea: () => textareaRef.value
})

onMounted(() => {
  currentHeight.value = props.height
  updateLineNumbersHeight()
})
</script>

<style scoped>
.code-editor {
  position: relative;
  width: 100%;
}

.editor-wrapper {
  display: flex;
  position: relative;
  overflow: hidden;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background: white;
}

/* 行号样式 */
.line-numbers {
  width: 50px;
  background-color: #fafafa;
  border-right: 1px solid #e6e6e6;
  padding: 10px 0;
  text-align: right;
  color: #999;
  font-size: 14px;
  overflow: hidden;
  user-select: none;
  flex-shrink: 0;
}

.line-number {
  padding: 0 8px;
  min-height: 21px;
  line-height: inherit;
  font-family: v-bind('fontFamily');
  font-size: v-bind('fontSize');
}

/* 文本编辑区域样式 */
.editor-textarea {
  flex: 1;
  padding: 10px;
  border: none;
  outline: none;
  resize: none;
  font-family: v-bind('fontFamily');
  font-size: v-bind('fontSize');
  line-height: v-bind('lineHeight');
  background: transparent;
  overflow-y: auto;
  overflow-x: auto;
  white-space: pre;
  word-wrap: normal;
}

/* 深色主题支持 */
:deep(.dark) .editor-wrapper {
  border-color: #4c4d4f;
  background-color: #1e1e1e;
}

:deep(.dark) .line-numbers {
  background-color: #252526;
  border-right-color: #3e3e42;
  color: #858585;
}

:deep(.dark) .editor-textarea {
  background-color: #1e1e1e;
  color: #d4d4d4;
}

/* 滚动条样式 */
.editor-textarea::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.editor-textarea::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.editor-textarea::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

.editor-textarea::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

:deep(.dark) .editor-textarea::-webkit-scrollbar-track {
  background: #252526;
}

:deep(.dark) .editor-textarea::-webkit-scrollbar-thumb {
  background: #4e4e4e;
}

:deep(.dark) .editor-textarea::-webkit-scrollbar-thumb:hover {
  background: #5e5e5e;
}

/* 拖拽调整大小手柄 */
.resize-handle {
  height: 8px;
  background-color: #f0f0f0;
  cursor: row-resize;
  position: relative;
  border-bottom-left-radius: 4px;
  border-bottom-right-radius: 4px;
  transition: background-color 0.2s;
}

.resize-handle:hover {
  background-color: #e0e0e0;
}

.resize-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #999;
  font-size: 12px;
  line-height: 1;
  letter-spacing: 2px;
  user-select: none;
}

:deep(.dark) .resize-handle {
  background-color: #2d2d2d;
}

:deep(.dark) .resize-handle:hover {
  background-color: #3a3a3a;
}

:deep(.dark) .resize-icon {
  color: #666;
}
</style>
