<template>
  <el-dialog
    v-model="visible"
    title="XPath 快捷生成器"
    width="900px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <div class="xpath-generator">
      <!-- 顶部刷新按钮 -->
      <div class="flex justify-between items-center mb-4">
        <span class="text-sm text-gray-500">从当前界面生成 XPath 表达式</span>
        <el-button type="primary" size="small" @click="refreshHierarchy" :loading="loading">
          刷新界面结构
        </el-button>
      </div>

      <!-- Tab 切换 -->
      <el-tabs v-model="activeTab" class="generator-tabs">
        <!-- 快捷模板 Tab -->
        <el-tab-pane label="快捷模板" name="template">
          <div class="space-y-4">
            <p class="text-sm text-gray-500">选择常用模板，快速生成 XPath 表达式</p>
            <div class="grid grid-cols-2 gap-3">
              <div
                v-for="template in templates"
                :key="template.name"
                class="template-card p-3 border rounded-lg cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition-all"
                :class="{ 'border-blue-500 bg-blue-50': selectedTemplate === template.name }"
                @click="selectTemplate(template)"
              >
                <div class="font-medium text-sm mb-1">{{ template.name }}</div>
                <div class="text-xs text-gray-500 mb-2">{{ template.description }}</div>
                <code class="text-xs bg-gray-100 px-2 py-1 rounded block overflow-hidden text-ellipsis">
                  {{ template.pattern }}
                </code>
              </div>
            </div>
            
            <!-- 模板参数填充 -->
            <div v-if="selectedTemplate" class="mt-4 p-4 bg-gray-50 rounded-lg">
              <div class="font-medium mb-3">填充参数</div>
              <div class="space-y-3">
                <div v-for="param in currentTemplateParams" :key="param.key" class="flex items-center gap-3">
                  <span class="w-32 text-sm">{{ param.label }}:</span>
                  <el-input
                    v-model="templateValues[param.key]"
                    :placeholder="param.placeholder"
                    size="small"
                    class="flex-1"
                    @input="generateFromTemplate"
                  />
                </div>
              </div>
            </div>
          </div>
        </el-tab-pane>

        <!-- 属性组合 Tab -->
        <el-tab-pane label="属性组合" name="combine">
          <div class="space-y-4">
            <p class="text-sm text-gray-500">选择元素属性，自动组合生成 XPath</p>
            
            <!-- 元素类型 -->
            <div class="flex items-center gap-3">
              <span class="w-28 text-sm">元素类型:</span>
              <el-select v-model="combineForm.elementType" placeholder="选择或输入" filterable allow-create class="flex-1" @change="generateFromCombine">
                <el-option label="任意元素 (*)" value="*" />
                <el-option label="android.widget.Button" value="android.widget.Button" />
                <el-option label="android.widget.TextView" value="android.widget.TextView" />
                <el-option label="android.widget.EditText" value="android.widget.EditText" />
                <el-option label="android.widget.ImageView" value="android.widget.ImageView" />
                <el-option label="android.widget.ImageButton" value="android.widget.ImageButton" />
                <el-option label="android.widget.CheckBox" value="android.widget.CheckBox" />
                <el-option label="android.widget.RadioButton" value="android.widget.RadioButton" />
                <el-option label="android.widget.Switch" value="android.widget.Switch" />
                <el-option label="android.widget.LinearLayout" value="android.widget.LinearLayout" />
                <el-option label="android.widget.RelativeLayout" value="android.widget.RelativeLayout" />
                <el-option label="android.widget.FrameLayout" value="android.widget.FrameLayout" />
                <el-option label="android.widget.ScrollView" value="android.widget.ScrollView" />
                <el-option label="android.widget.ListView" value="android.widget.ListView" />
                <el-option label="android.widget.RecyclerView" value="androidx.recyclerview.widget.RecyclerView" />
                <el-option label="android.view.View" value="android.view.View" />
                <el-option label="android.view.ViewGroup" value="android.view.ViewGroup" />
              </el-select>
            </div>

            <!-- 属性条件列表 -->
            <div class="border rounded-lg p-3">
              <div class="flex justify-between items-center mb-3">
                <span class="font-medium text-sm">属性条件</span>
                <el-button type="primary" size="small" text @click="addCondition">
                  + 添加条件
                </el-button>
              </div>
              
              <div v-for="(condition, index) in combineForm.conditions" :key="index" class="flex items-center gap-2 mb-2">
                <el-select v-model="condition.logic" size="small" class="w-20" v-if="index > 0" @change="generateFromCombine">
                  <el-option label="AND" value="and" />
                  <el-option label="OR" value="or" />
                </el-select>
                <span v-else class="w-20"></span>
                
                <el-select v-model="condition.attr" placeholder="属性" size="small" class="w-36" @change="generateFromCombine">
                  <el-option label="resource-id" value="resource-id" />
                  <el-option label="text" value="text" />
                  <el-option label="content-desc" value="content-desc" />
                  <el-option label="class" value="class" />
                  <el-option label="package" value="package" />
                  <el-option label="checkable" value="checkable" />
                  <el-option label="checked" value="checked" />
                  <el-option label="clickable" value="clickable" />
                  <el-option label="enabled" value="enabled" />
                  <el-option label="focusable" value="focusable" />
                  <el-option label="focused" value="focused" />
                  <el-option label="scrollable" value="scrollable" />
                  <el-option label="selected" value="selected" />
                </el-select>
                
                <el-select v-model="condition.operator" size="small" class="w-28" @change="generateFromCombine">
                  <el-option label="等于" value="=" />
                  <el-option label="包含" value="contains" />
                  <el-option label="开头是" value="starts-with" />
                  <el-option label="结尾是" value="ends-with" />
                </el-select>
                
                <el-input
                  v-model="condition.value"
                  placeholder="属性值"
                  size="small"
                  class="flex-1"
                  @input="generateFromCombine"
                />
                
                <el-button type="danger" size="small" text @click="removeCondition(index)" :disabled="combineForm.conditions.length <= 1">
                  删除
                </el-button>
              </div>
            </div>

            <!-- 索引选择 -->
            <div class="flex items-center gap-3">
              <el-checkbox v-model="combineForm.useIndex" @change="generateFromCombine">指定索引</el-checkbox>
              <el-input-number
                v-if="combineForm.useIndex"
                v-model="combineForm.index"
                :min="1"
                size="small"
                @change="generateFromCombine"
              />
              <span v-if="combineForm.useIndex" class="text-xs text-gray-500">(从 1 开始)</span>
            </div>
          </div>
        </el-tab-pane>

        <!-- XML 树选择 Tab -->
        <el-tab-pane label="XML 树选择" name="tree">
          <div class="space-y-4">
            <p class="text-sm text-gray-500">点击元素节点，自动生成 XPath</p>
            
            <div v-if="!hierarchyXml" class="text-center py-8 text-gray-400">
              请先点击"刷新界面结构"获取当前界面 XML
            </div>
            
            <div v-else class="border rounded-lg overflow-hidden">
              <!-- 搜索框 -->
              <div class="p-2 bg-gray-50 border-b">
                <el-input
                  v-model="treeSearchKeyword"
                  placeholder="搜索节点..."
                  size="small"
                  clearable
                >
                  <template #prefix>
                    <el-icon><Search /></el-icon>
                  </template>
                </el-input>
              </div>
              
              <!-- 树形结构 -->
              <div class="tree-container p-2 overflow-auto" style="max-height: 350px;">
                <el-tree
                  ref="treeRef"
                  :data="treeData"
                  :props="treeProps"
                  :filter-node-method="filterTreeNode"
                  node-key="id"
                  highlight-current
                  :expand-on-click-node="false"
                  @node-click="handleTreeNodeClick"
                >
                  <template #default="{ node, data }">
                    <div class="tree-node-content flex items-center gap-2 py-1">
                      <span class="text-blue-600 font-mono text-xs">{{ data.tagName }}</span>
                      <span v-if="data.resourceId" class="text-green-600 text-xs truncate max-w-48" :title="data.resourceId">
                        #{{ getShortId(data.resourceId) }}
                      </span>
                      <span v-if="data.text" class="text-orange-600 text-xs truncate max-w-32" :title="data.text">
                        "{{ truncateText(data.text, 20) }}"
                      </span>
                      <span v-if="data.contentDesc" class="text-purple-600 text-xs truncate max-w-32" :title="data.contentDesc">
                        [{{ truncateText(data.contentDesc, 15) }}]
                      </span>
                    </div>
                  </template>
                </el-tree>
              </div>
            </div>

            <!-- 选中节点信息 -->
            <div v-if="selectedTreeNode" class="p-3 bg-blue-50 rounded-lg">
              <div class="font-medium text-sm mb-2">选中节点属性</div>
              <div class="grid grid-cols-2 gap-2 text-xs">
                <div><span class="text-gray-500">class:</span> {{ selectedTreeNode.tagName }}</div>
                <div v-if="selectedTreeNode.resourceId"><span class="text-gray-500">resource-id:</span> {{ selectedTreeNode.resourceId }}</div>
                <div v-if="selectedTreeNode.text"><span class="text-gray-500">text:</span> {{ selectedTreeNode.text }}</div>
                <div v-if="selectedTreeNode.contentDesc"><span class="text-gray-500">content-desc:</span> {{ selectedTreeNode.contentDesc }}</div>
                <div v-if="selectedTreeNode.bounds"><span class="text-gray-500">bounds:</span> {{ selectedTreeNode.bounds }}</div>
              </div>
              
              <!-- XPath 生成策略选择 -->
              <div class="mt-3">
                <span class="text-sm text-gray-600 mr-2">生成策略:</span>
                <el-radio-group v-model="xpathStrategy" size="small" @change="generateFromTreeNode">
                  <el-radio-button value="auto">智能推荐</el-radio-button>
                  <el-radio-button value="id">优先 ID</el-radio-button>
                  <el-radio-button value="text">优先文本</el-radio-button>
                  <el-radio-button value="full">完整路径</el-radio-button>
                </el-radio-group>
              </div>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>

      <!-- 生成结果区域 -->
      <div class="mt-4 p-4 bg-gray-900 rounded-lg">
        <div class="flex justify-between items-center mb-2">
          <span class="text-gray-400 text-sm">生成的 XPath:</span>
          <div class="flex gap-2">
            <el-button size="small" @click="testXPath" :loading="testing" :disabled="!generatedXPath">
              测试
            </el-button>
            <el-button size="small" @click="copyXPath" :disabled="!generatedXPath">
              复制
            </el-button>
          </div>
        </div>
        <div class="bg-gray-800 p-3 rounded font-mono text-sm text-green-400 min-h-12 break-all">
          {{ generatedXPath || '// 请选择模板或填写属性条件' }}
        </div>
        
        <!-- 测试结果 -->
        <div v-if="testResult !== null" class="mt-3 p-2 rounded text-sm" :class="testResult.success ? 'bg-green-900 text-green-300' : 'bg-red-900 text-red-300'">
          <span v-if="testResult.success">
            找到 {{ testResult.count || 1 }} 个匹配元素
            <span v-if="testResult.element" class="ml-2 text-xs">
              ({{ testResult.element.class_name }}<span v-if="testResult.element.text">, text="{{ testResult.element.text }}"</span>)
            </span>
          </span>
          <span v-else>未找到匹配元素</span>
        </div>
      </div>
    </div>

    <template #footer>
      <div class="flex justify-between">
        <el-button @click="handleClose">取消</el-button>
        <div class="flex gap-2">
          <el-button type="primary" @click="handleInsert" :disabled="!generatedXPath">
            插入到输入框
          </el-button>
        </div>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { Search } from '@vicons/fa'
