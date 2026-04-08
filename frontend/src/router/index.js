import { createRouter, createWebHistory } from 'vue-router'
import AdminDashboard from '../views/AdminDashboard.vue'
import PatientHistory from '@/views/PatientHistory.vue'
import AddDoctor from '@/views/AddDoctor.vue'
import EditDoctor from '@/views/EditDoctor.vue'

const routes = [
  { path: '/admin', component: AdminDashboard },
  { path: '/add-doctor', component: AddDoctor },
  { path: '/patient-history', component: PatientHistory },
  { path: '/edit-doctor/:id',component:EditDoctor}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  const publicPages = ['/']   // only login is public
  const authRequired = !publicPages.includes(to.path)

  if (authRequired && !token) {
    return next('/')
  }

  if (to.path === '/' && token) {
    return next('/admin')
  }

  next()
})

export default router