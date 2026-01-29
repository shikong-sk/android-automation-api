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
  }
}
