<template>
  <div class="job-listings">
    <header class="header">
      <h1>Available Positions</h1>
      <p>Find your perfect job opportunity</p>
      <router-link to="/" class="home-btn">← Back to Home</router-link>
    </header>

    <main class="listings-content">
      <div class="filters">
        <select v-model="filterDepartment">
          <option value="">All Departments</option>
          <option value="engineering">Engineering</option>
          <option value="marketing">Marketing</option>
          <option value="sales">Sales</option>
          <option value="hr">Human Resources</option>
          <option value="finance">Finance</option>
        </select>

        <select v-model="filterExperience">
          <option value="">All Experience Levels</option>
          <option value="entry">Entry Level</option>
          <option value="mid">Mid Level</option>
          <option value="senior">Senior Level</option>
        </select>
      </div>

      <div v-if="loading" class="loading">Loading job positions...</div>

      <div v-else-if="filteredJobs.length === 0" class="no-jobs">
        No job positions available at the moment.
      </div>

      <div v-else class="job-grid">
        <div v-for="job in filteredJobs" :key="job.id" class="job-card">
          <h3>{{ job.title }}</h3>
          <div class="job-meta">
            <span class="department">{{
              formatDepartment(job.department)
            }}</span>
            <span class="location">📍 {{ job.location }}</span>
            <span class="experience"
              >⭐ {{ formatExperience(job.experience_level) }}</span
            >
          </div>

          <p class="description">{{ job.description.substring(0, 150) }}...</p>

          <div class="job-actions">
            <router-link :to="`/jobs/${job.id}`" class="view-btn">
              View Details
            </router-link>
            <router-link :to="`/apply/${job.id}`" class="apply-btn">
              Apply Now
            </router-link>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import axios from "axios";

const jobs = ref([]);
const loading = ref(true);
const filterDepartment = ref("");
const filterExperience = ref("");

const filteredJobs = computed(() => {
  return jobs.value.filter((job) => {
    const matchesDept =
      !filterDepartment.value || job.department === filterDepartment.value;
    const matchesExp =
      !filterExperience.value ||
      job.experience_level === filterExperience.value;
    return matchesDept && matchesExp;
  });
});

const fetchJobs = async () => {
  try {
    const response = await axios.get("/api/public/jobs/");
    jobs.value = response.data;
  } catch (error) {
    console.error("Error fetching jobs:", error);
  } finally {
    loading.value = false;
  }
};

const formatDepartment = (dept) => {
  return dept.charAt(0).toUpperCase() + dept.slice(1).replace("_", " ");
};

const formatExperience = (exp) => {
  const levels = {
    entry: "Entry Level",
    mid: "Mid Level",
    senior: "Senior Level",
  };
  return levels[exp] || exp;
};

onMounted(fetchJobs);
</script>

<style scoped>
.job-listings {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.header {
  text-align: center;
  padding: 3rem 2rem;
  color: white;
  position: relative;
}

.header h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.home-btn {
  position: absolute;
  top: 2rem;
  left: 2rem;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  backdrop-filter: blur(10px);
}

.listings-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  justify-content: center;
}

.filters select {
  padding: 0.5rem;
  border: none;
  border-radius: 4px;
  background: white;
}

.loading,
.no-jobs {
  text-align: center;
  color: white;
  font-size: 1.2rem;
  margin: 3rem 0;
}

.job-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
}

.job-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.job-card:hover {
  transform: translateY(-5px);
}

.job-card h3 {
  color: #333;
  margin-bottom: 1rem;
  font-size: 1.3rem;
}

.job-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.department,
.location,
.experience {
  background: #f8f9fa;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
  color: #666;
}

.description {
  color: #666;
  line-height: 1.5;
  margin-bottom: 1.5rem;
}

.job-actions {
  display: flex;
  gap: 1rem;
}

.view-btn,
.apply-btn {
  padding: 0.75rem 1.5rem;
  text-decoration: none;
  border-radius: 6px;
  font-weight: 500;
  text-align: center;
  flex: 1;
}

.view-btn {
  background: #f8f9fa;
  color: #333;
  border: 1px solid #dee2e6;
}

.apply-btn {
  background: #28a745;
  color: white;
}

.view-btn:hover {
  background: #e9ecef;
}

.apply-btn:hover {
  background: #218838;
}
</style>
