import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/pages/Dashboard.vue'),
    meta: { title: '控制台' }
  },
  {
    path: '/device',
    name: 'Device',
    component: () => import('@/pages/Device.vue'),
    meta: { title: '设备管理' }
  },
  {
    path: '/input',
    name: 'Input',
    component: () => import('@/pages/Input.vue'),
    meta: { title: '输入控制' }
  },
  {
    path: '/navigation',
    name: 'Navigation',
    component: () => import('@/pages/Navigation.vue'),
    meta: { title: '导航控制' }
  },
  {
    path: '/apps',
    name: 'Apps',
    component: () => import('@/pages/Apps.vue'),
    meta: { title: '应用管理' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
