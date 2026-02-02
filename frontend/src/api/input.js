import request from './request'

export const inputApi = {
  click(resourceId) {
    return request.post('/input/click', null, { params: { resource_id: resourceId } })
  },

  clickByText(text) {
    return request.post('/input/click-by-text', null, { params: { text } })
  },

  clickByClass(className) {
    return request.post('/input/click-by-class', null, { params: { class_name: className } })
  },

  clickByXpath(xpath) {
    return request.post('/input/click-by-xpath', null, { params: { xpath } })
  },

  existsByText(text) {
    return request.get('/input/exists-by-text', { params: { text } })
  },

  existsByClass(className) {
    return request.get('/input/exists-by-class', { params: { class_name: className } })
  },

  existsByXpath(xpath) {
    return request.get('/input/exists-by-xpath', { params: { xpath } })
  },

  setText(resourceId, text) {
    return request.post('/input/set-text', null, { params: { resource_id: resourceId, text } })
  },

  clearText(resourceId) {
    return request.post('/input/clear-text', null, { params: { resource_id: resourceId } })
  },

  // 通用选择器方法
  setTextBySelector(selectorType, selectorValue, text) {
    return request.post('/input/set-text-by-selector', null, { 
      params: { selector_type: selectorType, selector_value: selectorValue, text } 
    })
  },

  clearTextBySelector(selectorType, selectorValue) {
    return request.post('/input/clear-text-by-selector', null, { 
      params: { selector_type: selectorType, selector_value: selectorValue } 
    })
  },

  sendActionBySelector(selectorType, selectorValue) {
    return request.post('/input/send-action-by-selector', null, { 
      params: { selector_type: selectorType, selector_value: selectorValue } 
    })
  },

  waitAppearBySelector(selectorType, selectorValue, timeout = 10) {
    return request.get('/input/wait-appear-by-selector', { 
      params: { selector_type: selectorType, selector_value: selectorValue, timeout } 
    })
  },

  waitGoneBySelector(selectorType, selectorValue, timeout = 10) {
    return request.get('/input/wait-gone-by-selector', { 
      params: { selector_type: selectorType, selector_value: selectorValue, timeout } 
    })
  },

  getElementTextBySelector(selectorType, selectorValue) {
    return request.get('/input/text-by-selector', { 
      params: { selector_type: selectorType, selector_value: selectorValue } 
    })
  },

  getElementBoundsBySelector(selectorType, selectorValue, options = {}) {
    return request.get('/input/bounds-by-selector', {
      params: {
        selector_type: selectorType,
        selector_value: selectorValue,
        parent_selector_type: options.parent_selector_type || null,
        parent_selector_value: options.parent_selector_value || null,
        sibling_selector_type: options.sibling_selector_type || null,
        sibling_selector_value: options.sibling_selector_value || null,
        sibling_relation: options.sibling_relation || 'following',
        offset_x: options.offset_x || 0,
        offset_y: options.offset_y || 0
      }
    })
  },

  findWithParent(childSelectorType, childSelectorValue, parentSelectorType, parentSelectorValue) {
    return request.get('/input/find-with-parent', {
      params: {
        child_selector_type: childSelectorType,
        child_selector_value: childSelectorValue,
        parent_selector_type: parentSelectorType,
        parent_selector_value: parentSelectorValue
      }
    })
  },

  findWithSibling(targetSelectorType, targetSelectorValue, siblingSelectorType, siblingSelectorValue, siblingRelation = 'following') {
    return request.get('/input/find-with-sibling', {
      params: {
        target_selector_type: targetSelectorType,
        target_selector_value: targetSelectorValue,
        sibling_selector_type: siblingSelectorType,
        sibling_selector_value: siblingSelectorValue,
        sibling_relation: siblingRelation
      }
    })
  },

  swipe(direction, percent = 0.5) {
    return request.post('/input/swipe', null, { params: { direction, percent } })
  },

  execute(action, params = {}) {
    return request.post('/input/execute', { action, params })
  },

  findById(resourceId) {
    return request.get('/input/find-by-id', { params: { resource_id: resourceId } })
  },

  findByText(text) {
    return request.get('/input/find-by-text', { params: { text } })
  },

  findByClass(className) {
    return request.get('/input/find-by-class', { params: { class_name: className } })
  },

  findElementsByClass(className) {
    return request.get('/input/find-elements-by-class', { params: { class_name: className } })
  },

  findByXpath(xpath) {
    return request.get('/input/find-by-xpath', { params: { xpath } })
  },

  exists(resourceId) {
    return request.get('/input/exists', { params: { resource_id: resourceId } })
  },

  getElementText(resourceId) {
    return request.get('/input/text', { params: { resource_id: resourceId } })
  },

  getElementBounds(resourceId) {
    return request.get('/input/bounds', { params: { resource_id: resourceId } })
  },

  waitAppear(resourceId, timeout = 10) {
    return request.get('/input/wait-appear', { params: { resource_id: resourceId, timeout } })
  },

  waitGone(resourceId, timeout = 10) {
    return request.get('/input/wait-gone', { params: { resource_id: resourceId, timeout } })
  },

  getHierarchy() {
    return request.get('/input/hierarchy')
  },

  screenOn() {
    return request.post('/input/screen-on')
  },

  screenOff() {
    return request.post('/input/screen-off')
  },

  unlock() {
    return request.post('/input/unlock')
  },

  sendAction(resourceId, action = 'IME_ACTION_DONE') {
    return request.post('/input/send-action', null, { params: { resource_id: resourceId, action } })
  },

  // ============ 人类模拟操作 API ============

  /**
   * 模拟人类点击
   * @param {Object} options - 点击选项
   * @param {number} [options.x] - 目标 x 坐标
   * @param {number} [options.y] - 目标 y 坐标
   * @param {string} [options.selector_type] - 选择器类型: id, text, class, xpath
   * @param {string} [options.selector_value] - 选择器值
   * @param {string} [options.parent_selector_type] - 父元素选择器类型
   * @param {string} [options.parent_selector_value] - 父元素选择器值
   * @param {string} [options.sibling_selector_type] - 兄弟元素选择器类型
   * @param {string} [options.sibling_selector_value] - 兄弟元素选择器值
   * @param {string} [options.sibling_relation] - 兄弟关系: following(之后), preceding(之前)
   * @param {number} [options.offset_x] - X 坐标偏移
   * @param {number} [options.offset_y] - Y 坐标偏移
   * @param {number} [options.offset_min=3] - 随机偏移最小值
   * @param {number} [options.offset_max=10] - 随机偏移最大值
   * @param {number} [options.delay_min=0.05] - 点击前延迟最小值（秒）
   * @param {number} [options.delay_max=0.3] - 点击前延迟最大值（秒）
   * @param {number} [options.duration_min=0.05] - 按压时长最小值（秒）
   * @param {number} [options.duration_max=0.15] - 按压时长最大值（秒）
   */
  humanClick(options) {
    return request.post('/input/human-click', options)
  },

  /**
   * 模拟人类双击
   * @param {Object} options - 双击选项
   * @param {number} [options.x] - 目标 x 坐标
   * @param {number} [options.y] - 目标 y 坐标
   * @param {string} [options.selector_type] - 选择器类型
   * @param {string} [options.selector_value] - 选择器值
   * @param {string} [options.parent_selector_type] - 父元素选择器类型
   * @param {string} [options.parent_selector_value] - 父元素选择器值
   * @param {string} [options.sibling_selector_type] - 兄弟元素选择器类型
   * @param {string} [options.sibling_selector_value] - 兄弟元素选择器值
   * @param {string} [options.sibling_relation] - 兄弟关系: following(之后), preceding(之前)
   * @param {number} [options.offset_x] - X 坐标偏移
   * @param {number} [options.offset_y] - Y 坐标偏移
   * @param {number} [options.offset_min=3] - 随机偏移最小值
   * @param {number} [options.offset_max=8] - 随机偏移最大值
   * @param {number} [options.interval_min=0.1] - 两次点击间隔最小值（秒）
   * @param {number} [options.interval_max=0.2] - 两次点击间隔最大值（秒）
   * @param {number} [options.duration_min=0.03] - 按压时长最小值（秒）
   * @param {number} [options.duration_max=0.08] - 按压时长最大值（秒）
   */
  humanDoubleClick(options) {
    return request.post('/input/human-double-click', options)
  },

  /**
   * 模拟人类长按
   * @param {Object} options - 长按选项
   * @param {number} [options.x] - 目标 x 坐标
   * @param {number} [options.y] - 目标 y 坐标
   * @param {string} [options.selector_type] - 选择器类型
   * @param {string} [options.selector_value] - 选择器值
   * @param {string} [options.parent_selector_type] - 父元素选择器类型
   * @param {string} [options.parent_selector_value] - 父元素选择器值
   * @param {string} [options.sibling_selector_type] - 兄弟元素选择器类型
   * @param {string} [options.sibling_selector_value] - 兄弟元素选择器值
   * @param {string} [options.sibling_relation] - 兄弟关系: following(之后), preceding(之前)
   * @param {number} [options.offset_x] - X 坐标偏移
   * @param {number} [options.offset_y] - Y 坐标偏移
   * @param {number} [options.duration_min=0.8] - 长按时长最小值（秒）
   * @param {number} [options.duration_max=1.5] - 长按时长最大值（秒）
   * @param {number} [options.offset_min=3] - 随机偏移最小值
   * @param {number} [options.offset_max=10] - 随机偏移最大值
   * @param {number} [options.delay_min=0.05] - 操作前延迟最小值（秒）
   * @param {number} [options.delay_max=0.2] - 操作前延迟最大值（秒）
   */
  humanLongPress(options) {
    return request.post('/input/human-long-press', options)
  },

  /**
   * 模拟人类拖拽
   * @param {Object} options - 拖拽选项
   * @param {number} [options.start_x] - 起点 x 坐标
   * @param {number} [options.start_y] - 起点 y 坐标
   * @param {number} [options.end_x] - 终点 x 坐标
   * @param {number} [options.end_y] - 终点 y 坐标
   * @param {string} [options.start_selector_type] - 起点选择器类型
   * @param {string} [options.start_selector_value] - 起点选择器值
   * @param {string} [options.end_selector_type] - 终点选择器类型
   * @param {string} [options.end_selector_value] - 终点选择器值
   * @param {string} [options.trajectory_type='bezier'] - 轨迹类型: bezier, linear_jitter
   * @param {string} [options.speed_mode='ease_in_out'] - 速度模式: ease_in_out, ease_in, ease_out, linear, random
   * @param {number} [options.duration=1.0] - 拖拽总时间（秒）
   * @param {number} [options.num_points=50] - 轨迹采样点数量
   * @param {number} [options.offset_min=3] - 起点/终点随机偏移最小值
   * @param {number} [options.offset_max=10] - 起点/终点随机偏移最大值
   * @param {number} [options.jitter_min=1] - 直线轨迹抖动最小值
   * @param {number} [options.jitter_max=5] - 直线轨迹抖动最大值
   * @param {number} [options.delay_min=0.05] - 操作前延迟最小值（秒）
   * @param {number} [options.delay_max=0.2] - 操作前延迟最大值（秒）
   */
  humanDrag(options) {
    return request.post('/input/human-drag', options)
  }
}
