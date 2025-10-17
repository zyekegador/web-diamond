<template>
  <div class="admin-dashboard">
    <!-- Top Header -->
    <header class="top-header">
      <div class="header-left">
        <div class="header-title">
          <h1>ADMIN DASHBOARD</h1>
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

        <!-- Recent Activity Section -->
        <div class="recent-activity-section">
          <div class="activity-header">
            <h2>Activity</h2>
          </div>

          <div v-if="filteredDate" class="date-filter-badge">
            <span>Showing activities for: {{ formatSelectedDate }}</span>
            <button @click="clearDateFilter" class="clear-filter">
              <font-awesome-icon :icon="['fas', 'times']" />
            </button>
          </div>

          <div class="activity-table-container">
            <table class="activity-table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Activity Type</th>
                  <th>User</th>
                  <th>Details</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="activity in filteredActivities" :key="activity.id">
                  <td>{{ formatActivityDate(activity.created_at) }}</td>
                  <td>
                    <span :class="['activity-badge', activity.type]">
                      {{ activity.type }}
                    </span>
                  </td>
                  <td>{{ activity.user_name }}</td>
                  <td>{{ activity.details }}</td>
                  <td>
                    <span :class="['status-badge', activity.status]">
                      {{ activity.status }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
            <div v-if="filteredActivities.length === 0" class="no-activity">
              No activities found
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

      <!-- Calendar Modal -->
      <div
        v-if="showCalendarModal"
        class="modal-overlay"
        @click="closeCalendarModal"
      >
        <div class="modal-content calendar-modal" @click.stop>
          <div class="modal-header">
            <h2>Calendar</h2>
            <button class="close-btn" @click="closeCalendarModal">
              <font-awesome-icon :icon="['fas', 'times']" />
            </button>
          </div>
          <div class="modal-body">
            <div class="calendar-controls">
              <button @click="previousMonth" class="nav-btn">
                <font-awesome-icon :icon="['fas', 'chevron-left']" />
              </button>
              <h3>{{ formatMonthYear }}</h3>
              <button @click="nextMonth" class="nav-btn">
                <font-awesome-icon :icon="['fas', 'chevron-right']" />
              </button>
            </div>
            <div class="calendar-grid">
              <div
                class="calendar-day-header"
                v-for="day in ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']"
                :key="day"
              >
                {{ day }}
              </div>
              <div
                v-for="date in calendarDates"
                :key="date.key"
                :class="[
                  'calendar-date',
                  {
                    'other-month': date.otherMonth,
                    today: date.isToday,
                    selected: date.isSelected,
                  },
                ]"
                @click="selectDate(date)"
              >
                {{ date.day }}
              </div>
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
  name: "AdminDashboard",
  data() {
    return {
      user: JSON.parse(localStorage.getItem("user") || "{}"),
      showUserMenu: false,
      showCalendarModal: false,
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
      currentDate: new Date(),
      selectedDate: null,
      recentActivities: [],
      searchQuery: "",
      filteredDate: null,
    };
  },
  mounted() {
    this.loadHRList();
    this.loadRecentActivities();
    document.addEventListener("click", this.closeUserMenu);
    document.addEventListener("keydown", this.handleEscKey);
  },
  beforeUnmount() {
    document.removeEventListener("click", this.closeUserMenu);
    document.removeEventListener("keydown", this.handleEscKey);
  },
  computed: {
    formatMonthYear() {
      return this.currentDate.toLocaleDateString("en-US", {
        month: "long",
        year: "numeric",
      });
    },
    calendarDates() {
      const year = this.currentDate.getFullYear();
      const month = this.currentDate.getMonth();
      const firstDay = new Date(year, month, 1);
      const lastDay = new Date(year, month + 1, 0);
      const prevLastDay = new Date(year, month, 0);
      const firstDayOfWeek = firstDay.getDay();
      const lastDate = lastDay.getDate();
      const prevLastDate = prevLastDay.getDate();

      const dates = [];
      const today = new Date();
      today.setHours(0, 0, 0, 0);

      // Previous month days
      for (let i = firstDayOfWeek - 1; i >= 0; i--) {
        const day = prevLastDate - i;
        dates.push({
          day,
          otherMonth: true,
          isToday: false,
          isSelected: false,
          key: `prev-${day}`,
        });
      }

      // Current month days
      for (let day = 1; day <= lastDate; day++) {
        const date = new Date(year, month, day);
        date.setHours(0, 0, 0, 0);
        const isToday = date.getTime() === today.getTime();
        const isSelected =
          this.selectedDate && date.getTime() === this.selectedDate.getTime();

        dates.push({
          day,
          otherMonth: false,
          isToday,
          isSelected,
          date,
          key: `curr-${day}`,
        });
      }

      // Next month days
      const remainingDays = 42 - dates.length;
      for (let day = 1; day <= remainingDays; day++) {
        dates.push({
          day,
          otherMonth: true,
          isToday: false,
          isSelected: false,
          key: `next-${day}`,
        });
      }

      return dates;
    },
    formatSelectedDate() {
      if (!this.filteredDate) return "";
      return this.filteredDate.toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
      });
    },
    filteredActivities() {
      let activities = this.recentActivities;

      // Filter by date if selected
      if (this.filteredDate) {
        const filterDate = new Date(this.filteredDate);
        filterDate.setHours(0, 0, 0, 0);

        activities = activities.filter((activity) => {
          const activityDate = new Date(activity.created_at);
          activityDate.setHours(0, 0, 0, 0);
          return activityDate.getTime() === filterDate.getTime();
        });
      }

      // Filter by search query
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        activities = activities.filter(
          (activity) =>
            activity.user_name.toLowerCase().includes(query) ||
            activity.type.toLowerCase().includes(query) ||
            activity.details.toLowerCase().includes(query)
        );
      }

      return activities;
    },
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
    openCalendar() {
      this.showCalendarModal = true;
    },
    closeCalendarModal() {
      this.showCalendarModal = false;
    },
    handleEscKey(event) {
      if (event.key === "Escape" && this.showCalendarModal) {
        this.closeCalendarModal();
      }
    },
    previousMonth() {
      this.currentDate = new Date(
        this.currentDate.getFullYear(),
        this.currentDate.getMonth() - 1,
        1
      );
    },
    nextMonth() {
      this.currentDate = new Date(
        this.currentDate.getFullYear(),
        this.currentDate.getMonth() + 1,
        1
      );
    },
    selectDate(dateObj) {
      if (!dateObj.otherMonth) {
        this.selectedDate = dateObj.date;
        this.filteredDate = dateObj.date;
        this.closeCalendarModal();
        console.log("Selected date:", dateObj.date.toLocaleDateString());
      }
    },
    clearDateFilter() {
      this.filteredDate = null;
      this.selectedDate = null;
    },
    async loadRecentActivities() {
      try {
        const activities = [];

        this.hrList.forEach((hr) => {
          activities.push({
            id: `hr-${hr.id}`,
            created_at: hr.created_at,
            type: "HR Account Created",
            user_name: `${hr.first_name} ${hr.last_name}`,
            details: `New HR account created for ${hr.email}`,
            status: "completed",
          });
        });

        // Sort by date (newest first)
        activities.sort(
          (a, b) => new Date(b.created_at) - new Date(a.created_at)
        );

        this.recentActivities = activities;
      } catch (error) {
        console.error("Error loading recent activities:", error);
      }
    },
    formatActivityDate(dateString) {
      const date = new Date(dateString);
      const now = new Date();
      const diffTime = Math.abs(now - date);
      const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

      if (diffDays === 0) {
        return "Today";
      } else if (diffDays === 1) {
        return "Yesterday";
      } else if (diffDays < 7) {
        return `${diffDays} days ago`;
      } else {
        return date.toLocaleDateString("en-US", {
          year: "numeric",
          month: "short",
          day: "numeric",
        });
      }
    },
    async loadHRList() {
      try {
        const response = await api.getHRList();
        this.hrList = response.data;
        this.stats.hrCount = this.hrList.length;
        this.loadRecentActivities();
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
        localStorage.removeItem("user");
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
  gap: 30px;
}

.header-title h1 {
  color: white;
  font-size: 24px;
  font-weight: 700;
  letter-spacing: 1px;
  padding-left: 30px;
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

.sub-header-nav {
  background-color: whitesmoke;
  display: flex;
  justify-content: center;
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
  color: #333;
  font-weight: 500;
  transition: all 0.3s ease;
  font-size: 15px;
  text-align: center;
  padding: 10px 18px;
  border-radius: 6px;
}

.sub-nav-menu li:hover {
  background-color: #4caf79;
  color: white;
  transform: scale(1.05);
  box-shadow: 0 4px 10px rgba(76, 175, 121, 0.3);
}

.sub-nav-menu li.active {
  background-color: #4caf79;
  color: white;
  font-weight: 600;
  box-shadow: 0 4px 10px rgba(76, 175, 121, 0.3);
}

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

/* Calendar Modal */
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
  z-index: 9999;
}

.modal-content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  max-width: 90%;
  max-height: 90vh;
  overflow: auto;
}

