import { createRouter, createWebHistory } from 'vue-router'

import Login from '../views/Login.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import DoctorDashboard from '../views/DoctorDashboard.vue'
import AddDoctor from '../views/AddDoctor.vue'
import EditDoctor from '../views/EditDoctor.vue'
import Register from '@/views/Register.vue'
import UpdateHistory from '@/views/UpdateHistory.vue'
import PatientHistory from '@/views/PatientHistory.vue'
import DoctorAvailability from '@/views/DoctorAvailability.vue'

const routes = [
  { path: '/', component: Login },
  { path: '/register',component:Register},
  { path: '/admin', component: AdminDashboard },
  { path: '/doctor', component: DoctorDashboard },
  { path: '/add-doctor', component: AddDoctor },
  { path: '/edit-doctor/:id', component: EditDoctor },
  { path: '/update-history/:appointmentId', component: UpdateHistory },
  { path: '/patient-history/:patientId', component: PatientHistory },
  { path: '/availability', component: DoctorAvailability }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  const publicRoutes=['/','/register']

  if (!token) {
    if (!publicRoutes.includes(to.path)) {
      return next('/')
    }
    return next()
  }

  let role = null

  try {
    const decoded = JSON.parse(atob(token.split('.')[1]))
    role = decoded.role
  } catch (e) {
    console.log("Token decode error")
    localStorage.removeItem('token')
    return next('/')
  }

  // 🔴 Prevent logged-in user from visiting login page
  /*if (to.path === '/') {
    return next(role === 'admin' ? '/admin' : '/doctor')
  }*/

  // 🔴 Doctor trying to access admin routes
  if (to.path.startsWith('/admin') && role !== 'admin') {
    return next('/doctor')
  }

  // 🔴 Admin trying to access doctor routes
  if (to.path.startsWith('/doctor') && role !== 'doctor') {
    return next('/admin')
  }

  next()
})

export default router