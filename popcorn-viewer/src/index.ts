import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './components/App'
import CollectionViewer from './components/CollectionViewer'
import ManifestViewer from './components/ManifestViewer'
import './css/app.pcss'

Vue.use(VueRouter)

// new Vue({ render: createElement => createElement(App) }).$mount('#app')

const routes = [
  { path: '/', component: App },
  // { path: '/:id', component: ManifestViewer },
]

const router = new VueRouter({
  mode: 'hash',
  routes,
})

new Vue({ 
  template: '<router-view></router-view>',
  router,
}).$mount('#app')
