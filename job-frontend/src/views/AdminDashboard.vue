<template>
  <div class="admin-dashboard">
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
            <span class="user-name">{{ user.username }}</span>
            <span class="user-role">Admin</span>
          </div>
        </div>

        <div v-if="showUserMenu" class="user-dropdown" @click.stop>
          <div class="dropdown-header">
            <div class="dropdown-avatar">
              <font-awesome-icon :icon="['fas', 'user-circle']" />
            </div>
            <div class="dropdown-info">
              <strong>{{ user.username }} {{ user.last_name }}</strong>
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

    <!--Dashboard-->

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
            :class="{ active: activeTab === 'create-hr' }"
            @click="activeTab = 'create-hr'"
          >
            <font-awesome-icon :icon="['fas', 'user-plus']" />
            <span>Create HR Account</span>
          </li>
          <li
            :class="{ active: activeTab === 'hr-list' }"
            @click="activeTab = 'hr-list'"
          >
            <font-awesome-icon :icon="['fas', 'users']" />
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
                <font-awesome-icon :icon="['fas', 'users']" />
              </div>
              <div class="stat-info">
                <h3>Total HR Staff</h3>
                <p class="stat-number">{{ stats.hrCount }}</p>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon green">
                <font-awesome-icon :icon="['fas', 'user-check']" />
              </div>
              <div class="stat-info">
                <h3>Total Applicants</h3>
                <p class="stat-number">{{ stats.applicantCount }}</p>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon orange">
                <font-awesome-icon :icon="['fas', 'briefcase']" />
              </div>
              <div class="stat-info">
                <h3>Active Jobs</h3>
                <p class="stat-number">{{ stats.jobCount }}</p>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon purple">
                <font-awesome-icon :icon="['fas', 'file-alt']" />
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
      showUserMenu: false,
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
    document.addEventListener("click", this.closeUserMenu);
  },
  beforeUnmount() {
    document.removeEventListener("click", this.closeUserMenu);
  },
  methods: {
    toggleUserMenu() {
      this.showUserMenu = !this.showUserMenu;
    },
    closeUserMenu(event) {
      const menu = this.$el.querySelector(".user-dropdown");
      const avatar = this.$el.querySelector(".user-menu");
      if (
        this.showUserMenu &&
        menu &&
        !menu.contains(event.target) &&
        !avatar.contains(event.target)
      ) {
        this.showUserMenu = false;
      }
    },
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
    async handleLogout() {
      try {
        await api.logout();
      } catch (error) {
        console.error("Logout failed:", error);
      } finally {
        localStorage.removeItem("user"); //
        this.$router.push("/");
      }
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
