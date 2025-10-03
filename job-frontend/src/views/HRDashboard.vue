<script>
import api from "@/services/api";
import CreateJob from "./HRPanel/CreateJob.vue";

export default {
  name: "HRDashboard",
  components: {
    CreateJob,
  },
  data() {
    return {
      user: JSON.parse(localStorage.getItem("user") || "{}"),
      activeView: "participants",
      searchQuery: "",
      showUserMenu: false,
      jobs: [],
      showCreateJobModal: false,
      selectedJob: null,
      showApplicantsModal: false,
      currentPage: 1,
      itemsPerPage: 10,
      eligibilityOptions: [],
      educationOptions: [],
    };
  },
  computed: {
    filteredJobs() {
      if (!this.searchQuery) return this.paginatedJobs;

      const query = this.searchQuery.toLowerCase();
      return this.jobs.filter(
        (job) =>
          job.title.toLowerCase().includes(query) ||
          job.location.toLowerCase().includes(query)
      );
    },
    paginatedJobs() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.jobs.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.jobs.length / this.itemsPerPage);
    },
    displayedJobs() {
      return this.searchQuery ? this.filteredJobs : this.paginatedJobs;
    },
  },
  async mounted() {
    await this.loadOptions();
    this.loadJobs();
  },
  methods: {
    toggleUserMenu() {
      this.showUserMenu = !this.showUserMenu;
    },
    closeUserMenu() {
      this.showUserMenu = false;
    },
    async loadOptions() {
      try {
        const [eduRes, eligRes] = await Promise.all([
          api.getEducationOptions(),
          api.getEligibilityOptions(),
        ]);

        this.educationOptions = eduRes.data.flatMap((cat) =>
          cat.programs.map((prog) => prog.name)
        );

        this.eligibilityOptions = eligRes.data.flatMap((cat) =>
          cat.types.map((type) => type.name)
        );
      } catch (error) {
        console.error("Error loading options:", error);
        this.educationOptions = [];
        this.eligibilityOptions = [];
      }
    },
    async loadJobs() {
      try {
        const response = await api.getHRJobs();
        this.jobs = response.data.map((job) => ({
          ...job,
          applicationsCount: job.applications?.length || 0,
          status: this.getJobStatus(job),
        }));
      } catch (error) {
        console.error("Error loading jobs:", error);
      }
    },
    getJobStatus(job) {
      const deadline = new Date(job.deadline);
      const today = new Date();
      const daysLeft = Math.ceil((deadline - today) / (1000 * 60 * 60 * 24));

      if (daysLeft < 0) return { label: "Closed", color: "red" };
      if (daysLeft <= 5) return { label: "Re-open", color: "yellow" };
      if (job.applicationsCount > 0)
        return { label: "Screening", color: "blue" };
      return { label: "Open", color: "green" };
    },
    async viewApplicants(job) {
      try {
        const response = await api.getJobApplications(job.id);
        this.selectedJob = {
          ...job,
          applications: response.data,
        };
        this.showApplicantsModal = true;
      } catch (error) {
        console.error("Error loading applications:", error);
        alert("Failed to load applicants");
      }
    },
    handleJobCreated() {
      this.loadJobs();
    },
    handleLogout() {
      api.logout();
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      localStorage.removeItem("userType");
      this.$router.push("/");
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
      });
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
    getFileUrl(fileUrl) {
      if (!fileUrl) return null;
      // Ensure the URL is absolute
      if (fileUrl.startsWith("http")) return fileUrl;
      return `${api.defaults.baseURL}${fileUrl}`;
    },
  },
};
</script>

