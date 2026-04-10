<template>
  <div>
    <PatientNavbar />

    <div class="container mt-4">
      <h4 class="mb-4">Department of {{ department.name }}</h4>

      <div class="card p-3 mb-4" style="border: 2px solid black; border-radius: 10px;">
        <h5>Overview</h5>
        <p class="mt-2">{{ department.description }}</p>
      </div>

      <div class="card p-3" style="border: 2px solid black; border-radius: 10px;">
        <h5>Doctors List</h5>

        <div v-if="doctors.length === 0" class="text-center fw-bold fs-5 text-danger">
          No doctors available
        </div>

        <div v-for="d in doctors" :key="d.id"
             class="d-flex justify-content-between align-items-center p-2 mb-2"
             style="border: 1px solid gray;">

          <div>
            <div>{{ d.name }}</div>
            <small class="text-muted">{{ d.specialization }}</small>
          </div>

          <div class="d-flex gap-3">
            <button class="btn btn-primary me-2"
                    @click="checkAvailability(d.id)">
              Check Availability
            </button>
          </div>

        </div>
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
      department: {},
      doctors: []
    }
  },

  mounted() {
    this.fetchDepartment()
    this.fetchDoctors()
  },

  methods: {

    async fetchDepartment() {
      const id = this.$route.params.id
      const res = await API.get(`/patient/department/${id}`)
      this.department = res.data
    },

    async fetchDoctors() {
      const id = this.$route.params.id
      const res = await API.get(`/patient/department/${id}/doctors`)
      this.doctors = res.data
    },

      checkAvailability(id) {
        console.log("Doctor ID:",id)
      this.$router.push(`/patient/doctor-availability/${id}`)
    }
  }
}
</script>