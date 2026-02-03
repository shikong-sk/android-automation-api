<template>
  <div class="input-page">
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h2 class="text-2xl font-bold text-gray-800">输入控制</h2>
        <p class="text-gray-500 mt-1">控制设备的输入操作</p>
      </div>
      <div class="flex gap-2">
        <el-button-group>
          <el-button :type="layoutMode === 'split' ? 'primary' : ''" @click="layoutMode = 'split'">
            分栏
          </el-button>
          <el-button :type="layoutMode === 'single' ? 'primary' : ''" @click="layoutMode = 'single'">
            单一
          </el-button>
        </el-button-group>
      </div>
    </div>
    
    <div class="flex gap-6" :class="{ 'flex-col': layoutMode === 'single' }">
      <!-- 左侧：输入操作控制面板 -->
      <div class="flex-1 min-w-0" :class="{ 'w-full': layoutMode === 'single', 'w-1/2': layoutMode === 'split' }">
        <!-- 输入操作卡片 -->
        <el-card shadow="hover" class="mb-6">
          <template #header>
            <div class="flex items-center gap-2">
              <el-icon><Pen /></el-icon>
              <span class="font-semibold">输入操作</span>
            </div>
          </template>
          
          <el-tabs v-model="activeTab" class="input-tabs">
            <el-tab-pane label="点击元素" name="click">
          <div class="space-y-4">
            <!-- 定位方式选择 -->
            <div class="mb-3">
              <el-radio-group v-model="clickLocateMode">
                <el-radio value="selector">选择器定位</el-radio>
                <el-radio value="coordinate">坐标定位</el-radio>
              </el-radio-group>
            </div>

            <!-- 选择器定位 -->
            <div v-if="clickLocateMode === 'selector'" class="space-y-4">
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

              <!-- 高级定位选项 -->
              <el-collapse v-model="clickAdvancedExpanded">
                <el-collapse-item title="高级定位（父级/兄弟/偏移）" name="advanced">
                  <div class="space-y-4">
                    <!-- 父级定位 -->
                    <div class="border rounded p-3 bg-gray-50">
                      <div class="text-sm font-medium text-gray-700 mb-2">父级元素定位</div>
                      <div class="flex gap-2">
                        <el-select v-model="clickParentType" placeholder="父级类型" class="w-28">
                          <el-option label="By ID" value="id" />
                          <el-option label="By Text" value="text" />
                          <el-option label="By XPath" value="xpath" />
                        </el-select>
                        <el-input
                          v-model="clickParentValue"
                          placeholder="父元素定位值"
                          clearable
                          class="flex-1"
                        >
                          <template #append v-if="clickParentType === 'xpath'">
                            <el-button @click="openXPathGenerator('clickParent')">
                              生成
                            </el-button>
                          </template>
                        </el-input>
                      </div>
                    </div>

                    <!-- 兄弟元素定位 -->
                    <div class="border rounded p-3 bg-gray-50">
                      <div class="text-sm font-medium text-gray-700 mb-2">兄弟元素定位</div>
                      <div class="flex gap-2 mb-2">
                        <el-select v-model="clickSiblingType" placeholder="兄弟类型" class="w-28">
                          <el-option label="By ID" value="id" />
                          <el-option label="By Text" value="text" />
                          <el-option label="By XPath" value="xpath" />
                        </el-select>
                        <el-input
                          v-model="clickSiblingValue"
                          placeholder="兄弟元素定位值"
                          clearable
                          class="flex-1"
                        >
                          <template #append v-if="clickSiblingType === 'xpath'">
                            <el-button @click="openXPathGenerator('clickSibling')">
                              生成
                            </el-button>
                          </template>
                        </el-input>
                      </div>
                      <el-radio-group v-model="clickSiblingRelation" size="small">
                        <el-radio value="following">之后的兄弟</el-radio>
                        <el-radio value="preceding">之前的兄弟</el-radio>
                      </el-radio-group>
                    </div>

                    <!-- 坐标偏移 -->
                    <div class="border rounded p-3 bg-gray-50">
                      <div class="text-sm font-medium text-gray-700 mb-2">坐标偏移</div>
                      <div class="flex gap-4">
                        <div>
                          <span class="text-xs text-gray-500">X 偏移:</span>
                          <el-input-number v-model="clickOffsetX" :min="-500" :max="500" size="small" class="ml-2 w-24" />
                        </div>
                        <div>
                          <span class="text-xs text-gray-500">Y 偏移:</span>
                          <el-input-number v-model="clickOffsetY" :min="-500" :max="500" size="small" class="ml-2 w-24" />
                        </div>
                      </div>
                      <div class="text-xs text-gray-400 mt-1">
                        正值向右/向下，负值向左/向上
                      </div>
                    </div>
                  </div>
                </el-collapse-item>
              </el-collapse>
            </div>

            <!-- 坐标定位 -->
            <div v-else class="flex gap-2">
              <el-input-number v-model="clickPointX" :min="0" placeholder="X 坐标" controls-position="right" class="w-36" />
              <el-input-number v-model="clickPointY" :min="0" placeholder="Y 坐标" controls-position="right" class="w-36" />
            </div>

            <!-- 操作按钮 -->
            <div class="flex gap-2">
              <el-button type="primary" :disabled="!isClickValid" @click="handleClick">
                点击元素
              </el-button>
              <el-button v-if="clickLocateMode === 'selector'" :disabled="!clickLocateValue" @click="handleExists">
                检查存在
              </el-button>
            </div>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="输入文本" name="text">
          <div class="space-y-4">
            <div class="flex gap-2">
              <el-select v-model="textLocateType" placeholder="查找方式" class="w-32">
                <el-option label="By ID" value="id" />
                <el-option label="By Text" value="text" />
                <el-option label="By Class" value="class" />
                <el-option label="By XPath" value="xpath" />
              </el-select>
              <el-input
                v-model="textLocateValue"
                :placeholder="getPlaceholder(textLocateType)"
                clearable
                class="flex-1"
              >
                <template #append v-if="textLocateType === 'xpath'">
                  <el-button @click="openXPathGenerator('text')">
                    生成
                  </el-button>
                </template>
              </el-input>
            </div>
            <el-input
              v-model="textInput"
              placeholder="要输入的文本内容"
              clearable
            />
            <div class="flex gap-2 flex-wrap">
              <el-button type="primary" :disabled="!textLocateValue || !textInput" @click="handleSetText">
                输入文本
              </el-button>
              <el-button :disabled="!textLocateValue" @click="handleClearText">
                清除文本
              </el-button>
              <el-button :disabled="!textLocateValue" @click="handleSendAction">
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
            <div class="flex gap-2">
              <el-select v-model="waitLocateType" placeholder="查找方式" class="w-32">
                <el-option label="By ID" value="id" />
                <el-option label="By Text" value="text" />
                <el-option label="By Class" value="class" />
                <el-option label="By XPath" value="xpath" />
              </el-select>
              <el-input
                v-model="waitLocateValue"
                :placeholder="getPlaceholder(waitLocateType)"
                clearable
                class="flex-1"
              >
                <template #append v-if="waitLocateType === 'xpath'">
                  <el-button @click="openXPathGenerator('wait')">
                    生成
                  </el-button>
                </template>
              </el-input>
            </div>
            <div>
              <p class="text-sm text-gray-500 mb-2">等待时间（秒）: {{ waitTimeout }}</p>
              <el-slider v-model="waitTimeout" :min="1" :max="30" :step="1" />
            </div>
            <div class="flex gap-2">
              <el-button type="primary" :disabled="!waitLocateValue" @click="handleWaitAppear">
                等待出现
              </el-button>
              <el-button :disabled="!waitLocateValue" @click="handleWaitGone">
                等待消失
              </el-button>
            </div>
          </div>
        </el-tab-pane>

        <el-tab-pane label="元素信息" name="info">
          <div class="space-y-4">
            <div class="flex gap-2">
              <el-select v-model="infoLocateType" placeholder="查找方式" class="w-32">
                <el-option label="By ID" value="id" />
                <el-option label="By Text" value="text" />
                <el-option label="By Class" value="class" />
                <el-option label="By XPath" value="xpath" />
              </el-select>
              <el-input
                v-model="infoLocateValue"
                :placeholder="getPlaceholder(infoLocateType)"
                clearable
                class="flex-1"
              >
                <template #append v-if="infoLocateType === 'xpath'">
                  <el-button @click="openXPathGenerator('info')">
                    生成
                  </el-button>
                </template>
              </el-input>
            </div>
            <div class="flex gap-2">
              <el-button type="primary" :disabled="!infoLocateValue" @click="handleGetText">
                获取文本
              </el-button>
              <el-button :disabled="!infoLocateValue" @click="handleGetBounds">
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

        <el-tab-pane label="人类模拟" name="human">
          <div class="space-y-4">
            <el-alert 
              title="人类模拟操作" 
              type="info" 
              :closable="false"
              description="模拟真实人类的点击和拖拽行为，包含随机偏移、延迟和自然的运动轨迹。"
              show-icon
              class="mb-4"
            />
            
            <!-- 操作类型选择 -->
            <el-radio-group v-model="humanActionType" class="mb-4">
              <el-radio-button value="click">点击</el-radio-button>
              <el-radio-button value="doubleClick">双击</el-radio-button>
              <el-radio-button value="longPress">长按</el-radio-button>
              <el-radio-button value="drag">拖拽</el-radio-button>
            </el-radio-group>

            <!-- 点击/双击/长按 共用的目标定位 -->
            <div v-if="humanActionType !== 'drag'" class="space-y-4">
              <div class="text-sm font-medium text-gray-700 mb-2">目标定位方式</div>
              <el-radio-group v-model="humanTargetMode" class="mb-3">
                <el-radio value="selector">选择器定位</el-radio>
                <el-radio value="coordinate">坐标定位</el-radio>
              </el-radio-group>

              <!-- 选择器定位 -->
              <div v-if="humanTargetMode === 'selector'" class="space-y-4">
                <div class="flex gap-2">
                  <el-select v-model="humanSelectorType" placeholder="选择器类型" class="w-32">
                    <el-option label="By ID" value="id" />
                    <el-option label="By Text" value="text" />
                    <el-option label="By Class" value="class" />
                    <el-option label="By XPath" value="xpath" />
                  </el-select>
                  <el-input
                    v-model="humanSelectorValue"
                    :placeholder="getPlaceholder(humanSelectorType)"
                    clearable
                    class="flex-1"
                  >
                    <template #append v-if="humanSelectorType === 'xpath'">
                      <el-button @click="openXPathGenerator('human')">
                        生成
                      </el-button>
                    </template>
                  </el-input>
                </div>

                <!-- 人类模拟高级定位 -->
                <el-collapse v-model="humanAdvancedLocExpanded">
                  <el-collapse-item title="高级定位（父级/兄弟/偏移）" name="advanced">
                    <div class="space-y-4">
                      <!-- 父级定位 -->
                      <div class="border rounded p-3 bg-gray-50">
                        <div class="text-sm font-medium text-gray-700 mb-2">父级元素定位</div>
                        <div class="flex gap-2">
                          <el-select v-model="humanParentType" placeholder="父级类型" class="w-28">
                            <el-option label="By ID" value="id" />
                            <el-option label="By Text" value="text" />
                            <el-option label="By XPath" value="xpath" />
                          </el-select>
                          <el-input
                            v-model="humanParentValue"
                            placeholder="父元素定位值"
                            clearable
                            class="flex-1"
                          >
                            <template #append v-if="humanParentType === 'xpath'">
                              <el-button @click="openXPathGenerator('humanParent')">
                                生成
                              </el-button>
                            </template>
                          </el-input>
                        </div>
                      </div>

                      <!-- 兄弟元素定位 -->
                      <div class="border rounded p-3 bg-gray-50">
                        <div class="text-sm font-medium text-gray-700 mb-2">兄弟元素定位</div>
                        <div class="flex gap-2 mb-2">
                          <el-select v-model="humanSiblingType" placeholder="兄弟类型" class="w-28">
                            <el-option label="By ID" value="id" />
                            <el-option label="By Text" value="text" />
                            <el-option label="By XPath" value="xpath" />
                          </el-select>
                          <el-input
                            v-model="humanSiblingValue"
                            placeholder="兄弟元素定位值"
                            clearable
                            class="flex-1"
                          >
                            <template #append v-if="humanSiblingType === 'xpath'">
                              <el-button @click="openXPathGenerator('humanSibling')">
                                生成
                              </el-button>
                            </template>
                          </el-input>
                        </div>
                        <el-radio-group v-model="humanSiblingRelation" size="small">
                          <el-radio value="following">之后的兄弟</el-radio>
                          <el-radio value="preceding">之前的兄弟</el-radio>
                        </el-radio-group>
                      </div>

                      <!-- 坐标偏移 -->
                      <div class="border rounded p-3 bg-gray-50">
                        <div class="text-sm font-medium text-gray-700 mb-2">坐标偏移</div>
                        <div class="flex gap-4">
                          <div>
                            <span class="text-xs text-gray-500">X 偏移:</span>
                            <el-input-number v-model="humanOffsetX" :min="-500" :max="500" size="small" class="ml-2 w-24" />
                          </div>
                          <div>
                            <span class="text-xs text-gray-500">Y 偏移:</span>
                            <el-input-number v-model="humanOffsetY" :min="-500" :max="500" size="small" class="ml-2 w-24" />
                          </div>
                        </div>
                      </div>
                    </div>
                  </el-collapse-item>
                </el-collapse>
              </div>

              <!-- 坐标定位 -->
              <div v-else class="flex gap-2">
                <el-input-number v-model="humanTargetX" :min="0" placeholder="X 坐标" controls-position="right" class="w-36" />
                <el-input-number v-model="humanTargetY" :min="0" placeholder="Y 坐标" controls-position="right" class="w-36" />
              </div>
            </div>

            <!-- 拖拽的起点和终点 -->
            <div v-else class="space-y-4">
              <!-- 起点 -->
              <div class="border rounded-lg p-4 bg-gray-50">
                <div class="text-sm font-medium text-gray-700 mb-3">起点定位</div>
                <el-radio-group v-model="humanDragStartMode" class="mb-3">
                  <el-radio value="selector">选择器定位</el-radio>
                  <el-radio value="coordinate">坐标定位</el-radio>
                </el-radio-group>

                <div v-if="humanDragStartMode === 'selector'" class="flex gap-2">
                  <el-select v-model="humanDragStartSelectorType" placeholder="选择器类型" class="w-32">
                    <el-option label="By ID" value="id" />
                    <el-option label="By Text" value="text" />
                    <el-option label="By Class" value="class" />
                    <el-option label="By XPath" value="xpath" />
                  </el-select>
                  <el-input
                    v-model="humanDragStartSelectorValue"
                    :placeholder="getPlaceholder(humanDragStartSelectorType)"
                    clearable
                    class="flex-1"
                  >
                    <template #append v-if="humanDragStartSelectorType === 'xpath'">
                      <el-button @click="openXPathGenerator('humanDragStart')">
                        生成
                      </el-button>
                    </template>
                  </el-input>
                </div>
                <div v-else class="flex gap-2">
                  <el-input-number v-model="humanDragStartX" :min="0" placeholder="X 坐标" controls-position="right" class="w-36" />
                  <el-input-number v-model="humanDragStartY" :min="0" placeholder="Y 坐标" controls-position="right" class="w-36" />
                </div>
              </div>

              <!-- 交换起点和终点按钮 -->
              <div class="flex justify-center my-2">
                <el-button 
                  type="primary" 
                  plain
                  circle
                  :disabled="!canSwapDragPoints"
                  @click="swapDragStartEnd"
                  title="交换起点和终点"
                >
                  ⇅
                </el-button>
              </div>

              <!-- 终点 -->
              <div class="border rounded-lg p-4 bg-gray-50">
                <div class="text-sm font-medium text-gray-700 mb-3">终点定位</div>
                <el-radio-group v-model="humanDragEndMode" class="mb-3">
                  <el-radio value="selector">选择器定位</el-radio>
                  <el-radio value="coordinate">坐标定位</el-radio>
                </el-radio-group>

                <div v-if="humanDragEndMode === 'selector'" class="flex gap-2">
                  <el-select v-model="humanDragEndSelectorType" placeholder="选择器类型" class="w-32">
                    <el-option label="By ID" value="id" />
                    <el-option label="By Text" value="text" />
                    <el-option label="By Class" value="class" />
                    <el-option label="By XPath" value="xpath" />
                  </el-select>
                  <el-input
                    v-model="humanDragEndSelectorValue"
                    :placeholder="getPlaceholder(humanDragEndSelectorType)"
                    clearable
                    class="flex-1"
                  >
                    <template #append v-if="humanDragEndSelectorType === 'xpath'">
                      <el-button @click="openXPathGenerator('humanDragEnd')">
                        生成
                      </el-button>
                    </template>
                  </el-input>
                </div>
                <div v-else class="flex gap-2">
                  <el-input-number v-model="humanDragEndX" :min="0" placeholder="X 坐标" controls-position="right" class="w-36" />
                  <el-input-number v-model="humanDragEndY" :min="0" placeholder="Y 坐标" controls-position="right" class="w-36" />
                </div>
              </div>

              <!-- 拖拽轨迹和速度配置 -->
              <div class="border rounded-lg p-4 bg-blue-50">
                <div class="text-sm font-medium text-gray-700 mb-3">轨迹和速度配置</div>
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <div class="text-xs text-gray-500 mb-1">轨迹类型</div>
                    <el-select v-model="humanDragTrajectory" class="w-full">
                      <el-option label="贝塞尔曲线（推荐）" value="bezier" />
                      <el-option label="直线 + 抖动" value="linear_jitter" />
                    </el-select>
                  </div>
                  <div>
                    <div class="text-xs text-gray-500 mb-1">速度模式</div>
                    <el-select v-model="humanDragSpeedMode" class="w-full">
                      <el-option label="加速-匀速-减速（推荐）" value="ease_in_out" />
                      <el-option label="仅加速" value="ease_in" />
                      <el-option label="仅减速" value="ease_out" />
                      <el-option label="匀速" value="linear" />
                      <el-option label="随机" value="random" />
                    </el-select>
                  </div>
                </div>
                <div class="mt-3">
                  <div class="text-xs text-gray-500 mb-1">拖拽时间: {{ humanDragDuration.toFixed(1) }} 秒</div>
                  <el-slider v-model="humanDragDuration" :min="0.2" :max="5.0" :step="0.1" />
 </div>
                <div class="mt-3">
                  <div class="text-xs text-gray-500 mb-1">轨迹采样点数量: {{ humanDragNumPoints }}</div>
                  <el-slider v-model="humanDragNumPoints" :min="10" :max="maxHumanDragNumPoints" :step="5" />
                </div>
              </div>
            </div>

            <!-- 高级配置（可折叠） -->
            <el-collapse v-model="humanAdvancedExpanded" class="mt-4">
              <el-collapse-item title="高级配置" name="advanced">
                <div class="grid grid-cols-2 gap-4">
                  <!-- 偏移范围 -->
                  <div>
                    <div class="text-xs text-gray-500 mb-1">随机偏移范围（像素）</div>
                    <div class="flex gap-2 items-center">
                      <el-input-number v-model="humanOffsetMin" :min="0" :max="50" size="small" class="w-20" />
                      <span class="text-gray-400">~</span>
                      <el-input-number v-model="humanOffsetMax" :min="0" :max="50" size="small" class="w-20" />
                    </div>
                  </div>
                  <!-- 延迟范围 -->
                  <div>
                    <div class="text-xs text-gray-500 mb-1">操作前延迟（秒）</div>
                    <div class="flex gap-2 items-center">
                      <el-input-number v-model="humanDelayMin" :min="0" :max="2" :step="0.05" :precision="2" size="small" class="w-20" />
                      <span class="text-gray-400">~</span>
                      <el-input-number v-model="humanDelayMax" :min="0" :max="2" :step="0.05" :precision="2" size="small" class="w-20" />
                    </div>
                  </div>
                  <!-- 按压时长（点击/双击） -->
                  <div v-if="humanActionType === 'click' || humanActionType === 'doubleClick'">
                    <div class="text-xs text-gray-500 mb-1">按压时长（秒）</div>
                    <div class="flex gap-2 items-center">
                      <el-input-number v-model="humanDurationMin" :min="0.01" :max="1" :step="0.01" :precision="2" size="small" class="w-20" />
                      <span class="text-gray-400">~</span>
                      <el-input-number v-model="humanDurationMax" :min="0.01" :max="1" :step="0.01" :precision="2" size="small" class="w-20" />
                    </div>
                  </div>
                  <!-- 长按时长 -->
                  <div v-if="humanActionType === 'longPress'">
                    <div class="text-xs text-gray-500 mb-1">长按时长（秒）</div>
                    <div class="flex gap-2 items-center">
                      <el-input-number v-model="humanLongPressDurationMin" :min="0.3" :max="5" :step="0.1" :precision="1" size="small" class="w-20" />
                      <span class="text-gray-400">~</span>
                      <el-input-number v-model="humanLongPressDurationMax" :min="0.3" :max="5" :step="0.1" :precision="1" size="small" class="w-20" />
                    </div>
                  </div>
                  <!-- 双击间隔 -->
                  <div v-if="humanActionType === 'doubleClick'">
                    <div class="text-xs text-gray-500 mb-1">双击间隔（秒）</div>
                    <div class="flex gap-2 items-center">
                      <el-input-number v-model="humanIntervalMin" :min="0.05" :max="0.5" :step="0.01" :precision="2" size="small" class="w-20" />
                      <span class="text-gray-400">~</span>
                      <el-input-number v-model="humanIntervalMax" :min="0.05" :max="0.5" :step="0.01" :precision="2" size="small" class="w-20" />
                    </div>
                  </div>
                  <!-- 抖动范围（拖拽） -->
                  <div v-if="humanActionType === 'drag' && humanDragTrajectory === 'linear_jitter'">
                    <div class="text-xs text-gray-500 mb-1">抖动范围（像素）</div>
                    <div class="flex gap-2 items-center">
                      <el-input-number v-model="humanJitterMin" :min="0" :max="20" size="small" class="w-20" />
                      <span class="text-gray-400">~</span>
                      <el-input-number v-model="humanJitterMax" :min="0" :max="20" size="small" class="w-20" />
                    </div>
                  </div>
                </div>
              </el-collapse-item>
            </el-collapse>

            <!-- 预览和执行按钮 -->
            <div class="flex gap-2 mt-4">
              <el-button 
                v-if="humanActionType === 'drag'"
                type="warning" 
                plain
                :disabled="!isHumanActionValid" 
                @click="previewHumanDrag"
              >
                <el-icon class="mr-1"><Eye /></el-icon>
                预览轨迹
              </el-button>
              <el-button 
                type="primary" 
                :disabled="!isHumanActionValid" 
                :loading="humanActionLoading"
                @click="handleHumanAction"
              >
                {{ humanActionButtonText }}
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

    <!-- DSL 脚本预览卡片 -->
    <el-card shadow="hover" v-if="currentDslScript">
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <el-icon><Terminal /></el-icon>
            <span class="font-semibold">DSL 脚本预览</span>
          </div>
          <el-button size="small" @click="copyDslScript">
            <el-icon class="mr-1"><Copy /></el-icon>
            复制
          </el-button>
        </div>
      </template>
      
      <div class="bg-gray-900 text-green-400 p-3 rounded text-sm font-mono">
        <pre class="whitespace-pre-wrap">{{ currentDslScript }}</pre>
      </div>
      <div class="mt-2 text-xs text-gray-400">
        提示：此脚本可直接用于自动化脚本编辑器中
      </div>
    </el-card>

    <!-- XPath 生成器弹窗 -->
    <XPathGenerator
      v-model="showXPathGenerator"
      @insert="handleXPathInsert"
    />
  </div>

  <!-- 右侧：屏幕预览（仅在分栏模式下显示） -->
  <div 
    v-if="layoutMode === 'split'" 
    class="w-1/2 min-w-[400px] sticky top-0 self-start max-h-screen overflow-y-auto"
  >
    <ScreenPreview
      ref="screenPreviewRef"
      :auto-refresh-interval="5000"
      @coordinate-click="handleCoordinateClick"
      @coordinate-update="handleCoordinateUpdate"
    />
  </div>
