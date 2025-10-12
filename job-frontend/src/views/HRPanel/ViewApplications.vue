<template>
  <div class="view-application">
    <!-- Header -->
    <header class="page-header">
      <div class="header-content">
        <button @click="goBack" class="btn-back">
          <font-awesome-icon :icon="['fas', 'arrow-left']" />
          <span>Back to Dashboard</span>
        </button>
        <h1 v-if="selectedJob">Applicants for {{ selectedJob.title }}</h1>
        <h1 v-else>Loading...</h1>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      <div v-if="loading" class="loading-state">
        <font-awesome-icon :icon="['fas', 'spinner']" spin size="2x" />
        <p>Loading applicants...</p>
      </div>

      <div v-else-if="error" class="error-state">
        <font-awesome-icon :icon="['fas', 'exclamation-circle']" size="2x" />
        <p>{{ error }}</p>
        <button @click="loadApplications" class="btn-retry">Retry</button>
      </div>

      <div v-else class="content-wrapper">
        <!-- Job Info Card -->
        <div class="job-info-card">
          <div class="job-info-header">
            <h2>{{ selectedJob.title }}</h2>
            <span :class="['status-badge', selectedJob.status.color]">
              {{ selectedJob.status.label }}
            </span>
          </div>
          <div class="job-info-details">
            <div class="info-item">
              <font-awesome-icon :icon="['fas', 'calendar']" />
              <span>Posted: {{ formatDate(selectedJob.created_at) }}</span>
            </div>
            <div class="info-item">
              <font-awesome-icon :icon="['fas', 'calendar-times']" />
              <span>Deadline: {{ formatDate(selectedJob.deadline) }}</span>
            </div>
            <div class="info-item">
              <font-awesome-icon :icon="['fas', 'users']" />
              <span>{{ selectedJob.applications.length }} Applicants</span>
            </div>
            <div class="info-item">
              <font-awesome-icon :icon="['fas', 'map-marker-alt']" />
              <span>{{ selectedJob.location }}</span>
            </div>
          </div>
        </div>

        <!-- Applicants Table -->
        <div class="applicants-section">
          <div class="section-header">
            <h3>Applications</h3>
            <div class="header-actions">
              <button class="btn-download">
                <font-awesome-icon :icon="['fas', 'download']" />
                Download All
              </button>
            </div>
          </div>

          <div class="table-container">
            <table class="applicants-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Phone</th>
                  <th>Applied Date</th>
                  <th>Status</th>
                  <th>Documents</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="app in selectedJob.applications" :key="app.id">
                  <td class="applicant-name">
                    <div class="name-cell">
                      <div class="avatar">
                        {{
                          getInitials(
                            app.applicant.first_name,
                            app.applicant.last_name
                          )
                        }}
                      </div>
                      <span>
                        {{ app.applicant.first_name }}
                        {{ app.applicant.last_name }}
                      </span>
                    </div>
                  </td>
                  <td>{{ app.applicant.email }}</td>
                  <td>{{ app.applicant.phone_number || "N/A" }}</td>
                  <td>{{ formatDate(app.applied_at) }}</td>
                  <td>
                    <span :class="['status-badge', 'small', app.status]">
                      {{ formatStatus(app.status) }}
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
                    <span
                      v-if="!app.resume && !app.pds && !app.certificates"
                      class="no-docs"
                    >
                      No documents
                    </span>
                  </td>
                  <td class="actions-cell">
                    <button class="btn-action-sm" title="View Details">
                      <font-awesome-icon :icon="['fas', 'eye']" />
                    </button>
                    <button class="btn-action-sm" title="Update Status">
                      <font-awesome-icon :icon="['fas', 'edit']" />
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>

            <div v-if="selectedJob.applications.length === 0" class="no-data">
              <font-awesome-icon :icon="['fas', 'inbox']" size="3x" />
              <p>No applications yet</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "ViewApplication",
  data() {
    return {
      selectedJob: null,
      loading: true,
      error: null,
    };
  },
  async mounted() {
    await this.loadApplications();
  },
  methods: {
    async loadApplications() {
      this.loading = true;
      this.error = null;

      try {
        const jobId = this.$route.params.jobId;
        const query = this.$route.query;

        // Debug: Check what data we're receiving
        console.log("Job ID:", jobId);
        console.log("Query params:", query);

        // Fetch applications
        const applicationsResponse = await api.getJobApplications(jobId);
        console.log("Applications response:", applicationsResponse.data);

        // Use job data from query params
        this.selectedJob = {
          id: jobId,
          title: query.title || "Job Opening",
          location: query.location || "N/A",
          created_at: query.created_at || new Date().toISOString(),
          deadline: query.deadline || new Date().toISOString(),
          applications: applicationsResponse.data || [], // Ensure it's always an array
          status: {
            label: query.status_label || "Open",
            color: query.status_color || "green",
          },
        };

        console.log("Selected Job:", this.selectedJob);
        console.log(
          "Applications count:",
          this.selectedJob.applications.length
        ); // Add this debug
      } catch (error) {
        console.error("Error loading applications:", error);
        console.error("Error response:", error.response); // Add more debug info
        this.error =
          error.response?.data?.message ||
          "Failed to load applicants. Please try again.";
      } finally {
        this.loading = false;
      }
    },
    getJobStatus(job) {
      // Handle null or undefined job
      if (!job || !job.deadline) {
        return { label: "Open", color: "green" };
      }

      const deadline = new Date(job.deadline);
      const today = new Date();
      const daysLeft = Math.ceil((deadline - today) / (1000 * 60 * 60 * 24));

      if (daysLeft < 0) return { label: "Closed", color: "red" };
      if (daysLeft <= 5) return { label: "Re-open", color: "yellow" };
      if (job.applications?.length > 0)
        return { label: "Screening", color: "blue" };
      return { label: "Open", color: "green" };
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
      });
    },
    formatStatus(status) {
      return status.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase());
    },
    getFileUrl(fileUrl) {
      if (!fileUrl) return null;
      if (fileUrl.startsWith("http")) return fileUrl;
      return `${api.defaults.baseURL}${fileUrl}`;
    },
    getInitials(firstName, lastName) {
      return `${firstName?.charAt(0) || ""}${
        lastName?.charAt(0) || ""
      }`.toUpperCase();
    },
    goBack() {
      this.$router.push({ name: "HRDashboard" });
    },
  },
};
</script>

