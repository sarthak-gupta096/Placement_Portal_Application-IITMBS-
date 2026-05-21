<template>
  <div class="container mt-5 pt-5">
    <div class="row justify-content-center">
      <div class="col-md-10">
        <div class="row justify-content-center">
          <div class="card shadow-sm border-0">
            <h5 class="card-title text-center py-4">Quick Actions</h5>
            <div>
              <button class="btn btn-secondary" @click="$router.back()">← Back</button>
            </div>
            <br />
            <div class="col-12">
              <div class="card-header bg-warning text-dark">
                <h6 class="mb-0 fw-bold">
                  📋 Registered Companies ({{ registeredCompanies.length }})
                </h6>
              </div>
              <div class="card-body p-0">
                <div v-if="registeredCompanies.length === 0" class="text-center py-5">
                  <i class="bi bi-check-circle text-success fs-1 mb-3"></i>
                  <h5 class="text-muted">No registered companies</h5>
                </div>
                <div v-else class="table-responsive">
                  <table class="table table-hover mb-0">
                    <thead class="table-light">
                      <tr>
                        <th>Name</th>
                        <th>Website</th>
                        <th>HR Name</th>
                        <th>HR Contact</th>
                        <th>Status</th>
                        <th>Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="company in registeredCompanies" :key="company.user_id">
                        <td>{{ company.name }}</td>
                        <td>{{ company.website }}</td>
                        <td>{{ company.hr_name }}</td>
                        <td>{{ company.hr_contact }}</td>

                        <td>
                          <span class="badge bg-success" v-if="company.is_active">Active</span>
                          <span class="badge bg-danger" v-else>Blacklisted</span>

                        </td>
                        <td>
                          <button
                            v-if="company.is_active"
                            class="btn btn-danger btn-sm"
                            @click="blacklistCompany(company.user_id)"
                          >
                            Blacklist
                          </button>

                          <button
                            v-else
                            class="btn btn-success btn-sm"
                            @click="activateCompany(company.user_id)"
                          >
                            Activate
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
  </div>
</template>

<script>
export default {
  name: 'RegisteredCompanies',
  data() {
    return {
      registeredCompanies: [],
    }
  },
  async mounted() {
    this.fetchRegisteredCompanies()
  },
  methods: {
    async fetchRegisteredCompanies() {
      try {
        const token = localStorage.getItem('adminToken')
        const response = await fetch('http://127.0.0.1:5000/api/admin/registered-companies', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        if (!response.ok) throw new Error(`HTTP ${response.status}`)
        const result = await response.json()
        console.log('API Response:', result)
        this.registeredCompanies = result['registered-companies'] || []
        console.log('Loaded companies:', this.registeredCompanies.length)
      } catch (error) {
        console.error('Registered companies error:', error)
      }
    },
    goBack() {
      this.$router.push('/admin/dashboard')
    },
    async blacklistCompany(id) {
      if (!confirm('Blacklist this company?')) return

      const token = localStorage.getItem('adminToken')

      await fetch(`http://127.0.0.1:5000/api/company/status/${id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          action: 'blacklist',
        }),
      })

      this.fetchRegisteredCompanies()
    },
    async activateCompany(id) {
      const token = localStorage.getItem('adminToken')

      await fetch(`http://127.0.0.1:5000/api/company/status/${id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          action: 'active',
        }),
      })

      this.fetchRegisteredCompanies()
    },
  },
}
</script>
