import Vue from 'vue'
import App from './components/App'
import './css/app.pcss'

new Vue({ render: createElement => createElement(App) }).$mount('#app')
