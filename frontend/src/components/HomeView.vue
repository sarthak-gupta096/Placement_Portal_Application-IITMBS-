<template>
  <div class="home-page pt-6" style="padding-top: 110px">
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm fixed-top">
      <div class="container">
        <router-link class="navbar-brand fw-bold fs-3 text-primary" to="/">
          <h4
            class="display-5 fw-bold text-primary mb-4 shadow-sm border-start border-5 border-primary ps-4 manrope-heading"
          >
            Job<span class="text-warning">Syncr</span>
          </h4>
        </router-link>
        <div class="navbar-nav ms-auto">
          <router-link class="nav-link" to="/admin-login">
            <i class="bi bi-shield-lock me-1"></i>Admin Login
          </router-link>
          <router-link class="nav-link" to="/about">About Us</router-link>
        </div>
      </div>
    </nav>

    <div class="container-fluid py-5">
      <div class="row align-items-center h-100 mb-5">
        <div class="col-lg-6">
          <div class="text-center text-lg-start mb-5 mb-lg-0 ps-lg-5 pe-lg-5">
            <h1 class="display-5 text-primary mb-4 fw-bolder">Get your dream job</h1>
            <p class="lead text-muted mb-4 fs-5">
              Connect with top companies. Apply to jobs that match your skills.
            </p>
            <div class="d-flex gap-3 flex-wrap justify-content-center justify-content-lg-start">
              <router-link to="/student-login" class="btn btn-primary btn-lg px-5">
                Sign In
              </router-link>
              <router-link to="/student/signup" class="btn btn-outline-primary btn-lg px-5">
                Sign Up
              </router-link>
            </div>
          </div>
        </div>

        <div class="col-lg-6">
          <div class="row g-4 justify-content-center">
            <div class="col-md-6">
              <div class="text-center p-4">
                <div class="icon-circle bg-primary text-white mb-3 mx-auto">👨‍🎓</div>
                <h6 class="fw-bold mb-2">Top Companies</h6>
                <p class="text-muted small">Connect with top recruiters</p>
              </div>
            </div>
            <div class="col-md-6">
              <div class="text-center p-4">
                <div class="icon-circle bg-success text-white mb-3 mx-auto">📈</div>
                <h6 class="fw-bold mb-2">Easy Apply</h6>
                <p class="text-muted small">More options, less hassle</p>
              </div>
            </div>
            <div class="col-md-6">
              <div class="text-center p-4">
                <div class="icon-circle bg-info text-white mb-3 mx-auto">⏱️</div>
                <h6 class="fw-bold mb-2">One Click</h6>
                <p class="text-muted small">See profiles in one click</p>
              </div>
            </div>
            <div class="col-md-6">
              <div class="text-center p-4">
                <div class="icon-circle bg-warning text-white mb-3 mx-auto">🚀</div>
                <h6 class="fw-bold mb-2">Fast Track</h6>
                <p class="text-muted small">Unique startups & companies</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <hr />
      <div class="row align-items-center h-100">
        <div class="col-lg-6">
          <div class="row g-4 justify-content-center">
            <div class="col-md-6">
              <div class="text-center p-4">
                <div class="icon-circle bg-success text-white mb-3 mx-auto">👥</div>
                <h6 class="fw-bold mb-2">500K+ Talent</h6>
                <p class="text-muted small">Engaged developer community</p>
              </div>
            </div>
            <div class="col-md-6">
              <div class="text-center p-4">
                <div class="icon-circle bg-danger text-white mb-3 mx-auto">✅</div>
                <h6 class="fw-bold mb-2">Everything Free</h6>
                <p class="text-muted small">Post jobs after first interview</p>
              </div>
            </div>
            <div class="col-md-6">
              <div class="text-center p-4">
                <div class="icon-circle bg-warning text-white mb-3 mx-auto">📊</div>
                <h6 class="fw-bold mb-2">Free Analytics</h6>
                <p class="text-muted small">Track your hiring pipeline</p>
              </div>
            </div>
            <div class="col-md-6">
              <div class="text-center p-4">
                <div class="icon-circle bg-info text-white mb-3 mx-auto">🎯</div>
                <h6 class="fw-bold mb-2">Targeted Matches</h6>
                <p class="text-muted small">Download candidate schedules</p>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-6">
          <div class="text-center text-lg-end mb-5 mb-lg-0 ps-lg-5 pe-lg-5">
            <h1 class="display-4 fw-bold text-success mb-4">Hire top talent</h1>
            <p class="lead text-muted mb-4 fs-5">
              Build the best teams. Access qualified candidates instantly.
            </p>
            <div class="d-flex gap-3 flex-wrap justify-content-center justify-content-lg-end">
              <router-link to="/company-login" class="btn btn-success btn-lg px-5">
                Sign In
              </router-link>
              <router-link to="/company/signup" class="btn btn-outline-success btn-lg px-5">
                Sign Up
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
}
</script>

<style>
body {
  background-color: rgb(211, 211, 183);
}

.min-vh-90 {
  min-height: 90vh;
}
.icon-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}
.navbar-brand:hover {
  text-decoration: none;
}
@media (max-width: 768px) {
  .display-4 {
    font-size: 2rem;
  }
}
.manrope-heading {
  font-family: 'Manrope', sans-serif;
  font-weight: 700;
}
</style>
