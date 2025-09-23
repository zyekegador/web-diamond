<template>
  <div class="job-application">
    <header class="application-header">
      <router-link :to="`/jobs/${jobId}`" class="back-btn"
        >← Back to Job Details</router-link
      >
      <h1>Apply for Position</h1>
      <p v-if="job">{{ job.title }} - {{ formatDepartment(job.department) }}</p>
    </header>

    <main class="application-content">
      <div v-if="submitted" class="success-message">
        <h2>✅ Application Submitted Successfully!</h2>
        <p>
          Thank you for your interest in this position. We have received your
          application and will review it shortly.
        </p>
        <p>
          You will receive a confirmation email at
          <strong>{{ submittedEmail }}</strong>
        </p>
        <div class="success-actions">
          <router-link to="/jobs" class="btn">Browse More Jobs</router-link>
          <router-link to="/" class="btn secondary">Go Home</router-link>
        </div>
      </div>

      <form v-else @submit.prevent="submitApplication" class="application-form">
        <div class="form-section">
          <h2>Personal Information</h2>

          <div class="form-row">
            <div class="form-group">
              <label>Full Name *</label>
              <input
                v-model="formData.full_name"
                type="text"
                required
                :disabled="loading"
              />
            </div>

            <div class="form-group">
              <label>Email Address *</label>
              <input
                v-model="formData.email"
                type="email"
                required
                :disabled="loading"
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Phone Number *</label>
              <input
                v-model="formData.phone"
                type="tel"
                required
                :disabled="loading"
              />
            </div>

            <div class="form-group">
              <label>Years of Experience *</label>
              <select
                v-model="formData.years_of_experience"
                required
                :disabled="loading"
              >
                <option value="">Select experience</option>
                <option value="0">Fresh Graduate</option>
                <option value="1">1 Year</option>
                <option value="2">2 Years</option>
                <option value="3">3 Years</option>
                <option value="4">4 Years</option>
                <option value="5">5 Years</option>
                <option value="6">6+ Years</option>
                <option value="10">10+ Years</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label>Full Address *</label>
            <textarea
              v-model="formData.address"
              required
              :disabled="loading"
              rows="3"
            ></textarea>
          </div>
        </div>

        <div class="form-section">
          <h2>Professional Information</h2>

          <div class="form-row">
            <div class="form-group">
              <label>Current Position</label>
              <input
                v-model="formData.current_position"
                type="text"
                :disabled="loading"
                placeholder="e.g., Software Developer at ABC Company"
              />
            </div>

            <div class="form-group">
              <label>Expected Salary</label>
              <input
                v-model="formData.expected_salary"
                type="text"
                :disabled="loading"
                placeholder="e.g., $50,000 - $60,000"
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Portfolio URL</label>
              <input
                v-model="formData.portfolio_url"
                type="url"
                :disabled="loading"
                placeholder="https://your-portfolio.com"
              />
            </div>

            <div class="form-group">
              <label>LinkedIn Profile</label>
              <input
                v-model="formData.linkedin_url"
                type="url"
                :disabled="loading"
                placeholder="https://linkedin.com/in/yourprofile"
              />
            </div>
          </div>

          <div class="form-group">
            <label>Availability *</label>
            <select
              v-model="formData.availability"
              required
              :disabled="loading"
            >
              <option value="">Select availability</option>
              <option value="immediately">Immediately</option>
              <option value="2weeks">2 Weeks Notice</option>
              <option value="1month">1 Month Notice</option>
              <option value="2months">2 Months Notice</option>
              <option value="flexible">Flexible</option>
            </select>
          </div>
        </div>

        <div class="form-section">
          <h2>Documents & Additional Information</h2>

          <div class="form-group">
            <label>Resume/CV * (PDF, DOC, DOCX)</label>
            <input
              @change="handleFileChange"
              type="file"
              accept=".pdf,.doc,.docx"
              required
              :disabled="loading"
              ref="resumeInput"
            />
            <div class="file-info">Maximum file size: 5MB</div>
          </div>

          <div class="form-group">
            <label>Cover Letter</label>
            <textarea
              v-model="formData.cover_letter"
              :disabled="loading"
              rows="6"
              placeholder="Tell us why you're interested in this position and what makes you a great fit..."
            ></textarea>
          </div>

          <div class="form-group">
            <label>Why are you interested in this position? *</label>
            <textarea
              v-model="formData.why_interested"
              required
              :disabled="loading"
              rows="4"
              placeholder="Share your motivation for applying to this specific role..."
            ></textarea>
          </div>
        </div>

        <div v-if="errors.length > 0" class="error-section">
          <h3>Please fix the following errors:</h3>
          <ul>
            <li v-for="error in errors" :key="error">{{ error }}</li>
          </ul>
        </div>

        <div class="form-actions">
          <button
            type="submit"
            :disabled="loading || !resumeFile"
            class="submit-btn"
          >
            {{ loading ? "Submitting Application..." : "Submit Application" }}
          </button>
          <router-link :to="`/jobs/${jobId}`" class="cancel-btn"
            >Cancel</router-link
          >
        </div>
      </form>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

const route = useRoute();
const jobId = route.params.jobId;

const job = ref(null);
const loading = ref(false);
const submitted = ref(false);
const submittedEmail = ref("");
const errors = ref([]);
const resumeFile = ref(null);
const resumeInput = ref(null);

