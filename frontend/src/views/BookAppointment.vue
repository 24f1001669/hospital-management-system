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

            <!-- MORNING -->
            <td>
              <button
                :disabled="!day.morning"
                @click="selectSlot(day.date, 'morning')"
                :class="getClass(day.date, 'morning', day.morning)"
                style="width: 175px"
              >
                08:00am - 12:00pm
              </button>
            </td>

            <!-- EVENING -->
            <td>
              <button
                :disabled="!day.evening"
                @click="selectSlot(day.date, 'evening')"
                :class="getClass(day.date, 'evening', day.evening)"
                style="width: 175px"
              >
                04:00pm - 09:00pm
              </button>
            </td>

          </tr>
        </tbody>
      </table>

      <div class="text-end mt-3">
        <button class="btn btn-success"
                style="width:100px"
                :disabled="!selected.date"
                @click="bookAppointment">
          Book
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
      availability: [],
      selected: {
        date: '',
        slot: ''
      }
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

    async fetchAvailability() {
      const doctorId = this.$route.params.id
      const res = await API.get(`/patient/doctor/${doctorId}/availability`)

      res.data.forEach(saved => {
        const match = this.availability.find(d => d.date === saved.date)

        if (match) {
          match.morning = saved.morning
          match.evening = saved.evening
        }
      })
    },

    selectSlot(date, slot) {
      this.selected.date = date
      this.selected.slot = slot
    },

    getClass(date, slot, available) {
      if (!available) return 'btn btn-outline-danger'

      if (this.selected.date === date && this.selected.slot === slot) {
        return 'btn btn-success'
      }

      return 'btn btn-outline-success'
    },

    async bookAppointment() {
      const doctorId = this.$route.params.id

      await API.post('/patient/appointment', {
        doctor_id: doctorId,
        date: this.selected.date,
        slot: this.selected.slot
      })

      alert("Appointment booked")
      this.$router.push('/patient')
    }

  }
}
</script>