import { inputApi } from '@/api'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'insert'])

const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

// 状态
const activeTab = ref('template')
const loading = ref(false)
const testing = ref(false)
const hierarchyXml = ref('')
const generatedXPath = ref('')
const testResult = ref(null)

// 模板相关
const selectedTemplate = ref('')
const templateValues = ref({})
const templates = [
  {
    name: '按 resource-id 定位',
    description: '通过元素的 resource-id 属性精确定位',
    pattern: '//*[@resource-id="___"]',
    params: [{ key: 'resourceId', label: 'resource-id', placeholder: '如: com.example:id/button' }]
  },
  {
    name: '按文本精确匹配',
    description: '通过元素的 text 属性精确匹配',
    pattern: '//*[@text="___"]',
    params: [{ key: 'text', label: '文本内容', placeholder: '如: 确定' }]
  },
  {
    name: '按文本包含匹配',
    description: '匹配包含指定文本的元素',
    pattern: '//*[contains(@text, "___")]',
    params: [{ key: 'text', label: '包含文本', placeholder: '如: 登录' }]
  },
  {
    name: '按 content-desc 定位',
    description: '通过元素的无障碍描述定位',
    pattern: '//*[@content-desc="___"]',
    params: [{ key: 'desc', label: 'content-desc', placeholder: '如: 返回按钮' }]
  },
  {
    name: '按类型+文本组合',
    description: '指定元素类型和文本内容',
    pattern: '//___[@text="___"]',
    params: [
      { key: 'class', label: '元素类型', placeholder: '如: android.widget.Button' },
      { key: 'text', label: '文本内容', placeholder: '如: 确定' }
    ]
  },
  {
    name: '按类型+ID组合',
    description: '指定元素类型和 resource-id',
    pattern: '//___[@resource-id="___"]',
    params: [
      { key: 'class', label: '元素类型', placeholder: '如: android.widget.Button' },
      { key: 'resourceId', label: 'resource-id', placeholder: '如: com.example:id/btn' }
    ]
  },
  {
    name: '父子关系定位',
    description: '通过父元素定位子元素',
    pattern: '//*[@resource-id="___"]/___',
    params: [
      { key: 'parentId', label: '父元素 ID', placeholder: '如: com.example:id/container' },
      { key: 'childClass', label: '子元素类型', placeholder: '如: android.widget.TextView' }
    ]
  },
  {
    name: '索引定位',
    description: '定位同类元素中的第 N 个',
    pattern: '(//___)[___]',
    params: [
      { key: 'class', label: '元素类型', placeholder: '如: android.widget.Button' },
      { key: 'index', label: '索引(从1开始)', placeholder: '如: 1' }
    ]
  }
]

