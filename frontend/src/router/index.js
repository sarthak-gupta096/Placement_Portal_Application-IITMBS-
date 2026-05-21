import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/components/HomeView.vue'
import AdminLogin from '@/components/AdminLogin.vue'
import StudentLogin from '@/components/StudentLogin.vue'
import CompanyLogin from '@/components/CompanyLogin.vue'
import StudentSignup from '@/components/StudentSignup.vue'
import CompanySignup from '@/components/CompanySignup.vue'
import AdminDashboard from '@/components/AdminDashboard.vue'
import RegisteredStudents from '@/components/RegisteredStudents.vue'
import RegisteredCompanies from '@/components/RegisteredCompanies.vue'
import CompanyDashboard from '@/components/CompanyDashboard.vue'
import CreateDrive from '@/components/CreateDrive.vue'
import ManageDrives from '@/components/ManageDrives.vue'
import ViewDriveDetails from '@/components/ViewDriveDetails.vue'
import ApprovedDrives from '@/components/ApprovedDrives.vue'
import RecievedApplications from '../components/RecievedApplications.vue'
import StudentDashboard from '../components/StudentDashboard.vue'
import CompanyDrives from '../components/CompanyDrives.vue'
import DriveDetails from '../components/DriveDetails.vue'
import ViewApplications from '@/components/ViewApplications.vue'
import ViewProfile from '../components/ViewProfile.vue'
import StudentHistory from '@/components/StudentHistory.vue'
import SearchStudentCompanies from "../components/SearchStudentCompanies.vue"





const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomeView',
      component: HomeView,
    },
    {
      path: '/admin-login',
      name: 'AdminLogin',
      component: AdminLogin,
    },
    {
      path: '/student-login',
      name: 'StudentLogin',
      component: StudentLogin,
    },
    {
      path: '/company-login',
      name: 'CompanyLogin',
      component: CompanyLogin,
    },
    {
      path: '/student/signup',
      name: 'StudentSignup',
      component: StudentSignup,
    },
    {
      path: '/company/signup',
      name: 'CompanySignup',
      component: CompanySignup,
    },
    {
      path: '/admin/dashboard',
      name: '',
      component: AdminDashboard,
    },
    {
      path: '/admin/pending-students',
      name: 'PendingStudents',
      component: AdminDashboard,
    },
    {
      path: '/admin/pending-companies',
      name: 'PendingCompanies',
      component: AdminDashboard,
    },
    {
      path: '/admin/registered-students',
      name: 'RegisteredStudents',
      component: RegisteredStudents,
    },
    {
      path: '/admin/registered-companies',
      name: 'RegisteredCompanies',
      component: RegisteredCompanies,
    },
    {
      path: '/company-dashboard',
      name: 'CompanyDashboard',
      component: CompanyDashboard,
    },
    {
      path: '/company/create-drive',
      name: 'CreateDrive',
      component: CreateDrive,
    },
    {
      path: '/admin/manage-drives',
      component: ManageDrives,
    },
    {
      path: '/admin/drive/:id',
      component: ViewDriveDetails,
    },
    {
      path: '/admin/approved-drives',
      component: ApprovedDrives,
    },
    {
      path: '/drive/:id/applications',
      name: 'applications',
      component: RecievedApplications,
    },
    {
      path: '/student/dashboard',
      component: StudentDashboard,
    },

    {
      path: '/company/:id/drives',
      component: CompanyDrives,
    },
    {
      path: '/drive/:id',
      name: 'driveDetails',
      component: DriveDetails,
    },
    {
      path: '/admin/applications',
      name: 'viewApplications',
      component: ViewApplications,
    },
    {
      path: '/student/profile',
      name: 'studentProfile',
      component: ViewProfile,
    },
    {
      path: '/student/history',
      component: StudentHistory,
    },
    {
  path: "/admin/search",
  component: SearchStudentCompanies
}
    
  ],
})

export default router
