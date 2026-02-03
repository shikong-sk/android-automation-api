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
        <CodeEditor
          v-model="scriptContent"
          placeholder="在此输入脚本内容..."
          :height="400"
          font-family="monospace"
          font-size="14px"
          tab-size="2"
          show-line-numbers
          class="editor-area"
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

        <!-- 基础命令详解 -->
        <div class="space-y-6">
          <!-- 点击命令 -->
          <div class="border rounded-lg p-4">
            <h4 class="font-semibold mb-3 text-lg">1. 点击命令 (click)</h4>
            <p class="text-gray-600 text-sm mb-3">点击屏幕上的元素或坐标位置</p>
            
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <div>
                <h5 class="font-medium mb-2 text-sm">按选择器点击</h5>
                <pre class="bg-gray-100 p-3 rounded text-xs"># 通过 resource-id 点击（推荐）
click id:"com.example:id/submit_button"
click id:"login_button"
click id:"android:id/button1"

# 通过 text 点击
click text:"确定"
click text:"提交"
click text:"取消"
click text:"确认"

# 通过 XPath 点击
click xpath:"//android.widget.Button[@text='确定']"
click xpath:"//*[@resource-id='com.example:id/submit']"
click xpath:"//android.widget.LinearLayout[@clickable='true']//Button"

# 通过 class 点击
click class:"android.widget.Button"
click class:"android.widget.ImageView"
click class:"android.widget.TextView"</pre>
              </div>
              <div>
                <h5 class="font-medium mb-2 text-sm">按坐标点击</h5>
                <pre class="bg-gray-100 p-3 rounded text-xs"># 点击屏幕中央（假设在 1080x1920 屏幕上）
click 540, 960

# 点击左上角
click 0, 0

# 点击右下角
click 1080, 1920

# 点击特定位置（比如应用的图标位置）
click 300, 800
click 500, 1200
click 720, 1500

# 坐标格式：x, y
# x: 横坐标（从左到右 0 开始）
# y: 纵坐标（从上到下 0 开始）</pre>
              </div>
            </div>
          </div>

          <!-- 输入命令 -->
          <div class="border rounded-lg p-4">
            <h4 class="font-semibold mb-3 text-lg">2. 输入命令 (input)</h4>
            <p class="text-gray-600 text-sm mb-3">向输入框输入文本内容</p>
            
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <div>
                <h5 class="font-medium mb-2 text-sm">选择器 + 文本</h5>
                <pre class="bg-gray-100 p-3 rounded text-xs"># 通过 id 输入
input id:"username" "test@example.com"
input id:"password" "password123"
input id:"search_input" "搜索关键词"
input id:"phone" "13800138000"
input id:"email" "user@domain.com"

# 通过 text 输入
input text:"请输入用户名" "admin"
input text:"搜索" "搜索内容"

# 通过 XPath 输入
input xpath:"//EditText[@resource-id='com.example:id/input']" "文本内容"

# 通过 class 输入
input class:"android.widget.EditText" "默认文本"</pre>
              </div>
              <div>
                <h5 class="font-medium mb-2 text-sm">使用变量输入</h5>
                <pre class="bg-gray-100 p-3 rounded text-xs"># 使用变量插值
set $username = "admin"
set $password = "123456"
input id:"username" "${username}"
input id:"password" "${password}"

# 组合使用
set $prefix = "user_"
set $suffix = "@example.com"
set $username = "${prefix}test${suffix}"
input id:"email" "${username}"

# 清空后输入（配合 clear）
clear id:"search_input"
input id:"search_input" "新的搜索词"</pre>
              </div>
            </div>
          </div>

          <!-- 清除命令 -->
          <div class="border rounded-lg p-4">
            <h4 class="font-semibold mb-3 text-lg">3. 清除命令 (clear)</h4>
            <p class="text-gray-600 text-sm mb-3">清除输入框中的文本内容</p>
            
            <pre class="bg-gray-100 p-3 rounded text-xs"># 通过 id 清除
