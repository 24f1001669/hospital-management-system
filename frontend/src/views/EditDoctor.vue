<template>
    <div class="container mt-5">
        <h3 class="text-center mb-5">Edit Doctor</h3>
        <div class="d-flex justify-content-center">
            <form @submit.prevent="createDoctor" class="card p-4" style="width: 400px; border: 2px solid black; border-radius: 20px;">
                <label>Full Name</label>
                <input required v-model="doctor.name" class="form-control mb-4" style="border: 1px solid gray">
                <label>Department</label>
                <select required v-model="doctor.department_id" class="form-select mb-4" style="border: 1px solid gray">
                  <option disabled value="">Select Department</option>
                  <option v-for="d in departments" :key="d.id" :value="d.id">
                    {{ d.name }}
                  </option>
                </select>
                <label>Specialization</label>
                <input required v-model="doctor.specialization" class="form-control mb-4" style="border: 1px solid gray">
                <label>Availability</label>
                <input required v-model="doctor.availability" class="form-control mb-4" style="border: 1px solid gray">
                <button class="btn btn-warning mt-2" @click="updateDoctor" type="submit">Update</button>
            </form>
        </div>
    </div>
</template>

<script>
import API from '../services/api'

export default {
  data() {
    return {
      doctor: {},
      departments: []
    }
  },

  mounted() {
    this.fetchDepartments()
    this.fetchDoctor()
  },

  methods: {
    async fetchDepartments() {
      const res = await API.get('/admin/departments')
      this.departments = res.data
    },

    async fetchDoctor() {
      const id = this.$route.params.id
      const res = await API.get(`/admin/doctor/${id}`)
      this.doctor = res.data
    },

    async updateDoctor() {
      const id = this.$route.params.id
      await API.put(`/admin/doctor/${id}`, this.doctor)
      this.$router.push('/admin')
    }
  }
}
</script>