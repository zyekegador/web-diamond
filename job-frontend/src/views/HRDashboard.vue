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
          <span>NEW</span>
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
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="job in displayedJobs" :key="job.id">
                <td class="job-title">{{ job.title }}</td>
                <td>{{ formatDate(job.created_at) }}</td>
                <td>{{ formatDate(job.deadline) }}</td>
                <td class="text-center">{{ job.applicationsCount }}</td>
                <td>
                  <span :class="['status-badge', job.status.color]">
                    {{ job.status.label }}
                  </span>
                </td>
                <td class="text-center">
                  <div class="action-buttons-group">
                    <button
                      class="btn-view-action"
                      @click="viewApplicants(job)"
                    >
                      View
                    </button>
                    <button class="btn-edit-action" @click="openEditModal(job)">
                      Edit
                    </button>
                  </div>
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

    <!-- Edit Date Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click="closeEditModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Edit Posting Date</h2>
          <button class="close-btn" @click="closeEditModal">
            <font-awesome-icon :icon="['fas', 'times']" />
          </button>
        </div>

        <div class="modal-body">
          <div class="form-group">
            <label>Job Title</label>
            <input
              type="text"
              :value="editingJob?.title"
              disabled
              class="form-input disabled"
            />
          </div>

          <div class="form-group">
            <label>Post Date</label>
            <input type="date" v-model="editPostDate" class="form-input" />
          </div>

          <div class="form-group">
            <label>Close Date</label>
            <input
              type="date"
              v-model="editCloseDate"
              class="form-input"
              :min="editPostDate"
            />
          </div>

          <div v-if="isReopeningJob" class="reopen-notice">
            <font-awesome-icon :icon="['fas', 'info-circle']" />
            <span
              >This job posting is currently <strong>Closed</strong>. Updating
              the close date to a future date will <strong>reopen</strong> the
              job posting.</span
            >
          </div>

          <div v-if="isClosingJob" class="closing-notice">
            <font-awesome-icon :icon="['fas', 'exclamation-triangle']" />
            <span
              >The selected close date is in the past. This job posting will be
              marked as <strong>Closed</strong>.</span
            >
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-cancel" @click="closeEditModal">Cancel</button>
          <button class="btn-save" @click="saveEditedDates">
            Save Changes
          </button>
        </div>
      </div>
    </div>

    <!-- Create Job Modal -->
    <CreateJob
      v-if="showCreateJobModal"
      :eligibilityOptions="eligibilityOptions"
      :educationOptions="educationOptions"
      @close="showCreateJobModal = false"
      @jobCreated="handleJobCreated"
    />

    <!-- Toast Notification -->
    <transition name="toast">
      <div
        v-if="notification.show"
        :class="['toast-notification', notification.type]"
      >
        <div class="toast-icon">
          <font-awesome-icon
            :icon="[
              'fas',
              notification.type === 'success'
                ? 'check-circle'
                : notification.type === 'error'
                ? 'exclamation-circle'
                : 'info-circle',
            ]"
          />
        </div>
        <span class="toast-message">{{ notification.message }}</span>
      </div>
    </transition>
  </div>
