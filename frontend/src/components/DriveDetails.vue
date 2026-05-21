<template>
  <div class="container mt-4">
    <br />

    <div class="card mb-4">
      <div class="card-body">
        <h3>{{ drive.job_title }}</h3>

        <p><b>Location:</b> {{ drive.location }}</p>
        <p><b>Package:</b> {{ drive.package }}</p>
        <p><b>Minimum CGPA:</b> {{ drive.min_cgpa }}</p>
        <p><b>Eligible Branches:</b> {{ drive.eligible_branches }}</p>
        <p><b>Deadline:</b> {{ drive.deadline }}</p>
      </div>
    </div>
    <div class="mt-4">
      <button class="btn btn-success" @click="applyDrive">Apply</button>&nbsp;

      <button class="btn btn-secondary me-2" @click="goBack">← Go Back</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      drive: {},
    }
  },

  methods: {
    goBack() {
      this.$router.back()
    },

    async applyDrive() {
      const driveId = this.$route.params.id
      const token = localStorage.getItem('studentToken')

      const res = await fetch(`http://127.0.0.1:5000/apply/${driveId}`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      const data = await res.json()

      alert(data.message)
    },
  },

  async mounted() {
    const id = this.$route.params.id

    const token = localStorage.getItem('studentToken')

    const res = await fetch(`http://127.0.0.1:5000/drives/${id}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    const data = await res.json()

    this.drive = data.drive
  },
}
</script>
