<template>
  <div class="container mt-4">
    <h3 class="mb-3">Placement History</h3>
    <br />

    <button class="btn btn-secondary me-2" @click="goBack">← Go Back</button><br /><br />
    <table class="table table-bordered table-hover">
      <thead class="table-dark">
        <tr>
          <th>Company</th>
          <th>Job Title</th>
          <th>Status</th>
          <th>Applied On</th>
          <th>Salary</th>
          <th>Location</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="item in history" :key="item.application_id">
          <td>{{ item.company_name }}</td>

          <td>{{ item.job_title }}</td>

          <td>
            <span
              class="badge"
              :class="{
                'bg-light text-dark': item.drive_status === 'approved',
                'bg-success': item.drive_status === 'shortlisted',
                'bg-danger': item.drive_status === 'rejected',
                'bg-warning text-dark': item.drive_status === 'waiting',
              }"
            >
              {{ item.drive_status }}
            </span>
          </td>

          <td>{{ item.applied_on }}</td>

          <td>{{ item.salary }}</td>

          <td>{{ item.location }}</td>
        </tr>

        <tr v-if="history.length === 0">
          <td colspan="6" class="text-center">No placement history found</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      history: [],
    }
  },

  async mounted() {
    this.fetchHistory()
  },

  methods: {
    async fetchHistory() {
      const token = localStorage.getItem('studentToken')

      const response = await fetch('http://localhost:5000/student/history', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      const data = await response.json()

      this.history = data.placement_history
    },
  },
}
</script>