<template>
  <div class="hr-dashboard">
    <!-- Top Header -->
    <header class="top-header">
      <div class="header-left">
        <img src="@/assets/butuanon.png" alt="Logo" class="logo" />
        <div class="header-title">
          <h1>DASHBOARD</h1>
        </div>
      </div>

      <div class="header-right">
        <button class="icon-btn">
          <font-awesome-icon :icon="['fas', 'search']" />
        </button>
        <button class="icon-btn">
          <font-awesome-icon :icon="['fas', 'bell']" />
        </button>
        <button class="icon-btn">
          <font-awesome-icon :icon="['fas', 'cog']" />
        </button>

        <div class="user-menu" @click.stop="toggleUserMenu">
          <div class="user-avatar">
            <font-awesome-icon :icon="['fas', 'user-circle']" />
          </div>
          <div class="user-info">
            <span class="user-name"
              >{{ user.first_name }} {{ user.last_name }}</span
            >
            <span class="user-role">Human Resource</span>
          </div>
        </div>

        <div v-if="showUserMenu" class="user-dropdown" @click.stop>
          <div class="dropdown-header">
            <div class="dropdown-avatar">
              <font-awesome-icon :icon="['fas', 'user-circle']" />
            </div>
            <div class="dropdown-info">
              <strong>{{ user.first_name }} {{ user.last_name }}</strong>
              <span>{{ user.email }}</span>
            </div>
          </div>
          <div class="dropdown-divider"></div>
          <button @click="handleLogout" class="dropdown-item logout">
            <i class="fas fa-sign-out-alt"></i>
            <span>Logout</span>
          </button>
        </div>
      </div>
    </header>

    <!-- Navigation Tabs -->
    <nav class="main-nav">
      <div class="nav-tabs">
        <button
          :class="['nav-tab', { active: activeView === 'participants' }]"
          @click="activeView = 'participants'"
        >
          List of Participants
          <font-awesome-icon :icon="['fas', 'chevron-down']" />
        </button>
        <button
          :class="['nav-tab', { active: activeView === 'screening' }]"
          @click="activeView = 'screening'"
        >
          Screening Result
          <font-awesome-icon :icon="['fas', 'chevron-down']" />
        </button>
        <button
          :class="['nav-tab', { active: activeView === 'criteria' }]"
          @click="activeView = 'criteria'"
        >
          Criteria
          <font-awesome-icon :icon="['fas', 'chevron-down']" />
        </button>
        <button class="nav-tab">
          Archive
          <font-awesome-icon :icon="['fas', 'chevron-down']" />
        </button>
        <button class="nav-tab-add" @click="showCreateJobModal = true">
          <font-awesome-icon :icon="['fas', 'plus']" />
        </button>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="main-content">
      <div v-if="activeView === 'participants'" class="content-wrapper">
        <!-- Search and Actions Bar -->
        <div class="actions-bar">
          <div class="search-box">
            <font-awesome-icon :icon="['fas', 'search']" class="search-icon" />
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Search jobs..."
            />
          </div>

          <div class="action-buttons">
            <button class="btn-action">
              <font-awesome-icon :icon="['fas', 'sliders-h']" />
            </button>
            <button class="btn-primary" @click="showCreateJobModal = true">
              Edit
            </button>
          </div>
        </div>

        <!-- Jobs Table -->
        <div class="table-container">
          <table class="jobs-table">
            <thead>
              <tr>
                <th>Job Title</th>
                <th>Post Date</th>
                <th>Close Date</th>
                <th>No. Applicants</th>
                <th>Files</th>
                <th>Status</th>
                <th>View Applicant</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="job in displayedJobs" :key="job.id">
                <td class="job-title">{{ job.title }}</td>
                <td>{{ formatDate(job.created_at) }}</td>
                <td>{{ formatDate(job.deadline) }}</td>
                <td class="text-center">{{ job.applicationsCount }}</td>
                <td>
                  <a
                    v-if="job.applicationsCount > 0"
                    href="#"
                    class="file-link"
                    @click.prevent="viewApplicants(job)"
                  >
                    Applications_{{ job.id }}.zip
                  </a>
                  <span v-else class="no-files">No files</span>
                </td>
                <td>
                  <span :class="['status-badge', job.status.color]">
                    {{ job.status.label }}
                  </span>
                </td>
                <td class="text-center">
                  <button class="btn-view" @click="viewApplicants(job)">
                    View
                  </button>
                </td>
              </tr>
            </tbody>
          </table>

          <div v-if="displayedJobs.length === 0" class="no-data">
            <p>No jobs found</p>
          </div>
        </div>

        <!-- Pagination -->
        <div class="pagination">
          <span class="pagination-info">
            {{ (currentPage - 1) * itemsPerPage + 1 }} out of
            {{ jobs.length }} showing
          </span>

          <div class="pagination-controls">
            <button
              @click="changePage(currentPage - 1)"
              :disabled="currentPage === 1"
              class="pagination-btn"
            >
              <font-awesome-icon :icon="['fas', 'chevron-left']" />
            </button>

            <button
              v-for="page in totalPages"
              :key="page"
              @click="changePage(page)"
              :class="['pagination-btn', { active: currentPage === page }]"
            >
              {{ page }}
            </button>

            <button
              @click="changePage(currentPage + 1)"
              :disabled="currentPage === totalPages"
              class="pagination-btn"
            >
              <font-awesome-icon :icon="['fas', 'chevron-right']" />
            </button>
          </div>
        </div>
      </div>

      <!-- Other Views -->
      <div v-if="activeView === 'screening'" class="content-wrapper">
        <div class="placeholder">
          <h2>Screening Result</h2>
          <p>Feature coming soon...</p>
        </div>
      </div>

      <div v-if="activeView === 'criteria'" class="content-wrapper">
        <div class="placeholder">
          <h2>Criteria Management</h2>
          <p>Feature coming soon...</p>
        </div>
      </div>
    </main>

    <!-- Create Job Modal -->
    <CreateJob
      v-if="showCreateJobModal"
      :eligibilityOptions="eligibilityOptions"
      :educationOptions="educationOptions"
      @close="showCreateJobModal = false"
      @jobCreated="handleJobCreated"
    />

    <!-- View Applicants Modal -->
    <div
      v-if="showApplicantsModal"
      class="modal-overlay"
      @click="showApplicantsModal = false"
    >
      <div class="modal-content applicants-modal" @click.stop>
        <div class="modal-header">
          <h2>Applicants for {{ selectedJob?.title }}</h2>
          <button @click="showApplicantsModal = false" class="btn-close">
            <font-awesome-icon :icon="['fas', 'times']" />
          </button>
        </div>

        <div class="modal-body">
          <div class="applicants-list">
            <table class="applicants-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Phone</th>
                  <th>Applied Date</th>
                  <th>Status</th>
                  <th>Documents</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="app in selectedJob?.applications" :key="app.id">
                  <td>
                    {{ app.applicant.first_name }} {{ app.applicant.last_name }}
                  </td>
                  <td>{{ app.applicant.email }}</td>
                  <td>{{ app.applicant.phone_number || "N/A" }}</td>
                  <td>{{ formatDate(app.applied_at) }}</td>
                  <td>
                    <span :class="['status-badge', 'small', app.status]">
                      {{ app.status }}
                    </span>
                  </td>
                  <td class="documents-cell">
                    <a
                      v-if="app.resume"
                      :href="getFileUrl(app.resume)"
                      target="_blank"
                      class="doc-icon"
                      title="Resume"
                    >
                      <font-awesome-icon :icon="['fas', 'file-pdf']" />
                    </a>
                    <a
                      v-if="app.pds"
                      :href="getFileUrl(app.pds)"
                      target="_blank"
                      class="doc-icon"
                      title="PDS"
                    >
                      <font-awesome-icon :icon="['fas', 'file-alt']" />
                    </a>
                    <a
                      v-if="app.certificates"
                      :href="getFileUrl(app.certificates)"
                      target="_blank"
                      class="doc-icon"
                      title="Certificates"
                    >
                      <font-awesome-icon :icon="['fas', 'file-archive']" />
                    </a>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.hr-dashboard {
  min-height: 100vh;
}

