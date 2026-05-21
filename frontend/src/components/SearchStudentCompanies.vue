<template>
<div class="container mt-4">

<h3 class="mb-4">Search Students / Companies</h3>
      <button class="btn btn-secondary me-2" @click="goBack">← Go Back</button><br><br>

<div class="d-flex mb-3">

<select class="form-select w-25 me-2" v-model="role">
  <option value="student">Student</option>
  <option value="company">Company</option>
</select>

<input
  type="text"
  class="form-control me-2"
  placeholder="Search by name"
  v-model="searchText"
/>

<button class="btn btn-primary" @click="searchData">
  Search
</button>

</div>

<table class="table table-bordered" v-if="results.length">

<thead v-if="role=='student'">
<tr>
<th>Name</th>
<th>Roll</th>
<th>Branch</th>
<th>CGPA</th>
<th>Passout</th>
</tr>
</thead>

<thead v-if="role=='company'">
<tr>
<th>Name</th>
<th>Website</th>
<th>HR Name</th>
<th>Contact</th>
</tr>
</thead>

<tbody>

<tr v-for="item in results" :key="item.user_id">

<td v-if="role=='student'">{{item.full_name}}</td>
<td v-if="role=='student'">{{item.roll_number}}</td>
<td v-if="role=='student'">{{item.branch}}</td>
<td v-if="role=='student'">{{item.cgpa}}</td>
<td v-if="role=='student'">{{item.passout_year}}</td>

<td v-if="role=='company'">{{item.name}}</td>
<td v-if="role=='company'">{{item.website}}</td>
<td v-if="role=='company'">{{item.hr_name}}</td>
<td v-if="role=='company'">{{item.hr_contact}}</td>

</tr>

</tbody>

</table>

</div>
</template>

<script>

export default {

data(){
return{
role:"student",
searchText:"",
results:[]
}
},

methods:{
    goBack() {
      this.$router.back()
    },

async searchData(){

const token = localStorage.getItem("adminToken")

let url=""

if(this.role==="student"){
// url=`http://localhost:5000/api/student?search=${this.searchText}`
url=`http://localhost:5000/api/admin/search-students?search=${this.searchText}`
}

else{
// url=`http://localhost:5000/api/company?search=${this.searchText}`
url = `http://localhost:5000/api/admin/search-companies?search=${this.searchText}`
}

const response = await fetch(url,{
headers:{
"Authorization":`Bearer ${token}`
}
})

const data = await response.json()

if(this.role==="student"){
  this.results = data.students
}
else{
  this.results = data.companies
}

}

}

}

</script>