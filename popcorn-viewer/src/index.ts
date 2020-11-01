import Vue from 'vue'
import VueRouter from 'vue-router'
import CollectionView from './components/CollectionView'
import ManifestView from './components/ManifestView'
import Map from './components/Map'
import NavBar from './components/NavBar'
import './css/app.pcss'

Vue.use(VueRouter)

// new Vue({ render: createElement => createElement(App) }).$mount('#app')

const routes = [
  {
    path: '/', 
    component: CollectionView,
  },
  {
    path: '/kart',
    component: Map,
  },
  {
    path: '/:id', 
    component: ManifestView,
  },
]

const router = new VueRouter({
  mode: 'hash',
  routes,
})

new Vue({ 
  template: `
    <div class="h-full flex flex-col">
      <nav-bar></nav-bar>
      <router-view></router-view>
    </div>  
  `,
  components: {
    NavBar,
  },
  router,
}).$mount('#app')