</div>
</div>

</template>

<script setup>
import { ref, computed, nextTick, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { inputApi } from '@/api'
import { Pen, Code, Search, ArrowUp, ArrowDown, Terminal, Copy, Eye } from '@vicons/fa'
import XPathGenerator from './XPathGenerator.vue'
import ScreenPreview from './ScreenPreview.vue'

const activeTab = ref('click')
const layoutMode = ref('split')
const screenPreviewRef = ref(null)
const clickLocateType = ref('id')
const clickLocateValue = ref('')
const clickLocateMode = ref('selector') // 'selector' 或 'coordinate'
const clickPointX = ref(null)
const clickPointY = ref(null)
const clickAdvancedExpanded = ref([])
const clickParentType = ref('id')
const clickParentValue = ref('')
const clickSiblingType = ref('text')
const clickSiblingValue = ref('')
const clickSiblingRelation = ref('following')
const clickOffsetX = ref(0)
const clickOffsetY = ref(0)
const textLocateType = ref('id')
const textLocateValue = ref('')
const textInput = ref('')
const textAction = ref('IME_ACTION_DONE')
const swipeDirection = ref('up')
const swipePercent = ref(0.5)
const locateValue = ref('')
const locateType = ref('id')
const locateResult = ref(null)
const waitLocateType = ref('id')
const waitLocateValue = ref('')
const waitTimeout = ref(10)
const infoLocateType = ref('id')
const infoLocateValue = ref('')
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
const xpathInsertTarget = ref('') // 'click', 'clickParent', 'clickSibling', 'locate', 'text', 'wait', 'info', 'human', 'humanDragStart', 'humanDragEnd'

// ============ 人类模拟操作相关状态 ============
const humanActionType = ref('click') // 'click', 'doubleClick', 'longPress', 'drag'
const humanTargetMode = ref('selector') // 'selector', 'coordinate'
const humanSelectorType = ref('id')
const humanSelectorValue = ref('')
const humanTargetX = ref(null)
const humanTargetY = ref(null)

// 拖拽相关
const humanDragStartMode = ref('coordinate')
const humanDragStartSelectorType = ref('id')
const humanDragStartSelectorValue = ref('')
const humanDragStartX = ref(null)
const humanDragStartY = ref(null)
const humanDragEndMode = ref('coordinate')
const humanDragEndSelectorType = ref('id')
const humanDragEndSelectorValue = ref('')
const humanDragEndX = ref(null)
const humanDragEndY = ref(null)
const humanDragTrajectory = ref('bezier')
const humanDragSpeedMode = ref('ease_in_out')
const humanDragNumPoints = ref(50)
const humanDragDuration = ref(1.0)
const isSettingDragEnd = ref(false) // 追踪当前是否应该设置终点

// 高级配置
const humanAdvancedExpanded = ref([])
const humanAdvancedLocExpanded = ref([])
const humanOffsetMin = ref(3)
const humanOffsetMax = ref(10)

// 人类模拟高级定位
const humanParentType = ref('id')
const humanParentValue = ref('')
const humanSiblingType = ref('text')
const humanSiblingValue = ref('')
const humanSiblingRelation = ref('following')
const humanOffsetX = ref(0)
const humanOffsetY = ref(0)
const humanDelayMin = ref(0.05)
const humanDelayMax = ref(0.3)
const humanDurationMin = ref(0.05)
const humanDurationMax = ref(0.15)
const humanLongPressDurationMin = ref(0.8)
const humanLongPressDurationMax = ref(1.5)
const humanIntervalMin = ref(0.1)
const humanIntervalMax = ref(0.2)
const humanJitterMin = ref(1)
const humanJitterMax = ref(5)
const humanActionLoading = ref(false)

// 人类模拟操作按钮文本
const humanActionButtonText = computed(() => {
  const texts = {
    click: '执行人类点击',
    doubleClick: '执行人类双击',
    longPress: '执行人类长按',
    drag: '执行人类拖拽'
  }
  return texts[humanActionType.value] || '执行'
})

// 动态计算轨迹采样点的最大数量（根据拖拽时间限制）
const maxHumanDragNumPoints = computed(() => {
  const maxPoints = Math.floor(humanDragDuration.value * 100)
  return Math.max(10, maxPoints)
})

// 验证人类模拟操作是否有效
const isHumanActionValid = computed(() => {
  if (humanActionType.value === 'drag') {
  // 拖拽需要验证起点和终点
  const startValid = humanDragStartMode.value === 'coordinate' 
      ? (humanDragStartX.value != null && humanDragStartY.value != null && 
         !isNaN(humanDragStartX.value) && !isNaN(humanDragStartY.value))
      : !!humanDragStartSelectorValue.value
    const endValid = humanDragEndMode.value === 'coordinate'
      ? (humanDragEndX.value != null && humanDragEndY.value != null &&
         !isNaN(humanDragEndX.value) && !isNaN(humanDragEndY.value))
      : !!humanDragEndSelectorValue.value
    return startValid && endValid
  } else {
    // 点击/双击/长按需要验证目标
    return humanTargetMode.value === 'coordinate'
      ? (humanTargetX.value != null && humanTargetY.value != null &&
         !isNaN(humanTargetX.value) && !isNaN(humanTargetY.value))
      : !!humanSelectorValue.value
  }
})

const canSwapDragPoints = computed(() => {
  const hasStart = humanDragStartMode.value === 'coordinate'
    ? (humanDragStartX.value != null && humanDragStartY.value != null)
    : !!humanDragStartSelectorValue.value
  const hasEnd = humanDragEndMode.value === 'coordinate'
    ? (humanDragEndX.value != null && humanDragEndY.value != null)
    : !!humanDragEndSelectorValue.value
  return hasStart && hasEnd
})

function swapDragStartEnd() {
  const tempX = humanDragStartX.value
  const tempY = humanDragStartY.value
  const tempMode = humanDragStartMode.value
  const tempSelectorType = humanDragStartSelectorType.value
  const tempSelectorValue = humanDragStartSelectorValue.value

  humanDragStartX.value = humanDragEndX.value
  humanDragStartY.value = humanDragEndY.value
  humanDragStartMode.value = humanDragEndMode.value
  humanDragStartSelectorType.value = humanDragEndSelectorType.value
  humanDragStartSelectorValue.value = humanDragEndSelectorValue.value

  humanDragEndX.value = tempX
  humanDragEndY.value = tempY
  humanDragEndMode.value = tempMode
  humanDragEndSelectorType.value = tempSelectorType
  humanDragEndSelectorValue.value = tempSelectorValue

  ElMessage.success('已交换起点和终点')

  if (screenPreviewRef.value && 
      humanDragStartX.value && 
      humanDragStartY.value &&
      humanDragEndX.value && 
      humanDragEndY.value) {
    screenPreviewRef.value.showDragPreview(
      humanDragStartX.value,
      humanDragStartY.value,
      humanDragEndX.value,
      humanDragEndY.value,
      {
        trajectoryType: humanDragTrajectory.value,
        duration: humanDragDuration.value * 1000,
        speedMode: humanDragSpeedMode.value,
        numPoints: humanDragNumPoints.value
      }
    )
  }
}

function previewHumanDrag() {
  if (!screenPreviewRef.value) {
    ElMessage.error('屏幕预览不可用')
    return
  }
  
  if (humanDragStartX.value && 
      humanDragStartY.value &&
      humanDragEndX.value && 
      humanDragEndY.value) {
    // 调试信息
    console.log('[previewHumanDrag] Calling showDragPreview with:', {
      startX: humanDragStartX.value,
      startY: humanDragStartY.value,
      endX: humanDragEndX.value,
      endY: humanDragEndY.value,
      options: {
        trajectoryType: humanDragTrajectory.value,
        duration: humanDragDuration.value * 1000,
        speedMode: humanDragSpeedMode.value,
        numPoints: humanDragNumPoints.value
      }
    })
    
    screenPreviewRef.value.showDragPreview(
      humanDragStartX.value,
      humanDragStartY.value,
      humanDragEndX.value,
      humanDragEndY.value,
      {
        trajectoryType: humanDragTrajectory.value,
        duration: humanDragDuration.value * 1000,
        speedMode: humanDragSpeedMode.value,
        numPoints: humanDragNumPoints.value
      }
    )
    ElMessage.success('正在预览拖拽轨迹...')
  } else {
    ElMessage.error('请先设置起点和终点坐标')
  }
}

function openXPathGenerator(target) {
  xpathInsertTarget.value = target
  showXPathGenerator.value = true
}

function handleXPathInsert(xpath) {
  switch (xpathInsertTarget.value) {
    case 'click':
      clickLocateValue.value = xpath
      clickLocateType.value = 'xpath'
      break
    case 'clickParent':
      clickParentValue.value = xpath
      clickParentType.value = 'xpath'
      break
    case 'clickSibling':
      clickSiblingValue.value = xpath
      clickSiblingType.value = 'xpath'
      break
    case 'locate':
      locateValue.value = xpath
      locateType.value = 'xpath'
      break
    case 'text':
      textLocateValue.value = xpath
      textLocateType.value = 'xpath'
      break
    case 'wait':
      waitLocateValue.value = xpath
      waitLocateType.value = 'xpath'
      break
    case 'info':
      infoLocateValue.value = xpath
      infoLocateType.value = 'xpath'
      break
    case 'human':
      humanSelectorValue.value = xpath
      humanSelectorType.value = 'xpath'
      break
    case 'humanParent':
      humanParentValue.value = xpath
      humanParentType.value = 'xpath'
      break
    case 'humanSibling':
      humanSiblingValue.value = xpath
      humanSiblingType.value = 'xpath'
      break
    case 'humanDragStart':
      humanDragStartSelectorValue.value = xpath
      humanDragStartSelectorType.value = 'xpath'
      break
    case 'humanDragEnd':
      humanDragEndSelectorValue.value = xpath
      humanDragEndSelectorType.value = 'xpath'
      break
  }
  ElMessage.success('XPath 已插入')
}

// 通用 placeholder 获取函数
function getPlaceholder(locateType) {
  const placeholders = {
    id: '输入元素的 resource-id（如 com.example:id/button）',
    text: '输入元素的文本内容（如 确定）',
    class: '输入元素的类名（如 android.widget.Button）',
    xpath: '输入 XPath 表达式（如 //android.widget.Button[@text="确定"]）'
  }
  return placeholders[locateType] || '输入定位值'
}

const clickPlaceholder = computed(() => {
  return getPlaceholder(clickLocateType.value)
})

// 验证点击操作是否有效
const isClickValid = computed(() => {
  if (clickLocateMode.value === 'coordinate') {
    return clickPointX.value != null && clickPointY.value != null &&
           !isNaN(clickPointX.value) && !isNaN(clickPointY.value)
  }
  return !!clickLocateValue.value
})

async function handleClick() {
  try {
    let response

    // 坐标定位模式
    if (clickLocateMode.value === 'coordinate') {
      response = await inputApi.clickByPoint(clickPointX.value, clickPointY.value)
    }
    // 选择器定位 + 高级选项
    else if (clickParentValue.value || clickSiblingValue.value || clickOffsetX.value !== 0 || clickOffsetY.value !== 0) {
      const options = {
        parent_selector_type: clickParentValue.value ? clickParentType.value : null,
        parent_selector_value: clickParentValue.value || null,
        sibling_selector_type: clickSiblingValue.value ? clickSiblingType.value : null,
        sibling_selector_value: clickSiblingValue.value || null,
        sibling_relation: clickSiblingRelation.value,
        offset_x: clickOffsetX.value,
        offset_y: clickOffsetY.value
      }
      response = await inputApi.getElementBoundsBySelector(clickLocateType.value, clickLocateValue.value, options)
      if (response.result?.exists && response.result?.center_x != null && response.result?.center_y != null) {
        const x = response.result.center_x
        const y = response.result.center_y
        response = await inputApi.clickByPoint(x, y)
      } else {
        ElMessage.warning('元素不存在，无法点击')
        return
      }
    }
    // 简单的选择器定位
    else {
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
    }

    if (response.success) {
      ElMessage.success('点击成功')
    } else {
      ElMessage.warning('点击失败')
    }
  } catch (err) {
    ElMessage.error('点击失败: ' + err.message)
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
    await inputApi.setTextBySelector(textLocateType.value, textLocateValue.value, textInput.value)
    ElMessage.success('文本输入成功')
  } catch (err) {
    ElMessage.error('输入文本失败')
  }
}

async function handleClearText() {
  try {
    await inputApi.clearTextBySelector(textLocateType.value, textLocateValue.value)
    ElMessage.success('清除文本成功')
  } catch (err) {
    ElMessage.error('清除文本失败')
  }
}

async function handleSendAction() {
  try {
    await inputApi.sendActionBySelector(textLocateType.value, textLocateValue.value)
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
    const result = await inputApi.waitAppearBySelector(waitLocateType.value, waitLocateValue.value, waitTimeout.value)
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
    const result = await inputApi.waitGoneBySelector(waitLocateType.value, waitLocateValue.value, waitTimeout.value)
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
    const result = await inputApi.getElementTextBySelector(infoLocateType.value, infoLocateValue.value)
    elementInfo.value = result.result || result
    ElMessage.success('获取文本成功')
  } catch (err) {
    ElMessage.error('获取文本失败')
    elementInfo.value = null
  }
}

async function handleGetBounds() {
  try {
    const result = await inputApi.getElementBoundsBySelector(infoLocateType.value, infoLocateValue.value)
    elementInfo.value = result.result || result
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

// ============ 人类模拟操作处理函数 ============

async function handleHumanAction() {
  humanActionLoading.value = true
  try {
    let response
    const actionType = humanActionType.value

    if (actionType === 'click') {
      response = await handleHumanClick()
    } else if (actionType === 'doubleClick') {
      response = await handleHumanDoubleClick()
    } else if (actionType === 'longPress') {
      response = await handleHumanLongPress()
    } else if (actionType === 'drag') {
      response = await handleHumanDrag()
    }

    if (response?.success) {
      ElMessage.success(response.message || '操作成功')
    } else {
      ElMessage.warning(response?.message || '操作失败，目标可能不存在')
    }
  } catch (err) {
    console.error('Human action error:', err)
    ElMessage.error('操作失败: ' + (err.response?.data?.detail || err.message))
  } finally {
    humanActionLoading.value = false
  }
}

async function handleHumanClick() {
  const options = {
    offset_min: humanOffsetMin.value,
    offset_max: humanOffsetMax.value,
    delay_min: humanDelayMin.value,
    delay_max: humanDelayMax.value,
    duration_min: humanDurationMin.value,
    duration_max: humanDurationMax.value
  }

  if (humanTargetMode.value === 'coordinate') {
    options.x = humanTargetX.value
    options.y = humanTargetY.value
  } else {
    options.selector_type = humanSelectorType.value
    options.selector_value = humanSelectorValue.value

    if (humanParentValue.value) {
      options.parent_selector_type = humanParentType.value
      options.parent_selector_value = humanParentValue.value
    }

    if (humanSiblingValue.value) {
      options.sibling_selector_type = humanSiblingType.value
      options.sibling_selector_value = humanSiblingValue.value
      options.sibling_relation = humanSiblingRelation.value
    }

    if (humanOffsetX.value !== 0 || humanOffsetY.value !== 0) {
      options.offset_x = humanOffsetX.value
      options.offset_y = humanOffsetY.value
    }
  }

  return await inputApi.humanClick(options)
}

async function handleHumanDoubleClick() {
  const options = {
    offset_min: humanOffsetMin.value,
    offset_max: humanOffsetMax.value,
    interval_min: humanIntervalMin.value,
    interval_max: humanIntervalMax.value,
    duration_min: humanDurationMin.value,
    duration_max: humanDurationMax.value
  }

  if (humanTargetMode.value === 'coordinate') {
    options.x = humanTargetX.value
    options.y = humanTargetY.value
  } else {
    options.selector_type = humanSelectorType.value
    options.selector_value = humanSelectorValue.value

    if (humanParentValue.value) {
      options.parent_selector_type = humanParentType.value
      options.parent_selector_value = humanParentValue.value
    }

    if (humanSiblingValue.value) {
      options.sibling_selector_type = humanSiblingType.value
      options.sibling_selector_value = humanSiblingValue.value
      options.sibling_relation = humanSiblingRelation.value
    }

    if (humanOffsetX.value !== 0 || humanOffsetY.value !== 0) {
      options.offset_x = humanOffsetX.value
      options.offset_y = humanOffsetY.value
    }
  }

  return await inputApi.humanDoubleClick(options)
}

async function handleHumanLongPress() {
  const options = {
    offset_min: humanOffsetMin.value,
    offset_max: humanOffsetMax.value,
    delay_min: humanDelayMin.value,
    delay_max: humanDelayMax.value,
    duration_min: humanLongPressDurationMin.value,
    duration_max: humanLongPressDurationMax.value
  }

  if (humanTargetMode.value === 'coordinate') {
    options.x = humanTargetX.value
    options.y = humanTargetY.value
  } else {
    options.selector_type = humanSelectorType.value
    options.selector_value = humanSelectorValue.value

    if (humanParentValue.value) {
      options.parent_selector_type = humanParentType.value
      options.parent_selector_value = humanParentValue.value
    }

    if (humanSiblingValue.value) {
      options.sibling_selector_type = humanSiblingType.value
      options.sibling_selector_value = humanSiblingValue.value
      options.sibling_relation = humanSiblingRelation.value
    }

    if (humanOffsetX.value !== 0 || humanOffsetY.value !== 0) {
      options.offset_x = humanOffsetX.value
      options.offset_y = humanOffsetY.value
    }
  }

  return await inputApi.humanLongPress(options)
}

async function handleHumanDrag() {
  const options = {
    trajectory_type: humanDragTrajectory.value,
    speed_mode: humanDragSpeedMode.value,
    duration: humanDragDuration.value,
    num_points: humanDragNumPoints.value,
    offset_min: humanOffsetMin.value,
    offset_max: humanOffsetMax.value,
    delay_min: humanDelayMin.value,
    delay_max: humanDelayMax.value,
    jitter_min: humanJitterMin.value,
    jitter_max: humanJitterMax.value
  }

  // 起点
  if (humanDragStartMode.value === 'coordinate') {
    if (humanDragStartX.value != null && humanDragStartY.value != null) {
      options.start_x = Number(humanDragStartX.value)
      options.start_y = Number(humanDragStartY.value)
    }
  } else {
    options.start_selector_type = humanDragStartSelectorType.value
    options.start_selector_value = humanDragStartSelectorValue.value
  }

  // 终点
  if (humanDragEndMode.value === 'coordinate') {
    if (humanDragEndX.value != null && humanDragEndY.value != null) {
      options.end_x = Number(humanDragEndX.value)
      options.end_y = Number(humanDragEndY.value)
    }
  } else {
    options.end_selector_type = humanDragEndSelectorType.value
    options.end_selector_value = humanDragEndSelectorValue.value
  }

  return await inputApi.humanDrag(options)
}

// ============ DSL 脚本生成 ============

// 格式化字符串值（添加引号）
function formatStringValue(value) {
  if (value === null || value === undefined || value === '') return null
  // 如果包含双引号，使用单引号包裹
  if (value.includes('"')) {
    return `'${value}'`
  }
  return `"${value}"`
}

// 生成选择器 DSL 片段
function generateSelectorDsl(selectorType, selectorValue) {
  if (!selectorValue) return null
  const typeMap = {
    'id': 'id',
    'text': 'text',
    'class': 'class',
    'xpath': 'xpath'
  }
  const dslType = typeMap[selectorType] || 'id'
  return `${dslType}:${formatStringValue(selectorValue)}`
}

// 生成高级选择器 DSL（包含父级/兄弟/偏移）
function generateAdvancedSelectorDsl(options) {
  const { selectorType, selectorValue, parentType, parentValue, siblingType, siblingValue, siblingRelation, offsetX, offsetY } = options

  if (!selectorValue) return null

  const parts = []
  const typeMap = {
    'id': 'id',
    'text': 'text',
    'class': 'class',
    'xpath': 'xpath'
  }

  const mainSelector = `${typeMap[selectorType] || 'id'}:${formatStringValue(selectorValue)}`
  parts.push(mainSelector)

  if (parentValue) {
    const parentSelector = `${typeMap[parentType] || 'id'}:${formatStringValue(parentValue)}`
    parts.push(`parent=${parentSelector}`)
  }

  if (siblingValue) {
    const siblingSelector = `${typeMap[siblingType] || 'text'}:${formatStringValue(siblingValue)}`
    if (siblingRelation !== 'following') {
      parts.push(`sibling=${siblingSelector} sibling_relation=${siblingRelation}`)
    } else {
      parts.push(`sibling=${siblingSelector}`)
    }
  }

  if (offsetX !== 0 || offsetY !== 0) {
    if (offsetX !== 0) parts.push(`offset_x=${offsetX}`)
    if (offsetY !== 0) parts.push(`offset_y=${offsetY}`)
  }

  return parts.join(' ')
}

// 点击元素 DSL
const clickDsl = computed(() => {
  if (!clickLocateValue.value) return ''
  const selector = generateAdvancedSelectorDsl({
    selectorType: clickLocateType.value,
    selectorValue: clickLocateValue.value,
    parentType: clickParentType.value,
    parentValue: clickParentValue.value,
    siblingType: clickSiblingType.value,
    siblingValue: clickSiblingValue.value,
    siblingRelation: clickSiblingRelation.value,
    offsetX: clickOffsetX.value,
    offsetY: clickOffsetY.value
  })
  if (!selector) return ''
  return `click ${selector}`
})

// 输入文本 DSL
const textDsl = computed(() => {
  if (!textLocateValue.value) return ''
  const selector = generateSelectorDsl(textLocateType.value, textLocateValue.value)
  if (!selector) return ''
  
  const lines = []
  if (textInput.value) {
    lines.push(`input ${selector} ${formatStringValue(textInput.value)}`)
  } else {
    lines.push(`# 输入文本到元素`)
    lines.push(`input ${selector} "要输入的文本"`)
  }
  return lines.join('\n')
})

// 滑动屏幕 DSL
const swipeDsl = computed(() => {
  return `swipe ${swipeDirection.value} ${swipePercent.value}`
})

// 元素定位 DSL（查找元素通常用于条件判断）
const locateDsl = computed(() => {
  if (!locateValue.value) return ''
  const selector = generateSelectorDsl(locateType.value, locateValue.value)
  if (!selector) return ''
  return `# 检查元素是否存在\nif exists ${selector}\n    # 元素存在时的操作\nend`
})

// 等待元素 DSL
const waitDsl = computed(() => {
  if (!waitLocateValue.value) return ''
  const selector = generateSelectorDsl(waitLocateType.value, waitLocateValue.value)
  if (!selector) return ''
  return `wait_element ${selector} ${waitTimeout.value}`
})

// 清除文本 DSL
const clearDsl = computed(() => {
  if (!textLocateValue.value) return ''
  const selector = generateSelectorDsl(textLocateType.value, textLocateValue.value)
  if (!selector) return ''
  return `clear ${selector}`
})

// 发送动作 DSL
const sendActionDsl = computed(() => {
  if (!textLocateValue.value) return ''
  const selector = generateSelectorDsl(textLocateType.value, textLocateValue.value)
  if (!selector) return ''
  const action = textAction.value || 'IME_ACTION_DONE'
  return `send_action ${selector} ${formatStringValue(action)}`
})

// 等待元素消失 DSL
const waitGoneDsl = computed(() => {
  if (!waitLocateValue.value) return ''
  const selector = generateSelectorDsl(waitLocateType.value, waitLocateValue.value)
  if (!selector) return ''
  return `wait_gone ${selector} ${waitTimeout.value}`
})

// 获取完整元素信息 DSL
const getInfoDsl = computed(() => {
  if (!infoLocateValue.value) return ''
  const selector = generateSelectorDsl(infoLocateType.value, infoLocateValue.value)
  if (!selector) return ''
  return `set $info = get_info ${selector}`
})

// 查找元素 DSL（返回单个元素）
const findElementDsl = computed(() => {
  if (!locateValue.value) return ''
  const selector = generateSelectorDsl(locateType.value, locateValue.value)
  if (!selector) return ''
  return `set $element = find_element ${selector}`
})

// 查找所有元素 DSL（返回元素列表）
const findElementsDsl = computed(() => {
  if (!locateValue.value) return ''
  const selector = generateSelectorDsl(locateType.value, locateValue.value)
  if (!selector) return ''
  return `set $elements = find_elements ${selector}`
})

// 导航命令 DSL
const navigationDsl = computed(() => {
  return `# 导航命令\nback     # 返回\nhome     # 返回桌面\nmenu     # 打开菜单\nrecent   # 最近任务`
})

// 应用管理 DSL
const appDsl = computed(() => {
  const lines = ['# 应用管理']
  lines.push(`start_app "com.example.app"    # 启动应用`)
  lines.push(`stop_app "com.example.app"     # 停止应用`)
  lines.push(`clear_app "com.example.app"    # 清除应用数据`)
  return lines.join('\n')
})

// 坐标点击 DSL
const coordinateDsl = computed(() => {
  if (clickLocateValue.value) {
    const coords = clickLocateValue.value.split(',')
    if (coords.length === 2) {
      const x = coords[0].trim()
      const y = coords[1].trim()
      if (!isNaN(x) && !isNaN(y)) {
        return `click ${x}, ${y}`
      }
    }
  }
  return ''
})

// 元素信息 DSL
const infoDsl = computed(() => {
  if (!infoLocateValue.value) return ''
  const selector = generateSelectorDsl(infoLocateType.value, infoLocateValue.value)
  if (!selector) return ''
  return `# 元素信息获取示例

# 获取元素文本
set $text = get_text ${selector}

# 获取元素完整信息（包含text、class、bounds等）
set $info = get_info ${selector}

# 查找单个元素（返回元素信息）
set $element = find_element ${selector}

# 查找所有匹配元素（返回元素列表）
set $elements = find_elements ${selector}

# 导出当前界面XML层次结构
set $xml = dump_hierarchy`
})

// 屏幕控制 DSL
const screenDsl = computed(() => {
  return `# 屏幕控制命令\nscreen_on    # 亮屏\nscreen_off   # 锁屏\nunlock       # 解锁`
})

// 人类模拟操作 DSL
const humanDsl = computed(() => {
  const actionType = humanActionType.value

  if (actionType === 'drag') {
    const parts = ['human_drag']

    if (humanDragStartMode.value === 'coordinate') {
      if (humanDragStartX.value != null && humanDragStartY.value != null) {
        parts.push(`${humanDragStartX.value},${humanDragStartY.value}`)
      } else {
        return ''
      }
    } else if (humanDragStartSelectorValue.value) {
      const selector = generateSelectorDsl(humanDragStartSelectorType.value, humanDragStartSelectorValue.value)
      parts.push(selector)
    } else {
      return ''
    }

    if (humanDragEndMode.value === 'coordinate') {
      if (humanDragEndX.value != null && humanDragEndY.value != null) {
        parts.push(`${humanDragEndX.value},${humanDragEndY.value}`)
      } else {
        return ''
      }
    } else if (humanDragEndSelectorValue.value) {
      const selector = generateSelectorDsl(humanDragEndSelectorType.value, humanDragEndSelectorValue.value)
      parts.push(selector)
    } else {
      return ''
    }

    const options = []
    if (humanDragTrajectory.value !== 'bezier') {
      options.push(`trajectory=${humanDragTrajectory.value}`)
    }
    if (humanDragSpeedMode.value !== 'ease_in_out') {
      options.push(`speed=${humanDragSpeedMode.value}`)
    }
    if (humanDragDuration.value !== 1.0) {
      options.push(`duration=${humanDragDuration.value}`)
    }
    if (humanDragNumPoints.value !== 50) {
      options.push(`num_points=${humanDragNumPoints.value}`)
    }
    if (humanOffsetMin.value !== 3 || humanOffsetMax.value !== 10) {
      options.push(`offset_min=${humanOffsetMin.value} offset_max=${humanOffsetMax.value}`)
    }
    if (humanJitterMin.value !== 1 || humanJitterMax.value !== 5) {
      options.push(`jitter_min=${humanJitterMin.value} jitter_max=${humanJitterMax.value}`)
    }

    if (options.length > 0) {
      parts.push(options.join(' '))
    }

    return parts.join(' ')
  } else {
    const commandMap = {
      'click': 'human_click',
      'doubleClick': 'human_double_click',
      'longPress': 'human_long_press'
    }
    const command = commandMap[actionType]

    const parts = [command]

    if (humanTargetMode.value === 'coordinate') {
      if (humanTargetX.value != null && humanTargetY.value != null) {
        parts.push(`${humanTargetX.value},${humanTargetY.value}`)
      } else {
        return ''
      }
    } else if (humanSelectorValue.value) {
      const selectorParts = []
      const typeMap = {
        'id': 'id',
        'text': 'text',
        'class': 'class',
        'xpath': 'xpath'
      }
      const mainSelector = `${typeMap[humanSelectorType.value] || 'id'}:${formatStringValue(humanSelectorValue.value)}`
      selectorParts.push(mainSelector)

      if (humanParentValue.value) {
        const parentSelector = `${typeMap[humanParentType.value] || 'id'}:${formatStringValue(humanParentValue.value)}`
        selectorParts.push(`parent=${parentSelector}`)
      }

      if (humanSiblingValue.value) {
        const siblingSelector = `${typeMap[humanSiblingType.value] || 'text'}:${formatStringValue(humanSiblingValue.value)}`
        if (humanSiblingRelation.value !== 'following') {
          selectorParts.push(`sibling=${siblingSelector} sibling_relation=${humanSiblingRelation.value}`)
        } else {
          selectorParts.push(`sibling=${siblingSelector}`)
        }
      }

      if (humanOffsetX.value !== 0 || humanOffsetY.value !== 0) {
        if (humanOffsetX.value !== 0) selectorParts.push(`offset_x=${humanOffsetX.value}`)
        if (humanOffsetY.value !== 0) selectorParts.push(`offset_y=${humanOffsetY.value}`)
      }

      parts.push(selectorParts.join(' '))
    } else {
      return ''
    }

    const options = []
    if (humanOffsetMin.value !== 3 || humanOffsetMax.value !== 10) {
      options.push(`offset_min=${humanOffsetMin.value} offset_max=${humanOffsetMax.value}`)
    }
    if (humanDelayMin.value !== 0.05 || humanDelayMax.value !== 0.3) {
      options.push(`delay_min=${humanDelayMin.value} delay_max=${humanDelayMax.value}`)
    }

    if (options.length > 0) {
      parts.push(options.join(' '))
    }

    return parts.join(' ')
  }
})

// 当前选项卡对应的 DSL 脚本
const currentDslScript = computed(() => {
  const dslMap = {
    'click': clickDsl.value,
    'text': textDsl.value,
    'clear': clearDsl.value,
    'sendAction': sendActionDsl.value,
    'swipe': swipeDsl.value,
    'locate': locateDsl.value,
    'wait': waitDsl.value,
    'waitGone': waitGoneDsl.value,
    'info': infoDsl.value,
    'getInfo': getInfoDsl.value,
    'findElement': findElementDsl.value,
    'findElements': findElementsDsl.value,
    'coordinate': coordinateDsl.value,
    'navigation': navigationDsl.value,
    'app': appDsl.value,
    'screen': screenDsl.value,
    'human': humanDsl.value
  }
  return dslMap[activeTab.value] || ''
})

// 复制 DSL 脚本
function copyDslScript() {
  if (!currentDslScript.value) return
  navigator.clipboard.writeText(currentDslScript.value)
  ElMessage.success('DSL 脚本已复制到剪贴板')
}

// ============ 屏幕预览事件处理 ============

function handleCoordinateClick(coordinate) {
  console.log('Coordinate clicked:', coordinate)

  if (activeTab.value === 'click') {
    if (clickLocateMode.value === 'coordinate') {
      clickPointX.value = coordinate.x
      clickPointY.value = coordinate.y
      ElMessage.success(`已将坐标 ${coordinate.x}, ${coordinate.y} 填入，点击元素执行点击`)
    } else {
      clickLocateValue.value = `${coordinate.x}, ${coordinate.y}`
      ElMessage.success(`已将坐标 ${coordinate.x}, ${coordinate.y} 填入`)
    }
  } else if (activeTab.value === 'human') {
    if (humanActionType.value === 'drag') {
      if (!isSettingDragEnd.value) {
        humanDragStartX.value = coordinate.x
        humanDragStartY.value = coordinate.y
        humanDragStartMode.value = 'coordinate'
        isSettingDragEnd.value = true
        ElMessage.success(`已将起点坐标设置为 ${coordinate.x}, ${coordinate.y}`)
        
        // 起点标记动画
        if (screenPreviewRef.value) {
          screenPreviewRef.value.addClickMarker(coordinate.x, coordinate.y, 'click')
        }
      } else {
        humanDragEndX.value = coordinate.x
        humanDragEndY.value = coordinate.y
        humanDragEndMode.value = 'coordinate'
        isSettingDragEnd.value = false
        ElMessage.success(`已将终点坐标设置为 ${coordinate.x}, ${coordinate.y}`)
        
        // 终点标记动画
        if (screenPreviewRef.value) {
          screenPreviewRef.value.addClickMarker(coordinate.x, coordinate.y, 'long-press')
        }
        
        // 触发拖拽预览动画
        if (screenPreviewRef.value && 
            humanDragStartX.value && 
            humanDragStartY.value &&
            humanDragEndX.value && 
            humanDragEndY.value) {
          
          screenPreviewRef.value.showDragPreview(
            humanDragStartX.value,
            humanDragStartY.value,
            humanDragEndX.value,
            humanDragEndY.value,
            {
              trajectoryType: humanDragTrajectory.value,
              duration: humanDragDuration.value * 1000,
              speedMode: humanDragSpeedMode.value,
              numPoints: humanDragNumPoints.value
            }
          )
        }
      }
    } else {
      humanTargetX.value = coordinate.x
      humanTargetY.value = coordinate.y
      humanTargetMode.value = 'coordinate'
      ElMessage.success(`已将目标坐标设置为 ${coordinate.x}, ${coordinate.y}`)
      
      // 点击标记动画
      if (screenPreviewRef.value) {
        screenPreviewRef.value.addClickMarker(coordinate.x, coordinate.y, 'click')
      }
    }
  }
}

function handleCoordinateUpdate(coordinate) {
  console.log('Coordinate updated:', coordinate)
}

// 监听拖拽模式，自动切换到坐标模式
watch(humanDragStartMode, (newVal) => {
  if (newVal === 'coordinate') {
    humanDragStartSelectorValue.value = ''
  }
})

watch(humanDragEndMode, (newVal) => {
  if (newVal === 'coordinate') {
    humanDragEndSelectorValue.value = ''
  }
})

// 监听拖拽时间变化，动态调整采样点数量限制
watch(maxHumanDragNumPoints, (newMax) => {
  if (humanDragNumPoints.value > newMax) {
    humanDragNumPoints.value = newMax
    ElMessage.warning(`拖拽时间过短，采样点数量已自动调整为最大值 ${newMax}`)
  }
})

// 监听人类操作类型变化，重置拖拽坐标设置状态
watch(humanActionType, (newVal) => {
  if (newVal === 'drag') {
    isSettingDragEnd.value = false
  }
})

// 监听拖拽坐标变化，自动重置设置状态
watch([humanDragStartX, humanDragStartY, humanDragEndX, humanDragEndY], () => {
  if (!humanDragStartX.value && !humanDragStartY.value && !humanDragEndX.value && !humanDragEndY.value) {
    isSettingDragEnd.value = false
  }
})

watch(humanTargetMode, (newVal) => {
  if (newVal === 'coordinate') {
    humanSelectorValue.value = ''
  }
})

// 监听点击定位模式切换
watch(clickLocateMode, (newVal) => {
  if (newVal === 'coordinate') {
    clickLocateValue.value = ''
  } else {
    clickPointX.value = null
    clickPointY.value = null
  }
})
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