.calendar-modal {
  width: 600px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  border-bottom: 1px solid #e0e0e0;
}

.modal-header h2 {
  margin: 0;
  font-size: 24px;
  color: #333;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  color: #666;
  cursor: pointer;
  padding: 5px 10px;
  transition: color0.3s;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 25px;
}

.calendar-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.calendar-controls h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
  font-weight: 600;
}

.nav-btn {
  background: #f5f5f5;
  border: none;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #333;
  transition: all 0.3s;
}

.nav-btn:hover {
  background: #e0e0e0;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 5px;
}

.calendar-day-header {
  text-align: center;
  font-weight: 600;
  color: #666;
  padding: 10px;
  font-size: 14px;
}

.calendar-date {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
  color: #333;
}

.calendar-date:hover:not(.other-month) {
  background: #f0f0f0;
}

.calendar-date.other-month {
  color: #ccc;
  cursor: default;
}

.calendar-date.today {
  background: #e3f2fd;
  color: #1976d2;
  font-weight: 600;
}

.calendar-date.selected {
  background: #2b3e75;
  color: white;
  font-weight: 600;
}

.calendar-date.selected:hover {
  background: #1e2f5a;
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
  background: #2b3e75;
  font-weight: 600;
  color: white;
  padding: 10px;
}

.data-table th:first-child {
  border-top-left-radius: 8px;
}

