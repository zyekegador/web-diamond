<script setup>
import { useRouter } from "vue-router";
import { logout, currentUser, isAdmin, isHR } from "@/stores/auth";

const router = useRouter();

const handleLogout = async () => {
  await logout();
  router.push("/login");
};
</script>

<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <h1>Dashboard</h1>
      <div class="user-info">
        <span>Welcome, {{ currentUser?.username }}</span>
        <span class="user-type">{{
          currentUser?.user_type?.toUpperCase()
        }}</span>
        <button @click="handleLogout" class="logout-btn">Logout</button>
      </div>
    </header>

    <main class="dashboard-content">
      <div class="role-actions">
        <div v-if="isAdmin" class="admin-actions">
          <h2>Admin Actions</h2>
          <p>You have full system control</p>
          <router-link to="/admin" class="action-btn">
            Admin Panel
          </router-link>
        </div>

        <div v-if="isHR || isAdmin" class="hr-actions">
          <h2>HR Actions</h2>
          <p>Manage job postings and applications</p>
          <div class="action-btn disabled">HR Panel (Coming Soon)</div>
        </div>

        <div v-if="!isAdmin && !isHR" class="pending-approval">
          <h2>Account Pending</h2>
          <p>Your account is waiting for admin approval.</p>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.dashboard {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.dashboard-header {
  background: white;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-type {
  background-color: #007bff;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
}

.logout-btn {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.logout-btn:hover {
  background-color: #c82333;
}

.dashboard-content {
  padding: 2rem;
}

.role-actions {
  display: grid;
  gap: 2rem;
  max-width: 800px;
}

.admin-actions,
.hr-actions,
.pending-approval {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.action-btn {
  display: inline-block;
  background-color: #28a745;
  color: white;
  text-decoration: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  margin-top: 1rem;
}

.action-btn:hover {
  background-color: #218838;
}

.action-btn.disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}
</style>
