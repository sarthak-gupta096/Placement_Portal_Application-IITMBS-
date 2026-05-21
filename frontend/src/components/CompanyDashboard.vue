<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top shadow">
      <div class="container">
        <router-link class="navbar-brand fw-bold" to="/company-dashboard">
          Company Dashboard
        </router-link>

        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto align-items-lg-center">
            <li class="nav-item ms-lg-3">
              <button class="btn btn-outline-danger btn-sm" @click="logout">Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container dashboard-wrapper">
      <div class="card shadow-lg border-0 p-4 mb-4">
        <h3 class="fw-bold mb-3">{{ company?.name }}</h3>
        <p class="text-muted">
          {{ company?.description }}
        </p>
      </div>

      <div class="card border-0 shadow-sm p-4 action-container">
        <div class="d-flex flex-column flex-md-row justify-content-between align-items-center">
          <div>
            <h5 class="fw-bold mb-1">Manage Placement Drives</h5>
            <p class="text-muted mb-0">Create and manage your campus recruitment drives.</p>
          </div>

          <button class="btn btn-outline-primary create-drive-btn" @click="goToCreateDrive">
            <i class="bi bi-plus-circle me-2"></i>
            Create Drive
          </button>
        </div>
      </div>

      <br /><br />

      <div class="card border-0 shadow-sm p-4 action-container">
        <div class="card shadow-sm border-0">
          <div class="card-header bg-warning text-dark">
            <h6 class="mb-0 fw-bold">📋 Upcoming Drives</h6>
          </div>
          <br />
          <div class="col-12">
            <div class="card-body p-0">
              <div v-if="upcomingDrives.length === 0" class="text-center py-5">
                <i class="bi bi-check-circle text-success fs-1 mb-3"></i>
                <h5 class="text-muted">No upcoming drives</h5>
              </div>
              <div class="table-responsive" v-if="upcomingDrives.length != 0">
                <table class="table table-hover mb-0">
                  <thead class="table-light">
                    <tr>
                      <th>Sr. No.</th>
                      <th>Job Title</th>
                      <th>Status</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="drive in upcomingDrives" :key="drive.id">
                      <td>{{ drive.drive_id }}</td>
                      <td>{{ drive.job_title }}</td>
                      <td v-if="drive.status === 'approved'">
                        <span class="badge bg-success">{{ drive.status }}</span>
                      </td>
                      <td v-else>
                        <span class="badge bg-warning">{{ drive.status }}</span>
                      </td>

                      <td>
                        <button
                          class="btn btn-primary btn-sm me-2"
                          @click="$router.push(`/drive/${drive.drive_id}/applications`)"
                        >
                          View Details
                        </button>

                        <button
                          class="btn btn-success btn-sm"
                          v-if="drive.status === 'approved'"
                          @click="markComplete(drive.drive_id)"
                        >
                          Mark as Complete
                        </button>

                        <span v-if="drive.status === 'closed'" class="badge bg-secondary">
                          Completed
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <br /><br />

          <!-- Closed Drives -->
          <div class="card-header bg-warning text-dark">
            <h6 class="mb-0 fw-bold">📋 Closed Drives</h6>
          </div>
          <br />

          <div class="col-12">
            <div class="card-body p-0">
              <div v-if="closedDrives.length === 0" class="text-center py-5">
                <i class="bi bi-check-circle text-success fs-1 mb-3"></i>
                <h5 class="text-muted">No closed drives</h5>
              </div>
              <div class="table-responsive" v-if="closedDrives.length != 0">
                <table class="table table-hover mb-0">
                  <thead class="table-light">
                    <tr>
                      <th>Sr. No.</th>
                      <th>Drive Name</th>
                      <th>Applicants Applied</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="drive in closedDrives" :key="drive.id">
                      <td>{{ drive.drive_id }}</td>
                      <td>{{ drive.job_title }}</td>
                      <td>{{ drive.applicants_count }}</td>
                      <td>
                        <button class="btn btn-success btn-sm" @click="reopenDrive(drive.drive_id)">
                          Update
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CompanyDashboard',

  data() {
    return {
      company: {},
      drives: [],
      totalDrives: 0,
      totalApplicants: 0,
      closedDrives: [],
      upcomingDrives: [],
    }
  },

  async mounted() {
    await this.fetchDashboard()
  },

  methods: {
    async fetchDashboard() {
      try {
        const token = localStorage.getItem('companyToken')

        const response = await fetch('http://127.0.0.1:5000/api/company-dashboard', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.message)
        }

        this.company = data.company
        this.drives = data.drives
        this.totalDrives = data.total_drives
        this.totalApplicants = data.total_applicants

        this.upcomingDrives = data.drives.filter((d) => d.status !== 'closed')

        this.closedDrives = data.drives.filter((d) => d.status === 'closed')
      } catch (error) {
        console.error('Dashboard Error:', error)
      }
    },

    goToCreateDrive() {
      this.$router.push('/company/create-drive')
    },

    logout() {
      localStorage.removeItem('companyToken')
      this.$router.push('/company-login')
    },

    async markComplete(drive_id) {
      if (!confirm('Mark this drive as completed?')) return

      const token = localStorage.getItem('companyToken')

      const response = await fetch(`http://127.0.0.1:5000/drives/${drive_id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ action: 'complete' }),
      })

      const data = await response.json()

      alert(data.message)

      await this.fetchDashboard()
    },
    async reopenDrive(id) {
      if (!confirm('Reopen this drive?')) return

      const token = localStorage.getItem('companyToken')

      const response = await fetch(`http://127.0.0.1:5000/drives/${id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          action: 'reopen',
        }),
      })

      const data = await response.json()

      alert(data.message)

      await this.fetchDashboard()
    },
  },
}
</script>

<style>
.dashboard-wrapper {
  padding-top: 100px;
}

.fab-btn {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 65px;
  height: 65px;
  border-radius: 50%;
  border: none;
  background: linear-gradient(135deg, #0d6efd, #6610f2);
  color: white;
  font-size: 24px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  z-index: 1050;
}

.fab-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
}
</style>