/* Header */
.top-header {
  background: #2b3e75;

  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-left .logo {
  height: 75px;
}

.header-title h1 {
  color: white;
  font-size: 24px;
  font-weight: 700;
  letter-spacing: 1px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 15px;
  position: relative;
}

.icon-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.icon-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  padding: 8px 15px;
  border-radius: 25px;
  transition: background 0.3s;
}

.user-menu:hover {
  background: rgba(255, 255, 255, 0.1);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.user-name {
  color: white;
  font-weight: 600;
  font-size: 14px;
}

.user-role {
  color: rgba(255, 255, 255, 0.7);
  font-size: 12px;
}

.user-dropdown {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  min-width: 250px;
  z-index: 1000;
  overflow: hidden;
}

.dropdown-header {
  padding: 20px;
  background: #f8f9fc;
  display: flex;
  gap: 15px;
  align-items: center;
}

.dropdown-avatar {
  width: 50px;
  height: 50px;
  background: #4a5f8d;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 26px;
}

.dropdown-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.dropdown-info strong {
  color: #333;
  font-size: 15px;
}

.dropdown-info span {
  color: #666;
  font-size: 13px;
}

.dropdown-divider {
  height: 1px;
  background: #e3e8ef;
}

.dropdown-item {
  width: 100%;
  padding: 15px 20px;
  border: none;
  background: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  color: #333;
  transition: background 0.2s;
}

.dropdown-item:hover {
  background: #f8f9fc;
}

.dropdown-item.logout {
  color: #d32f2f;
}

.dropdown-item.logout:hover {
  background: #ffebee;
}

/* Navigation */
.main-nav {
  background: #3d4f75;
  padding: 0 30px;
}

.nav-tabs {
  display: flex;
  gap: 5px;
  align-items: center;
}

.nav-tab {
  padding: 15px 25px;
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.8);
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
  border-bottom: 3px solid transparent;
}

