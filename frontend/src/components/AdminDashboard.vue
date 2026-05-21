<template>
  <div class="admin-dashboard">
    <nav class="navbar navbar-expand navbar-dark bg-primary shadow-sm fixed-top">
      <div class="container">
        <i class="bi bi-suitcase text-white fs-3"></i>&nbsp;
        <span class="navbar-brand fw-bold fs-5"> JobSyncr - Admin Dashboard </span>
        
        <div class="navbar-nav ms-auto">
          
          <router-link 
  to="/admin/search" 
  class="btn btn-primary d-inline-flex align-items-center gap-2"
>
  🔍 <span>Search Students / Companies</span>
</router-link>
          <button class="btn btn-outline-light btn-sm ms-4" @click="logout">Logout</button>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="container mt-5 pt-5">
      <div class="row justify-content-center">
        <div class="col-md-10">
          <h5 class="card-title text-center py-4 display-6">Overall Summary</h5>

          <!-- Stats Cards Row -->
          <div class="row g-4 mb-5">
            <div class="col-md-4">
              <router-link to="/admin/registered-students" class="text-decoration-none">
                <div
                  class="card h-100 bg-light shadow border-start border-primary border-2 hover-card"
                >
                  <div class="card-body text-center p-4">
                    <div class="fs-1 mb-3 text-primary">👨‍🎓</div>
                    <h3 class="display-5 fw-bold mb-1">{{ stats.total_reg_students || 0 }}</h3>
                    <p class="fs-5 fw-bold mb-0">Registered Students</p>
                    <small class="opacity-75">Approved students only</small>
                  </div>
                </div>
              </router-link>
            </div>

            <!-- Total Companies -->
            <div class="col-md-4">
              <router-link to="/admin/registered-companies" class="text-decoration-none">
                <div
                  class="card h-100 bg-light shadow border-start border-primary border-2 hover-card"
                >
                  <div class="card-body text-center p-4">
                    <div class="fs-1 mb-3 text-success">🏢</div>
                    <h3 class="display-5 fw-bold mb-1">{{ stats.total_reg_companies || 0 }}</h3>
                    <p class="fs-5 fw-bold mb-0">Registered Companies</p>
                    <small class="opacity-75">Approved companies only</small>
                  </div>
                </div>
              </router-link>
            </div>

            <div class="col-md-4">
              <router-link to="/admin/approved-drives" class="text-decoration-none">
                <div
                  class="card h-100 bg-light shadow border-start border-primary border-2 hover-card"
                >
                  <div class="card-body text-center p-4">
                    <div class="fs-1 mb-3 text-success">
                      <img
                        width="48"
                        height="48"
                        src="https://img.icons8.com/emoji/48/spiral-notepad-emoji.png"
                        alt="spiral-notepad-emoji"
                      />
                    </div>
                    <h3 class="display-5 fw-bold mb-1">{{ stats.total_approved_drives || 0 }}</h3>
                    <p class="fs-5 fw-bold mb-0">Total Drives</p>
                    <small class="opacity-75">Active drives only</small>
                  </div>
                </div>
              </router-link>
            </div>
          </div>
          <!-- Pending Students Section -->
          <div class="row justify-content-center">
            <div class="card shadow-sm border-0">
              <h5 class="card-title text-center py-4">Quick Actions</h5>
              <div class="col-12">
                <div class="card-header bg-warning text-dark">
                  <h6 class="mb-0 fw-bold">
                    📋 Pending Student Requests ({{ pendingStudents.length }})
                  </h6>
                </div>
                <div class="card-body p-0">
                  <div v-if="pendingStudents.length === 0" class="text-center py-5">
                    <i class="bi bi-check-circle text-success fs-1 mb-3"></i>
                    <h5 class="text-muted">No pending student requests</h5>
                  </div>
                  <div v-else class="table-responsive">
                    <table class="table table-hover mb-0">
                      <thead class="table-light">
                        <tr>
                          <th>Name</th>
                          <th>Roll No</th>
                          <th>Branch</th>
                          <th>CGPA</th>
                          <th>Status</th>
                          <th>Action</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="student in pendingStudents" :key="student.user_id">
                          <td>{{ student.full_name }}</td>
                          <td>{{ student.roll_number }}</td>
                          <td>{{ student.branch }}</td>
                          <td>{{ student.cgpa }}</td>
                          <td>
                            <span class="badge bg-warning">{{ student.status }}</span>
                          </td>
                          <td>
                            <button
                              class="btn btn-success btn-sm me-2"
                              v-if="student.status === 'pending'"
                              @click="approveStudent(student.user_id)"
                            >
                              Approve
                            </button>

                            <button
                              class="btn btn-danger btn-sm"
                              v-if="student.status === 'pending'"
                              @click="rejectStudent(student.user_id)"
                            >
                              Reject
                            </button>

                            <span v-if="student.status === 'approved'" class="badge bg-success">
                              Approved
                            </span>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>

              <br /><br />

              <!-- Pending Company Requests -->

              <div class="col-12">
                <div class="card-header bg-warning text-dark">
                  <h6 class="mb-0 fw-bold">
                    📋 Pending Company Requests ({{ pendingCompanies.length }})
                  </h6>
                </div>
                <div class="card-body p-0">
                  <div v-if="pendingCompanies.length === 0" class="text-center py-5">
                    <i class="bi bi-check-circle text-success fs-1 mb-3"></i>
                    <h5 class="text-muted">No pending company requests</h5>
                  </div>
                  <div v-else class="table-responsive">
                    <table class="table table-hover mb-0">
                      <thead class="table-light">
                        <tr>
                          <th>Name</th>
                          <th>Website</th>
                          <th>HR Name</th>
                          <th>HR Contact</th>
                          <th>About</th>
                          <th>Status</th>
                          <th>Action</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="company in pendingCompanies" :key="company.user_id">
                          <td>{{ company.name }}</td>
                          <td>{{ company.website }}</td>
                          <td>{{ company.hr_name }}</td>
                          <td>{{ company.hr_contact }}</td>
                          <td>{{ company.desc }}</td>

                          <td>
                            <span class="badge bg-warning">{{ company.status }}</span>
                          </td>
                          <td>
                            <button
                              class="btn btn-success btn-sm me-2"
                              v-if="company.status === 'pending'"
                              @click="approveCompany(company.user_id)"
                            >
                              Approve
                            </button>

                            <button
                              class="btn btn-danger btn-sm"
                              v-if="company.status === 'pending'"
                              @click="rejectCompany(company.user_id)"
                            >
                              Reject
                            </button>

                            <span v-if="company.status === 'approved'" class="badge bg-success">
                              Approved
                            </span>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <br /><br />

          <!-- Action Buttons -->
          <div class="row justify-content-center">
            <div class="col-md-8 text-center">
              <div class="card shadow-sm border-0">
                <div class="card-body py-5">
                  <h5 class="card-title mb-4">More Actions</h5>

                  <div class="row g-3">
                    <div class="col-md-6">
                      <button
                        class="btn btn-outline-primary w-100 py-3 fs-5"
                        @click="$router.push('/admin/applications')"
                      >
                        View Applications
                      </button>
                    </div>
                    <div class="col-md-6">
                      <button
                        class="btn btn-outline-success w-100 py-3 fs-5"
                        @click="$router.push('/admin/manage-drives')"
                      >
                        Manage Drives
                      </button>
                    </div>
                  </div>
                </div>
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
  name: 'AdminDashboard',
  data() {
    return {
      stats: {
        total_reg_students: 0,
        total_reg_companies: 0,
        total_approved_drives: 0,
      },

      loading: true,
      pendingStudents: [],
      pendingCompanies: [],
    }
  },
  async mounted() {
    ;(this.fetchDashboardStats(), this.fetchPendingStudents(), this.fetchPendingCompanies())
  },
  methods: {
    async fetchDashboardStats() {
      try {
        const token = localStorage.getItem('adminToken')
        const response = await fetch('http://127.0.0.1:5000/api/admin/dashboard', {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        })

        if (!response.ok) {
          throw new Error('Failed to fetch stats')
        }

        this.stats = await response.json()
      } catch (error) {
        console.error('Dashboard stats error:', error)
      } finally {
        this.loading = false
      }
    },

    goToDrives() {
      this.$router.push('/drives')
    },
    logout() {
      localStorage.removeItem('adminToken')
      this.$router.push('/')
    },

    async fetchPendingStudents() {
      try {
        const token = localStorage.getItem('adminToken')
        const response = await fetch('http://127.0.0.1:5000/api/admin/pending-students', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        if (!response.ok) throw new Error(`HTTP ${response.status}`)
        const result = await response.json()
        console.log('API Response:', result)
        this.pendingStudents = result.pending_students || []
        console.log('Loaded students:', this.pendingStudents.length)
      } catch (error) {
        console.error('Pending students error:', error)
      }
    },
    async fetchPendingCompanies() {
      try {
        const token = localStorage.getItem('adminToken')
        const response = await fetch('http://127.0.0.1:5000/api/admin/pending-companies', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        if (!response.ok) throw new Error(`HTTP ${response.status}`)
        const result = await response.json()
        console.log('API Response:', result)
        this.pendingCompanies = result.pending_companies || []
        console.log('Loaded companies:', this.pendingCompanies.length)
      } catch (error) {
        console.error('Pending companies error:', error)
      }
    },
    async approveStudent(id) {
      const token = localStorage.getItem('adminToken')

      await fetch(`http://127.0.0.1:5000/api/student/${id}`, {
        method: 'PATCH',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      this.fetchPendingStudents()
      this.fetchDashboardStats()
    },
    async rejectStudent(id) {
      if (!confirm('Reject this student request?')) return

      const token = localStorage.getItem('adminToken')

      await fetch(`http://127.0.0.1:5000/api/student/${id}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      this.fetchPendingStudents()
      this.fetchDashboardStats()
    },
    async approveCompany(id) {
      const token = localStorage.getItem('adminToken')

      await fetch(`http://127.0.0.1:5000/api/company/${id}`, {
        method: 'PATCH',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      this.fetchPendingCompanies()
      this.fetchDashboardStats()
    },
    async rejectCompany(id) {
      if (!confirm('Reject this company request?')) return

      const token = localStorage.getItem('adminToken')

      await fetch(`http://127.0.0.1:5000/api/company/${id}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      this.fetchPendingCompanies()
      this.fetchDashboardStats()
    },
  },
}
</script>

<style scoped>
.card {
  transition:
    transform 0.2s,
    box-shadow 0.2s;
  border-radius: 15px;
}
.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1) !important;
}
.hover-card {
  transition: all 0.2s ease;
  cursor: pointer;
}

.hover-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15) !important;
  border-color: #8f8849 !important;
}
.btn {
  transition: transform 0.2s ease;
}

.btn:hover {
  transform: translateY(-2px);
}
</style>
