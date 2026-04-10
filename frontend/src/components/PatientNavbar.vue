<template>
  <nav class="navbar navbar-dark px-3" style="background-color: #6E1A37;">
    <span class="navbar-brand" style="cursor: pointer;" @click="$router.push('/patient')">Welcome, {{name}}</span>
    <div class="d-flex gap-4">
      <span class="btn btn-light" @click="$router.push('/edit-profile')">Edit Profile</span>
      <span class="btn btn-light" @click="$router.push('/history')">History</span>
      <span class="btn btn-danger" @click="logout">
        Logout
      </span>
    </div>
  </nav>
</template>

<script>
import API from '../services/api'

export default {
  data() {
    return {
      name: ''
    }
  },

  mounted() {
    this.fetchProfile()
  },

  methods: {
    async fetchProfile() {
      const res = await API.get('/patient/profile')
      console.log(res.data)
      this.name = res.data.name
    },

    logout() {
      localStorage.removeItem('token')
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.link {
  cursor: pointer;
  font-size: 14px;
}

.link:hover {
  text-decoration: underline;
}
</style>