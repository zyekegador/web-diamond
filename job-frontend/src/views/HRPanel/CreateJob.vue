<template>
  <div class="modal-overlay">
    <div class="modal-content csc-modal">
      <div class="modal-header">
        <h2>Create Job Posting (CSC Format)</h2>
        <button @click="$emit('close')" class="btn-close">
          <font-awesome-icon :icon="['fas', 'times']" />
        </button>
      </div>

      <div class="modal-body">
        <form @submit.prevent="handleSubmit" class="csc-form">
          <div class="form-section">
            <h3>Position Information</h3>

            <div class="form-group">
              <label>Position Title *</label>
              <input
                type="text"
                v-model="jobForm.title"
                required
                placeholder="e.g. Administrative Officer II"
              />
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Plantilla Item No.</label>
                <input
                  type="text"
                  v-model="jobForm.plantilla_no"
                  placeholder="e.g. 1081-19"
                />
              </div>
              <div class="form-group">
                <label>Salary/Job/Pay Grade</label>
                <input
                  type="text"
                  v-model="jobForm.pay_grade"
                  placeholder="e.g. 11"
                />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Monthly Salary *</label>
                <input
                  type="text"
                  v-model="jobForm.salary_range"
                  required
                  placeholder="e.g. Php 30,024.00"
                />
              </div>
              <div class="form-group">
                <label>Job Type *</label>
                <select v-model="jobForm.job_type" required>
                  <option value="">Select Type</option>
                  <option value="full_time">Full Time</option>
                  <option value="part_time">Part Time</option>
                  <option value="contract">Contract</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label>Place of Assignment *</label>
              <input
                type="text"
                v-model="jobForm.location"
                required
                placeholder="e.g. City Accounting Department"
              />
            </div>
          </div>

          <div class="form-section">
            <h3>Qualifications</h3>

            <div class="form-group">
              <label>Eligibility *</label>
              <div class="autocomplete-wrapper">
                <input
                  type="text"
                  v-model="jobForm.eligibility"
                  @input="filterEligibility"
                  @focus="filterEligibility"
                  required
                  placeholder="Start typing or select from suggestions..."
                />
                <div
                  v-if="
                    showEligibilitySuggestions && filteredEligibility.length > 0
                  "
                  class="suggestions-dropdown"
                >
                  <div
                    v-for="(option, index) in filteredEligibility"
                    :key="index"
                    @click="selectEligibility(option)"
                    class="suggestion-item"
                  >
                    {{ option }}
                  </div>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label>Education *</label>
              <div class="autocomplete-wrapper">
                <input
                  type="text"
                  v-model="jobForm.education"
                  @input="filterEducation"
                  @focus="filterEducation"
                  required
                  placeholder="Start typing or select from suggestions..."
                />
                <div
                  v-if="
                    showEducationSuggestions && filteredEducation.length > 0
                  "
                  class="suggestions-dropdown"
                >
                  <div
                    v-for="(option, index) in filteredEducation"
                    :key="index"
                    @click="selectEducation(option)"
                    class="suggestion-item"
                  >
                    {{ option }}
                  </div>
                </div>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Training</label>
                <input
                  type="text"
                  v-model="jobForm.training"
                  placeholder="None Required or specify"
                />
              </div>
              <div class="form-group">
                <label>Work Experience</label>
                <input
                  type="text"
                  v-model="jobForm.work_experience"
                  placeholder="None Required or specify"
                />
              </div>
            </div>

            <div class="form-group">
              <label>Job Description/Competency *</label>
              <textarea
                v-model="jobForm.description"
                rows="4"
                required
                placeholder="Describe the job responsibilities and competencies"
              ></textarea>
            </div>

            <div class="form-group">
              <label>Required Documents/Remarks</label>
              <textarea
                v-model="jobForm.requirements"
                rows="4"
                placeholder="List required documents for application"
              ></textarea>
            </div>
          </div>

          <div class="form-section">
            <h3>Application Details</h3>

            <div class="form-row">
              <div class="form-group">
                <label>Posting Date *</label>
                <input type="date" v-model="jobForm.posting_date" required />
              </div>
              <div class="form-group">
                <label>Closing Date *</label>
                <input type="date" v-model="jobForm.deadline" required />
              </div>
            </div>
          </div>

          <div v-if="error" class="error-message">{{ error }}</div>
          <div v-if="success" class="success-message">{{ success }}</div>

          <div class="form-actions">
            <button type="button" @click="$emit('close')" class="btn-cancel">
              Cancel
            </button>
            <button type="submit" class="btn-submit" :disabled="loading">
              {{ loading ? "Creating..." : "Create Job Posting" }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "CreateJob",
  props: {
    eligibilityOptions: {
      type: Array,
      default: () => [],
    },
    educationOptions: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      jobForm: {
        title: "",
        plantilla_no: "",
        pay_grade: "",
        salary_range: "",
        job_type: "",
        location: "",
        eligibility: "",
        education: "",
        training: "",
        work_experience: "",
        description: "",
        requirements: "",
        posting_date: "",
        deadline: "",
      },
      showEligibilitySuggestions: false,
      showEducationSuggestions: false,
      filteredEligibility: [],
      filteredEducation: [],
      error: "",
      success: "",
      loading: false,
    };
  },
  mounted() {
    document.addEventListener("click", this.handleClickOutside);
  },
  beforeUnmount() {
    document.removeEventListener("click", this.handleClickOutside);
  },
  methods: {
    handleClickOutside(e) {
      if (!e.target.closest(".autocomplete-wrapper")) {
        this.closeAllSuggestions();
      }
    },
    filterEligibility() {
      if (!this.jobForm.eligibility) {
        this.filteredEligibility = this.eligibilityOptions;
      } else {
        const search = this.jobForm.eligibility.toLowerCase();
        this.filteredEligibility = this.eligibilityOptions.filter((option) =>
          option.toLowerCase().includes(search)
        );
      }
      this.showEligibilitySuggestions = true;
    },
    selectEligibility(option) {
      this.jobForm.eligibility = option;
      this.showEligibilitySuggestions = false;
    },
    filterEducation() {
      if (!this.jobForm.education) {
        this.filteredEducation = this.educationOptions;
      } else {
        const search = this.jobForm.education.toLowerCase();
        this.filteredEducation = this.educationOptions.filter((option) =>
          option.toLowerCase().includes(search)
        );
      }
      this.showEducationSuggestions = true;
    },
    selectEducation(option) {
      this.jobForm.education = option;
      this.showEducationSuggestions = false;
    },
    closeAllSuggestions() {
      this.showEligibilitySuggestions = false;
      this.showEducationSuggestions = false;
    },
    async handleSubmit() {
      this.loading = true;
      this.error = "";
      this.success = "";

      try {
        const fullDescription = `
Position: ${this.jobForm.title}
Plantilla Item No: ${this.jobForm.plantilla_no || "N/A"}
Pay Grade: ${this.jobForm.pay_grade || "N/A"}
Eligibility: ${this.jobForm.eligibility}
Education: ${this.jobForm.education}
Training: ${this.jobForm.training || "None Required"}
Work Experience: ${this.jobForm.work_experience || "None Required"}

${this.jobForm.description}
        `;

        await api.createJob({
          title: this.jobForm.title,
          description: fullDescription,
          requirements: this.jobForm.requirements,
          job_type: this.jobForm.job_type,
          location: this.jobForm.location,
          salary_range: this.jobForm.salary_range,
          deadline: this.jobForm.deadline,
        });

        this.success = "Job posted successfully!";

        setTimeout(() => {
          this.$emit("jobCreated");
          this.$emit("close");
        }, 1500);
      } catch (error) {
        this.error = "Failed to create job posting";
        console.error("Error creating job:", error);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 10px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

.csc-modal {
  max-width: 900px;
}

.modal-header {
  padding: 20px 25px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  background: white;
  z-index: 10;
}

.modal-header h2 {
  color: #333;
  font-size: 20px;
}

.btn-close {
  width: 35px;
  height: 35px;
  border: none;
  background: #f5f7fa;
  border-radius: 50%;
  cursor: pointer;
  font-size: 18px;
  color: #666;
}

.btn-close:hover {
  background: #e3e8ef;
}

.modal-body {
  padding: 25px;
}

.csc-form .form-section {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.csc-form .form-section:last-of-type {
  border-bottom: none;
}

.csc-form .form-section h3 {
  color: #4a5f8d;
  margin-bottom: 20px;
  font-size: 18px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  color: #555;
  font-weight: 500;
  font-size: 14px;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
  font-family: inherit;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #4a5f8d;
}

.autocomplete-wrapper {
  position: relative;
}

.suggestions-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #ddd;
  border-top: none;
  border-radius: 0 0 5px 5px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 100;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.suggestion-item {
  padding: 10px 15px;
  cursor: pointer;
  transition: background 0.2s;
  font-size: 14px;
  color: #333;
  border-bottom: 1px solid #f5f7fa;
}

.suggestion-item:last-child {
  border-bottom: none;
}

.suggestion-item:hover {
  background: #f8f9fc;
  color: #4a5f8d;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.btn-cancel {
  padding: 10px 25px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.btn-cancel:hover {
  background: #f5f7fa;
}

.btn-submit {
  padding: 10px 25px;
  background: #4a5f8d;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.btn-submit:hover {
  background: #3d4f75;
}

.btn-submit:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.error-message {
  color: #f44336;
  padding: 10px;
  background: #ffebee;
  border-radius: 5px;
  margin-bottom: 10px;
  font-size: 14px;
}

.success-message {
  color: #4caf50;
  padding: 10px;
  background: #e8f5e9;
  border-radius: 5px;
  margin-bottom: 10px;
  font-size: 14px;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .suggestions-dropdown {
    max-height: 150px;
  }
}
</style>
