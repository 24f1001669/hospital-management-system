<template>
    <div class="container mt-5">
        <h3 class="text-center mb-4">Add a new Doctor</h3>
        <div class="d-flex justify-content-center">
            <form @submit.prevent="createDoctor" class="card p-4" style="width: 400px; border: 2px solid black; border-radius: 20px;">
                <label>Username</label>
                <input style="border: 1px solid gray" required v-model="doctor.username" class="form-control mb-3">
                <label>Password</label>
                <input style="border: 1px solid gray" type="password" required v-model="doctor.password" class="form-control mb-3">
                <label>Full Name</label>
                <input required v-model="doctor.name" class="form-control mb-3" style="border: 1px solid gray">
                <label>Department</label>
                <select required v-model="doctor.department_id" class="form-select mb-3" style="border: 1px solid gray">
                  <option disabled value="">Select Department</option>
                  <option v-for="d in departments" :key="d.id" :value="d.id">
                    {{ d.name }}
                  </option>
                </select>
                <label>Specialization</label>
                <input required v-model="doctor.specialization" class="form-control mb-3" style="border: 1px solid gray">
                <label>Availability</label>
                <input required v-model="doctor.availability" class="form-control mb-3" style="border: 1px solid gray">
                <button class="btn btn-success mt-3" @click="createDoctor" type="submit">Create</button>
            </form>
        </div>
    </div>
</template>

<script>
import Navbar from '../components/AdminNavbar.vue'
import API from '../services/api'

export default {
  components: { Navbar },

  data() {
    return {
      doctor: {},
      departments: []
    }
  },

  mounted() {
    this.fetchDepartments()
  },

  methods: {
    async fetchDepartments() {
      const res = await API.get('/admin/departments')
      this.departments=res.data
    },

    async createDoctor() {
      await API.post('/admin/doctor', this.doctor)
      this.$router.push('/admin')
    }
  }
}
</script>