clear id:"username"
clear id:"password"
clear id:"search_input"
clear id:"comment"

# 通过 text 清除
clear text:"搜索"
clear text:"请输入"

# 通过 XPath 清除
clear xpath:"//EditText[@resource-id='com.example:id/input']"

# 通过 class 清除
clear class:"android.widget.EditText"

# 使用场景：登录前清空输入框
clear id:"username"
clear id:"password"
input id:"username" "admin"
input id:"password" "pass123"</pre>
          </div>

          <!-- 滑动命令 -->
          <div class="border rounded-lg p-4">
            <h4 class="font-semibold mb-3 text-lg">4. 滑动命令 (swipe)</h4>
            <p class="text-gray-600 text-sm mb-3">在屏幕上执行滑动操作</p>
            
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <div>
                <h5 class="font-medium mb-2 text-sm">方向滑动</h5>
                <pre class="bg-gray-100 p-3 rounded text-xs"># 向上滑动（从下往上）
swipe up
swipe up 0.3    # 滑动 30% 屏幕高度
swipe up 0.5    # 滑动 50%（默认）
swipe up 0.8    # 滑动 80% 屏幕高度

# 向下滑动（从上往下）
swipe down
swipe down 0.5
swipe down 0.7

# 向左滑动（从右往左）
swipe left
swipe left 0.5
swipe left 0.8

# 向右滑动（从左往右）
swipe right
swipe right 0.5
swipe right 0.8

# 百分比范围：0.1 - 1.0
# 0.1 = 10% 屏幕距离
# 1.0 = 100% 屏幕距离</pre>
              </div>
              <div>
                <h5 class="font-medium mb-2 text-sm">坐标滑动</h5>
                <pre class="bg-gray-100 p-3 rounded text-xs"># 从起点滑动到终点
# swipe start_x, start_y, end_x, end_y

# 从 (100, 1000) 滑动到 (100, 300)
swipe 100, 1000, 100, 300

# 从屏幕底部滑动到顶部
swipe 540, 1800, 540, 200

# 从左往右滑动
swipe 200, 960, 880, 960

# 从右往左滑动
swipe 880, 960, 200, 960

# 斜向滑动
swipe 200, 1500, 880, 300

# 带持续时间的滑动（毫秒）
swipe 100, 1000, 100, 300, 500</pre>
              </div>
            </div>
          </div>

          <!-- 等待命令 -->
          <div class="border rounded-lg p-4">
            <h4 class="font-semibold mb-3 text-lg">5. 等待命令 (wait)</h4>
            <p class="text-gray-600 text-sm mb-3">等待指定时间或等待元素状态变化</p>
            
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <div>
                <h5 class="font-medium mb-2 text-sm">固定时间等待</h5>
                <pre class="bg-gray-100 p-3 rounded text-xs"># 等待指定秒数
wait 1           # 等待 1 秒
wait 2           # 等待 2 秒
wait 0.5         # 等待 0.5 秒（500毫秒）
wait 0.1         # 等待 0.1 秒（100毫秒）
wait 10          # 等待 10 秒

# 常用等待场景
wait 0.3         # 短等待（动画过渡）
wait 0.5         # 中等等待
wait 1           # 标准等待
wait 2           # 较长等待
wait 3           # 长等待（应用启动）</pre>
              </div>
              <div>
                <h5 class="font-medium mb-2 text-sm">等待元素出现/消失</h5>
                <pre class="bg-gray-100 p-3 rounded text-xs"># 等待元素出现（最多 N 秒）
wait_element id:"loading" 10
wait_element id:"submit_button" 30
wait_element text:"确定" 15
wait_element xpath:"//Button[@text='提交']" 20

# 等待元素消失（最多 N 秒）
wait_gone id:"loading" 10
wait_gone text:"加载中" 15
wait_gone class:"android.widget.ProgressBar" 20