</template>

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
      currentPage: 1,
      itemsPerPage: 10,
      eligibilityOptions: [],
      educationOptions: [],
      activeActionMenu: null,
      showEditModal: false,
      editingJob: null,
      editPostDate: "",
      editCloseDate: "",
      notification: {
        show: false,
        message: "",
        type: "success", // success, error, info
      },
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
    isReopeningJob() {
      if (!this.editingJob || !this.editCloseDate) return false;

      const wasClosedBefore = this.editingJob.status.label === "Closed";
      const newDeadline = new Date(this.editCloseDate);
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      newDeadline.setHours(0, 0, 0, 0);

      return wasClosedBefore && newDeadline >= today;
    },
    isClosingJob() {
      if (!this.editingJob || !this.editCloseDate) return false;

      const newDeadline = new Date(this.editCloseDate);
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      newDeadline.setHours(0, 0, 0, 0);

      // Show warning if setting deadline to past date
      return newDeadline < today;
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
    openEditModal(job) {
      this.editingJob = job;

      // Parse dates more carefully
      const createdDate = new Date(job.created_at);
      const deadlineDate = new Date(job.deadline);

      // Format as YYYY-MM-DD for input[type="date"]
      this.editPostDate = this.formatDateForInput(createdDate);
      this.editCloseDate = this.formatDateForInput(deadlineDate);

      this.showEditModal = true;
    },
    formatDateForInput(date) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, "0");
      const day = String(date.getDate()).padStart(2, "0");
      return `${year}-${month}-${day}`;
    },
    closeEditModal() {
      this.showEditModal = false;
      this.editingJob = null;
      this.editPostDate = "";
      this.editCloseDate = "";
    },
    async saveEditedDates() {
      try {
        // Validate that close date is after post date
        if (new Date(this.editCloseDate) < new Date(this.editPostDate)) {
          this.showNotification("Close date must be after post date", "error");
          return;
        }

        // Check the new status based on the deadline
        const newDeadline = new Date(this.editCloseDate);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        newDeadline.setHours(0, 0, 0, 0);

        const wasClosedBefore = this.editingJob.status.label === "Closed";
        const willBeClosed = newDeadline < today;
        const willBeReopened = wasClosedBefore && newDeadline >= today;

        // Prepare data to send
        const updateData = {
          created_at: this.editPostDate,
          deadline: this.editCloseDate,
        };

        console.log("Sending update data:", updateData);

        // Update job dates via API
        const response = await api.updateJobDates(
          this.editingJob.id,
          updateData
        );
        console.log("Update response:", response);

        // Reload jobs to reflect changes
        await this.loadJobs();
        this.closeEditModal();

        // Show appropriate success message
        if (willBeClosed) {
          this.showNotification(
            "Job posting has been closed due to past deadline!",
            "info"
          );
        } else if (willBeReopened) {
          this.showNotification(
            "Job posting has been successfully reopened!",
            "success"
          );
        } else {
          this.showNotification("Job dates updated successfully!", "success");
        }
      } catch (error) {
        console.error("Error updating job dates:", error);
        console.error("Error response:", error.response?.data);
        this.showNotification(
          `Failed to update job dates: ${
            error.response?.data?.error || error.message
          }`,
          "error"
        );
      }
    },
    showNotification(message, type = "success") {
      this.notification.message = message;
      this.notification.type = type;
      this.notification.show = true;

      setTimeout(() => {
        this.notification.show = false;
      }, 3000);
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

        this.eligibilityOptions = eligRes.data.all_categories.flatMap((cat) =>
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
          applicationsCount: job.applications_count || 0,
          status: this.getJobStatus(job),
        }));
      } catch (error) {
        console.error("Error loading jobs:", error);
      }
    },
    getJobStatus(job) {
      const deadline = new Date(job.deadline);
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      deadline.setHours(0, 0, 0, 0);

      const daysLeft = Math.ceil((deadline - today) / (1000 * 60 * 60 * 24));

      if (daysLeft < 0) return { label: "Closed", color: "red" };
      if (daysLeft <= 5) return { label: "Re-open", color: "orange" };
      if (job.applicationsCount > 0)
        return { label: "Screening", color: "blue" };
      return { label: "Open", color: "green" };
    },
    viewApplicants(job) {
      this.$router.push({
        name: "ViewApplication",
        params: { jobId: job.id },
        query: {
          title: job.title,
          location: job.place_of_assignment || job.location,
          created_at: job.created_at,
          deadline: job.deadline,
          status_label: job.status.label,
          status_color: job.status.color,
          applications_count: job.applicationsCount,
        },
      });
    },
    handleJobCreated() {
      this.loadJobs();
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
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
  },
};
</script>

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

.status-badge.orange {
  background: #fff3e0;
  color: #e65100;
}

.status-badge.blue {
  background: #e3f2fd;
  color: #1976d2;
}

.status-badge.red {
  background: #ffebee;
  color: #c62828;
}

/* Action Buttons Group */
.action-buttons-group {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.btn-view-action {
  padding: 8px 20px;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-weight: 500;
  font-size: 13px;
  transition: all 0.3s;
  min-width: 70px;
}

.btn-view-action:hover {
  background: #45a049;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
}

.btn-edit-action {
  padding: 8px 20px;
  background: #9e9e9e;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-weight: 500;
  font-size: 13px;
  transition: all 0.3s;
  min-width: 70px;
}

.btn-edit-action:hover {
  background: #757575;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(158, 158, 158, 0.3);
}

.no-data {
  text-align: center;
  padding: 60px 20px;
  color: #999;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.modal-header {
  padding: 20px 25px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  color: #2b3e75;
  font-size: 20px;
  font-weight: 600;
}

.close-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #f5f5f5;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
  transition: all 0.3s;
}

.close-btn:hover {
  background: #e0e0e0;
  color: #333;
}

.modal-body {
  padding: 25px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 500;
  font-size: 14px;
}

.form-input {
  width: 100%;
  padding: 10px 15px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  transition: all 0.3s;
}

.form-input:focus {
  border-color: #2b3e75;
  box-shadow: 0 0 0 3px rgba(43, 62, 117, 0.1);
}

.form-input.disabled {
  background: #f5f5f5;
  color: #999;
  cursor: not-allowed;
}

.reopen-notice {
  background: #fff3e0;
  border-left: 4px solid #f57c00;
  padding: 12px 15px;
  border-radius: 6px;
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 13px;
  color: #e65100;
  margin-top: 10px;
}

.reopen-notice svg {
  flex-shrink: 0;
  margin-top: 2px;
  font-size: 16px;
}

.reopen-notice strong {
  font-weight: 600;
}

.closing-notice {
  background: #ffebee;
  border-left: 4px solid #d32f2f;
  padding: 12px 15px;
  border-radius: 6px;
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 13px;
  color: #c62828;
  margin-top: 10px;
}

.closing-notice svg {
  flex-shrink: 0;
  margin-top: 2px;
  font-size: 16px;
}

.closing-notice strong {
  font-weight: 600;
}

.modal-footer {
  padding: 20px 25px;
  border-top: 1px solid #e0e0e0;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.btn-cancel {
  padding: 10px 20px;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  color: #666;
  transition: all 0.3s;
}

.btn-cancel:hover {
  background: #f5f5f5;
}

.btn-save {
  padding: 10px 20px;
  background: #2b3e75;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s;
}

.btn-save:hover {
  background: #1f2d54;
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

  .modal-content {
    width: 95%;
  }
}
</style>