const currentTemplateParams = computed(() => {
  const template = templates.find(t => t.name === selectedTemplate.value)
  return template?.params || []
})

// 属性组合相关
const combineForm = ref({
  elementType: '*',
  conditions: [
    { logic: 'and', attr: 'resource-id', operator: '=', value: '' }
  ],
  useIndex: false,
  index: 1
})

// XML 树相关
const treeRef = ref(null)
const treeSearchKeyword = ref('')
const treeData = ref([])
const selectedTreeNode = ref(null)
const xpathStrategy = ref('auto')
const treeProps = {
  children: 'children',
  label: 'label'
}

// 监听搜索关键词
watch(treeSearchKeyword, (val) => {
  treeRef.value?.filter(val)
})

// 方法
function handleClose() {
  visible.value = false
  resetState()
}

function resetState() {
  selectedTemplate.value = ''
  templateValues.value = {}
  testResult.value = null
}

async function refreshHierarchy() {
  loading.value = true
  try {
    const result = await inputApi.getHierarchy()
    hierarchyXml.value = result.xml || ''
    parseXmlToTree()
    ElMessage.success('界面结构已刷新')
  } catch (err) {
    ElMessage.error('获取界面结构失败')
  } finally {
    loading.value = false
  }
}

function parseXmlToTree() {
  if (!hierarchyXml.value) {
    treeData.value = []
    return
  }
  
  try {
    const parser = new DOMParser()
    const xmlDoc = parser.parseFromString(hierarchyXml.value, 'text/xml')
    const root = xmlDoc.documentElement
    
    let nodeId = 0
    function parseNode(node, path = '') {
      if (node.nodeType !== 1) return null
      
      const tagName = node.tagName || node.nodeName
      const resourceId = node.getAttribute('resource-id') || ''
      const text = node.getAttribute('text') || ''
      const contentDesc = node.getAttribute('content-desc') || ''
      const bounds = node.getAttribute('bounds') || ''
      const className = node.getAttribute('class') || tagName
      
      const currentPath = path ? `${path}/${className}` : `/${className}`
      const id = nodeId++
      
      const treeNode = {
        id,
        tagName: className,
        resourceId,
        text,
        contentDesc,
        bounds,
        path: currentPath,
        label: className,
        attributes: {},
        children: []
      }
      
      // 收集所有属性
      for (let i = 0; i < node.attributes.length; i++) {
        const attr = node.attributes[i]
        treeNode.attributes[attr.name] = attr.value
      }
      
      // 递归处理子节点
      for (let i = 0; i < node.childNodes.length; i++) {
        const childNode = parseNode(node.childNodes[i], currentPath)
        if (childNode) {
          treeNode.children.push(childNode)
        }
      }
      
      return treeNode
    }
    
    const rootNode = parseNode(root)
    treeData.value = rootNode ? [rootNode] : []
  } catch (err) {
    console.error('解析 XML 失败:', err)
    treeData.value = []
  }
}

