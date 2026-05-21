<template>
  <div class="container create-drive-wrapper">
    <div class="card shadow-lg border-0 p-4">
      <h3 class="fw-bold mb-4 text-center">Create New Drive</h3>

      <form @submit.prevent="createDrive">
        <div class="mb-3">
          <label class="form-label">Job Title</label>
          <input
            type="text"
            class="form-control"
            v-model="drive.job_title"
            placeholder="Enter Job Title"
            required
          />
        </div>

        <div class="mb-3">
          <label class="form-label">Job Description</label>
          <textarea
            class="form-control"
            rows="4"
            v-model="drive.description"
            placeholder="Enter Job Description"
          ></textarea>
        </div>

        <div class="mb-3">
          <label class="form-label">CTC / Package (LPA)</label>
          <input
            type="number"
            class="form-control"
            v-model="drive.package"
            placeholder="Enter Package"
            required
          />
        </div>

        <div class="mb-3">
          <label class="form-label">Job Location</label>
          <input
            type="text"
            class="form-control"
            v-model="drive.location"
            placeholder="Enter Job Location"
            required
          />
        </div>

        <div class="mb-3">
          <label class="form-label">Minimum CGPA</label>
          <input
            type="number"
            step="0.01"
            class="form-control"
            v-model="drive.min_cgpa"
            placeholder="Enter Minimum CGPA"
            required
          />
        </div>

        <div class="row">
          <div class="col-md-6 mb-3">
            <label class="form-label">Eligible From (Passout Year)</label>
            <input
              type="number"
              class="form-control"
              v-model="drive.year_start"
              placeholder=""
              required
            />
          </div>

          <div class="col-md-6 mb-3">
            <label class="form-label">Eligible Till (Passout Year)</label>
            <input
              type="number"
              class="form-control"
              v-model="drive.year_end"
              placeholder=""
              required
            />
          </div>
        </div>

        <div class="mb-3">
          <label class="form-label">Eligible Branches</label>
          <input
            type="text"
            class="form-control"
            v-model="drive.eligible_branches"
            placeholder=""
            required
          />
        </div>
        <br />

        <div class="mb-3">
          <label class="form-label">Application Deadline</label>
          <input type="date" class="form-control" v-model="drive.deadline" required />
        </div>

        <br />
        <div class="d-flex justify-content-between">
          <button class="btn btn-secondary mb-3" @click="goBack">← Back to Dashboard</button>

          <button type="submit" class="btn btn-primary px-4">Create Drive</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CreateDrive',

  data() {
    return {
      drive: {
        job_title: '',
        description: '',
        deadline: '',
        location: '',
        min_cgpa: '',
        package: '',
        year_start: '',
        year_end: '',
        eligible_branches: '', // ee,ec,it
      },
      message: '',
      error: '',
    }
  },

  methods: {
    async createDrive() {
      try {
        const token = localStorage.getItem('companyToken')

        const response = await fetch('http://127.0.0.1:5000/drives', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            job_title: this.drive.job_title,
            description: this.drive.description,
            deadline: this.drive.deadline,
            location: this.drive.location,
            min_cgpa: parseFloat(this.drive.min_cgpa),
            package: parseInt(this.drive.package),
            year_start: parseInt(this.drive.year_start),
            year_end: parseInt(this.drive.year_end),
            eligible_branches: this.drive.eligible_branches,
          }),
        })

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.message)
        }

        this.drive = {
          job_title: '',
          description: '',
          deadline: '',
          location: '',
          min_cgpa: '',
          package: '',
          year_start: '',
          year_end: '',
          eligible_branches: '',
        }

        alert(data.message)
        this.error = ''
        this.message = data.message
      } catch (err) {
        this.error = err.message
        console.error(err)
      }
    },
    goBack() {
      this.$router.push('/company-dashboard')
    },
  },
}
</script>

<style scoped>
.create-drive-wrapper {
  padding-top: 100px;
  max-width: 700px;
}

.card {
  border-radius: 15px;
}

button {
  border-radius: 8px;
}
</style>
