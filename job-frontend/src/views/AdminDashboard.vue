<template>
  <div class="admin-dashboard">
    <!-- Top Header -->
    <header class="top-header">
      <div class="header-left">
        <img src="@/assets/butuanon.png" alt="Logo" class="logo" />
        <div class="header-title">
          <h1>ADMIN PANEL</h1>
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

    <div class="dashboard">
      <!-- NAV BAR UNDER HEADER -->
      <nav class="sub-header-nav">
        <ul class="sub-nav-menu">
          <li
            :class="{ active: activeTab === 'overview' }"
            @click="activeTab = 'overview'"
          >
            <span>Overview</span>
          </li>
          <li
            :class="{ active: activeTab === 'create-hr' }"
            @click="activeTab = 'create-hr'"
          >
            <span>Create HR Account</span>
          </li>
          <li
            :class="{ active: activeTab === 'hr-list' }"
            @click="activeTab = 'hr-list'"
          >
            <span>HR Staff List</span>
          </li>
        </ul>

        <!-- Right-side button 
        <button class="new-btn">NEW +</button> -->
      </nav>
    </div>

    <main class="main-content">
      <!-- Overview Tab -->
      <div v-if="activeTab === 'overview'" class="content-section">
        <div class="overview-header">
          <h1>SYSTEM OVERVIEW</h1>
          <button class="calendar-btn" @click="openCalendar">
            <font-awesome-icon :icon="['far', 'calendar']" />
            Calendar
          </button>
        </div>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-header blue-header">Total HR Staff</div>
            <div class="stat-body">
              <div class="stat-icon blue">
                <font-awesome-icon :icon="['fas', 'users']" />
              </div>
              <p class="stat-number">{{ stats.hrCount }}</p>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-header green-header">Total Applicants</div>
            <div class="stat-body">
              <div class="stat-icon green">
                <font-awesome-icon :icon="['fas', 'user-check']" />
              </div>
              <p class="stat-number">{{ stats.applicantCount }}</p>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-header orange-header">Active Job</div>
            <div class="stat-body">
              <div class="stat-icon orange">
                <font-awesome-icon :icon="['fas', 'briefcase']" />
              </div>
              <p class="stat-number">{{ stats.jobCount }}</p>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-header purple-header">Total Applications</div>
            <div class="stat-body">
              <div class="stat-icon purple">
                <font-awesome-icon :icon="['fas', 'file-alt']" />
              </div>
              <p class="stat-number">{{ stats.applicationCount }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Create HR Tab -->
      <div v-if="activeTab === 'create-hr'" class="content-section">
        <h1>CREATE HR ACCOUNT</h1>
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
        <h1>HR STAFF LIST</h1>
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
  width: 220px;
  background-color: #2f3e6e;
  color: white;
  display: flex;
  flex-direction: column;
  padding: 20px;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
}

.sub-header-nav {
  background-color: #3b4d7a;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  padding-left: 30px;
  padding-right: 30px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  min-height: 60px;
}

.sub-nav-menu {
  display: flex;
  align-items: center;
  list-style: none;
  padding: 0;
  margin: 0;
  gap: 40px;
}

.sub-nav-menu li {
  position: relative;
  cursor: pointer;
  color: #dce3f2;
  font-weight: 500;
  transition: all 0.3s ease;
  font-size: 15px;
}

.sub-nav-menu li:hover {
  color: #ffffff;
}

.sub-nav-menu li.active {
  color: #ffffff;
  border-bottom: 3px solid #b4c8ff;
  padding-bottom: 3px;
}

/* NEW button below the menu 
.new-btn {
  background-color: #5d74c7;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 8px 20px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  margin-left: auto;
}

.new-btn:hover {
  background-color: #4a61b5;
  transform: translateY(-1px);
}
  */

/* Main Content */
.main-content {
  flex: 1;
  background-color: #fff;
  padding: 40px;
  overflow-y: auto;
}
.content-section h1 {
  margin-bottom: 30px;
  color: #003366;
  font-weight: 750;
  font-size: 25px;
  letter-spacing: 0.5px;
}

.overview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.calendar-btn {
  background: #2b3e75;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  padding: 10px 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 14px;
  color: white;
  transition: all 0.3s;
}

.calendar-btn:hover {
  background: transparent;
  border-color: #2b3e75;
  color: black;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-top: 20px;
}

.stat-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.stat-header {
  padding: 12px 20px;
  color: white;
  font-weight: 600;
  font-size: 14px;
  text-align: left;
}

.stat-header.blue-header {
  background: #003d7a;
}

.stat-header.green-header {
  background: #4caf50;
}

.stat-header.orange-header {
  background: #ff9800;
}

.stat-header.purple-header {
  background: #7b1fa2;
}

.stat-body {
  padding: 30px 20px;
  display: flex;
  align-items: center;
  gap: 20px;
  background: white;
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
  flex-shrink: 0;
}

.stat-icon.blue {
  background: #2196f3;
}
.stat-icon.green {
  background: #66bb6a;
}
.stat-icon.orange {
  background: #ffa726;
}
.stat-icon.purple {
  background: #ab47bc;
}

.stat-number {
  font-size: 48px;
  font-weight: 700;
  color: #003366;
  margin: 0;
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
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #354775;
    padding: 0 30px;
    height: 50px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
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
