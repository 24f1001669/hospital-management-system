<template>
  <div class="container mt-5">
    <h4 class="text-center mb-4">Patient History</h4>
    <div class="mb-4">
      <p><b>Patient:</b> {{ patientName }}</p>
      <p><b>Doctor:</b> {{ doctorName }}</p>
      <p><b>Department:</b> {{ department }}</p>
    </div>
    <div class="card p-4" style="border-radius: 10px; border: 2px solid black;">
      <table class="table table-stripped" >
        <thead>
          <tr>
            <th>Date</th>
            <th>Diagnosis</th>
            <th>Prescription</th>
            <th>Tests</th>
            <th>Medicines</th>
          </tr>
        </thead>

        <tbody class="table-group-divider">
          <tr v-if="history.length === 0">
            <td colspan="5" class="text-center">No history found</td>
          </tr>

          <tr v-for="h in history" :key="h.id">
            <td>{{ h.date }}</td>
            <td>{{ h.diagnosis }}</td>
            <td>{{ h.prescription }}</td>
            <td>{{ h.tests }}</td>
            <td>{{ h.medicines }}</td>
          </tr>
        </tbody>
      </table>

    </div>
  </div>
</template>

<script>
import API from '../services/api'

export default {
  data() {
    return {
      history: [],
      patientName: '',
      doctorName: '',
      department: ''
    }
  },

  mounted() {
    this.fetchHistory()
  },

  methods: {
    async fetchHistory() {
      const id = this.$route.params.patientId
      const res = await API.get(`/doctor/patient-history/${id}`)

      this.patientName = res.data.patient_name
      this.history = res.data.history

      if (this.history.length > 0) {
        this.doctorName = this.history[0].doctor_name
        this.department = this.history[0].department
      }
    }
  }
}
</script>