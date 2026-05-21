<template>
  <div class="container mt-4">
    <div class="mb-3">
      <button class="btn btn-secondary" @click="goBack">← Back</button>
    </div>
    <h3>Overview</h3>
    <p>{{ description }}</p>

    <h3>Active Drives</h3>

    <table class="table table-bordered mt-3">
      <thead>
        <tr>
          <th>Job Role</th>
          <th>Location</th>
          <th>Package</th>
          <th>Deadline</th>
          <th>Action</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="drive in drives" :key="drive.drive_id">
          <td>{{ drive.job_title }}</td>
          <td>{{ drive.location }}</td>
          <td>{{ drive.package }}</td>
          <td>{{ drive.deadline }}</td>

          <td>
            <button class="btn btn-info btn-sm" @click="viewDrive(drive.drive_id)">
              View Details
            </button>
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
      drives: [],
      description: null,
    }
  },
  methods: {
    goBack() {
      this.$router.back()
    },
    viewDrive(driveId) {
      this.$router.push(`/drive/${driveId}`)
    },
  },

  async mounted() {
    const token = localStorage.getItem('studentToken')

    const companyId = this.$route.params.id

    const res = await fetch(`http://127.0.0.1:5000/api/company/${companyId}/drives`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    const data = await res.json()

    this.drives = data.drives
    this.description = data.description
  },
}
</script>
