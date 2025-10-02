<script>
import api from "@/services/api";

export default {
  name: "HRDashboard",
  data() {
    return {
      user: JSON.parse(localStorage.getItem("user") || "{}"),
      activeView: "participants",
      searchQuery: "",
      selectedJob: "",
      showUserMenu: false,
      jobs: [],
      applications: [],
      showCreateJobModal: false,
      selectedApplication: null,
      jobForm: {
        title: "",
        plantilla_no: "",
        pay_grade: "",
        salary_range: "",
        job_type: "",
        location: "",
        eligibility: "",
        education: "",
        training: "",
        work_experience: "",
        description: "",
        requirements: "",
        posting_date: "",
        deadline: "",
      },
      statusForm: {
        status: "",
        notes: "",
      },
      error: "",
      success: "",
      loading: false,

      showEligibilitySuggestions: false,
      showEducationSuggestions: false,
      eligibilityOptions: [],
      educationOptions: [],
      filteredEligibility: [],
      filteredEducation: [],
    };
  },
  computed: {
    filteredApplications() {
      if (!this.selectedJob) return [];
      return this.applications.filter((app) => app.job.id == this.selectedJob);
    },
  },
  async mounted() {
    await this.loadOptions();
    this.loadJobs();
    this.loadAllApplications();

    // Close dropdowns when clicking outside
    document.addEventListener("click", (e) => {
      if (!e.target.closest(".autocomplete-wrapper")) {
        this.closeAllSuggestions();
      }
      if (!e.target.closest(".user-menu")) {
        this.closeUserMenu();
      }
    });
  },
  beforeUnmount() {
    document.removeEventListener("click", this.closeUserMenu);
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

        // Flatten education options from categories
        this.educationOptions = eduRes.data.flatMap((cat) =>
          cat.programs.map((prog) => prog.name)
        );

        // Flatten eligibility options from categories
        this.eligibilityOptions = eligRes.data.flatMap((cat) =>
          cat.types.map((type) => type.name)
        );
      } catch (error) {
        console.error("Error loading options:", error);
        // Fallback to empty arrays if backend fails
        this.educationOptions = [];
        this.eligibilityOptions = [];
      }
    },
    filterEligibility() {
      if (!this.jobForm.eligibility) {
        this.filteredEligibility = this.eligibilityOptions;
      } else {
        const search = this.jobForm.eligibility.toLowerCase();
        this.filteredEligibility = this.eligibilityOptions.filter((option) =>
          option.toLowerCase().includes(search)
        );
      }
      this.showEligibilitySuggestions = true;
    },
    selectEligibility(option) {
      this.jobForm.eligibility = option;
      this.showEligibilitySuggestions = false;
    },
    filterEducation() {
      if (!this.jobForm.education) {
        this.filteredEducation = this.educationOptions;
      } else {
        const search = this.jobForm.education.toLowerCase();
        this.filteredEducation = this.educationOptions.filter((option) =>
          option.toLowerCase().includes(search)
        );
      }
      this.showEducationSuggestions = true;
    },
    selectEducation(option) {
      this.jobForm.education = option;
      this.showEducationSuggestions = false;
    },
    closeAllSuggestions() {
      this.showEligibilitySuggestions = false;
      this.showEducationSuggestions = false;
    },
    async loadJobs() {
      try {
        const response = await api.getHRJobs();
        this.jobs = response.data;
      } catch (error) {
        console.error("Error loading jobs:", error);
      }
    },
    async loadAllApplications() {
      try {
        if (this.jobs.length === 0) return;
        const promises = this.jobs.map((job) => api.getJobApplications(job.id));
        const results = await Promise.all(promises);
        this.applications = results.flatMap((res) => res.data);
      } catch (error) {
        console.error("Error loading applications:", error);
      }
    },
    async createJob() {
      this.loading = true;
      this.error = "";
      this.success = "";

      try {
        const fullDescription = `
Position: ${this.jobForm.title}
Plantilla Item No: ${this.jobForm.plantilla_no || "N/A"}
Pay Grade: ${this.jobForm.pay_grade || "N/A"}
Eligibility: ${this.jobForm.eligibility}
Education: ${this.jobForm.education}
Training: ${this.jobForm.training || "None Required"}
Work Experience: ${this.jobForm.work_experience || "None Required"}

${this.jobForm.description}
        `;

        await api.createJob({
          title: this.jobForm.title,
          description: fullDescription,
          requirements: this.jobForm.requirements,
          job_type: this.jobForm.job_type,
          location: this.jobForm.location,
          salary_range: this.jobForm.salary_range,
          deadline: this.jobForm.deadline,
        });

        this.success = "Job posted successfully!";
        setTimeout(() => {
          this.closeCreateModal();
          this.loadJobs();
        }, 1500);
      } catch (error) {
        this.error = "Failed to create job posting";
      } finally {
        this.loading = false;
      }
    },
    closeCreateModal() {
      this.showCreateJobModal = false;
      this.jobForm = {
        title: "",
        plantilla_no: "",
        pay_grade: "",
        salary_range: "",
        job_type: "",
        location: "",
        eligibility: "",
        education: "",
        training: "",
        work_experience: "",
        description: "",
        requirements: "",
        posting_date: "",
        deadline: "",
      };
      this.error = "";
      this.success = "";
    },
    viewApplication(app) {
      this.selectedApplication = app;
      this.statusForm.status = app.status;
      this.statusForm.notes = app.notes || "";
    },
    async updateStatus() {
      try {
        await api.updateApplicationStatus(
          this.selectedApplication.id,
          this.statusForm
        );
        alert("Status updated successfully!");
        this.selectedApplication = null;
        this.loadAllApplications();
      } catch (error) {
        alert("Failed to update status");
      }
    },
    handleLogout() {
      api.logout();
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      localStorage.removeItem("userType");
      this.$router.push("/login");
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
      });
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
      </div>
      <div class="header-center">
        <div class="search-bar">
          <i class="fas fa-search"></i>
          <input type="text" v-model="searchQuery" placeholder="Search" />
        </div>
      </div>
      <div class="header-right">
        <div class="user-menu" @click.stop="toggleUserMenu">
          <div class="user-info">
            <span class="user-name"
              >{{ user.first_name }} {{ user.last_name }}</span
            >
            <span class="user-role">Human Resource</span>
          </div>
          <div class="user-avatar">
            <i class="fas fa-user-circle"></i>
          </div>
        </div>
        <div v-if="showUserMenu" class="user-dropdown" @click.stop>
          <div class="dropdown-header">
            <div class="dropdown-avatar">
              <i class="fas fa-user-circle"></i>
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

    <!-- Navigation Bar -->
    <nav class="main-nav">
      <ul class="nav-menu">
        <li
          :class="{ active: activeView === 'participants' }"
          @click="activeView = 'participants'"
        >
          <span>List of Job Posts</span>
          <i class="fas fa-chevron-down"></i>
        </li>
        <li
          :class="{ active: activeView === 'screening' }"
          @click="activeView = 'screening'"
        >
          <span>Screening Result</span>
          <i class="fas fa-chevron-down"></i>
        </li>
        <li
          :class="{ active: activeView === 'criteria' }"
          @click="activeView = 'criteria'"
        >
          <span>Criteria</span>
          <i class="fas fa-chevron-down"></i>
        </li>
      </ul>
      <div class="nav-actions">
        <button @click="showCreateJobModal = true" class="btn-new">
          <i class="fas fa-plus"></i> New
        </button>
        <button class="btn-settings">
          <i class="fas fa-cog"></i>
        </button>
      </div>
    </nav>

    <!-- Main Content Area -->
    <main class="main-content">
      <!-- Job Posts List View -->
      <div v-if="activeView === 'participants'" class="content-section">
        <div class="filter-section">
          <select v-model="selectedJob" class="filter-select">
            <option value="">Select Position Title</option>
            <option v-for="job in jobs" :key="job.id" :value="job.id">
              {{ job.title }}
            </option>
          </select>
          <button class="btn-filter">
            <i class="fas fa-filter"></i>
            <span>Filter</span>
          </button>
        </div>

        <div v-if="!selectedJob" class="placeholder-message">
          <p>Please Select Type of Job to View Applicant Entries</p>
        </div>

        <div v-else class="applicants-table-wrapper">
          <table class="applicants-table">
            <thead>
              <tr>
                <th>Phone Number</th>
                <th>Email</th>
                <th>First Name</th>
                <th>Last Name</th>
                <th>Nationality</th>
                <th>PDS</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="app in filteredApplications"
                :key="app.id"
                @click="viewApplication(app)"
              >
                <td>{{ app.applicant.phone_number || "N/A" }}</td>
                <td>{{ app.applicant.email }}</td>
                <td>{{ app.applicant.first_name }}</td>
                <td>{{ app.applicant.last_name }}</td>
                <td>Filipino</td>
                <td>
                  <a
                    v-if="app.pds"
                    :href="app.pds"
                    target="_blank"
                    class="file-link"
                  >
                    <i class="fas fa-file-pdf"></i> View
                  </a>
                  <span v-else>N/A</span>
                </td>
              </tr>
            </tbody>
          </table>
          <div v-if="filteredApplications.length === 0" class="no-data">
            Nothing to show...
          </div>
        </div>

        <!-- Pagination -->
        <div class="pagination">
          <button class="pagination-btn">‹</button>
          <button class="pagination-btn active">1</button>
          <button class="pagination-btn">2</button>
          <button class="pagination-btn">3</button>
          <button class="pagination-btn">4</button>
          <button class="pagination-btn">5</button>
          <button class="pagination-btn">›</button>
        </div>
      </div>

      <!-- Screening Result View -->
      <div v-if="activeView === 'screening'" class="content-section">
        <h2>Screening Result</h2>
        <p>Feature coming soon...</p>
      </div>

      <!-- Criteria View -->
      <div v-if="activeView === 'criteria'" class="content-section">
        <h2>Criteria Management</h2>
        <p>Feature coming soon...</p>
      </div>
    </main>

    <!-- Create Job Modal (CSC Format) -->
    <div
      v-if="showCreateJobModal"
      class="modal-overlay"
      @click="closeCreateModal"
    >
      <div class="modal-content csc-modal" @click.stop>
        <div class="modal-header">
          <h2>Create Job Posting (CSC Format)</h2>
          <button @click="closeCreateModal" class="btn-close">
            <i class="fas fa-times"></i>
          </button>
        </div>

        <div class="modal-body">
          <form @submit.prevent="createJob" class="csc-form">
            <div class="form-section">
              <h3>Position Information</h3>

              <div class="form-group">
                <label>Position Title *</label>
                <input
                  type="text"
                  v-model="jobForm.title"
                  required
                  placeholder="e.g. Administrative Officer II"
                />
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Plantilla Item No.</label>
                  <input
                    type="text"
                    v-model="jobForm.plantilla_no"
                    placeholder="e.g. 1081-19"
                  />
                </div>
                <div class="form-group">
                  <label>Salary/Job/Pay Grade</label>
                  <input
                    type="text"
                    v-model="jobForm.pay_grade"
                    placeholder="e.g. 11"
                  />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Monthly Salary *</label>
                  <input
                    type="text"
                    v-model="jobForm.salary_range"
                    required
                    placeholder="e.g. Php 30,024.00"
                  />
                </div>
                <div class="form-group">
                  <label>Job Type *</label>
                  <select v-model="jobForm.job_type" required>
                    <option value="">Select Type</option>
                    <option value="full_time">Full Time</option>
                    <option value="part_time">Part Time</option>
                    <option value="contract">Contract</option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label>Place of Assignment *</label>
                <input
                  type="text"
                  v-model="jobForm.location"
                  required
                  placeholder="e.g. City Accounting Department"
                />
              </div>
            </div>

            <div class="form-section">
              <h3>Qualifications</h3>

              <div class="form-group">
                <label>Eligibility *</label>
                <div class="autocomplete-wrapper">
                  <input
                    type="text"
                    v-model="jobForm.eligibility"
                    @input="filterEligibility"
                    @focus="filterEligibility"
                    required
                    placeholder="Start typing or select from suggestions..."
                  />
                  <div
                    v-if="
                      showEligibilitySuggestions &&
                      filteredEligibility.length > 0
                    "
                    class="suggestions-dropdown"
                  >
                    <div
                      v-for="(option, index) in filteredEligibility"
                      :key="index"
                      @click="selectEligibility(option)"
                      class="suggestion-item"
                    >
                      {{ option }}
                    </div>
                  </div>
                </div>
              </div>

              <div class="form-group">
                <label>Education *</label>
                <div class="autocomplete-wrapper">
                  <input
                    type="text"
                    v-model="jobForm.education"
                    @input="filterEducation"
                    @focus="filterEducation"
                    required
                    placeholder="Start typing or select from suggestions..."
                  />
                  <div
                    v-if="
                      showEducationSuggestions && filteredEducation.length > 0
                    "
                    class="suggestions-dropdown"
                  >
                    <div
                      v-for="(option, index) in filteredEducation"
                      :key="index"
                      @click="selectEducation(option)"
                      class="suggestion-item"
                    >
                      {{ option }}
                    </div>
                  </div>
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Training</label>
                  <input
                    type="text"
                    v-model="jobForm.training"
                    placeholder="None Required or specify"
                  />
                </div>
                <div class="form-group">
                  <label>Work Experience</label>
                  <input
                    type="text"
                    v-model="jobForm.work_experience"
                    placeholder="None Required or specify"
                  />
                </div>
              </div>

              <div class="form-group">
                <label>Job Description/Competency *</label>
                <textarea
                  v-model="jobForm.description"
                  rows="4"
                  required
                  placeholder="Describe the job responsibilities and competencies"
                ></textarea>
              </div>

              <div class="form-group">
                <label>Required Documents/Remarks</label>
                <textarea
                  v-model="jobForm.requirements"
                  rows="4"
                  placeholder="List required documents for application"
                ></textarea>
              </div>
            </div>

            <div class="form-section">
              <h3>Application Details</h3>

              <div class="form-row">
                <div class="form-group">
                  <label>Posting Date *</label>
                  <input type="date" v-model="jobForm.posting_date" required />
                </div>
                <div class="form-group">
                  <label>Closing Date *</label>
                  <input type="date" v-model="jobForm.deadline" required />
                </div>
              </div>
            </div>

            <div v-if="error" class="error-message">{{ error }}</div>
            <div v-if="success" class="success-message">{{ success }}</div>

            <div class="form-actions">
              <button
                type="button"
                @click="closeCreateModal"
                class="btn-cancel"
              >
                Cancel
              </button>
              <button type="submit" class="btn-submit" :disabled="loading">
                {{ loading ? "Creating..." : "Create Job Posting" }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- View Application Modal -->
    <div
      v-if="selectedApplication"
      class="modal-overlay"
      @click="selectedApplication = null"
    >
      <div class="modal-content application-modal" @click.stop>
        <div class="modal-header">
          <h2>Application Details</h2>
          <button @click="selectedApplication = null" class="btn-close">
            <i class="fas fa-times"></i>
          </button>
        </div>

        <div class="modal-body">
          <div class="applicant-details">
            <h3>Applicant Information</h3>
            <div class="info-grid">
              <div class="info-item">
                <strong>Name:</strong>
                <span
                  >{{ selectedApplication.applicant.first_name }}
                  {{ selectedApplication.applicant.last_name }}</span
                >
              </div>
              <div class="info-item">
                <strong>Email:</strong>
                <span>{{ selectedApplication.applicant.email }}</span>
              </div>
              <div class="info-item">
                <strong>Phone:</strong>
                <span>{{
                  selectedApplication.applicant.phone_number || "N/A"
                }}</span>
              </div>
              <div class="info-item">
                <strong>Applied Date:</strong>
                <span>{{ formatDate(selectedApplication.applied_at) }}</span>
              </div>
            </div>

            <div class="documents-section">
              <h3>Submitted Documents</h3>
              <div class="doc-list">
                <a
                  v-if="selectedApplication.resume"
                  :href="selectedApplication.resume"
                  target="_blank"
                  class="doc-item"
                >
                  <i class="fas fa-file-pdf"></i> Resume/CV
                </a>
                <a
                  v-if="selectedApplication.pds"
                  :href="selectedApplication.pds"
                  target="_blank"
                  class="doc-item"
                >
                  <i class="fas fa-file-pdf"></i> Personal Data Sheet (PDS)
                </a>
                <a
                  v-if="selectedApplication.certificates"
                  :href="selectedApplication.certificates"
                  target="_blank"
                  class="doc-item"
                >
                  <i class="fas fa-file-archive"></i> Certificates
                </a>
              </div>
            </div>

            <div class="cover-letter-section">
              <h3>Cover Letter</h3>
              <p>{{ selectedApplication.cover_letter }}</p>
            </div>

            <div class="status-section">
              <h3>Update Status</h3>
              <select v-model="statusForm.status" class="status-select">
                <option value="pending">Pending</option>
                <option value="under_review">Under Review</option>
                <option value="shortlisted">Shortlisted</option>
                <option value="accepted">Accepted</option>
                <option value="rejected">Rejected</option>
              </select>
              <textarea
                v-model="statusForm.notes"
                placeholder="Add notes for applicant"
                rows="3"
              ></textarea>
              <button @click="updateStatus" class="btn-update-status">
                Update Status
              </button>
            </div>
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
  background: linear-gradient(to bottom, #e8f0f7 0%, #f5f7fa 100%);
}

.top-header {
  background: white;
  padding: 15px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.header-left .logo {
  height: 50px;
}

.header-center {
  flex: 1;
  max-width: 500px;
  margin: 0 40px;
}

.search-bar {
  position: relative;
  width: 100%;
}

.search-bar i {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
}

.search-bar input {
  width: 100%;
  padding: 10px 15px 10px 45px;
  border: 1px solid #ddd;
  border-radius: 25px;
  background: #f5f7fa;
  font-size: 14px;
}

.search-bar input:focus {
  outline: none;
  border-color: #4a5f8d;
  background: white;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 15px;
  position: relative;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 15px;
  cursor: pointer;
  padding: 5px;
  border-radius: 8px;
  transition: background 0.2s;
}

.user-menu:hover {
  background: #f5f7fa;
}

.user-info {
  text-align: right;
}

.user-name {
  display: block;
  font-weight: 600;
  color: #333;
  font-size: 15px;
}

.user-role {
  display: block;
  font-size: 13px;
  color: #666;
}

.user-avatar {
  width: 45px;
  height: 45px;
  background: #4a5f8d;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
}

.user-dropdown {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  min-width: 280px;
  z-index: 1000;
  overflow: hidden;
}

.dropdown-header {
  padding: 20px;
  display: flex;
  gap: 15px;
  align-items: center;
  background: #f8f9fc;
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
  flex-shrink: 0;
}

.dropdown-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  overflow: hidden;
}

.dropdown-info strong {
  color: #333;
  font-size: 15px;
  font-weight: 600;
}

.dropdown-info span {
  color: #666;
  font-size: 13px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
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
  text-align: left;
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

.dropdown-item i {
  width: 20px;
  font-size: 16px;
}

.main-nav {
  background: #4a5f8d;
  padding: 0 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-menu {
  display: flex;
  list-style: none;
  gap: 5px;
}

.nav-menu li {
  padding: 15px 20px;
  cursor: pointer;
  color: white;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background 0.3s;
  font-size: 14px;
}

.nav-menu li:hover {
  background: rgba(255, 255, 255, 0.1);
}

.nav-menu li.active {
  background: rgba(255, 255, 255, 0.2);
}

.nav-actions {
  display: flex;
  gap: 10px;
}

.btn-new {
  background: #6c88c4;
  color: white;
  border: none;
  padding: 8px 20px;
  border-radius: 5px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.btn-new:hover {
  background: #5a76b0;
}

.btn-settings {
  background: transparent;
  color: white;
  border: none;
  width: 35px;
  height: 35px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

.btn-settings:hover {
  background: rgba(255, 255, 255, 0.1);
}

.main-content {
  padding: 20px 30px;
}

.content-section {
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  min-height: 500px;
}

.filter-section {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.filter-select {
  flex: 1;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background: #f8f9fc;
  font-size: 14px;
}

.btn-filter {
  padding: 10px 20px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 5px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.btn-filter:hover {
  background: #f5f7fa;
}

.placeholder-message {
  text-align: center;
  padding: 100px 20px;
  color: #999;
  font-size: 16px;
}

.applicants-table-wrapper {
  overflow-x: auto;
}

.applicants-table {
  width: 100%;
  border-collapse: collapse;
}

.applicants-table thead {
  background: #4a5f8d;
  color: white;
}

.applicants-table th {
  padding: 15px;
  text-align: left;
  font-weight: 600;
  font-size: 13px;
}

.applicants-table td {
  padding: 15px;
  border-bottom: 1px solid #eee;
  font-size: 14px;
  color: #333;
}

.applicants-table tbody tr {
  cursor: pointer;
  transition: background 0.2s;
}

.applicants-table tbody tr:hover {
  background: #f8f9fc;
}

.file-link {
  color: #4a5f8d;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 5px;
}

.file-link:hover {
  text-decoration: underline;
}

.no-data {
  text-align: center;
  padding: 60px 20px;
  color: #999;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: flex-end;
  gap: 5px;
  margin-top: 20px;
}

.pagination-btn {
  padding: 8px 12px;
  border: 1px solid #ddd;
  background: white;
  cursor: pointer;
  border-radius: 3px;
  font-size: 14px;
}

.pagination-btn:hover {
  background: #f5f7fa;
}

.pagination-btn.active {
  background: #4a5f8d;
  color: white;
  border-color: #4a5f8d;
}

/* Modal Styles */
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
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 10px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

.csc-modal {
  max-width: 900px;
}

.application-modal {
  max-width: 700px;
}

.modal-header {
  padding: 20px 25px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  background: white;
  z-index: 10;
}

.modal-header h2 {
  color: #333;
  font-size: 20px;
}

.btn-close {
  width: 35px;
  height: 35px;
  border: none;
  background: #f5f7fa;
  border-radius: 50%;
  cursor: pointer;
  font-size: 18px;
  color: #666;
}

.btn-close:hover {
  background: #e3e8ef;
}

.modal-body {
  padding: 25px;
}

/* CSC Form */
.csc-form .form-section {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.csc-form .form-section:last-of-type {
  border-bottom: none;
}

.csc-form .form-section h3 {
  color: #4a5f8d;
  margin-bottom: 20px;
  font-size: 18px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  color: #555;
  font-weight: 500;
  font-size: 14px;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
  font-family: inherit;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #4a5f8d;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.btn-cancel {
  padding: 10px 25px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.btn-cancel:hover {
  background: #f5f7fa;
}

.btn-submit {
  padding: 10px 25px;
  background: #4a5f8d;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.btn-submit:hover {
  background: #3d4f75;
}

.btn-submit:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.error-message {
  color: #f44336;
  padding: 10px;
  background: #ffebee;
  border-radius: 5px;
  margin-bottom: 10px;
  font-size: 14px;
}

.success-message {
  color: #4caf50;
  padding: 10px;
  background: #e8f5e9;
  border-radius: 5px;
  margin-bottom: 10px;
  font-size: 14px;
}

/* Application Details */
.applicant-details h3 {
  color: #4a5f8d;
  margin-bottom: 15px;
  font-size: 16px;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-bottom: 25px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.info-item strong {
  color: #666;
  font-size: 13px;
}

.info-item span {
  color: #333;
  font-size: 14px;
}

.documents-section,
.cover-letter-section,
.status-section {
  margin-top: 25px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.doc-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.doc-item {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 15px;
  background: #f8f9fc;
  border-radius: 5px;
  color: #4a5f8d;
  text-decoration: none;
  transition: background 0.2s;
}

.doc-item:hover {
  background: #e3e8ef;
}

.cover-letter-section p {
  color: #555;
  line-height: 1.6;
  font-size: 14px;
}

.status-select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  margin-bottom: 10px;
  font-size: 14px;
}

.status-section textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-family: inherit;
  font-size: 14px;
  margin-bottom: 10px;
}

.btn-update-status {
  padding: 10px 20px;
  background: #4a5f8d;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.btn-update-status:hover {
  background: #3d4f75;
}
</style>
