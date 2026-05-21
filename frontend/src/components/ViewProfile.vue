<template>
  <div class="container mt-4">
    <h3>Edit Profile</h3>

    <form @submit.prevent="updateProfile">
      <div class="mb-3">
        <label>Full Name</label>
        <input v-model="profile.full_name" class="form-control" />
      </div>

      <div class="mb-3">
        <label>Roll Number</label>
        <input v-model="profile.roll_number" class="form-control" />
      </div>

      <div class="mb-3">
        <label>Branch</label>
        <input v-model="profile.branch" class="form-control" />
      </div>

      <div class="mb-3">
        <label>CGPA</label>
        <input v-model="profile.cgpa" class="form-control" />
      </div>

      <div class="mb-3">
        <label>Passout Year</label>
        <input v-model="profile.passout_year" class="form-control" />
      </div>

      <div class="mb-3">
        <label>Resume Link</label>
        <input
          type="text"
          v-model="profile.resume"
          class="form-control"
          placeholder="Paste Google Drive resume link"
        />
      </div>

      <button class="btn btn-success" @click="updateProfile">Update Profile</button>

      <button
        type="button"
        class="btn btn-secondary ms-2"
        @click="$router.push('/student/dashboard')"
      >
        Cancel
      </button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      profile: {
        full_name: '',
        roll_number: '',
        branch: '',
        cgpa: '',
        passout_year: '',
        resume: '',
      },
    }
  },

  methods: {
    async fetchProfile() {
      const token = localStorage.getItem('studentToken')

      const response = await fetch('http://127.0.0.1:5000/api/student', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      const data = await response.json()

      this.profile = data
    },

    async updateProfile() {
      const token = localStorage.getItem('studentToken')

      const response = await fetch('http://127.0.0.1:5000/api/student', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(this.profile),
      })

      const data = await response.json()

      alert(data.message)

      this.$router.push('/student/dashboard')
    },
  },

  mounted() {
    this.fetchProfile()
  },
}
</script>
