import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { setupElementPlus } from './plugins/element-plus'
import './styles/tailwind.css'

const app = createApp(App)

setupElementPlus(app)

app.use(createPinia())
app.use(router)

app.mount('#app')
