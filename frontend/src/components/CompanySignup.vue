<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card">
          <div class="card-header">Company Signup</div>
          <div class="card-body">
            <form @submit.prevent="companysignup">
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

              <!-- Company-specific fields -->
              <div class="form-group">
                <label for="company_name">Company Name</label>
                <input
                  type="text"
                  class="form-control"
                  id="company_name"
                  v-model="form.company_name"
                  required
                />
              </div>
              <div class="form-group">
                <label for="website">Website</label>
                <input type="url" class="form-control" id="website" v-model="form.website" />
              </div>
              <div class="form-group">
                <label for="description">Description</label>
                <input
                  type="text"
                  class="form-control"
                  id="description"
                  v-model="form.description"
                />
              </div>
              <div class="form-group">
                <label for="hr_name">HR Name</label>
                <input
                  type="text"
                  class="form-control"
                  id="hr_name"
                  v-model="form.hr_name"
                  required
                />
              </div>
              <div class="form-group">
                <label for="hr_contact">HR Contact</label>
                <input
                  type="text"
                  class="form-control"
                  id="hr_contact"
                  v-model="form.hr_contact"
                  required
                />
              </div>

              <br />
              <div v-if="errorMessage" class="text-danger">{{ errorMessage }}</div>
              <div v-if="successMessage" class="text-success">{{ successMessage }}</div>

              <button type="submit" class="btn btn-success">Signup</button>&nbsp;
              <router-link to="/company-login" class="btn btn-secondary ml-2"
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
  name: 'CompanySignup',
  data() {
    return {
      form: {
        email: '',
        password: '',
        role: 'company',
        company_name: '',
        website: '',
        description: '',
        hr_name: '',
        hr_contact: '',
      },
      errorMessage: null,
      successMessage: null,
    }
  },
  methods: {
    async companysignup() {
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
        this.$router.push('/company-login')
      } catch (error) {
        this.errorMessage = 'Unable to connect to server'
      }
    },
  },
}
</script>