<style scoped>
.view-application {
  min-height: 100vh;
  background: #f5f7fa;
}

/* Header */
.page-header {
  background: white;
  border-bottom: 1px solid #e0e0e0;
  padding: 20px 30px;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
}

.btn-back {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 20px;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  color: #666;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 15px;
  transition: all 0.3s;
}

.btn-back:hover {
  background: #f5f5f5;
  border-color: #2b3e75;
  color: #2b3e75;
}

.page-header h1 {
  color: #2b3e75;
  font-size: 28px;
  font-weight: 700;
  margin: 0;
}

/* Main Content */
.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 30px;
}

/* Loading & Error States */
.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100px 20px;
  color: #666;
  gap: 20px;
}

.error-state {
  color: #d32f2f;
}

.btn-retry {
  padding: 10px 25px;
  background: #2b3e75;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s;
}

.btn-retry:hover {
  background: #1f2d54;
}

/* Content Wrapper */
.content-wrapper {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

/* Job Info Card */
.job-info-card {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.job-info-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.job-info-header h2 {
  color: #2b3e75;
  font-size: 22px;
  font-weight: 700;
  margin: 0;
}

.job-info-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #666;
  font-size: 14px;
}

.info-item svg {
  color: #2b3e75;
  font-size: 16px;
}

/* Applicants Section */
.applicants-section {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.section-header h3 {
  color: #2b3e75;
  font-size: 20px;
  font-weight: 700;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.btn-download {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s;
}

.btn-download:hover {
  background: #45a049;
}

/* Table */
.table-container {
  overflow-x: auto;
}

.applicants-table {
  width: 100%;
  border-collapse: collapse;
}

.applicants-table thead {
  background: #f8f9fc;
}

.applicants-table th {
  padding: 15px;
  text-align: left;
  font-weight: 600;
  font-size: 13px;
  color: #2b3e75;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 2px solid #e0e0e0;
}

.applicants-table td {
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
  font-size: 14px;
  color: #333;
}

.applicants-table tbody tr {
  transition: background 0.2s;
}

.applicants-table tbody tr:hover {
  background: #f8f9fc;
}

.name-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 14px;
}

.applicant-name {
  font-weight: 600;
}

.documents-cell {
  display: flex;
  gap: 10px;
  align-items: center;
}

.doc-icon {
  width: 36px;
  height: 36px;
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

.no-docs {
  color: #999;
  font-size: 13px;
  font-style: italic;
}

.actions-cell {
  display: flex;
  gap: 8px;
}

.btn-action-sm {
  width: 32px;
  height: 32px;
  background: #f8f9fc;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  color: #667eea;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-action-sm:hover {
  background: #667eea;
  color: white;
}

/* Status Badges */
.status-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  display: inline-block;
  text-transform: capitalize;
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

/* No Data State */
.no-data {
  text-align: center;
  padding: 80px 20px;
  color: #999;
}

.no-data svg {
  margin-bottom: 20px;
  opacity: 0.5;
}

.no-data p {
  font-size: 16px;
}

/* Responsive */
@media (max-width: 1024px) {
  .job-info-details {
    grid-template-columns: repeat(2, 1fr);
  }

  .table-container {
    overflow-x: scroll;
  }
}

@media (max-width: 768px) {
  .main-content {
    padding: 15px;
  }

  .job-info-card,
  .applicants-section {
    padding: 20px;
  }

  .job-info-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }

  .job-info-details {
    grid-template-columns: 1fr;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }

  .page-header h1 {
    font-size: 22px;
  }
}
</style>
