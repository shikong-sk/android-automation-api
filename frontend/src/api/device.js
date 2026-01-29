import request from './request'

export const deviceApi = {
  connect(deviceSerial = null) {
    return request.post('/device/connect', { device_serial: deviceSerial })
  },

  getStatus() {
    return request.get('/device/status')
  },

  disconnect() {
    return request.post('/device/disconnect')
  }
}