# 组合使用：等待加载完成再操作
wait_element id:"loading" 5
# ... 执行操作 ...
wait_gone id:"loading" 10

# 超时自动继续（不报错）
wait_element id:"optional_element" 3
if exists id:"optional_element"
    log "元素出现"
else
    log "元素未出现，继续执行"
end</pre>
              </div>
            </div>
          </div>

          <!-- 导航命令 -->
          <div class="border rounded-lg p-4">
            <h4 class="font-semibold mb-3 text-lg">6. 导航命令 (navigation)</h4>
            <p class="text-gray-600 text-sm mb-3">系统导航操作</p>
            
            <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
              <div>
                <h5 class="font-medium mb-2 text-sm">返回键</h5>
                <pre class="bg-gray-100 p-3 rounded text-xs"># 返回上一页
back

# 返回多个层级
back
back
back</pre>
              </div>
              <div>
                <h5 class="font-medium mb-2 text-sm">主页键</h5>
                <pre class="bg-gray-100 p-3 rounded text-xs"># 返回桌面
home

# 返回桌面后等待
home
wait 1</pre>
              </div>
              <div>
                <h5 class="font-medium mb-2 text-sm">菜单键</h5>
                <pre class="bg-gray-100 p-3 rounded text-xs"># 打开菜单
menu

# 等待菜单加载
menu
wait 0.5</pre>
              </div>
              <div>
                <h5 class="font-medium mb-2 text-sm">最近应用</h5>
                <pre class="bg-gray-100 p-3 rounded text-xs"># 打开最近应用
recent

# 切换应用场景
recent
wait 1
# 点击切换到目标应用</pre>
              </div>
            </div>
          </div>

          <!-- 应用管理命令 -->
          <div class="border rounded-lg p-4">
            <h4 class="font-semibold mb-3 text-lg">7. 应用管理命令 (app)</h4>
            <p class="text-gray-600 text-sm mb-3">应用的启动、停止和清除</p>
            
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
              <div>
                <h5 class="font-medium mb-2 text-sm">启动应用</h5>
                <pre class="bg-gray-100 p-3 rounded text-xs"># 通过包名启动
start_app "com.example.app"
start_app "com.android.settings"
start_app "com.tencent.mm"

# 启动并等待
start_app "com.example.app"
wait 3

# 启动带 Activity
start_app "com.example.app/.MainActivity"
start_app "com.example.app/com.example.MainActivity"</pre>
              </div>
              <div>
                <h5 class="font-medium mb-2 text-sm">停止应用</h5>
                <pre class="bg-gray-100 p-3 rounded text-xs"># 强制停止应用
stop_app "com.example.app"
stop_app "com.android.settings"

# 停止后清理
stop_app "com.example.app"
wait 1
clear_app "com.example.app"</pre>
              </div>
              <div>
                <h5 class="font-medium mb-2 text-sm">清除应用数据</h5>
                <pre class="bg-gray-100 p-3 rounded text-xs"># 清除应用数据（重置应用）
clear_app "com.example.app"

# 清除后重新启动
clear_app "com.example.app"
wait 1
start_app "com.example.app"
wait 3</pre>
              </div>
            </div>
          </div>

          <!-- 屏幕控制命令 -->
          <div class="border rounded-lg p-4">
            <h4 class="font-semibold mb-3 text-lg">8. 屏幕控制命令</h4>
            <p class="text-gray-600 text-sm mb-3">控制设备屏幕的开关和锁定状态</p>
            
            <pre class="bg-gray-100 p-3 rounded text-xs"># 亮屏（唤醒设备）
screen_on

# 锁屏（关闭屏幕）
screen_off

# 解锁屏幕
unlock

# 完整流程：亮屏并解锁
screen_on
wait 0.5
unlock

# 锁屏流程
swipe up 0.3
screen_off

# 检查屏幕状态后操作
if exists id:"lock_screen"
    unlock
