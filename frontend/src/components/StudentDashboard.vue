<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand">JobSyncr</a>

      <div class="ms-auto">
        <button class="btn btn-secondary" @click="$router.push('/student/profile')">
          Edit Profile
        </button>
        &nbsp;&nbsp;&nbsp;

        <router-link to="/student/history" style="text-decoration: none; color: aliceblue">
          History </router-link
        >&nbsp;&nbsp;&nbsp;

        <button class="btn btn-danger" @click="logout">Logout</button>
      </div>
    </div>
  </nav>

  <div class="container mt-4">
    <h2 class="mb-4">Welcome {{ studentName }}</h2>
    <hr />

    <h3>Organizations</h3>

    <table class="table table-bordered mt-3">
      <thead>
        <tr>
          <th>Company Name</th>
          <th>Action</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="company in companies" :key="company.id">
          <td>{{ company.name }}</td>

          <td>
            <button class="btn btn-primary btn-sm" @click="viewDetails(company.user_id)">
              View Details
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <h3 class="mt-5">My Applications</h3>

    <table class="table table-bordered mt-3">
      <thead>
        <tr>
          <th>Company</th>
          <th>Job Title</th>
          <th>Status</th>
          <th>Applied On</th>
          <th>Deadline</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="app in appliedDrives" :key="app.application_id">
          <td>{{ app.company_name }}</td>
          <td>{{ app.job_title }}</td>
          <td>{{ app.status }}</td>
          <td>{{ app.applied_on }}</td>
          <td>{{ app.deadline }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      studentName: '',
      companies: [],
      appliedDrives: [],
    }
  },

  methods: {
    logout() {
      localStorage.removeItem('studentToken')
      localStorage.removeItem('studentName')

      this.$router.push('/')
    },
    async fetchAppliedDrives() {
      const token = localStorage.getItem('studentToken')

      const res = await fetch('http://127.0.0.1:5000/student/applications', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      const data = await res.json()

      this.appliedDrives = data.my_applications
    },
    async fetchCompanies() {
      const token = localStorage.getItem('studentToken')

      const res = await fetch('http://127.0.0.1:5000/api/company', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      const data = await res.json()

      this.companies = data['registered-companies']
    },
    viewDetails(companyId) {
      this.$router.push(`/company/${companyId}/drives`)
    },

    viewCompany(companyId) {
      this.$router.push(`/company/${companyId}/drives`)
    },
  },

  mounted() {
    this.studentName = localStorage.getItem('studentName')

    this.fetchCompanies()
    this.fetchAppliedDrives()
  },
}
</script>
