<template>
  <div class="container mt-5">

    <h3 class="text-center mb-5">Register</h3>

    <div class="d-flex justify-content-center">
      <form @submit.prevent="register"
            class="card p-4"
            style="width: 350px; border-radius: 15px; border: 2px solid black;">

        <label>Name</label>
        <input style="border: 1px solid gray" v-model="form.name" class="form-control mb-4" required>
        <label>Contact</label>
        <input style="border: 1px solid gray" v-model="form.contact" class="form-control mb-4" required>
        <label>Username</label>
        <input style="border: 1px solid gray" v-model="form.username" class="form-control mb-4" required>
        <label>Password</label>
        <input style="border: 1px solid gray" type="password" v-model="form.password" class="form-control mb-4" required>

        <button class="btn btn-success mt-2">Register</button>

        <p class="mt-3 text-center">
          Already have an account?
          <span style="color: blue; cursor: pointer; font-weight: bold;" @click="$router.push('/')">
            Sign in
          </span>
        </p>

        <p v-if="error" class="text-danger fw-bold text-center">{{ error }}</p>

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
        name: '',
        contact: '',
        username: '',
        password: ''
      },
      error: ''
    }
  },

  methods: {
    async register() {
      try {
        await API.post('/auth/register', this.form)

        alert("Registration successful")
        this.$router.push('/')

      } catch (err) {
        this.error = err.response?.data?.message || 'Registration failed'
      }
    }
  }
}
</script>