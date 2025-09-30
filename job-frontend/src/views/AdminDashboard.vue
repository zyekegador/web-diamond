<template>
  <div class="admin-dashboard">
    <nav class="dashboard-nav">
      <div class="nav-brand">
        <h2>Admin Panel</h2>
      </div>
      <div class="nav-user">
        <span>Welcome, {{ user.username }}</span>
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
            :class="{ active: activeTab === 'create-hr' }"
            @click="activeTab = 'create-hr'"
          >
            <i class="fas fa-user-plus"></i>
            <span>Create HR Account</span>
          </li>
          <li
            :class="{ active: activeTab === 'hr-list' }"
            @click="activeTab = 'hr-list'"
          >
            <i class="fas fa-users"></i>
            <span>HR Staff List</span>
          </li>
        </ul>
      </aside>

      <main class="main-content">
        <!-- Overview Tab -->
        <div v-if="activeTab === 'overview'" class="content-section">
          <h1>System Overview</h1>
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon blue">
                <i class="fas fa-users"></i>
              </div>
              <div class="stat-info">
                <h3>Total HR Staff</h3>
                <p class="stat-number">{{ stats.hrCount }}</p>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon green">
                <i class="fas fa-user-check"></i>
              </div>
              <div class="stat-info">
                <h3>Total Applicants</h3>
                <p class="stat-number">{{ stats.applicantCount }}</p>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon orange">
                <i class="fas fa-briefcase"></i>
              </div>
              <div class="stat-info">
                <h3>Active Jobs</h3>
                <p class="stat-number">{{ stats.jobCount }}</p>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon purple">
                <i class="fas fa-file-alt"></i>
              </div>
              <div class="stat-info">
                <h3>Total Applications</h3>
                <p class="stat-number">{{ stats.applicationCount }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Create HR Tab -->
        <div v-if="activeTab === 'create-hr'" class="content-section">
          <h1>Create HR Account</h1>
          <div class="form-container">
            <form @submit.prevent="createHR" class="hr-form">
              <div class="form-row">
                <div class="form-group">
                  <label>First Name *</label>
                  <input type="text" v-model="hrForm.first_name" required />
                </div>
                <div class="form-group">
                  <label>Last Name *</label>
                  <input type="text" v-model="hrForm.last_name" required />
                </div>
              </div>

              <div class="form-group">
                <label>Username *</label>
                <input type="text" v-model="hrForm.username" required />
              </div>

              <div class="form-group">
                <label>Email *</label>
                <input type="email" v-model="hrForm.email" required />
              </div>

              <div class="form-group">
                <label>Employee ID</label>
                <input type="text" v-model="hrForm.employee_id" />
              </div>

              <div class="form-group">
                <label>Department</label>
                <input type="text" v-model="hrForm.department" />
              </div>

              <div class="form-group">
                <label>Phone Number</label>
                <input type="tel" v-model="hrForm.phone_number" />
              </div>

              <div class="form-group">
                <label>Password *</label>
                <input type="password" v-model="hrForm.password" required />
              </div>

              <div v-if="error" class="error-message">{{ error }}</div>
              <div v-if="success" class="success-message">{{ success }}</div>

              <button type="submit" class="btn-primary" :disabled="loading">
                {{ loading ? "Creating..." : "Create HR Account" }}
              </button>
            </form>
          </div>
        </div>

        <!-- HR List Tab -->
        <div v-if="activeTab === 'hr-list'" class="content-section">
          <h1>HR Staff List</h1>
          <div class="table-container">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Employee ID</th>
                  <th>Name</th>
                  <th>Username</th>
                  <th>Email</th>
                  <th>Department</th>
                  <th>Phone</th>
                  <th>Date Created</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="hr in hrList" :key="hr.id">
                  <td>{{ hr.employee_id || "N/A" }}</td>
                  <td>{{ hr.first_name }} {{ hr.last_name }}</td>
                  <td>{{ hr.username }}</td>
                  <td>{{ hr.email }}</td>
                  <td>{{ hr.department || "N/A" }}</td>
                  <td>{{ hr.phone_number || "N/A" }}</td>
                  <td>{{ formatDate(hr.created_at) }}</td>
                </tr>
              </tbody>
            </table>
            <div v-if="hrList.length === 0" class="no-data">
              No HR staff found
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "AdminDashboard",
  data() {
    return {
      user: JSON.parse(localStorage.getItem("user") || "{}"),
      activeTab: "overview",
      stats: {
        hrCount: 0,
        applicantCount: 0,
        jobCount: 0,
        applicationCount: 0,
      },
      hrForm: {
        username: "",
        email: "",
        password: "",
        first_name: "",
        last_name: "",
        phone_number: "",
        department: "",
        employee_id: "",
      },
      hrList: [],
      error: "",
      success: "",
      loading: false,
    };
  },
  mounted() {
    this.loadHRList();
  },
  methods: {
    async loadHRList() {
      try {
        const response = await api.getHRList();
        this.hrList = response.data;
        this.stats.hrCount = this.hrList.length;
      } catch (error) {
        console.error("Error loading HR list:", error);
      }
    },
    async createHR() {
      this.loading = true;
      this.error = "";
      this.success = "";

      try {
        await api.createHR(this.hrForm);
        this.success = "HR account created successfully!";
        this.hrForm = {
          username: "",
          email: "",
          password: "",
          first_name: "",
          last_name: "",
          phone_number: "",
          department: "",
          employee_id: "",
        };
        this.loadHRList();
      } catch (error) {
        if (error.response?.data) {
          const errors = error.response.data;
          this.error = Object.values(errors).flat().join(" ");
        } else {
          this.error = "Failed to create HR account";
        }
      } finally {
        this.loading = false;
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

<style scoped>
.admin-dashboard {
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
}

.content-section h1 {
  margin-bottom: 30px;
  color: #333;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
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

.form-container {
  background: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  max-width: 600px;
}

.hr-form .form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  color: #555;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
}

.form-group input:focus {
  outline: none;
  border-color: #4caf50;
}

.btn-primary {
  width: 100%;
  padding: 12px;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 10px;
}

.btn-primary:hover {
  background: #45a049;
}

.btn-primary:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.error-message {
  color: #f44336;
  padding: 10px;
  background: #ffebee;
  border-radius: 5px;
  margin-bottom: 10px;
}

.success-message {
  color: #4caf50;
  padding: 10px;
  background: #e8f5e9;
  border-radius: 5px;
  margin-bottom: 10px;
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

.no-data {
  text-align: center;
  padding: 40px;
  color: #999;
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

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .hr-form .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
