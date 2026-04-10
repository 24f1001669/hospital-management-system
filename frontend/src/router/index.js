import { createRouter, createWebHistory } from 'vue-router'

import Login from '../views/Login.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import DoctorDashboard from '../views/DoctorDashboard.vue'
import AddDoctor from '../views/AddDoctor.vue'
import EditDoctor from '../views/EditDoctor.vue'
import Register from '@/views/Register.vue'
import UpdateHistory from '@/views/UpdateHistory.vue'
import DoctorAvailability from '@/views/DoctorAvailability.vue'
import PatientDashboard from '@/views/PatientDashboard.vue'
import DepartmentDetails from '@/views/DepartmentDetails.vue'
import EditProfile from '@/views/EditProfile.vue'
import BookAppointment from '@/views/BookAppointment.vue'
import History from '@/views/History.vue'

const routes = [
  { path: '/', component: Login },
  { path: '/register',component:Register},
  { path: '/admin', component: AdminDashboard },
  { path: '/doctor', component: DoctorDashboard },
  { path: '/add-doctor', component: AddDoctor },
  { path: '/edit-doctor/:id', component: EditDoctor },
  { path: '/update-history/:appointmentId', component: UpdateHistory },
  { path: '/availability', component: DoctorAvailability },
  { path: '/patient', component: PatientDashboard },
  { path: '/department/:id', component: DepartmentDetails },
  { path: '/edit-profile', component: EditProfile },
  { path: '/patient/doctor-availability/:id', component: BookAppointment },
  { path: '/history', component: History },
  { path: '/history/:id', component: History }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const token = localStorage.getItem('token')

  if (to.path === '/' || to.path === '/register') {
    if (!token) return true

    const payload = JSON.parse(atob(token.split('.')[1]))
    const role = payload.role

    if (role === 'admin') return '/admin'
    if (role === 'doctor') return '/doctor'
    if (role === 'patient') return '/patient'
  }

  if (!token) {
    return '/'
  }

  const payload = JSON.parse(atob(token.split('.')[1]))
  const role = payload.role

  if (to.path.startsWith('/admin') && role !== 'admin') {
    return `/${role}`
  }

  if (to.path.startsWith('/doctor') && role !== 'doctor') {
    return `/${role}`
  }

  if (to.path.startsWith('/patient') && role !== 'patient') {
    return `/${role}`
  }
  
  return true
})

export default router