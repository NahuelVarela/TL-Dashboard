import Vue from 'vue'
import VueRouter from 'vue-router'
import Dashboard from '../views/dashboard.vue'

Vue.use(VueRouter)

  const routes = [
  {
    path: '/',
    name: 'dashboard',
    component: Dashboard
  },
  {
    path: '/workflow',
    name: 'Workflow',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/workflow.vue')
  },
  {
    path: '/settings',
    name: 'Settings',
    // route level code-splitting
    component: () => import(/* webpackChunkName: "about" */ '../views/settings.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router
