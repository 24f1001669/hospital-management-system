<template>
    <div class="container mt-5">
      <div class="position-relative mb-5">
        <h3 class="text-center">Patient History</h3>
        <button class="btn btn-secondary position-absolute top-0 end-0" @click="$router.push('/admin')">Back</button>
      </div>
      <div class="d-flex gap-2 justify-content-center">
        <b class="text-center mb-2">Patient Name: </b>
        <p>{{ patient }}</p>
      </div>
      <div class="d-flex gap-2 justify-content-center">
        <b class="text-center mb-2">Doctor Name: </b>
        <p>{{ doctor }}</p>
      </div>
      <div class="d-flex gap-2 justify-content-center">
        <b class="text-center mb-5">Department: </b>
        <p>{{ department }}</p>
      </div>

      <table class="table table-striped">
        <thead>
          <tr>
            <th>Visit No.</th>
            <th>Visit Type</th>
            <th>Tests Done</th>
            <th>Diagnosis</th>
            <th>Prescription</th>
          </tr>
        </thead>
        <tbody class="table-group-divider">
          <tr v-for="(t, i) in treatments" :key="i">
            <td>{{ i + 1 }}</td>
            <td>{{ t.visit_type }}</td>
            <td>{{ t.test }}</td>
            <td>{{ t.diagnosis }}</td>
            <td>{{ t.prescription }}</td>
          </tr>
        </tbody>
      </table>
    </div>
</template>

<script>
import Navbar from '../components/AdminNavbar.vue'

export default {
  components: { Navbar },

  data() {
    return {
      patient: 'Mr. abcde',
      doctor: 'Dr. prst',
      department: 'Cardio',
      treatments: []
    }
  }
}
</script>