else
    log "屏幕已解锁"
end</pre>
          </div>

          <!-- 变量与插值 -->
          <div class="border rounded-lg p-4">
            <h4 class="font-semibold mb-3 text-lg">9. 变量与插值</h4>
            <p class="text-gray-600 text-sm mb-3">变量赋值、获取和插值使用</p>
            
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <div>
                <h5 class="font-medium mb-2 text-sm">变量赋值</h5>
                <pre class="bg-gray-100 p-3 rounded text-xs"># 字符串变量
set $name = "World"
set $app = "com.example.app"
set $message = "操作成功"

# 数字变量
set $count = 10
set $timeout = 30
set $delay = 0.5

# 获取元素文本
set $title = get_text id:"android:id/title"
set $button_text = get_text text:"确定"

# 检查元素是否存在
set $has_loading = exists id:"loading"
set $is_visible = exists text:"确认"

# 获取元素信息
set $info = get_info id:"button"
set $bounds = get_info id:"element"

# 获取元素是否存在
set $element = find_element id:"button"</pre>
              </div>
              <div>
                <h5 class="font-medium mb-2 text-sm">变量插值</h5>
                <pre class="bg-gray-100 p-3 rounded text-xs"># 基础插值
set $name = "World"
log "Hello ${name}"              # Hello World

# 多变量插值
set $x = 10
set $y = 20
log "x=${x}, y=${y}"             # x=10, y=20

# 选择器值插值
set $button_id = "com.example:id/submit"
click id:"${button_id}"

# 命令参数插值
set $username = "test"
set $password = "123456"
input id:"username" "${username}"
input id:"password" "${password}"

# 组合使用
set $app = "com.android.settings"
set $element = "search"
start_app "${app}"
click id:"com.android.settings:id/${element}"

# 重要：必须使用 ${variable} 格式
# ❌ 错误：log "Hello $name"（不会解析）
# ✅ 正确：log "Hello ${name}"</pre>
              </div>
            </div>
          </div>

          <!-- 条件判断 -->
          <div class="border rounded-lg p-4">
            <h4 class="font-semibold mb-3 text-lg">10. 条件判断</h4>
            <p class="text-gray-600 text-sm mb-3">基于元素存在性进行条件判断</p>
            
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <div>
                <h5 class="font-medium mb-2 text-sm">元素存在判断</h5>
                <pre class="bg-gray-100 p-3 rounded text-xs"># 元素存在时执行
if exists id:"submit_button"
    click id:"submit_button"
    log "已点击提交按钮"
end

# 元素不存在时执行
if not exists id:"loading"
    log "加载已完成，继续操作"
end

# 存在则点击，不存在则等待
if exists id:"next_button"
    click id:"next_button"
else
    wait 1
end

# 多个条件判断
if exists id:"confirm"
    click id:"confirm"
elif exists id:"cancel"
    click id:"cancel"
else
    log "未找到操作按钮"
end</pre>
              </div>
              <div>
                <h5 class="font-medium mb-2 text-sm">完整条件结构</h5>
                <pre class="bg-gray-100 p-3 rounded text-xs"># if - elif - else - end 结构
if exists id:"button_primary"
    click id:"button_primary"
    log "点击主要按钮"
elif exists id:"button_secondary"
    click id:"button_secondary"
    log "点击次要按钮"
else
    log "未找到按钮，使用默认操作"
end

# 嵌套条件
if exists id:"login_form"
    if exists id:"username"
        if exists id:"password"
            log "登录表单完整"
        else
            log "缺少密码输入框"
        end
    else
        log "缺少用户名输入框"
    end
else
    log "未找到登录表单"
end

# 配合循环的条件
loop 5
    if exists id:"success"
        log "操作成功"
        break
    end
    wait 1
