<template>
  <div class="container mt-4">
    <button class="btn btn-secondary mb-3" @click="$router.back()">← Back</button>

    <h2 class="mb-4">Drive Details</h2>

    <div class="card mb-4">
      <div class="card-body">
        <h4>Job Title: {{ drive?.job_title }}</h4>
        <br />

        <p><b>Description:</b> {{ drive?.description }}</p>
        <p><b>Location:</b> {{ drive?.location }}</p>
        <p><b>Package:</b> {{ drive?.package }} (LPA)</p>
        <p><b>Minimum CGPA:</b> {{ drive?.min_cgpa }}</p>
        <p><b>Deadline:</b> {{ drive?.deadline }}</p>
        <p><b>Eligible Branches:</b> {{ drive?.eligible_branches }}</p>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h5>Applicants</h5>
      </div>

      <div class="card-body">
        <table class="table table-bordered">
          <thead class="table-dark">
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Branch</th>
              <th>CGPA</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="student in applicants" :key="student.id">
              <td>{{ student.name }}</td>
              <td>{{ student.email }}</td>
              <td>{{ student.branch }}</td>
              <td>{{ student.cgpa }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      drive: {},
      applicants: [],
    }
  },

  async mounted() {
    this.fetchDriveDetails()
  },

  methods: {
    async fetchDriveDetails() {
      const token = localStorage.getItem('adminToken')
      const driveId = this.$route.params.id

      const response = await fetch(`http://127.0.0.1:5000/drives/${driveId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      const data = await response.json()

      this.drive = data.drive
      this.applicants = data.applicants
      console.log(this.drive)
    },
  },
}
</script>
