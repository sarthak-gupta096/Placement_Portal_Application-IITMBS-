<template>
  <div class="container mt-4">
    <h2>Received Applications</h2>

    <div v-if="drive">
      <h5>Job Title: {{ drive.job_title }}</h5>
    </div>
    <br />
    <button class="btn btn-secondary me-2" @click="goBack">← Go Back</button>

    <table class="table table-bordered mt-3">
      <thead>
        <tr>
          <th>Name</th>
          <th>Branch</th>
          <th>CGPA</th>
          <th>Email</th>

          <th>Resume</th>
          <th>Action</th>
          <th>Update</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="app in applicants" :key="app.application_id">
          <td>{{ app.name }}</td>
          <td>{{ app.branch }}</td>
          <td>{{ app.cgpa }}</td>
          <td>{{ app.email }}</td>
          <td><a :href="app.resume" target="_blank" class="btn btn-sm btn-info">View Resume</a></td>
          <td>
            <select class="form-select form-select-sm" v-model="app.status">
              <option value="Waiting">Waiting</option>
              <option value="Shortlisted">Shortlisted</option>
              <option value="Rejected">Rejected</option>
            </select>
          </td>

          <td>
            <button class="btn btn-primary btn-sm" @click="updateStatus(app)">Update</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      drive: null,
      applicants: [],
    }
  },
  methods: {
    goBack() {
      this.$router.back()
    },

    async fetchApplications() {
      const driveId = this.$route.params.id
      const token = localStorage.getItem('companyToken')

      const response = await fetch(`http://127.0.0.1:5000/drives/${driveId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      const data = await response.json()

      this.drive = data.drive
      this.applicants = data.applicants
    },

    async updateStatus(app) {
      try {
        console.log('Application object:', app)
        console.log('Application ID:', app.application_id)

        const token = localStorage.getItem('companyToken')

        const response = await fetch(
          `http://localhost:5000/company/applications/${app.application_id}`,
          {
            method: 'PATCH',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              status: app.status,
            }),
          },
        )

        const data = await response.json()

        if (response.ok) {
          alert('Application status updated successfully!')
        } else {
          alert(data.message || 'Failed to update status')
        }
      } catch (error) {
        console.error(error)
        alert('Error updating application status')
      }
    },
  },

  async mounted() {
    this.fetchApplications()
  },
}
</script>
