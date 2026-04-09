<template>
  <div class="container mt-5">

    <h3 class="text-center mb-5">Login</h3>

    <div class="d-flex justify-content-center">
      <form @submit.prevent="login"
            class="card p-4"
            style="width: 350px; border-radius: 15px; border: 2px solid black;">

        <label class="mt-1">Username</label>
        <input type="username" style="border: 1px solid gray" v-model="form.username" class="form-control mb-4" required>

        <label class="mt-1">Password</label>
        <input style="border: 1px solid gray" type="password" v-model="form.password" class="form-control mb-4" required>

        <button class="mt-2 btn btn-primary">Login</button>
        <p class="mt-3 text-center">
          Don't have an account?
          <span style="color: blue; cursor: pointer; font-weight: bold;" @click="$router.push('/register')">
            Register
          </span>
        </p>
        <p v-if="error" class="text-danger mt-2 text-center fw-bold">{{ error }}</p>

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
        username: '',
        password: ''
      },
      error: ''
    }
  },

  methods: {
    async login() {
      try {
        const res = await API.post('/auth/login', this.form)

        const token = res.data.token
        localStorage.setItem('token', token)

        const decoded = JSON.parse(atob(token.split('.')[1]))

        if (decoded.role === 'admin') {
          this.$router.push('/admin')
        } else if (decoded.role === 'doctor') {
          this.$router.push('/doctor')
        }

      } catch (err) {
        this.error = 'Invalid credentials'
      }
    }
  }
}
</script>