<template>
  <div>
    <nav class="navbar navbar-dark bg-dark">
      <div class="container-fluid">
        <span class="navbar-brand">JobSyncr</span>
      </div>
    </nav>

    <div class="container mt-4">
      <h3>All Applications</h3>
      <br />
      <button class="btn btn-dark" @click="goBack">← Back</button>

      <table class="table table-bordered mt-3">
        <thead>
          <tr>
            <th>Sr. No.</th>
            <th>Student Name</th>
            <th>Department</th>
            <th>Company</th>
            <th>Job Title</th>
            <th>Status</th>
            <th>Applied On</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="app in applications" :key="app.id">
            <td>{{ app.application_id }}.</td>
            <td>{{ app.student_name }}</td>
            <td>{{ app.department }}</td>
            <td>{{ app.company_name }}</td>
            <td>{{ app.job_title }}</td>
            <td>{{ app.status }}</td>
            <td>{{ app.applied_on }}</td>
            <td>
              <a :href="app.resume" target="_blank" class="btn btn-sm btn-info"> View Resume </a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      applications: [],
    }
  },

  methods: {
    goBack() {
      this.$router.push('/admin/dashboard')
    },

    async fetchApplications() {
      console.log(app)
      const token = localStorage.getItem('adminToken')

      const response = await fetch('http://127.0.0.1:5000/admin/all_applications', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      const data = await response.json()
      this.applications = data.applications
    },
  },

  async mounted() {
    this.fetchApplications()
  },
}
</script>
