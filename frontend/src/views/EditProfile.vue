<template>
  <div>
    <PatientNavbar />

    <div class="container mt-5">

      <h4 class="text-center mb-4">Edit Profile</h4>

      <div class="d-flex justify-content-center">
        <form @submit.prevent="updateProfile"
              class="card p-4"
              style="width: 400px; border: 2px solid black; border-radius: 15px;">

          <label>Name</label>
          <input v-model="form.name" class="form-control mb-3" required>

          <label>Contact</label>
          <input v-model="form.contact" class="form-control mb-4" required>

          <button class="btn btn-success">Save</button>

        </form>
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
      form: {
        name: '',
        contact: ''
      }
    }
  },

  mounted() {
    this.fetchProfile()
  },

  methods: {

    async fetchProfile() {
      const res = await API.get('/patient/profile')
      this.form = res.data
    },

    async updateProfile() {
      await API.put('/patient/profile', this.form)
      this.$router.push('/patient')
    }

  }
}
</script>