function filterTreeNode(value, data) {
  if (!value) return true
  const searchLower = value.toLowerCase()
  return (
    data.tagName?.toLowerCase().includes(searchLower) ||
    data.resourceId?.toLowerCase().includes(searchLower) ||
    data.text?.toLowerCase().includes(searchLower) ||
    data.contentDesc?.toLowerCase().includes(searchLower)
  )
}

function handleTreeNodeClick(data) {
  selectedTreeNode.value = data
  generateFromTreeNode()
}

function generateFromTreeNode() {
  if (!selectedTreeNode.value) return
  
  const node = selectedTreeNode.value
  let xpath = ''
  
  switch (xpathStrategy.value) {
    case 'id':
      if (node.resourceId) {
        xpath = `//*[@resource-id="${node.resourceId}"]`
      } else if (node.text) {
        xpath = `//*[@text="${node.text}"]`
      } else {
        xpath = `//${node.tagName}`
      }
      break
      
    case 'text':
      if (node.text) {
        xpath = `//*[@text="${node.text}"]`
      } else if (node.contentDesc) {
        xpath = `//*[@content-desc="${node.contentDesc}"]`
      } else if (node.resourceId) {
        xpath = `//*[@resource-id="${node.resourceId}"]`
      } else {
        xpath = `//${node.tagName}`
      }
      break
      
    case 'full':
      xpath = node.path || `//${node.tagName}`
      break
      
    case 'auto':
    default:
      // 智能推荐：优先使用唯一性最高的属性
      if (node.resourceId && node.resourceId.includes(':id/')) {
        xpath = `//*[@resource-id="${node.resourceId}"]`
      } else if (node.text && node.text.length <= 20) {
        xpath = `//${node.tagName}[@text="${node.text}"]`
      } else if (node.contentDesc) {
        xpath = `//*[@content-desc="${node.contentDesc}"]`
      } else if (node.resourceId) {
        xpath = `//*[@resource-id="${node.resourceId}"]`
      } else if (node.text) {
        xpath = `//*[contains(@text, "${node.text.substring(0, 10)}")]`
      } else {
        xpath = `//${node.tagName}`
      }
      break
  }
  
  generatedXPath.value = xpath
  testResult.value = null
}

