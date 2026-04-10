<template>
    <nav class="navbar navbar-dark px-3" style="background-color: #3852B4;">
      <span class="navbar-brand" style="cursor: pointer;" @click="$router.push('/doctor')">Welcome, {{doctorName}}</span>
      <button class="btn btn-danger" @click="logout">Logout</button>
    </nav>
</template>


<script>

import API from '../services/api'

export default {
    data() {
        return {
            doctorName: ''
        }
    },
    mounted() {
        this.fetchProfile()
    },
    methods: {
        async fetchProfile() {
            const res = await API.get('/doctor/profile')
            this.doctorName = res.data.name
        },
        logout() {
            localStorage.removeItem('token')
            this.$router.push('/login')
        }
    }
}
</script>