end</pre>
              </div>
            </div>
          </div>

          <!-- 循环控制 -->
          <div class="border rounded-lg p-4">
            <h4 class="font-semibold mb-3 text-lg">11. 循环控制</h4>
            <p class="text-gray-600 text-sm mb-3">固定次数循环和条件循环</p>
            
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <div>
                <h5 class="font-medium mb-2 text-sm">固定次数循环</h5>
                <pre class="bg-gray-100 p-3 rounded text-xs"># 循环 N 次
loop 3
    click id:"next"
    wait 0.5
end

# 循环读取列表
loop 10
    # 执行操作
    wait 1
end

# 循环配合变量
set $max_pages = 5
loop $max_pages
    log "处理页面"
    swipe up 0.5
    wait 1
end

# 循环内跳出
loop 20
    if exists id:"done"
        break     # 跳出循环
    end
    click id:"next"
    wait 1
end

# 循环内跳过
loop 10
    if exists id:"skip"
        continue  # 跳过后续，进入下一次
    end
    click id:"process"
    wait 1
end</pre>
              </div>
              <div>
                <h5 class="font-medium mb-2 text-sm">条件循环</h5>
                <pre class="bg-gray-100 p-3 rounded text-xs"># 使用 loop 配合 exists 进行条件循环

# 等待元素消失（最多 15 秒）
loop 30
    if not exists id:"loading"
        log "加载完成"
        break
    end
    wait 0.5
end

# 等待元素出现（最多 30 秒）
loop 60
    if exists id:"content"
        log "内容已加载"
        break
    end
    wait 0.5
end

# 循环执行直到条件满足
loop 10
    if exists id:"success"
        log "操作成功"
        break
    end
    click id:"retry"
    wait 1
end</pre>
              </div>
            </div>
          </div>

          <!-- 错误处理 -->
          <div class="border rounded-lg p-4">
            <h4 class="font-semibold mb-3 text-lg">12. 错误处理</h4>
            <p class="text-gray-600 text-sm mb-3">try-catch 异常捕获和处理</p>
            
            <pre class="bg-gray-100 p-3 rounded text-xs"># 基础错误处理
try
    click id:"maybe_not_exist"
    wait 1
catch
    log "元素不存在，跳过操作"
end

# 错误后重试
loop 3
    try
        click id:"submit"
        log "点击成功"
        break     # 成功后跳出循环
    catch
        log "点击失败，重试"
        wait 1
    end
end

# 多个可能出错的操作
try
    click id:"button1"
    wait_element id:"result" 5
    set $result = get_text id:"result"
catch
    log "操作失败，执行备用方案"
    click id:"backup_button"
end

# 嵌套错误处理
try
    start_app "com.example.app"
    wait 2
    
    try
        click id:"login"
    catch
        log "登录按钮点击失败，尝试备用方式"
        click text:"登录"
    end
catch
    log "应用启动失败"
    start_app "com.example.app"
end</pre>
          </div>

          <!-- 元素信息获取 -->
          <div class="border rounded-lg p-4">
            <h4 class="font-semibold mb-3 text-lg">13. 元素信息获取</h4>
            <p class="text-gray-600 text-sm mb-3">获取元素的文本、信息和层次结构</p>
            
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <div>
                <h5 class="font-medium mb-2 text-sm">获取文本和信息</h5>
                <pre class="bg-gray-100 p-3 rounded text-xs"># 获取元素文本
set $title = get_text id:"android:id/title"
set $button_text = get_text text:"确定"
set $content = get_text xpath:"//TextView[@resource-id='content']"

# 获取元素完整信息
set $info = get_info id:"button"
# info 包含: exists, text, class_name, resource_id, bounds, enabled 等

# 检查元素是否存在
if exists id:"loading"
    log "元素存在"
else
    log "元素不存在"
end

# 查找单个元素
set $element = find_element id:"button"
if $element
    log "找到元素"
end

