<template>
  <DoctorNavbar />
  <div class="container mt-4">
    <div class="card p-4 mb-3" style="border-radius: 10px; border: 2px solid black;">
      <h5>Upcoming Appointments</h5>

      <table class="table table-striped mt-3">
        <thead>
          <tr>
            <th>Patient Name</th>
            <th>Date</th>
            <th>Time</th>
            <th>Status</th>
            <th>Patient History</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody class="table-group-divider">
          <tr v-if="appointments.length === 0">
            <td colspan="6" class="text-center fw-bold fs-5 text-danger">No appointments</td>
          </tr>

          <tr v-for="a in appointments" :key="a.id">
            <td>{{ a.patient_name }}</td>
            <td>{{ a.date }}</td>
            <td>{{ a.time }}</td>
            <td>{{ a.status }}</td>
            <td>
              <button class="btn btn-warning btn-sm" style="width:100px" @click="$router.push(`/update-history/${a.id}`)">Update</button>
            </td>
            <td>
              <button class="btn btn-success btn-sm me-3" style="width:100px" @click="markComplete(a.id)">Complete</button>
              <button class="btn btn-danger btn-sm" style="width:100px" @click="markCancel(a.id)">Cancel</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="container mt-5">
    <div class="card p-3 mb-3" style="border-radius: 10px; border: 2px solid black;">
      <h5>Assigned Patients</h5>

      <div v-if="patients.length === 0" class="text-center fw-bold fs-5 text-danger">
        No patients found
      </div>

      <div v-for="p in patients" :key="p.id"
          class="d-flex justify-content-between p-2 mb-2"
          style="border:1px solid gray">

        <span>{{ p.name }}</span>

        <button class="btn btn-primary btn-sm" style="width:100px"
                @click="goToHistory(p)">
          View
        </button>
      </div>
    </div>
  </div>
  <div class="container mt-5">
    <div class="mb-3 d-flex justify-content-end" style="border: none;">
      <button class="btn btn-success" style="width:200px" @click="$router.push('/availability')">Provide Availability</button>
    </div>
  </div>
</template>

<script>
import DoctorNavbar from '@/components/DoctorNavbar.vue';
import API from '../services/api'

export default {
  components: { DoctorNavbar },
  data() {
    return {
      appointments: [],
      patients:[]
    }
  },

  mounted() {
    this.fetchAppointments()
    this.fetchPatients()
  },

  methods: {
    async fetchAppointments() {
      const res = await API.get('/doctor/appointments')
      this.appointments = res.data
    },

    async fetchPatients() {
      const res = await API.get('/doctor/patients')
      this.patients=res.data
    },

    async markComplete(id) {
      await API.put(`/doctor/appointment/${id}/complete`)
      this.fetchAppointments()
    },

    async markCancel(id) {
      await API.put(`/doctor/appointment/${id}/cancel`)
      this.fetchAppointments()
    },

    goToHistory(p) {
      this.$router.push(`/history/${p.id}`)
    },

    logout() {
      localStorage.removeItem('token')
      this.$router.push('/')
    }
  }
}
</script>