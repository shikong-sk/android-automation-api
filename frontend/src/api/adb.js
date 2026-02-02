import request from './request'

export const adbApi = {
  // 应用管理
  listPackages(filterType = null) {
    const params = filterType ? { filter_type: filterType } : {}
    return request.get('/adb/packages', { params })
  },

  getPackageInfo(packageName) {
    return request.get(`/adb/packages/${packageName}`)
  },

  getAllPackagesInfo(filterType = null) {
    const params = filterType ? { filter_type: filterType } : {}
    return request.get('/adb/packages-info', { params })
  },

  installApk(apkPath, reinstall = false, grantPermissions = true) {
    return request.post('/adb/install', {
      apk_path: apkPath,
      reinstall,
      grant_permissions: grantPermissions
    })
  },

  uninstallPackage(packageName, keepData = false) {
    return request.delete(`/adb/packages/${packageName}`, {
      params: { keep_data: keepData }
    })
  },

  // 设备信息
  getDeviceInfo() {
    return request.get('/adb/device-info')
  },

  getBatteryInfo() {
    return request.get('/adb/battery')
  },

  getScreenResolution() {
    return request.get('/adb/screen/resolution')
  },

  getScreenDensity() {
    return request.get('/adb/screen/density')
  },

  getProp(propName) {
    return request.get(`/adb/prop/${propName}`)
  },

  // Shell 命令
  executeShell(command) {
    return request.post('/adb/shell', { command })
  },

  // 文件操作
  pushFile(localPath, remotePath) {
    return request.post('/adb/push', {
      local_path: localPath,
      remote_path: remotePath
    })
  },

  pullFile(remotePath, localPath) {
    return request.post('/adb/pull', {
      local_path: localPath,
      remote_path: remotePath
    })
  },

  takeScreenshot(localPath) {
    return request.post('/adb/screenshot', null, {
      params: { local_path: localPath }
    })
  },

  takeScreenshotBase64() {
    return request.get('/adb/screenshot-base64')
  },

  // 设备控制
  reboot(mode = null) {
    const params = mode ? { mode } : {}
    return request.post('/adb/reboot', null, { params })
  }
}
