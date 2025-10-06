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
            <font-awesome-icon :icon="['fas', 'chart-line']" />
            <span>Overview</span>
          </li>
          <li
            :class="{ active: activeTab === 'browse-jobs' }"
            @click="activeTab = 'browse-jobs'"
          >
            <font-awesome-icon :icon="['fas', 'search']" />
            <span>Browse Jobs</span>
          </li>
          <li
            :class="{ active: activeTab === 'my-applications' }"
            @click="activeTab = 'my-applications'"
          >
            <font-awesome-icon :icon="['fas', 'file-alt']" />
            <span>My Applications</span>
          </li>
          <li
            :class="{ active: activeTab === 'profile' }"
            @click="activeTab = 'profile'"
          >
            <font-awesome-icon :icon="['fas', 'user']" />
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
                <font-awesome-icon :icon="['fas', 'file-alt']" />
              </div>
              <div class="stat-info">
                <h3>Total Applications</h3>
                <p class="stat-number">{{ applications.length }}</p>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon orange">
                <font-awesome-icon :icon="['fas', 'clock']" />
              </div>
              <div class="stat-info">
                <h3>Pending</h3>
                <p class="stat-number">{{ getPendingCount }}</p>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon green">
                <font-awesome-icon :icon="['fas', 'check-circle']" />
              </div>
              <div class="stat-info">
                <h3>Shortlisted</h3>
                <p class="stat-number">{{ getShortlistedCount }}</p>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon purple">
                <font-awesome-icon :icon="['fas', 'star']" />
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
                  <font-awesome-icon :icon="['fas', 'building']" />
                  {{ app.job.location }}
                  <span class="separator">|</span>
                  <font-awesome-icon :icon="['fas', 'calendar']" /> Applied
                  {{ formatDate(app.applied_at) }}
                </p>
                <p v-if="app.notes" class="app-notes">
                  <font-awesome-icon :icon="['fas', 'comment']" /> HR Notes:
                  {{ app.notes }}
                </p>
              </div>
              <div v-if="applications.length === 0" class="no-data">
                <font-awesome-icon :icon="['fas', 'inbox']" />
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
            <div
              v-for="job in openJobs"
              :key="job.id"
              class="job-card"
              :class="{ expanded: expandedJobId === job.id }"
            >
              <div class="job-header">
                <h3>{{ job.title }}</h3>
                <span class="job-type">{{ formatJobType(job.job_type) }}</span>
              </div>

              <!-- Basic Info (Always Visible) -->
              <div class="job-basic-info">
                <p class="job-location">
                  <font-awesome-icon :icon="['fas', 'map-marker-alt']" />
                  {{ job.place_of_assignment || job.location }}
                </p>
                <p class="job-salary">
                  <font-awesome-icon :icon="['fas', 'money-bill-wave']" /> PHP
                  {{ formatSalary(job.monthly_salary || job.salary_range) }}
                </p>
                <p class="job-education">
                  {{ truncateText(job.education_requirement, 100) }}
                </p>
              </div>

              <!-- Detailed Info (Shown when expanded) -->
              <div v-if="expandedJobId === job.id" class="job-details">
                <div class="detail-section">
                  <h4>
                    <font-awesome-icon :icon="['fas', 'info-circle']" />
                    Position Details
                  </h4>
                  <div class="detail-grid">
                    <div class="detail-item" v-if="job.plantilla_item_no">
                      <span class="detail-label">Plantilla Item No:</span>
                      <span class="detail-value">{{
                        job.plantilla_item_no
                      }}</span>
                    </div>
                    <div class="detail-item" v-if="job.salary_job_grade">
                      <span class="detail-label">Salary/Job Grade:</span>
                      <span class="detail-value">{{
                        job.salary_job_grade
                      }}</span>
                    </div>
                    <div class="detail-item">
                      <span class="detail-label">Monthly Salary:</span>
                      <span class="detail-value"
                        >PHP
                        {{
                          formatSalary(job.monthly_salary || job.salary_range)
                        }}</span
                      >
                    </div>
                    <div class="detail-item">
                      <span class="detail-label">Employment Type:</span>
                      <span class="detail-value">{{
                        formatJobType(job.job_type)
                      }}</span>
                    </div>
                  </div>
                </div>

                <div class="detail-section">
                  <h4>
                    <font-awesome-icon :icon="['fas', 'graduation-cap']" />
                    Qualifications
                  </h4>
                  <div class="qualification-item">
                    <span class="qual-label">Education:</span>
                    <span class="qual-value">{{
                      job.education_requirement || "Not specified"
                    }}</span>
                  </div>
                  <div class="qualification-item">
                    <span class="qual-label">Eligibility:</span>
                    <span class="qual-value">{{
                      job.eligibility_requirement || "Not specified"
                    }}</span>
                  </div>
                  <div class="qualification-item">
                    <span class="qual-label">Training:</span>
                    <span class="qual-value">{{
                      job.training_requirement || "None Required"
                    }}</span>
                  </div>
                  <div class="qualification-item">
                    <span class="qual-label">Work Experience:</span>
                    <span class="qual-value">{{
                      job.experience_requirement || "None Required"
                    }}</span>
                  </div>
                </div>

                <div class="detail-section">
                  <h4>
                    <font-awesome-icon :icon="['fas', 'clipboard-list']" /> Job
                    Description
                  </h4>
                  <p class="full-description">{{ job.description }}</p>
                </div>

                <div class="detail-section" v-if="job.competency_requirement">
                  <h4>
                    <font-awesome-icon :icon="['fas', 'tasks']" /> Competency
                    Requirements
                  </h4>
                  <p class="full-description">
                    {{ job.competency_requirement }}
                  </p>
                </div>

                <div class="detail-section">
                  <h4>
                    <font-awesome-icon :icon="['fas', 'calendar-alt']" />
                    Important Dates
                  </h4>
                  <div class="detail-grid">
                    <div class="detail-item">
                      <span class="detail-label">Posted:</span>
                      <span class="detail-value">{{
                        formatDate(job.created_at)
                      }}</span>
                    </div>
                    <div class="detail-item">
                      <span class="detail-label">Deadline:</span>
                      <span class="detail-value deadline">{{
                        formatDate(job.deadline)
                      }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="job-footer">
                <button @click="toggleJobDetails(job.id)" class="btn-details">
                  <font-awesome-icon
                    :icon="[
                      'fas',
                      expandedJobId === job.id ? 'chevron-up' : 'chevron-down',
                    ]"
                  />
                  {{
                    expandedJobId === job.id ? "Hide Details" : "View Details"
                  }}
                </button>
                <button
                  @click="openApplicationForm(job)"
                  class="btn-apply"
                  :disabled="hasAppliedToJob(job.id)"
                  :class="{ 'already-applied': hasAppliedToJob(job.id) }"
                >
                  <font-awesome-icon :icon="['fas', 'paper-plane']" />
                  {{
                    hasAppliedToJob(job.id) ? "Already Applied" : "Apply Now"
                  }}
                </button>
              </div>
            </div>
          </div>
          <div v-if="openJobs.length === 0" class="no-data">
            <font-awesome-icon :icon="['fas', 'briefcase']" />
            <p>No open positions available at the moment.</p>
            <p class="sub-text">Check back later for new opportunities!</p>
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
                      <font-awesome-icon :icon="['fas', 'eye']" /> View
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
                  <font-awesome-icon :icon="['fas', 'user-circle']" />
                </div>
                <h2>{{ user.first_name }} {{ user.last_name }}</h2>
                <p>@{{ user.username }}</p>
              </div>
              <div class="profile-details">
                <div class="detail-item">
                  <font-awesome-icon :icon="['fas', 'envelope']" />
                  <span>{{ user.email }}</span>
                </div>
                <div class="detail-item" v-if="user.phone_number">
                  <font-awesome-icon :icon="['fas', 'phone']" />
                  <span>{{ user.phone_number }}</span>
                </div>
                <div class="detail-item" v-if="user.date_of_birth">
                  <font-awesome-icon :icon="['fas', 'birthday-cake']" />
                  <span>{{ user.date_of_birth }}</span>
                </div>
                <div class="detail-item" v-if="user.address">
                  <font-awesome-icon :icon="['fas', 'map-marker-alt']" />
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
      expandedJobId: null,
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
    // Filter to show only open jobs
    openJobs() {
      return this.availableJobs.filter((job) => job.is_open !== false);
    },
    // Check if user applied to a specific job
    hasAppliedToJob() {
      return (jobId) => {
        return this.applications.some((app) => app.job.id === jobId);
      };
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
      // Check if user already applied for this job
      const alreadyApplied = this.applications.some(
        (app) => app.job.id === job.id
      );

      if (alreadyApplied) {
        alert("You have already submitted an application for this position.");
        return;
      }

      this.selectedJob = job;
      this.showApplicationForm = true;
    },
    closeApplicationForm() {
      this.showApplicationForm = false;
      this.selectedJob = null;
    },
    handleApplicationSubmitted() {
      this.closeApplicationForm();
      this.loadApplications();
      this.activeTab = "my-applications";
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
    toggleJobDetails(jobId) {
      this.expandedJobId = this.expandedJobId === jobId ? null : jobId;
    },
    formatSalary(salary) {
      if (!salary) return "Not specified";
      const num =
        typeof salary === "string"
          ? parseFloat(salary.replace(/[^\d.]/g, ""))
          : salary;
      return num.toLocaleString("en-US", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      });
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

.sidebar-menu li svg {
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

.app-details svg {
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
  transition: all 0.3s ease;
}

.job-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
}

.job-card.expanded {
  grid-column: 1 / -1;
  max-width: 100%;
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

.job-location svg,
.job-salary svg {
  color: #4caf50;
  margin-right: 8px;
}

.job-education {
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
  gap: 10px;
}

.btn-details {
  padding: 8px 16px;
  background: #f5f7fa;
  color: #666;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.btn-details:hover {
  background: #e3e8ef;
  color: #333;
}

.btn-details svg {
  font-size: 12px;
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
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-apply:hover {
  background: #45a049;
}

.btn-apply.already-applied {
  background: #9e9e9e;
  cursor: not-allowed;
}

.btn-apply:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.no-data .sub-text {
  font-size: 14px;
  color: #bbb;
  margin-bottom: 20px;
}

.job-details {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 2px solid #f5f7fa;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.detail-section {
  margin-bottom: 20px;
  padding: 15px;
  background: #f9fafb;
  border-radius: 8px;
}

.detail-section h4 {
  color: #4caf50;
  font-size: 16px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.detail-section h4 svg {
  font-size: 14px;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-label {
  font-size: 12px;
  color: #888;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-value {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

.detail-value.deadline {
  color: #ff9800;
  font-weight: 600;
}

.qualification-item {
  padding: 10px 0;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.qualification-item:last-child {
  border-bottom: none;
}

.qual-label {
  font-size: 13px;
  color: #666;
  font-weight: 600;
  min-width: 140px;
}

.qual-value {
  font-size: 13px;
  color: #333;
  flex: 1;
}

.full-description {
  font-size: 14px;
  color: #555;
  line-height: 1.6;
  white-space: pre-wrap;
  margin: 0;
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

.detail-item svg {
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

.no-data svg {
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

  .detail-grid {
    grid-template-columns: 1fr;
  }

  .job-footer {
    flex-direction: column;
    align-items: stretch;
  }

  .btn-details,
  .btn-apply {
    width: 100%;
    justify-content: center;
  }
}
</style>