.nav-tab:hover {
  background: rgba(255, 255, 255, 0.05);
  color: white;
}

.nav-tab.active {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border-bottom-color: white;
}

.nav-tab-add {
  margin-left: auto;
  padding: 10px 15px;
  background: #5b72a8;
  border: none;
  color: white;
  cursor: pointer;
  border-radius: 5px;
  transition: all 0.3s;
}

.nav-tab-add:hover {
  background: #4a5f8d;
}

/* Main Content */
.main-content {
  padding: 30px;
}

.content-wrapper {
  background: white;
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

/* Actions Bar */
.actions-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.search-box {
  position: relative;
  width: 300px;
}

.search-icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
}

.search-box input {
  width: 100%;
  padding: 10px 15px 10px 40px;
  border: 1px solid #e0e0e0;
  border-radius: 25px;
  font-size: 14px;
  outline: none;
  transition: all 0.3s;
}

.search-box input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.btn-action {
  padding: 10px 15px;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-action:hover {
  background: #f5f5f5;
}

.btn-primary {
  padding: 10px 25px;
  background: #2b3e75;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s;
}

.btn-primary:hover {
  background: #1f2d54;
}

/* Table */
.table-container {
  overflow-x: auto;
  margin-bottom: 20px;
}

.jobs-table {
  width: 100%;
  border-collapse: collapse;
}

.jobs-table thead {
  background: #2b3e75;
}

.jobs-table th {
  padding: 15px;
  text-align: left;
  font-weight: 600;
  font-size: 13px;
  color: white;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.jobs-table td {
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
  font-size: 14px;
  color: #333;
}

.jobs-table tbody tr {
  transition: background 0.2s;
}

.jobs-table tbody tr:hover {
  background: #f8f9fc;
}

.job-title {
  font-weight: 600;
  color: #2b3e75;
}

.text-center {
  text-align: center;
}

.file-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 5px;
}

.file-link:hover {
  text-decoration: underline;
}

.no-files {
  color: #999;
  font-size: 13px;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  display: inline-block;
}

.status-badge.green {
  background: #e8f5e9;
  color: #2e7d32;
}

.status-badge.yellow {
  background: #fff3e0;
  color: #f57c00;
}

.status-badge.blue {
  background: #e3f2fd;
  color: #1976d2;
}

.status-badge.red {
  background: #ffebee;
  color: #c62828;
}

.status-badge.small {
  padding: 4px 10px;
  font-size: 11px;
}

.status-badge.pending {
  background: #fff3e0;
  color: #f57c00;
}

.status-badge.under_review {
  background: #e3f2fd;
  color: #1976d2;
}

.status-badge.shortlisted {
  background: #f3e5f5;
  color: #7b1fa2;
}

.status-badge.accepted {
  background: #e8f5e9;
  color: #2e7d32;
}

.status-badge.rejected {
  background: #ffebee;
  color: #c62828;
}

.btn-view {
  padding: 8px 20px;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s;
}

.btn-view:hover {
  background: #45a049;
}

.no-data {
  text-align: center;
  padding: 60px 20px;
  color: #999;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

.pagination-info {
  color: #666;
  font-size: 14px;
}

.pagination-controls {
  display: flex;
  gap: 5px;
}

.pagination-btn {
  padding: 8px 12px;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  cursor: pointer;
  color: #333;
  font-size: 14px;
  transition: all 0.3s;
}

.pagination-btn:hover:not(:disabled) {
  background: #f5f5f5;
  border-color: #667eea;
}

.pagination-btn.active {
  background: #2b3e75;
  color: white;
  border-color: #2b3e75;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 15px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

.applicants-modal {
  max-width: 1200px;
}

.modal-header {
  padding: 25px 30px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  background: white;
  z-index: 10;
}

.modal-header h2 {
  color: #2b3e75;
  font-size: 22px;
  font-weight: 700;
}

.btn-close {
  width: 40px;
  height: 40px;
  border: none;
  background: #f5f5f5;
  border-radius: 50%;
  cursor: pointer;
  font-size: 18px;
  color: #666;
  transition: all 0.3s;
}

.btn-close:hover {
  background: #e0e0e0;
}

.modal-body {
  padding: 30px;
}

.applicants-table {
  width: 100%;
  border-collapse: collapse;
}

.applicants-table thead {
  background: #f8f9fc;
}

.applicants-table th {
  padding: 12px 15px;
  text-align: left;
  font-weight: 600;
  font-size: 13px;
  color: #2b3e75;
  text-transform: uppercase;
}

.applicants-table td {
  padding: 12px 15px;
  border-bottom: 1px solid #f0f0f0;
  font-size: 14px;
}

.documents-cell {
  display: flex;
  gap: 10px;
  align-items: center;
}

.doc-icon {
  width: 35px;
  height: 35px;
  background: #f8f9fc;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #667eea;
  text-decoration: none;
  transition: all 0.3s;
  font-size: 16px;
}

.doc-icon:hover {
  background: #667eea;
  color: white;
  transform: translateY(-2px);
}

/* Placeholder */
.placeholder {
  text-align: center;
  padding: 100px 20px;
}

.placeholder h2 {
  color: #2b3e75;
  font-size: 28px;
  margin-bottom: 10px;
}

.placeholder p {
  color: #666;
  font-size: 16px;
}

/* Responsive */
@media (max-width: 1024px) {
  .header-title h1 {
    font-size: 20px;
  }

  .nav-tabs {
    overflow-x: auto;
  }

  .actions-bar {
    flex-direction: column;
    gap: 15px;
    align-items: stretch;
  }

  .search-box {
    width: 100%;
  }

  .table-container {
    overflow-x: scroll;
  }
}

@media (max-width: 768px) {
  .top-header {
    padding: 15px;
  }

  .header-left .logo {
    height: 40px;
  }

  .user-info {
    display: none;
  }

  .main-content {
    padding: 15px;
  }

  .content-wrapper {
    padding: 15px;
  }

  .pagination {
    flex-direction: column;
    gap: 15px;
  }
}
</style>
