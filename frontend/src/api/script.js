import request from './request'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

export const scriptApi = {
  // 获取脚本列表
  list() {
    return request.get('/script/list')
  },

  // 获取脚本内容
  get(name) {
    return request.get(`/script/get/${name}`)
  },

  // 保存脚本
  save(name, content) {
    return request.post('/script/save', { name, content })
  },

  // 删除脚本
  delete(name) {
    return request.delete(`/script/delete/${name}`)
  },

  // 执行脚本内容
  execute(content, variables = null) {
    return request.post('/script/execute', { content, variables })
  },

  // 执行脚本文件
  executeFile(name, variables = null) {
    return request.post(`/script/execute/${name}`, variables)
  },

  // 验证脚本语法
  validate(content) {
    return request.post('/script/validate', { content })
  },

  /**
   * 执行脚本并通过 SSE 实时获取日志
   * @param {string} content - 脚本内容
   * @param {object} variables - 初始变量
   * @param {object} callbacks - 回调函数对象
   * @param {function} callbacks.onLog - 日志回调
   * @param {function} callbacks.onResult - 结果回调
   * @param {function} callbacks.onError - 错误回调
   * @param {function} callbacks.onEnd - 结束回调
   * @returns {object} - 包含 sessionId 和 abort 方法的对象
   */
  executeStream(content, variables = null, callbacks = {}) {
    const { onLog, onResult, onError, onEnd, onSession } = callbacks
    
    let sessionId = null
    const abortController = new AbortController()

    // 使用 fetch 发起 SSE 请求
    fetch(`${API_BASE_URL}/script/execute/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ content, variables }),
      signal: abortController.signal,
    })
      .then(async (response) => {
        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'Request failed')
        }

        const reader = response.body.getReader()
        const decoder = new TextDecoder()
        let buffer = ''

        while (true) {
          const { done, value } = await reader.read()
          if (done) break

          buffer += decoder.decode(value, { stream: true })
          const lines = buffer.split('\n')
          buffer = lines.pop() || ''

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              try {
                const event = JSON.parse(line.slice(6))
                
                switch (event.type) {
                  case 'session':
                    sessionId = event.data
                    onSession?.(sessionId)
                    break
                  case 'log':
                    onLog?.(event.data)
                    break
                  case 'result':
                    onResult?.(event.data)
                    break
                  case 'error':
                    onError?.(event.data)
                    break
                  case 'end':
                    onEnd?.()
                    break
                }
              } catch (e) {
                console.error('Failed to parse SSE event:', e)
              }
            }
          }
        }
      })
      .catch((error) => {
        if (error.name !== 'AbortError') {
          onError?.(error.message)
        }
        onEnd?.()
      })

    return {
      getSessionId: () => sessionId,
      abort: () => abortController.abort(),
    }
  },

  // 停止脚本执行
  stop(sessionId) {
    return request.post(`/script/stop/${sessionId}`)
  }
}
