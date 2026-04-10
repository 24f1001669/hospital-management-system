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
  { path: '/', component: Login ,meta: { title: 'Login' } },
  { path: '/register',component:Register, meta: { title: 'Register' }},
  { path: '/admin', component: AdminDashboard ,meta: { title: 'Admin Dashboard' }},
  { path: '/doctor', component: DoctorDashboard,meta: { title: 'Doctor Dashboard' } },
  { path: '/add-doctor', component: AddDoctor,meta: { title: 'Add a new doctor' } },
  { path: '/edit-doctor/:id', component: EditDoctor,meta: { title: 'Edit doctor' } },
  { path: '/update-history/:appointmentId', component: UpdateHistory,meta: { title: 'Update patient history' } },
  { path: '/availability', component: DoctorAvailability,meta: { title: 'Availability of doctor' } },
  { path: '/patient', component: PatientDashboard,meta: { title: 'Patient Dashboard' } },
  { path: '/department/:id', component: DepartmentDetails,meta: { title: 'Department Details' } },
  { path: '/edit-profile', component: EditProfile,meta: { title: 'Edit profile' } },
  { path: '/patient/doctor-availability/:id', component: BookAppointment,meta: { title: 'Book an appointment' } },
  { path: '/history', component: History,meta: { title: 'Patient history' } },
  { path: '/history/:id', component: History,meta: { title: 'Patient history' } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const token = localStorage.getItem('token')

  document.title = to.meta.title || 'Vite';

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