# 查找所有匹配元素
set $elements = find_elements class:"android.widget.Button"</pre>
              </div>
              <div>
                <h5 class="font-medium mb-2 text-sm">导出界面结构</h5>
                <pre class="bg-gray-100 p-3 rounded text-xs"># 导出当前界面 XML 结构
set $xml = dump_hierarchy
log "界面结构已导出"

# 保存到文件（通过 shell）
shell "echo '${xml}' > /sdcard/hierarchy.xml"

# 调试时导出
try
    click id:"button"
    wait 1
    set $xml = dump_hierarchy
    log "操作后界面结构"
catch
    log "出错时导出结构"
    set $xml = dump_hierarchy
    shell "echo '${xml}' > /sdcard/error.xml"
end</pre>
              </div>
            </div>
          </div>

          <!-- 其他命令 -->
          <div class="border rounded-lg p-4">
            <h4 class="font-semibold mb-3 text-lg">14. 其他命令</h4>
            <p class="text-gray-600 text-sm mb-3">日志、Shell、子脚本调用</p>
            
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
              <div>
                <h5 class="font-medium mb-2 text-sm">日志输出</h5>
                <pre class="bg-gray-100 p-3 rounded text-xs"># 输出日志
log "操作完成"
log "开始执行"
log "错误信息"

# 输出变量
log $variable
log ${name}
log "变量值: ${value}"

# 输出多行
log "=== 脚本开始 ==="
log "步骤1: 启动应用"
log "步骤2: 等待加载"
log "=== 脚本结束 ==="</pre>
              </div>
              <div>
                <h5 class="font-medium mb-2 text-sm">Shell 命令</h5>
                <pre class="bg-gray-100 p-3 rounded text-xs"># 执行 Shell 命令
shell "ls /sdcard"
shell "pm list packages"
shell "screencap -p /sdcard/screenshot.png"

# 获取命令输出
set $packages = shell "pm list packages | grep com.example"
log $packages

# 截图
shell "screencap -p /sdcard/debug.png"

# 获取设备信息
set $info = shell "dumpsys deviceinfo"
set $memory = shell "dumpsys meminfo com.example.app"</pre>
              </div>
              <div>
                <h5 class="font-medium mb-2 text-sm">子脚本调用</h5>
                <pre class="bg-gray-100 p-3 rounded text-xs"># 调用同目录下的子脚本
call "login.script"
call "navigate.script"
call "common_actions.script"

# 子脚本示例 (common_actions.script)
# =================================
# log "执行通用操作"
# wait_element id:"ready" 10
# click id:"confirm"

# 传递参数（通过变量）
set $target_page = "settings"
call "navigate.script"

# 在 navigate.script 中使用 ${target_page}
# click id:"${target_page}"</pre>
              </div>
            </div>
          </div>
        </div>

        <!-- 人类模拟操作 -->
        <div class="mt-4 bg-purple-50 p-4 rounded border border-purple-200">
          <h4 class="font-semibold mb-3 text-lg text-purple-800">15. 人类模拟操作</h4>
          <p class="text-xs text-purple-700 mb-3">模拟真实人类的点击和拖拽行为，包含随机偏移、延迟和自然的运动轨迹，可用于反检测场景。</p>
          
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <div>
              <h5 class="font-medium mb-2 text-sm">人类点击/双击/长按</h5>
              <pre class="bg-purple-100 p-3 rounded text-xs"># 通过选择器点击
human_click id:"button_id"
human_click text:"确定"
human_click xpath:"//Button[@text='提交']"

# 通过坐标点击
human_click 500, 800
human_click 300, 1200

# 自定义参数
human_click 500, 800, offset_min=5, offset_max=15
human_click 500, 800, delay_min=0.1, delay_max=0.5

# 人类双击
human_double_click id:"item"
human_double_click 500, 800
human_double_click 500, 800, interval_min=0.1, interval_max=0.3

