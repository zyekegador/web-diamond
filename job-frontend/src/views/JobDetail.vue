<template>
  <div class="job-detail">
    <header class="detail-header">
      <router-link to="/jobs" class="back-btn">← Back to Jobs</router-link>
      <h1 v-if="job">{{ job.title }}</h1>
    </header>

    <main class="detail-content">
      <div v-if="loading" class="loading">Loading job details...</div>

      <div v-else-if="error" class="error">
        {{ error }}
      </div>

      <div v-else-if="job" class="job-details">
        <div class="job-header">
          <div class="job-meta">
            <span class="department">{{
              formatDepartment(job.department)
            }}</span>
            <span class="location">📍 {{ job.location }}</span>
            <span class="experience"
              >⭐ {{ formatExperience(job.experience_level) }}</span
            >
            <span v-if="job.salary_range" class="salary"
              >💰 {{ job.salary_range }}</span
            >
          </div>

          <div class="apply-section">
            <router-link :to="`/apply/${job.id}`" class="apply-btn-large">
              Apply for this Position
            </router-link>
          </div>
        </div>

        <div class="job-content">
          <section class="description-section">
            <h2>Job Description</h2>
            <div
              class="content-text"
              v-html="formatText(job.description)"
            ></div>
          </section>

          <section class="requirements-section">
            <h2>Requirements</h2>
            <div
              class="content-text"
              v-html="formatText(job.requirements)"
            ></div>
          </section>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

const route = useRoute();
const job = ref(null);
const loading = ref(true);
const error = ref("");

const fetchJobDetail = async () => {
  try {
    const response = await axios.get(`/api/public/jobs/${route.params.id}/`);
    job.value = response.data;
  } catch (err) {
    error.value = "Job not found or no longer available";
    console.error("Error fetching job detail:", err);
  } finally {
    loading.value = false;
  }
};

const formatDepartment = (dept) => {
  return dept.charAt(0).toUpperCase() + dept.slice(1).replace("_", " ");
};

const formatExperience = (exp) => {
  const levels = {
    entry: "Entry Level (0-2 years)",
    mid: "Mid Level (3-5 years)",
    senior: "Senior Level (5+ years)",
  };
  return levels[exp] || exp;
};

const formatText = (text) => {
  // Convert line breaks to HTML and handle basic formatting
  return text
    .replace(/\n/g, "<br>")
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
};

onMounted(fetchJobDetail);
</script>

<style scoped>
.job-detail {
  min-height: 100vh;
  background: #f8f9fa;
}

.detail-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  position: relative;
}

.back-btn {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  backdrop-filter: blur(10px);
  display: inline-block;
  margin-bottom: 1rem;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.detail-header h1 {
  font-size: 2.5rem;
  margin: 0;
}

.detail-content {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
}

.loading {
  text-align: center;
  font-size: 1.2rem;
  color: #666;
  margin: 3rem 0;
}

.error {
  text-align: center;
  color: #dc3545;
  background: #f8d7da;
  padding: 1rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.job-details {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.job-header {
  padding: 2rem;
  border-bottom: 1px solid #e9ecef;
}

.job-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
}

.department,
.location,
.experience,
.salary {
  background: #f8f9fa;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 500;
  color: #495057;
}

.apply-section {
  text-align: center;
}

.apply-btn-large {
  display: inline-block;
  background: #28a745;
  color: white;
  text-decoration: none;
  padding: 1rem 2rem;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  transition: all 0.2s;
}

.apply-btn-large:hover {
  background: #218838;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
}

.job-content {
  padding: 2rem;
}

.description-section,
.requirements-section {
  margin-bottom: 2rem;
}

.description-section h2,
.requirements-section h2 {
  color: #333;
  margin-bottom: 1rem;
  font-size: 1.5rem;
  border-bottom: 2px solid #667eea;
  padding-bottom: 0.5rem;
}

.content-text {
  line-height: 1.7;
  color: #555;
  font-size: 1rem;
}

.content-text :deep(strong) {
  color: #333;
}

@media (max-width: 768px) {
  .detail-header {
    padding: 1rem;
  }

  .detail-header h1 {
    font-size: 2rem;
  }

  .job-meta {
    flex-direction: column;
    align-items: flex-start;
  }

  .detail-content {
    padding: 1rem;
  }

  .job-content {
    padding: 1rem;
  }
}
</style>
