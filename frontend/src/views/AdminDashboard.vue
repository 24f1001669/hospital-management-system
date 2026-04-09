<template>
  <div>
    <AdminNavbar @search="handleSearch"/>

    <div class="container mt-4">
      <div class="card p-3 mb-3" style="border-radius: 10px; border: 2px solid black;">
        <div class="d-flex justify-content-between">
            <h5>Registered Doctors</h5>
            <button class="btn btn-success btn-sm mb-2" style="width:75px" @click="$router.push('/add-doctor')">Create</button>
        </div>
        <div v-if="doctors.length === 0" class="text-center fw-bold fs-5 text-danger">
          No doctors found
        </div>
        <div v-else v-for="d in doctors" :key="d.id" class="d-flex justify-content-between align-items-center p-2 mb-2" style="border: 1px solid gray;">
          <span>{{ d.name }}</span>
          <div class="d-flex gap-2">
            <button class="btn btn-warning btn-sm me-2" style="width:100px" @click="$router.push(`/edit-doctor/${d.id}`)">Edit</button>
            <button class="btn btn-danger btn-sm me-2" style="width:100px" @click="deleteUser(d.user_id)">Delete</button>
            <button 
              :class="d.is_blacklisted ? 'btn btn-secondary btn-sm' : 'btn btn-dark btn-sm'"
              style="width:100px"
              @click="toggleBlacklist(d)"
            >
              {{ d.is_blacklisted ? 'Unblacklist' : 'Blacklist' }}
            </button>
          </div>
        </div>
      </div>

      <div class="card p-3 mb-3" style="border-radius: 10px; border: 2px solid black;">
        <h5>Registered Patients</h5>
        <div v-if="patients.length === 0" class="text-center fw-bold fs-5 text-danger">
          No patients found
        </div>
        <div v-else v-for="p in patients" :key="p.id" class="d-flex justify-content-between align-items-center p-2 mb-2" style="border: 1px solid gray;">
          <span>{{ p.name }}</span>
          <div class="d-flex gap-2">
            <button class="btn btn-danger btn-sm me-2" style="width:100px" @click="deleteUser(p.user_id)">Delete</button>
            <button 
              :class="p.is_blacklisted ? 'btn btn-secondary btn-sm' : 'btn btn-dark btn-sm'"
              style="width:100px"
              @click="toggleBlacklist(p)"
            >
              {{ p.is_blacklisted ? 'Unblacklist' : 'Blacklist' }}
            </button>
          </div>
        </div>
      </div>

      <div class="card p-3 mb-3" style="border-radius: 10px; border: 2px solid black;">
        <h5>Upcoming Appointments</h5>
        <div v-if="appointments.length === 0" class="text-center fw-bold fs-5 text-danger">
          No appointments found
        </div>
        <table v-else class="table table-striped">
          <thead>
            <tr>
              <th>Sr No.</th>
              <th>Patient</th>
              <th>Doctor</th>
              <th>Date</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody class="table-group-divider">
            <tr v-for="(a, index) in appointments" :key="a.id">
              <td>{{ index + 1 }}</td>
              <td>{{ a.patient_name }}</td>
              <td>{{ a.doctor_name }}</td>
              <td>{{ a.date }}</td>
              <td>
                <button class="btn btn-primary btn-sm" style="width:100px" @click="goToHistory(a.patient_id)">View</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
<script>
import AdminNavbar from '../components/AdminNavbar.vue'
import API from '../services/api'

export default {
  components: { AdminNavbar },

  data() {
    return {
      doctors: [],
      patients: [],
      appointments: [],
      doctor: {},
      searchQuery: '',
      editMode: false,
      editDoctorId: null
    }
  },

  mounted() {
    this.fetchDoctors()
    this.fetchPatients()
    this.fetchAppointments()
  },

  methods: {

    goToHistory(p) {
      this.$router.push(`/patient-history/${p}`)
    },

    async fetchDoctors() {
      const res = await API.get(`/admin/doctors/search?q=${this.searchQuery}`)
      this.doctors = res.data
    },

    async fetchPatients() {
      const res = await API.get(`/admin/patients/search?q=${this.searchQuery}`)
      this.patients = res.data
    },

    async fetchAppointments() {
      const res = await API.get('/admin/appointments')
      this.appointments = res.data
    },

    async handleSearch(query) {
      this.searchQuery = query
      await this.fetchDoctors()
      await this.fetchPatients()
    },

    async addDoctor() {
      if (this.editMode) {
        await API.put(`/admin/doctor/${this.editDoctorId}`, this.doctor)
        this.editMode = false
        this.editDoctorId = null
      } else {
        await API.post('/admin/doctor', this.doctor)
      }

      this.doctor = {}
      this.fetchDoctors()
    },

    editDoctor(d) {
      this.doctor = { ...d }
      this.editMode = true
      this.editDoctorId = d.id
    },

    async deleteUser(id) {
      try {
        await API.delete(`/admin/delete/user/${id}`)
        this.fetchDoctors()
        this.fetchPatients()
      } catch (err) {
        alert(err.response?.data?.message || "Delete Failed")
      }
    },

    async toggleBlacklist(d) {
      if (d.is_blacklisted) {
        await API.put(`/admin/unblacklist/user/${d.user_id}`)
      } else {
        await API.put(`/admin/blacklist/user/${d.user_id}`)
      }

      this.fetchDoctors()
      this.fetchPatients()
    }

  }
}
</script>