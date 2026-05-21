<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card">
          <div class="card-header">Student Signup</div>
          <div class="card-body">
            <form @submit.prevent="studentsignup">
              <div class="form-group">
                <label for="email">Email</label>
                <input type="email" class="form-control" id="email" v-model="form.email" required />
              </div>
              <div class="form-group">
                <label for="password">Password</label>
                <input
                  type="password"
                  class="form-control"
                  id="password"
                  v-model="form.password"
                  required
                />
              </div>

              <div class="form-group">
                <label for="full_name">Full Name</label>
                <input
                  type="text"
                  class="form-control"
                  id="full_name"
                  v-model="form.full_name"
                  required
                />
              </div>
              <div class="form-group">
                <label for="roll_number">Roll Number</label>
                <input
                  type="text"
                  class="form-control"
                  id="roll_number"
                  v-model="form.roll_number"
                  required
                />
              </div>
              <div class="form-group">
                <label for="branch">Branch</label>
                <input
                  type="text"
                  class="form-control"
                  id="branch"
                  v-model="form.branch"
                  required
                />
              </div>
              <div class="form-group">
                <label for="cgpa">CGPA</label>
                <input
                  type="number"
                  step="0.01"
                  class="form-control"
                  id="cgpa"
                  v-model="form.cgpa"
                  required
                />
              </div>
              <div class="form-group">
                <label for="passout_year">Passout Year</label>
                <input
                  type="number"
                  class="form-control"
                  id="passout_year"
                  v-model="form.passout_year"
                  required
                />
              </div>

              <br />
              <div v-if="errorMessage" class="text-danger">{{ errorMessage }}</div>
              <div v-if="successMessage" class="text-success">{{ successMessage }}</div>

              <button type="submit" class="btn btn-success">Signup</button> &nbsp;
              <router-link to="/student-login" class="btn btn-secondary ml-2"
                >Have Account? Login</router-link
              >
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StudentSignup',
  data() {
    return {
      form: {
        email: '',
        password: '',
        role: 'student',
        full_name: '',
        roll_number: '',
        branch: '',
        cgpa: '',
        passout_year: '',
      },
      errorMessage: null,
      successMessage: null,
    }
  },
  methods: {
    async studentsignup() {
      this.errorMessage = null
      this.successMessage = null

      try {
        const response = await fetch('http://127.0.0.1:5000/api/signup', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.form),
        })

        const result = await response.json()

        if (!response.ok) {
          this.errorMessage = result.message || result.error || 'Signup failed'
          return
        }

        this.successMessage = result.message
        alert('Signup successful! Please login.')
        this.$router.push('/student-login')
      } catch (error) {
        this.errorMessage = 'Unable to connect to server'
      }
    },
  },
}
</script>