const formData = ref({
  full_name: "",
  email: "",
  phone: "",
  address: "",
  current_position: "",
  years_of_experience: "",
  expected_salary: "",
  portfolio_url: "",
  linkedin_url: "",
  cover_letter: "",
  why_interested: "",
  availability: "",
});

const fetchJobDetail = async () => {
  try {
    const response = await axios.get(`/api/public/jobs/${jobId}/`);
    job.value = response.data;
  } catch (error) {
    console.error("Error fetching job detail:", error);
  }
};

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    // Validate file size (5MB)
    if (file.size > 5 * 1024 * 1024) {
      alert("File size must be less than 5MB");
      event.target.value = "";
      resumeFile.value = null;
      return;
    }

    // Validate file type
    const allowedTypes = [
      "application/pdf",
      "application/msword",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ];
    if (!allowedTypes.includes(file.type)) {
      alert("Please upload a PDF, DOC, or DOCX file");
      event.target.value = "";
      resumeFile.value = null;
      return;
    }

    resumeFile.value = file;
  }
};

const validateForm = () => {
  errors.value = [];

  if (!formData.value.full_name.trim())
    errors.value.push("Full name is required");
  if (!formData.value.email.trim()) errors.value.push("Email is required");
  if (!formData.value.phone.trim())
    errors.value.push("Phone number is required");
  if (!formData.value.address.trim()) errors.value.push("Address is required");
  if (!formData.value.years_of_experience)
    errors.value.push("Years of experience is required");
  if (!formData.value.why_interested.trim())
    errors.value.push("Please explain why you're interested");
  if (!formData.value.availability)
    errors.value.push("Availability is required");
  if (!resumeFile.value) errors.value.push("Resume is required");

  return errors.value.length === 0;
};

const submitApplication = async () => {
  if (!validateForm()) {
    return;
  }

  loading.value = true;

  try {
    const submitData = new FormData();

    // Add all form fields
    submitData.append("job", jobId);
    Object.keys(formData.value).forEach((key) => {
      if (formData.value[key]) {
        submitData.append(key, formData.value[key]);
      }
    });

    // Add resume file
    if (resumeFile.value) {
      submitData.append("resume", resumeFile.value);
    }

    await axios.post("/api/public/apply/", submitData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    submittedEmail.value = formData.value.email;
    submitted.value = true;
  } catch (error) {
    console.error("Error submitting application:", error);

    if (error.response?.data) {
      const serverErrors = error.response.data;
      errors.value = [];

      Object.keys(serverErrors).forEach((field) => {
        if (Array.isArray(serverErrors[field])) {
          errors.value.push(...serverErrors[field]);
        } else {
          errors.value.push(serverErrors[field]);
        }
      });
    } else {
      errors.value = [
        "An error occurred while submitting your application. Please try again.",
      ];
    }
  } finally {
    loading.value = false;
  }
};

const formatDepartment = (dept) => {
  return dept.charAt(0).toUpperCase() + dept.slice(1).replace("_", " ");
};

onMounted(fetchJobDetail);
</script>

<style scoped>
.job-application {
  min-height: 100vh;
  background: #f8f9fa;
}

.application-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
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

.application-header h1 {
  font-size: 2.5rem;
  margin: 0 0 0.5rem 0;
}

.application-header p {
  font-size: 1.1rem;
  opacity: 0.9;
}

.application-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.success-message {
  background: white;
  border-radius: 12px;
  padding: 3rem;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.success-message h2 {
  color: #28a745;
  margin-bottom: 1rem;
  font-size: 2rem;
}

.success-message p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.success-actions {
  margin-top: 2rem;
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.success-actions .btn {
  padding: 0.75rem 1.5rem;
  text-decoration: none;
  border-radius: 6px;
  font-weight: 500;
}

.success-actions .btn:not(.secondary) {
  background: #28a745;
  color: white;
}

.success-actions .btn.secondary {
  background: #6c757d;
  color: white;
}

.application-form {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.form-section {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #e9ecef;
}

.form-section:last-of-type {
  border-bottom: none;
}

.form-section h2 {
  color: #333;
  margin-bottom: 1.5rem;
  font-size: 1.3rem;
  border-bottom: 2px solid #667eea;
  padding-bottom: 0.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

.file-info {
  font-size: 0.875rem;
  color: #666;
  margin-top: 0.5rem;
}

.error-section {
  background: #f8d7da;
  color: #721c24;
  padding: 1rem;
  border-radius: 6px;
  margin-bottom: 2rem;
}

.error-section h3 {
  margin-bottom: 0.5rem;
}

.error-section ul {
  margin: 0;
  padding-left: 1.5rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  align-items: center;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e9ecef;
}

.submit-btn {
  background: #28a745;
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.submit-btn:hover:not(:disabled) {
  background: #218838;
  transform: translateY(-1px);
}

.submit-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.cancel-btn {
  color: #6c757d;
  text-decoration: none;
  padding: 1rem 2rem;
  border-radius: 6px;
  font-weight: 500;
}

.cancel-btn:hover {
  background: #f8f9fa;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .application-content {
    padding: 1rem;
  }

  .application-form {
    padding: 1rem;
  }

  .form-actions {
    flex-direction: column-reverse;
  }

  .submit-btn,
  .cancel-btn {
    width: 100%;
    text-align: center;
  }
}
</style>