function selectTemplate(template) {
  selectedTemplate.value = template.name
  templateValues.value = {}
  template.params.forEach(p => {
    templateValues.value[p.key] = ''
  })
  generateFromTemplate()
}

function generateFromTemplate() {
  const template = templates.find(t => t.name === selectedTemplate.value)
  if (!template) {
    generatedXPath.value = ''
    return
  }
  
  let xpath = template.pattern
  template.params.forEach(param => {
    const value = templateValues.value[param.key] || '___'
    xpath = xpath.replace('___', value)
  })
  
  generatedXPath.value = xpath
  testResult.value = null
}

function addCondition() {
  combineForm.value.conditions.push({
    logic: 'and',
    attr: 'text',
    operator: '=',
    value: ''
  })
}

function removeCondition(index) {
  combineForm.value.conditions.splice(index, 1)
  generateFromCombine()
}

function generateFromCombine() {
  const form = combineForm.value
  const elementType = form.elementType || '*'
  
  const validConditions = form.conditions.filter(c => c.value)
  
  if (validConditions.length === 0) {
    generatedXPath.value = `//${elementType}`
    if (form.useIndex) {
      generatedXPath.value = `(${generatedXPath.value})[${form.index}]`
    }
    testResult.value = null
    return
  }
  
  let conditionStr = ''
  validConditions.forEach((condition, index) => {
    let part = ''
    
    switch (condition.operator) {
      case '=':
        part = `@${condition.attr}="${condition.value}"`
        break
      case 'contains':
        part = `contains(@${condition.attr}, "${condition.value}")`
        break
      case 'starts-with':
        part = `starts-with(@${condition.attr}, "${condition.value}")`
        break
      case 'ends-with':
        // XPath 1.0 不直接支持 ends-with，使用变通方法
        part = `substring(@${condition.attr}, string-length(@${condition.attr}) - string-length("${condition.value}") + 1) = "${condition.value}"`
        break
    }
    
    if (index === 0) {
      conditionStr = part
    } else {
      const logic = condition.logic === 'or' ? ' or ' : ' and '
      conditionStr += logic + part
    }
  })
  
  let xpath = `//${elementType}[${conditionStr}]`
  
  if (form.useIndex) {
    xpath = `(${xpath})[${form.index}]`
  }
  
  generatedXPath.value = xpath
  testResult.value = null
}

