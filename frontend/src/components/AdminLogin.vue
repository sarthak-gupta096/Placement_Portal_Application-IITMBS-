<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card">
          <div class="card-header">Admin Login</div>
          <div class="card-body">
            <form @submit.prevent="adminlogin">
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

              <button type="submit" class="btn btn-primary">Login</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminLogin',
  data() {
    return {
      email: '',
      password: '',
      errorMessage: null,
    }
  },
  methods: {
    async adminlogin() {
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

        const { token, role } = result
        if (role !== 'admin') {
          this.errorMessage = 'You are not authorized as Admin'
          return
        }

        alert('Login Successful')
        localStorage.setItem('adminToken', token)
        this.$router.push('/admin/dashboard')
      } catch (error) {
        this.errorMessage = 'Unable to connect to server'
      }
    },
  },
}
</script>
