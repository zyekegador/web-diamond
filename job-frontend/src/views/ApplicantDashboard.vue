<template>
  <div class="applicant-dashboard">
    <nav class="dashboard-nav">
      <div class="nav-brand">
        <h2>Applicant Dashboard</h2>
      </div>
      <div class="nav-user">
        <span>Welcome, {{ user.first_name }} {{ user.last_name }}</span>
        <button @click="handleLogout" class="btn-logout">Logout</button>
      </div>
    </nav>

    <div class="dashboard-container">
      <aside class="sidebar">
        <ul class="sidebar-menu">
          <li
            :class="{ active: activeTab === 'overview' }"
            @click="activeTab = 'overview'"
          >
            <i class="fas fa-chart-line"></i>
            <span>Overview</span>
          </li>
          <li
            :class="{ active: activeTab === 'browse-jobs' }"
            @click="activeTab = 'browse-jobs'"
          >
            <i class="fas fa-search"></i>
            <span>Browse Jobs</span>
          </li>
          <li
            :class="{ active: activeTab === 'my-applications' }"
            @click="activeTab = 'my-applications'"
          >
            <i class="fas fa-file-alt"></i>
            <span>My Applications</span>
          </li>
          <li
            :class="{ active: activeTab === 'profile' }"
            @click="activeTab = 'profile'"
          >
            <i class="fas fa-user"></i>
            <span>Profile</span>
          </li>
        </ul>
      </aside>

      <main class="main-content">
        <!-- Overview Tab -->
        <div v-if="activeTab === 'overview'" class="content-section">
          <h1>Application Overview</h1>
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon blue">
                <i class="fas fa-file-alt"></i>
              </div>
              <div class="stat-info">
                <h3>Total Applications</h3>
                <p class="stat-number">{{ applications.length }}</p>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon orange">
                <i class="fas fa-clock"></i>
              </div>
              <div class="stat-info">
                <h3>Pending</h3>
                <p class="stat-number">{{ getPendingCount }}</p>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon green">
                <i class="fas fa-check-circle"></i>
              </div>
              <div class="stat-info">
                <h3>Shortlisted</h3>
                <p class="stat-number">{{ getShortlistedCount }}</p>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon purple">
                <i class="fas fa-star"></i>
              </div>
              <div class="stat-info">
                <h3>Accepted</h3>
                <p class="stat-number">{{ getAcceptedCount }}</p>
              </div>
            </div>
          </div>

          <div class="recent-applications">
            <h2>Recent Applications</h2>
            <div class="application-list">
              <div
                v-for="app in applications.slice(0, 5)"
                :key="app.id"
                class="application-item"
              >
                <div class="app-header">
                  <h3>{{ app.job.title }}</h3>
                  <span :class="['status-badge', app.status]">{{
                    formatStatus(app.status)
                  }}</span>
                </div>
                <p class="app-details">
                  <i class="fas fa-building"></i> {{ app.job.location }}
                  <span class="separator">|</span>
                  <i class="fas fa-calendar"></i> Applied
                  {{ formatDate(app.applied_at) }}
                </p>
                <p v-if="app.notes" class="app-notes">
                  <i class="fas fa-comment"></i> HR Notes: {{ app.notes }}
                </p>
              </div>
              <div v-if="applications.length === 0" class="no-data">
                <i class="fas fa-inbox"></i>
                <p>No applications yet. Start browsing jobs!</p>
                <button @click="activeTab = 'browse-jobs'" class="btn-primary">
                  Browse Jobs
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Browse Jobs Tab -->
        <div v-if="activeTab === 'browse-jobs'" class="content-section">
          <h1>Browse Available Jobs</h1>
          <div class="jobs-grid">
            <div v-for="job in availableJobs" :key="job.id" class="job-card">
              <div class="job-header">
                <h3>{{ job.title }}</h3>
                <span class="job-type">{{ formatJobType(job.job_type) }}</span>
              </div>
              <p class="job-location">
                <i class="fas fa-map-marker-alt"></i> {{ job.location }}
              </p>
              <p class="job-salary" v-if="job.salary_range">
                <i class="fas fa-money-bill-wave"></i> {{ job.salary_range }}
              </p>
              <p class="job-description">
                {{ truncateText(job.description, 100) }}
              </p>
              <div class="job-footer">
                <span class="job-date"
                  >Posted {{ formatDate(job.created_at) }}</span
                >
                <button @click="openApplicationForm(job)" class="btn-apply">
                  Apply Now
                </button>
              </div>
            </div>
          </div>
          <div v-if="availableJobs.length === 0" class="no-data">
            No jobs available at the moment.
          </div>
        </div>

        <!-- My Applications Tab -->
        <div v-if="activeTab === 'my-applications'" class="content-section">
          <h1>My Applications</h1>
          <div class="table-container">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Job Title</th>
                  <th>Location</th>
                  <th>Applied Date</th>
                  <th>Status</th>
                  <th>Notes</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="app in applications" :key="app.id">
                  <td>
                    <strong>{{ app.job.title }}</strong>
                  </td>
                  <td>{{ app.job.location }}</td>
                  <td>{{ formatDate(app.applied_at) }}</td>
                  <td>
                    <span :class="['status-badge', app.status]">{{
                      formatStatus(app.status)
                    }}</span>
                  </td>
                  <td>{{ app.notes || "N/A" }}</td>
                  <td>
                    <button
                      @click="viewApplication(app.id)"
                      class="btn-action view"
                    >
                      <i class="fas fa-eye"></i> View
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
            <div v-if="applications.length === 0" class="no-data">
              No applications yet
            </div>
          </div>
        </div>

        <!-- Profile Tab -->
        <div v-if="activeTab === 'profile'" class="content-section">
          <h1>My Profile</h1>
          <div class="profile-container">
            <div class="profile-card">
              <div class="profile-header">
                <div class="profile-avatar">
                  <i class="fas fa-user-circle"></i>
                </div>
                <h2>{{ user.first_name }} {{ user.last_name }}</h2>
                <p>@{{ user.username }}</p>
              </div>
              <div class="profile-details">
                <div class="detail-item">
                  <i class="fas fa-envelope"></i>
                  <span>{{ user.email }}</span>
                </div>
                <div class="detail-item" v-if="user.phone_number">
                  <i class="fas fa-phone"></i>
                  <span>{{ user.phone_number }}</span>
                </div>
                <div class="detail-item" v-if="user.date_of_birth">
                  <i class="fas fa-birthday-cake"></i>
                  <span>{{ user.date_of_birth }}</span>
                </div>
                <div class="detail-item" v-if="user.address">
                  <i class="fas fa-map-marker-alt"></i>
                  <span>{{ user.address }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- Application Form Modal -->
    <ApplicationForm
      v-if="showApplicationForm"
      :jobId="selectedJob.id"
      :jobTitle="selectedJob.title"
      @close="closeApplicationForm"
      @application-submitted="handleApplicationSubmitted"
    />
  </div>
</template>

<script>
import api from "@/services/api";
import ApplicationForm from "./ApplicantPanel/ApplicationForm.vue";

export default {
  name: "ApplicantDashboard",
  components: {
    ApplicationForm,
  },
  data() {
    return {
      user: JSON.parse(localStorage.getItem("user") || "{}"),
      activeTab: "overview",
      applications: [],
      availableJobs: [],
      showApplicationForm: false,
      selectedJob: null,
    };
  },
  computed: {
    getPendingCount() {
      return this.applications.filter((app) => app.status === "pending").length;
    },
    getShortlistedCount() {
      return this.applications.filter((app) => app.status === "shortlisted")
        .length;
    },
    getAcceptedCount() {
      return this.applications.filter((app) => app.status === "accepted")
        .length;
    },
  },
  mounted() {
    this.loadApplications();
    this.loadJobs();
  },
  methods: {
    async loadApplications() {
      try {
        const response = await api.getMyApplications();
        this.applications = response.data;
      } catch (error) {
        console.error("Error loading applications:", error);
      }
    },
    async loadJobs() {
      try {
        const response = await api.getJobs();
        this.availableJobs = response.data;
      } catch (error) {
        console.error("Error loading jobs:", error);
      }
    },
    openApplicationForm(job) {
      this.selectedJob = job;
      this.showApplicationForm = true;
    },
    closeApplicationForm() {
      this.showApplicationForm = false;
      this.selectedJob = null;
    },
    handleApplicationSubmitted() {
      this.closeApplicationForm();
      this.loadApplications(); // Refresh applications list
      this.activeTab = "my-applications"; // Switch to applications tab
    },
    viewApplication(appId) {
      alert("View application details - Feature coming soon!");
    },
    async handleLogout() {
      await api.logout();
      this.$router.push("/");
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
      });
    },
    formatStatus(status) {
      return status.replace("_", " ").replace(/\b\w/g, (l) => l.toUpperCase());
    },
    formatJobType(type) {
      return type.replace("_", " ").replace(/\b\w/g, (l) => l.toUpperCase());
    },
    truncateText(text, length) {
      return text.length > length ? text.substring(0, length) + "..." : text;
    },
  },
};
</script>