async function testXPath() {
  if (!generatedXPath.value) return
  
  testing.value = true
  testResult.value = null
  
  try {
    const result = await inputApi.findByXpath(generatedXPath.value)
    if (result && result.exists) {
      testResult.value = {
        success: true,
        count: 1,
        element: result
      }
    } else {
      testResult.value = { success: false }
    }
  } catch (err) {
    testResult.value = { success: false }
  } finally {
    testing.value = false
  }
}

function copyXPath() {
  if (!generatedXPath.value) return
  navigator.clipboard.writeText(generatedXPath.value)
  ElMessage.success('已复制到剪贴板')
}

function handleInsert() {
  if (!generatedXPath.value) return
  emit('insert', generatedXPath.value)
  handleClose()
}

function getShortId(resourceId) {
  if (!resourceId) return ''
  const parts = resourceId.split('/')
  return parts[parts.length - 1]
}

function truncateText(text, maxLen) {
  if (!text) return ''
  return text.length > maxLen ? text.substring(0, maxLen) + '...' : text
}

// 初始化时自动获取界面结构
watch(visible, (val) => {
  if (val && !hierarchyXml.value) {
    refreshHierarchy()
  }
})
</script>

<style scoped>
.xpath-generator {
  min-height: 400px;
}

.generator-tabs :deep(.el-tabs__content) {
  padding: 16px 0;
}

.template-card {
  transition: all 0.2s ease;
}

.template-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.tree-container :deep(.el-tree-node__content) {
  height: auto;
  padding: 4px 0;
}

.tree-node-content {
  font-size: 12px;
}

.tree-container :deep(.el-tree-node.is-current > .el-tree-node__content) {
  background-color: #e6f7ff;
}
</style>