# 人类长按
human_long_press id:"item"
human_long_press 500, 800
human_long_press 500, 800, duration_min=1.0, duration_max=2.0</pre>
              
              <h5 class="font-medium mt-3 mb-2 text-sm">参数说明</h5>
              <table class="w-full text-xs bg-purple-100 rounded">
                <tbody>
                  <tr><td class="p-1">offset_min/max</td><td class="p-1">随机偏移范围（像素），默认 3/10</td></tr>
                  <tr><td class="p-1">delay_min/max</td><td class="p-1">操作前延迟范围（秒），默认 0.05/0.3</td></tr>
                  <tr><td class="p-1">duration_min/max</td><td class="p-1">按压时长范围（秒），默认 0.05/0.15</td></tr>
                  <tr><td class="p-1">interval_min/max</td><td class="p-1">双击间隔范围（秒），默认 0.1/0.2</td></tr>
                </tbody>
              </table>
            </div>
            <div>
              <h5 class="font-medium mb-2 text-sm">人类拖拽</h5>
              <pre class="bg-purple-100 p-3 rounded text-xs"># 坐标拖拽
human_drag 100, 1500, 100, 500
human_drag 500, 1000, 500, 300

# 指定拖拽时间（秒）
human_drag 100, 1500, 100, 500, duration=1.5
human_drag 100, 1500, 100, 500, duration=2.0

# 贝塞尔曲线轨迹（推荐，最自然）
human_drag 100, 1500, 100, 500, trajectory="bezier", speed="ease_in_out"

# 直线抖动轨迹（模拟手指不稳）
human_drag 100, 1500, 100, 500, trajectory="linear_jitter"

# 元素到元素拖拽
human_drag id:"source_item", id:"target_area"
human_drag text:"文件A", text:"文件夹B"</pre>
              
              <h5 class="font-medium mt-3 mb-2 text-sm">拖拽参数</h5>
              <table class="w-full text-xs bg-purple-100 rounded">
                <tbody>
                  <tr><td class="p-1">duration</td><td class="p-1">拖拽总时间（秒），默认 1.0</td></tr>
                  <tr><td class="p-1">trajectory</td><td class="p-1">bezier(贝塞尔曲线), linear_jitter(直线抖动)</td></tr>
                  <tr><td class="p-1">speed</td><td class="p-1">ease_in_out, ease_in, ease_out, linear, random</td></tr>
                  <tr><td class="p-1">num_points</td><td class="p-1">轨迹采样点数量，默认 50</td></tr>
                  <tr><td class="p-1">jitter_min/max</td><td class="p-1">直线轨迹抖动范围（像素），默认 1/5</td></tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- 完整示例 -->
        <div class="mt-4">
          <h4 class="font-semibold mb-2">完整脚本示例</h4>
          <pre class="bg-gray-100 p-3 rounded text-xs overflow-x-auto"># ================================
# 自动化登录流程示例
# ================================

log "=== 开始自动化登录 ==="

# 配置测试账号
set $test_username = "test@example.com"
set $test_password = "password123"
set $app_package = "com.example.app"

# 步骤 1: 启动应用
log "1. 启动应用"
start_app "${app_package}"
wait 3

# 步骤 2: 检查登录页面
if exists id:"login_button"
    log "2. 输入账号信息"
    input id:"username" "${test_username}"
    wait 0.5
    input id:"password" "${test_password}"
    wait 0.5
    
    log "3. 点击登录按钮"
    click id:"login_button"
    
    log "4. 等待登录结果"
    wait 3
    
    if exists id:"welcome_message"
        set $welcome = get_text id:"welcome_message"
        log "登录成功: ${welcome}"
    else
        log "登录结果未知，检查错误"
        if exists id:"error_message"
            set $error = get_text id:"error_message"
            log "登录失败: ${error}"
        end
    end
else
    log "未找到登录按钮，可能已登录"
end

# 步骤 5: 返回主页
home
log "=== 自动化登录完成 ==="</pre>
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
import CodeEditor from './CodeEditor.vue'

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
