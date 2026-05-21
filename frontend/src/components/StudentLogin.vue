<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card">
          <div class="card-header">Student Login</div>
          <div class="card-body">
            <form @submit.prevent="studentlogin">
              <div class="form-group">
                <label for="email">Email</label>
                <input type="email" class="form-control" id="email" v-model="email" required />
              </div>

              <div class="form-group">
                <label for="password">Password</label>
                <input
                  type="password"
                  class="form-control"
                  id="password"
                  v-model="password"
                  required
                />
              </div>

              <br />
              <div v-if="errorMessage" class="text-danger">
                {{ errorMessage }}
              </div>

              <div class="d-flex justify-content-between align-items-center mt-3">
                <button type="submit" class="btn btn-primary">Login</button>
                <router-link to="/student/signup" class="btn btn-link ml-2"
                  >New Student? Signup</router-link
                >
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StudentLogin',
  data() {
    return {
      email: '',
      password: '',
      errorMessage: null,
    }
  },
  methods: {
    async studentlogin() {
      this.errorMessage = null
      const payload = {
        email: this.email,
        password: this.password,
      }

      try {
        const response = await fetch('http://127.0.0.1:5000/api/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(payload),
        })

        const result = await response.json()

        if (!response.ok) {
          this.errorMessage = result.message || 'Something went wrong'
          return
        }

        const { token, role, status } = result

        if (role !== 'student') {
          this.errorMessage = 'You are not authorized!'
          return
        }

        if (status !== 'approved') {
          this.errorMessage = 'Your account is pending admin approval. Please wait.'
          return
        }

        alert('Login Successful')
        localStorage.setItem('studentToken', token)
        this.$router.push('/student/dashboard')
      } catch (error) {
        this.errorMessage = 'Unable to connect to server'
      }
    },
  },
}
</script>
