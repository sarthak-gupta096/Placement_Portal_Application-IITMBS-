<template>
  <div class="container mt-5 pt-5">
    <div class="row justify-content-center">
      <div class="col-md-10">
        <div class="row justify-content-center">
          <div class="card shadow-sm border-0">
            <h5 class="card-title text-center py-4">Quick Actions</h5>
            <div class="mb-3 d-flex">
              <button class="btn btn-secondary" @click="$router.back()">← Back</button>
            </div>

            <br />
            <div class="col-12">
              <div class="card-header bg-warning text-dark">
                <h6 class="mb-0 fw-bold">
                  📋 Registered Student ({{ registeredStudents.length }})
                </h6>
              </div>
              <div class="card-body p-0">
                <div v-if="registeredStudents.length === 0" class="text-center py-5">
                  <i class="bi bi-check-circle text-success fs-1 mb-3"></i>
                  <h5 class="text-muted">No registered students</h5>
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
                      <tr v-for="student in registeredStudents" :key="student.user_id">
                        <td>{{ student.full_name }}</td>
                        <td>{{ student.roll_number }}</td>
                        <td>{{ student.branch }}</td>
                        <td>{{ student.cgpa }}</td>

                        <td>
                          <span v-if="student.is_active" class="badge bg-success"> Active </span>
                          <span v-else class="badge bg-danger"> Blacklisted </span>
                        </td>
                        <td>
                          <button
                            v-if="student.status === 'approved' && student.is_active"
                            class="btn btn-danger btn-sm"
                            @click="blacklistStudent(student.user_id)"
                          >
                            Blacklist
                          </button>
                          <button
                            v-if="student.status === 'approved' && !student.is_active"
                            class="btn btn-success btn-sm"
                            @click="activateStudent(student.user_id)"
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
  name: 'RegisteredStudents',
  data() {
    return {
      registeredStudents: [],
    }
  },
  async mounted() {
    this.fetchRegisteredStudents()
  },
  methods: {
    async fetchRegisteredStudents() {
      try {
        const token = localStorage.getItem('adminToken')
        const response = await fetch('http://127.0.0.1:5000/api/admin/registered-students', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        if (!response.ok) throw new Error(`HTTP ${response.status}`)
        const result = await response.json()
        console.log('API Response:', result)
        this.registeredStudents = result['registered-students'] || []
        console.log('Loaded students:', this.registeredStudents.length)
      } catch (error) {
        console.error('Registered students error:', error)
      }
    },
    goBack() {
      this.$router.push('/admin/dashboard')
    },
    async blacklistStudent(id) {
      if (!confirm('Blacklist this student?')) return

      const token = localStorage.getItem('adminToken')

      await fetch(`http://127.0.0.1:5000/api/student/status/${id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          action: 'blacklist',
        }),
      })

      this.fetchRegisteredStudents()
    },
    async activateStudent(id) {
      if (!confirm('Reactivate this student?')) return

      const token = localStorage.getItem('adminToken')

      await fetch(`http://127.0.0.1:5000/api/student/status/${id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          action: 'active',
        }),
      })

      this.fetchRegisteredStudents()
    },
  },
}
</script>
