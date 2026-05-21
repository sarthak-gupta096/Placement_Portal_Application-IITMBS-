<template>
  <div class="container mt-4">
    <h2 class="mb-4">Manage Placement Drives</h2>
    <div>
      <button class="btn btn-outline-secondary" @click="$router.back()">← Back</button>
    </div>
    <br />

    <table class="table table-bordered table-striped">
      <thead class="table-dark">
        <tr>
          <th>Drive Name</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="drive in drives" :key="drive.drive_id">
          <td>{{ drive.job_title }}</td>

          <td>
            <span class="badge" :class="drive.status === 'approved' ? 'bg-success' : 'bg-warning'">
              {{ drive.status }}
            </span>
          </td>

          <td>
            <button
              v-if="drive.status === 'pending'"
              class="btn btn-success btn-sm me-2"
              @click="approveDrive(drive.drive_id)"
            >
              Approve
            </button>

            <button
              v-if="drive.status === 'pending'"
              class="btn btn-danger btn-sm"
              @click="rejectDrive(drive.drive_id)"
            >
              Reject</button
            >&nbsp;

            <button class="btn btn-primary btn-sm" @click="viewDrive(drive.drive_id)">
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
  name: 'ManageDrives',

  data() {
    return {
      drives: [],
    }
  },

  async mounted() {
    this.fetchDrives()
  },

  methods: {
    async fetchDrives() {
      const token = localStorage.getItem('adminToken')

      const response = await fetch('http://127.0.0.1:5000/drives', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      const data = await response.json()

      this.drives = data.drives
    },

    async approveDrive(id) {
      if (!confirm('Approve this drive?')) return

      const token = localStorage.getItem('adminToken')

      await fetch(`http://127.0.0.1:5000/drives/${id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          action: 'approve',
        }),
      })

      this.fetchDrives()
    },

    async rejectDrive(id) {
      if (!confirm('Reject this drive?')) return
      const token = localStorage.getItem('adminToken')

      await fetch(`http://127.0.0.1:5000/drives/${id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          action: 'reject',
        }),
      })

      this.fetchDrives()
    },

    viewDrive(id) {
      this.$router.push(`/admin/drive/${id}`)
    },
    goBack() {
      this.$router.push('/admin/dashboard')
    },
  },
}
</script>
