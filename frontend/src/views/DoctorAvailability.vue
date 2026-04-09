<template>
  <div class="container mt-5">

    <h4 class="text-center mb-4">Doctor's Availability</h4>

    <div class="card p-4" style="border: 2px solid black; border-radius: 10px;">

      <table class="table text-center">
        <thead>
          <tr>
            <th>Date</th>
            <th>Morning</th>
            <th>Evening</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="day in availability" :key="day.date">
            <td>
              <span class="badge bg-secondary p-2">{{ day.date }}</span>
            </td>

            <td>
              <button
                @click="toggleSlot(day, 'morning')"
                :class="day.morning ? 'btn btn-success' : 'btn btn-outline-danger'"
                style="width: 175px"
              >
                08:00am - 12:00am
              </button>
            </td>

            <td>
              <button
                @click="toggleSlot(day, 'evening')"
                :class="day.evening ? 'btn btn-success' : 'btn btn-outline-danger'"
                style="width: 175px"
              >
                04:00pm - 09:00pm
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div class="text-end mt-3">
        <button class="btn btn-success" style="width:100px" @click="saveAvailability">
          Save
        </button>
      </div>

    </div>
  </div>
</template>

<script>
import API from '../services/api'

export default {
  data() {
    return {
      availability: []
    }
  },

  mounted() {
    this.generateDates()
    this.fetchAvailability()
  },

  methods: {

    generateDates() {
        const today = new Date()

        for (let i = 0; i < 7; i++) {
            let d = new Date()
            d.setDate(today.getDate() + i)

            const day = String(d.getDate()).padStart(2, '0')
            const month = String(d.getMonth() + 1).padStart(2, '0')
            const year = d.getFullYear()

            const formatted = `${day}-${month}-${year}`

            this.availability.push({
            date: formatted,
            morning: false,
            evening: false
            })
        }
    },

    toggleSlot(day, slot) {
      day[slot] = !day[slot]
    },

    async fetchAvailability() {
      try {
        const res = await API.get('/doctor/availability')

        res.data.forEach(saved => {
          const match = this.availability.find(d => d.date === saved.date)

          if (match) {
            match.morning = saved.morning
            match.evening = saved.evening
          }
        })

      } catch (err) {
        console.log("No previous data")
      }
    },

    async saveAvailability() {
      await API.post('/doctor/availability', this.availability)
      this.$router.push('/doctor')
    }

  }
}
</script>