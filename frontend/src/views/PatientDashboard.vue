<template>
  <div>
    <PatientNavbar />

    <div class="container mt-4">

      <div class="card p-3 mb-4" style="border: 2px solid black; border-radius: 10px;">
        <h5>Departments</h5>

        <div class="row mt-2">
          <div class="col-md-6" v-for="d in departments" :key="d.id">
            
            <div class="d-flex justify-content-between align-items-center p-2 mb-3"
                style="border: 1px solid gray;">

              <span>{{ d.name }}</span>

              <button class="btn btn-primary btn-sm" style="width: 100px;"
                      @click="viewDepartment(d.id)">
                View Details
              </button>

            </div>

          </div>
        </div>
      </div>

      <div class="card p-3 mb-5 mt-5" style="border: 2px solid black; border-radius: 10px;">
        <h5>Upcoming Appointments</h5>

        <table class="table table-striped mt-3">
          <thead>
            <tr>
              <th>Sr No.</th>
              <th>Doctor</th>
              <th>Department</th>
              <th>Date</th>
              <th>Time</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            <tr v-if="appointments.length === 0">
              <td colspan="7" class="text-center text-danger fw-bold fs-5">
                No appointments found
              </td>
            </tr>

            <tr v-for="(a, index) in appointments" :key="a.id">
              <td>{{ index + 1 }}</td>
              <td>{{ a.doctor_name }}</td>
              <td>{{ a.department }}</td>
              <td>{{ a.date }}</td>
              <td>{{ a.time }}</td>
              <td>{{ a.status }}</td>
              <td class="d-flex gap-2">
                <button class="btn btn-danger btn-sm me-2"
                        @click="cancelAppointment(a.id)">
                  Cancel
                </button>
              </td>
            </tr>
          </tbody>
        </table>

      </div>

    </div>
  </div>
</template>

<script>
import PatientNavbar from '@/components/PatientNavbar.vue'
import API from '../services/api'

export default {
  components: { PatientNavbar },

  data() {
    return {
      departments: [],
      appointments: []
    }
  },

  mounted() {
    this.fetchDepartments()
    this.fetchAppointments()
  },

  methods: {

    async fetchDepartments() {
      const res = await API.get('/patient/departments')
      this.departments = res.data
    },

    async fetchAppointments() {
      const res = await API.get('/patient/appointments')
      this.appointments = res.data
    },

    viewDepartment(id) {
      this.$router.push(`/department/${id}`)
    },

    async cancelAppointment(id) {
      await API.put(`/patient/appointment/${id}/cancel`)
      this.fetchAppointments()
    }
  }
}
</script>