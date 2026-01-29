import request from './request'

export const navigationApi = {
  home() {
    return request.post('/navigation/home')
  },

  back() {
    return request.post('/navigation/back')
  },

  menu() {
    return request.post('/navigation/menu')
  },

  goHome() {
    return request.post('/navigation/go-home')
  },

  recentApps() {
    return request.post('/navigation/recent-apps')
  }
}
