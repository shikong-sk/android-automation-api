import request from './request'

export const appApi = {
  start(packageName) {
    return request.post(`/app/start/${packageName}`)
  },

  stop(packageName) {
    return request.post(`/app/stop/${packageName}`)
  },

  clear(packageName) {
    return request.post(`/app/clear/${packageName}`)
  },

  getVersion(packageName) {
    return request.get(`/app/version/${packageName}`)
  },

  getStatus(packageName) {
    return request.get(`/app/status/${packageName}`)
  },

  getCurrent() {
    return request.get('/app/current')
  }
}
