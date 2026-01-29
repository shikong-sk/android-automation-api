import { defineStore } from 'pinia'
import { ref } from 'vue'
import { deviceApi } from '@/api'

export const useDeviceStore = defineStore('device', () => {
  const connected = ref(false)
  const deviceInfo = ref(null)
  const loading = ref(false)
  const error = ref(null)

  async function connect(deviceSerial = null) {
    loading.value = true
    error.value = null
    try {
      const data = await deviceApi.connect(deviceSerial)
      deviceInfo.value = data
      connected.value = true
      return data
    } catch (err) {
      error.value = err.message || '连接设备失败'
      connected.value = false
      throw err
    } finally {
      loading.value = false
    }
  }

  async function disconnect() {
    loading.value = true
    try {
      await deviceApi.disconnect()
      connected.value = false
      deviceInfo.value = null
    } catch (err) {
      error.value = err.message || '断开设备失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchStatus() {
    loading.value = true
    try {
      const data = await deviceApi.getStatus()
      connected.value = data.connected
      if (data.connected) {
        deviceInfo.value = data.device_info
      } else {
        deviceInfo.value = null
      }
      return data
    } catch (err) {
      error.value = err.message || '获取设备状态失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    connected,
    deviceInfo,
    loading,
    error,
    connect,
    disconnect,
    fetchStatus
  }
})