<style scoped>
.applicant-dashboard {
  min-height: 100vh;
  background: #f5f7fa;
}

.dashboard-nav {
  background: white;
  padding: 15px 30px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand h2 {
  color: #333;
  font-size: 24px;
}

.nav-user {
  display: flex;
  align-items: center;
  gap: 20px;
}

.btn-logout {
  padding: 8px 20px;
  background: #f44336;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn-logout:hover {
  background: #d32f2f;
}

.dashboard-container {
  display: flex;
  min-height: calc(100vh - 70px);
}

.sidebar {
  width: 250px;
  background: white;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.sidebar-menu {
  list-style: none;
  padding: 20px 0;
}

.sidebar-menu li {
  padding: 15px 25px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 15px;
  transition: all 0.3s;
}

.sidebar-menu li:hover {
  background: #f5f7fa;
}

.sidebar-menu li.active {
  background: #4caf50;
  color: white;
  border-right: 4px solid #45a049;
}

.sidebar-menu li i {
  font-size: 18px;
  width: 20px;
}

.main-content {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
}

.content-section h1 {
  margin-bottom: 30px;
  color: #333;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: white;
  padding: 25px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 20px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.stat-icon.blue {
  background: #2196f3;
}
.stat-icon.green {
  background: #4caf50;
}
.stat-icon.orange {
  background: #ff9800;
}
.stat-icon.purple {
  background: #9c27b0;
}

.stat-info h3 {
  font-size: 14px;
  color: #666;
  margin-bottom: 5px;
}

.stat-number {
  font-size: 32px;
  font-weight: 700;
  color: #333;
}

.recent-applications h2 {
  margin-bottom: 20px;
  color: #333;
}

.application-list {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.application-item {
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.application-item:last-child {
  border-bottom: none;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.app-header h3 {
  color: #333;
  font-size: 18px;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge.pending {
  background: #fff3e0;
  color: #ff9800;
}

.status-badge.under_review {
  background: #e3f2fd;
  color: #2196f3;
}

.status-badge.shortlisted {
  background: #f3e5f5;
  color: #9c27b0;
}

.status-badge.accepted {
  background: #e8f5e9;
  color: #4caf50;
}

.status-badge.rejected {
  background: #ffebee;
  color: #f44336;
}

.app-details {
  color: #666;
  font-size: 14px;
  margin: 5px 0;
}

.app-details i {
  color: #4caf50;
  margin-right: 5px;
}

.separator {
  margin: 0 10px;
  color: #ddd;
}

.app-notes {
  margin-top: 10px;
  padding: 10px;
  background: #f5f7fa;
  border-radius: 5px;
  font-size: 14px;
  color: #666;
}

.jobs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.job-card {
  background: white;
  padding: 25px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.job-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 15px;
}

.job-header h3 {
  color: #333;
  font-size: 18px;
  flex: 1;
}

.job-type {
  background: #e3f2fd;
  color: #2196f3;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.job-location,
.job-salary {
  color: #666;
  font-size: 14px;
  margin: 8px 0;
}

.job-location i,
.job-salary i {
  color: #4caf50;
  margin-right: 8px;
}

.job-description {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
  margin: 15px 0;
}

.job-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.job-date {
  color: #999;
  font-size: 13px;
}

.btn-apply {
  padding: 8px 20px;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
}

.btn-apply:hover {
  background: #45a049;
}

.table-container {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 800px;
}

.data-table th,
.data-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.data-table th {
  background: #f5f7fa;
  font-weight: 600;
  color: #333;
}

.data-table tr:hover {
  background: #f9f9f9;
}

.btn-action {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  background: #2196f3;
  color: white;
}

.btn-action:hover {
  background: #1976d2;
}

.profile-container {
  max-width: 600px;
}

.profile-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.profile-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 40px;
  text-align: center;
  color: white;
}

.profile-avatar {
  font-size: 80px;
  margin-bottom: 15px;
}

.profile-header h2 {
  margin-bottom: 5px;
}

.profile-header p {
  opacity: 0.9;
}

.profile-details {
  padding: 30px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-item i {
  color: #4caf50;
  font-size: 18px;
  width: 20px;
}

.detail-item span {
  color: #666;
}

.no-data {
  text-align: center;
  padding: 60px 20px;
  color: #999;
}

.no-data i {
  font-size: 64px;
  color: #ddd;
  margin-bottom: 20px;
}

.no-data p {
  font-size: 18px;
  margin-bottom: 20px;
}

.btn-primary {
  padding: 12px 30px;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

.btn-primary:hover {
  background: #45a049;
}

@media (max-width: 768px) {
  .dashboard-container {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
  }

  .sidebar-menu {
    display: flex;
    overflow-x: auto;
  }

  .sidebar-menu li {
    white-space: nowrap;
  }

  .stats-grid,
  .jobs-grid {
    grid-template-columns: 1fr;
  }

  .app-header {
    flex-direction: column;
    align-items: start;
    gap: 10px;
  }
}
</style>
