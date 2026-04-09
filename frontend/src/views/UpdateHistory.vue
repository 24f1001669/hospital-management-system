<template>
  <div class="container mt-5">

    <h4 class="mb-4 text-center">Update Patient History</h4>

    <div class="d-flex justify-content-center">
        
        <form @submit.prevent="saveTreatment" class="card p-4"
        style="width: 500px; border-radius: 15px; border: 2px solid black;">
            <p><b>Patient Name:</b> {{ patientName }}</p>
            <div class="mb-3">
            <label>Visit Type</label>
            <input required style="border: 1px solid gray" v-model="form.visit_type" class="form-control mb-1">
            </div>

            <div class="mb-3">
            <label>Tests Done</label>
            <input required style="border: 1px solid gray" v-model="form.tests" class="form-control mb-1">
            </div>

            <div class="mb-3">
            <label>Diagnosis</label>
            <input required style="border: 1px solid gray" v-model="form.diagnosis" class="form-control mb-1">
            </div>

            <div class="mb-3">
            <label>Prescription</label>
            <input required style="border: 1px solid gray" v-model="form.prescription" class="form-control mb-1">
            </div>

            <div class="mb-3">
            <label>Medicines</label>
            <input required style="border: 1px solid gray" v-model="form.medicines" class="form-control mb-2">
            </div>

            <button class="btn btn-success">Save</button>

        </form>

    </div>
  </div>
</template>

<script>
import API from '../services/api'

export default {
  data() {
    return {
      form: {
        visit_type: '',
        tests: '',
        diagnosis: '',
        prescription: '',
        medicines: ''
      },
      patientName: ''
    }
  },

  mounted() {
      this.fetchDetails()
      this.fetchTreatment()
  },

    methods: {
    async fetchTreatment() {
        const id = this.$route.params.appointmentId

        const res = await API.get(`/doctor/treatment/${id}`)

        if (res.data && Object.keys(res.data).length > 0) {
            this.form = {
            visit_type: res.data.visit_type || '',
            tests: res.data.tests || '',
            diagnosis: res.data.diagnosis || '',
            prescription: res.data.prescription || '',
            medicines: res.data.medicines || ''
            }
        }
        },
    
    async fetchDetails() {
      const id = this.$route.params.appointmentId
      const res = await API.get(`/doctor/appointment/${id}`)
      this.patientName = res.data.patient_name
    },

    async saveTreatment() {
      const id = this.$route.params.appointmentId

      await API.post(`/doctor/treatment/${id}`, this.form)

      alert("Saved successfully")
      this.$router.push('/doctor')
    }
  }
}
</script>