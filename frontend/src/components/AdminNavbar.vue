<template>
  <nav class="navbar navbar-dark bg-dark px-3">
    <span class="navbar-brand" style="cursor:pointer;" @click="$router.push('/admin')">Welcome, Admin</span>
    <span>
        <input v-model="searchQuery" style="
            height: 40px;
            width: 300px;
            border: none;
            padding: 15px;
            border-radius: 15px;
            margin-right: 15px;
            margin-top: 2px;
        " placeholder="Doctor, Patient, Department..."/>
        <button class="btn btn-primary mb-1 me-3" @click="handleSearch">Search</button>
        <button class="btn btn-danger mb-1" @click="logout">Logout</button>
    </span>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: ''
    }
  },
  methods: {
    handleSearch() {
      this.$emit('search', this.searchQuery)
    },
    logout() {
      localStorage.removeItem('token')
      this.$router.push('/login')
    }
  }
}
</script>