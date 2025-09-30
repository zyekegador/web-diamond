<template>
  <div class="admin-panel">
    <header class="admin-header">
      <h1>Admin Panel</h1>
      <router-link to="/dashboard" class="back-btn"
        >← Back to Dashboard</router-link
      >
    </header>

    <main class="admin-content">
      <div class="pending-approvals">
        <h2>Pending HR Approvals</h2>

        <div v-if="loading" class="loading">Loading pending users...</div>

        <div v-else-if="pendingUsers.length === 0" class="no-data">
          No pending HR approvals
        </div>

        <div v-else class="user-list">
          <div v-for="user in pendingUsers" :key="user.id" class="user-card">
            <div class="user-info">
              <h3>{{ user.username }}</h3>
              <p>{{ user.email }}</p>
              <span class="user-type">{{ user.user_type.toUpperCase() }}</span>
            </div>

            <button
              @click="approveUser(user.id)"
              class="approve-btn"
              :disabled="approving === user.id"
            >
              {{ approving === user.id ? "Approving..." : "Approve" }}
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const pendingUsers = ref([]);
const loading = ref(true);
const approving = ref(null);

const fetchPendingUsers = async () => {
  try {
    const response = await axios.get("/auth/admin/pending-hr/");
    pendingUsers.value = response.data;
  } catch (error) {
    console.error("Error fetching pending users:", error);
  } finally {
    loading.value = false;
  }
};

const approveUser = async (userId) => {
  approving.value = userId;
  try {
    await axios.post(`/auth/admin/approve-hr/${userId}/`);
    // Remove approved user from list
    pendingUsers.value = pendingUsers.value.filter(
      (user) => user.id !== userId
    );
    alert("User approved successfully!");
  } catch (error) {
    console.error("Error approving user:", error);
    alert("Error approving user");
  } finally {
    approving.value = null;
  }
};

onMounted(fetchPendingUsers);
</script>

<style scoped>
.admin-panel {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.admin-header {
  background: white;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.back-btn {
  background-color: #6c757d;
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
}

.back-btn:hover {
  background-color: #5a6268;
}

.admin-content {
  padding: 2rem;
}

.pending-approvals {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.loading,
.no-data {
  text-align: center;
  padding: 2rem;
  color: #6c757d;
}

.user-list {
  display: grid;
  gap: 1rem;
  margin-top: 1rem;
}

.user-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f8f9fa;
}

.user-info h3 {
  margin: 0 0 0.5rem 0;
}

.user-info p {
  margin: 0 0 0.5rem 0;
  color: #6c757d;
}

.user-type {
  background-color: #ffc107;
  color: #212529;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: bold;
}

.approve-btn {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.approve-btn:hover:not(:disabled) {
  background-color: #218838;
}

.approve-btn:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}
</style>
