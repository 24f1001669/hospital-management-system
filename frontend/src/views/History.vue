<template>
  <div>

    <div class="container mt-5">

      <div class="d-flex justify-content-between align-items-center mb-3">
        <h4>
          <span v-if="role === 'patient'">My Medical History</span>
          <span v-else-if="role === 'doctor'">Patient History</span>
          <span v-else>Patient History</span>
        </h4>

        <button class="btn btn-primary btn-sm" style="width:100px" @click="goBack">
          Back
        </button>
      </div>

      <div class="card p-3" style="border: 2px solid black; border-radius: 10px;">

        <table class="table table-striped">

          <thead>
            <tr>
              <th>Date</th>
              <th>Doctor</th>
              <th>Department</th>
              <th>Diagnosis</th>
              <th>Prescription</th>
              <th>Tests</th>
              <th>Medicines</th>
            </tr>
          </thead>

          <tbody>

            <tr v-if="history.length === 0">
              <td colspan="8" class="text-center text-danger fw-bold fs-5">
                No history found
              </td>
            </tr>

            <tr v-for="(h, index) in history" :key="index">
              <td>{{ h.date }}</td>
              <td>{{ h.doctor || h.doctor_name }}</td>
              <td>{{ h.department }}</td>
              <td>{{ h.diagnosis }}</td>
              <td>{{ h.prescription }}</td>
              <td>{{ h.tests || h.tests_done }}</td>
              <td>{{ h.medicines }}</td>
            </tr>

          </tbody>

        </table>

      </div>

    </div>
  </div>
</template>

<script>
import API from '../services/api'

export default {
  data() {
    return {
      history: [],
      role: ''
    }
  },

  mounted() {
    this.getRole()
    this.fetchHistory()
  },

  methods: {

    getRole() {
      const token = localStorage.getItem('token')
      const payload = JSON.parse(atob(token.split('.')[1]))
      this.role = payload.role
    },

    async fetchHistory() {
      try {
        if (this.role === 'patient') {
          const res = await API.get('/patient/history')
          this.history = res.data

        } else if (this.role === 'doctor') {
          const patientId = this.$route.params.id
          const res = await API.get(`/doctor/patient-history/${patientId}`)
          this.history = res.data.history

        } else if (this.role === 'admin') {
          const patientId = this.$route.params.id
          const res = await API.get(`/admin/patient-history/${patientId}`)
          this.history = res.data.history
        }

      } catch (err) {
        console.log("Error loading history:", err)
      }
    },

    goBack() {
      if (this.role === 'admin') {
        this.$router.push('/admin')
      } else if (this.role === 'doctor') {
        this.$router.push('/doctor')
      } else {
        this.$router.push('/patient')
      }
    }

  }
}
</script>