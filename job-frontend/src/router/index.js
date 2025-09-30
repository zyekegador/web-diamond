import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import ApplicantRegister from "@/views/ApplicantRegister.vue";
import JobList from "../views/JobList.vue";
import JobDetail from "../views/JobDetail.vue";

// Admin Views
import AdminDashboard from "../views/AdminDashboard.vue";
import CreateHR from "../views/AdminPanel/CreateHR.vue";

// HR Views
import HRDashboard from "../views/HRDashboard.vue";
import CreateJob from "../views/HRPanel/CreateJob.vue";
import ManageJobs from "../views/HRPanel/ManageJobs.vue";
import ViewApplications from "../views/HRPanel/ViewApplications.vue";

// Applicant Views
import ApplicantDashboard from "../views/ApplicantDashboard.vue";
import ApplyJob from "../views/ApplicantPanel/ApplyJob.vue";
import MyApplications from "../views/ApplicantPanel/MyApplications.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/register",
    name: "Register",
    component: ApplicantRegister,
  },
  {
    path: "/jobs",
    name: "JobList",
    component: JobList,
  },
  {
    path: "/jobs/:id",
    name: "JobDetail",
    component: JobDetail,
  },

  // Admin Routes
  {
    path: "/admin/dashboard",
    name: "AdminDashboard",
    component: AdminDashboard,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/admin/create-hr",
    name: "CreateHR",
    component: CreateHR,
    meta: { requiresAuth: true, role: "admin" },
  },

  // HR Routes
  {
    path: "/hr/dashboard",
    name: "HRDashboard",
    component: HRDashboard,
    meta: { requiresAuth: true, role: "hr" },
  },
  {
    path: "/hr/create-job",
    name: "CreateJob",
    component: CreateJob,
    meta: { requiresAuth: true, role: "hr" },
  },
  {
    path: "/hr/manage-jobs",
    name: "ManageJobs",
    component: ManageJobs,
    meta: { requiresAuth: true, role: "hr" },
  },
  {
    path: "/hr/applications/:jobId",
    name: "ViewApplications",
    component: ViewApplications,
    meta: { requiresAuth: true, role: "hr" },
  },

  // Applicant Routes
  {
    path: "/applicant/dashboard",
    name: "ApplicantDashboard",
    component: ApplicantDashboard,
    meta: { requiresAuth: true, role: "applicant" },
  },
  {
    path: "/applicant/apply/:jobId",
    name: "ApplyJob",
    component: ApplyJob,
    meta: { requiresAuth: true, role: "applicant" },
  },
  {
    path: "/applicant/my-applications",
    name: "MyApplications",
    component: MyApplications,
    meta: { requiresAuth: true, role: "applicant" },
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// Navigation Guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  const userType = localStorage.getItem("userType");

  if (to.meta.requiresAuth && !token) {
    next("/login");
  } else if (to.meta.role && to.meta.role !== userType) {
    next("/");
  } else {
    next();
  }
});

export default router;