.data-table th:last-child {
  border-top-right-radius: 8px;
}

.data-table tr:hover {
  background: #f9f9f9;
}

.no-data {
  text-align: center;
  padding: 40px;
  color: #999;
}

/* Recent Activity Section */
.recent-activity-section {
  margin-top: 40px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 25px;
}

.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.activity-header h2 {
  color: #003366;
  font-size: 20px;
  font-weight: 700;
  margin: 0;
}

.activity-controls {
  display: flex;
  gap: 10px;
  align-items: center;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
}

.search-input {
  padding: 8px 35px 8px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-size: 14px;
  width: 250px;
  transition: border-color 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: #2b3e75;
}

.search-icon {
  position: absolute;
  right: 12px;
  color: #999;
  pointer-events: none;
}

.filter-btn {
  width: 40px;
  height: 40px;
  border: 1px solid #e0e0e0;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
  transition: all 0.3s;
}

.filter-btn:hover {
  background: #f5f5f5;
  border-color: #d0d0d0;
}

.date-filter-badge {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 15px;
  background: #e3f2fd;
  border-radius: 6px;
  margin-bottom: 15px;
  color: #1976d2;
  font-size: 14px;
}

.clear-filter {
  background: none;
  border: none;
  color: #1976d2;
  cursor: pointer;
  padding: 2px 5px;
  font-size: 14px;
  transition: color 0.3s;
}

.clear-filter:hover {
  color: #0d47a1;
}

.activity-table-container {
  overflow-x: auto;
}

.activity-table {
  width: 100%;
  border-collapse: collapse;
}

.activity-table thead {
  background: #003d7a;
  color: white;
}

.activity-table th {
  padding: 15px;
  text-align: left;
  font-weight: 600;
  font-size: 14px;
  white-space: nowrap;
}

.activity-table td {
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
  font-size: 14px;
}

.activity-table tbody tr:hover {
  background: #f9f9f9;
}

.activity-badge {
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
  background: #e3f2fd;
  color: #1976d2;
}

.status-badge {
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: capitalize;
  white-space: nowrap;
}

.status-badge.completed {
  background: #e8f5e9;
  color: #4caf50;
}

.status-badge.pending {
  background: #fff3e0;
  color: #ff9800;
}

.status-badge.failed {
  background: #ffebee;
  color: #f44336;
}

.no-activity {
  text-align: center;
  padding: 60px 20px;
  color: #999;
  font-size: 16px;
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

  .activity-controls {
    flex-direction: column;
    align-items: stretch;
  }

  .search-input {
    width: 100%;
  }
}
</style>
