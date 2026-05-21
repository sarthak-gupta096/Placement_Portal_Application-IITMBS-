<template>
  <div class="container mt-4">
    <h2>Approved Drives</h2>
    <br />

    <button class="btn btn-secondary mb-3" @click="$router.back()">← Back</button>

    <table class="table table-bordered">
      <thead class="table-dark">
        <tr>
          <th>Company</th>
          <th>Job Title</th>
          <th>Location</th>
          <th>Package (LPA)</th>
          <th>Deadline</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="drive in drives" :key="drive.drive_id">
          <td>{{ drive.company_name }}</td>
          <td>{{ drive.job_title }}</td>
          <td>{{ drive.location }}</td>
          <td>{{ drive.package }}</td>
          <td>{{ drive.deadline }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      drives: [],
    }
  },

  mounted() {
    this.fetchApprovedDrives()
  },

  methods: {
    async fetchApprovedDrives() {
      const token = localStorage.getItem('adminToken')

      const response = await fetch('http://127.0.0.1:5000/drives', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      const data = await response.json()

      this.drives = data.drives.filter((d) => d.status === 'approved')
    },
  },
}
</script>
