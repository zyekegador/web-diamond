<script>
import api from "@/services/api";

export default {
  name: "ApplicationForm",
  props: {
    jobId: {
      type: Number,
      required: true,
    },
    jobTitle: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      formData: {
        cover_letter: "",
      },
      // PDS file (for OCR extraction)
      pdsFile: null,

      // Extracted documents (certificates, training, eligibility)
      extractedDocs: {
        graduation_cert: null,
        eligibility_cert: null,
        training_cert: null,
      },

      // Non-extracted documents (resume, etc.)
      nonExtractedDocs: [],

      currentStep: 1,
      totalSteps: 4,
      isSubmitting: false,
      errors: {},
      successMessage: "",
    };
  },
  computed: {
    canProceed() {
      if (this.currentStep === 1)
        return this.formData.cover_letter.trim().length > 0;
      if (this.currentStep === 2) return this.pdsFile !== null;
      if (this.currentStep === 3)
        return Object.values(this.extractedDocs).some((doc) => doc !== null);
      return true;
    },
    progressPercentage() {
      return (this.currentStep / this.totalSteps) * 100;
    },
  },
  methods: {
    nextStep() {
      if (this.canProceed && this.currentStep < this.totalSteps) {
        this.currentStep++;
        this.errors = {};
      }
    },
    prevStep() {
      if (this.currentStep > 1) {
        this.currentStep--;
        this.errors = {};
      }
    },
    handlePDSFile(event) {
      const file = event.target.files[0];
      if (file) {
        if (file.type !== "application/pdf" && !file.name.endsWith(".pdf")) {
          this.errors.pds = "Please upload a PDF file";
          this.pdsFile = null;
          return;
        }
        if (file.size > 5 * 1024 * 1024) {
          // 5MB
          this.errors.pds = "File size must be less than 5MB";
          this.pdsFile = null;
          return;
        }
        this.pdsFile = file;
        this.errors.pds = null;
      }
    },
    handleExtractedDoc(event, docType) {
      const file = event.target.files[0];
      if (file) {
        const validTypes = ["application/pdf", "image/jpeg", "image/png"];
        if (!validTypes.includes(file.type)) {
          this.errors[docType] = "Please upload PDF, JPG, or PNG file";
          this.extractedDocs[docType] = null;
          return;
        }
        if (file.size > 5 * 1024 * 1024) {
          this.errors[docType] = "File size must be less than 5MB";
          this.extractedDocs[docType] = null;
          return;
        }
        this.extractedDocs[docType] = file;
        this.errors[docType] = null;
      }
    },
    handleNonExtractedDocs(event) {
      const files = Array.from(event.target.files);
      const validFiles = [];

      for (const file of files) {
        if (file.size > 10 * 1024 * 1024) {
          this.errors.nonExtracted = "Each file must be less than 10MB";
          continue;
        }
        validFiles.push(file);
      }

      this.nonExtractedDocs = validFiles;
      if (validFiles.length > 0) {
        this.errors.nonExtracted = null;
      }
    },
    removeNonExtractedDoc(index) {
      this.nonExtractedDocs.splice(index, 1);
    },
    removeExtractedDoc(docType) {
      this.extractedDocs[docType] = null;
      const input = this.$refs[`${docType}Input`];
      if (input) input.value = "";
    },
    removePDSFile() {
      this.pdsFile = null;
      if (this.$refs.pdsInput) {
        this.$refs.pdsInput.value = "";
      }
    },
    async submitApplication() {
      this.isSubmitting = true;
      this.errors = {};
      this.successMessage = "";

      try {
        // Create FormData for file upload
        const formData = new FormData();

        // Add basic info
        formData.append("job", this.jobId);
        formData.append("cover_letter", this.formData.cover_letter);

        // Add PDS file (for OCR) - REQUIRED
        if (this.pdsFile) {
          formData.append("pds_file", this.pdsFile);
        }

        // Add extracted documents (certificates)
        if (this.extractedDocs.graduation_cert) {
          formData.append(
            "graduation_cert",
            this.extractedDocs.graduation_cert
          );
        }
        if (this.extractedDocs.eligibility_cert) {
          formData.append(
            "eligibility_cert",
            this.extractedDocs.eligibility_cert
          );
        }
        if (this.extractedDocs.training_cert) {
          formData.append("training_cert", this.extractedDocs.training_cert);
        }

        // Add other supporting documents
        this.nonExtractedDocs.forEach((file) => {
          formData.append("other_documents", file);
        });

        // Submit application
        const response = await api.submitApplication(formData);

        if (response.data.success) {
          this.successMessage = "Application submitted successfully!";

          // Redirect after 2 seconds
          setTimeout(() => {
            this.$emit("application-submitted");
            // Redirect based on user type
            const userType = localStorage.getItem("userType");
            if (userType === "applicant") {
              this.$router.push("/applicant/dashboard");
            } else {
              this.$router.push("/jobs");
            }
          }, 2000);
        } else {
          this.errors.submit =
            response.data.message || "Failed to submit application";
        }
      } catch (error) {
        console.error("Submission error:", error);
        if (error.response?.data?.errors) {
          // Handle validation errors
          const errors = error.response.data.errors;
          if (typeof errors === "object") {
            this.errors = errors;
            this.errors.submit = "Please check the form for errors";
          } else {
            this.errors.submit = errors;
          }
        } else if (error.response?.data?.error) {
          this.errors.submit = error.response.data.error;
        } else {
          this.errors.submit =
            "Failed to submit application. Please try again.";
        }
      } finally {
        this.isSubmitting = false;
      }
    },
    formatFileSize(bytes) {
      if (bytes === 0) return "0 Bytes";
      const k = 1024;
      const sizes = ["Bytes", "KB", "MB"];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + " " + sizes[i];
    },
  },
};
</script>

<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal-content application-form" @click.stop>
      <!-- Header -->
      <div class="modal-header">
        <div class="header-content">
          <h2>Apply for {{ jobTitle }}</h2>
          <p class="step-indicator">
            Step {{ currentStep }} of {{ totalSteps }}
          </p>
        </div>
        <button @click="$emit('close')" class="btn-close">
          <font-awesome-icon :icon="['fas', 'times']" />
        </button>
      </div>

      <!-- Progress Bar -->
      <div class="progress-bar">
        <div
          class="progress-fill"
          :style="{ width: progressPercentage + '%' }"
        ></div>
      </div>

      <!-- Form Steps -->
      <div class="modal-body">
        <!-- Success Message -->
        <div v-if="successMessage" class="success-message">
          <i class="fas fa-check-circle"></i>
          {{ successMessage }}
        </div>

        <!-- Error Message -->
        <div v-if="errors.submit" class="error-message">
          <i class="fas fa-exclamation-circle"></i>
          {{ errors.submit }}
        </div>

        <!-- Step 1: Cover Letter -->
        <div v-if="currentStep === 1" class="form-step">
          <div class="step-header">
            <i class="fas fa-envelope step-icon"></i>
            <h3>Cover Letter</h3>
            <p>Tell us why you're interested in this position</p>
          </div>

          <div class="form-group">
            <label for="cover_letter">Your Cover Letter *</label>
            <textarea
              id="cover_letter"
              v-model="formData.cover_letter"
              rows="10"
              placeholder="Write your cover letter here..."
              :class="{ error: errors.cover_letter }"
            ></textarea>
            <span v-if="errors.cover_letter" class="error-text">{{
              errors.cover_letter
            }}</span>
            <span class="helper-text">Minimum 100 characters recommended</span>
          </div>
        </div>

        <!-- Step 2: PDS File (For OCR) -->
        <div v-if="currentStep === 2" class="form-step">
          <div class="step-header">
            <i class="fas fa-file-pdf step-icon"></i>
            <h3>Personal Data Sheet (PDS)</h3>
            <p>Upload your PDS for automatic data extraction</p>
          </div>

          <div class="form-group">
            <label>Upload PDS File *</label>
            <div class="file-upload-area">
              <input
                ref="pdsInput"
                type="file"
                accept=".pdf"
                @change="handlePDSFile"
                class="file-input"
                id="pds-file"
              />
              <label for="pds-file" class="file-upload-label">
                <i class="fas fa-cloud-upload-alt"></i>
                <span v-if="!pdsFile">Click to upload PDS (PDF only)</span>
                <span v-else>Change PDS file</span>
              </label>
            </div>

            <div v-if="pdsFile" class="uploaded-file">
              <div class="file-info">
                <i class="fas fa-file-pdf"></i>
                <div class="file-details">
                  <span class="file-name">{{ pdsFile.name }}</span>
                  <span class="file-size">{{
                    formatFileSize(pdsFile.size)
                  }}</span>
                </div>
              </div>
              <button @click="removePDSFile" class="btn-remove">
                <i class="fas fa-trash"></i>
              </button>
            </div>

            <span v-if="errors.pds" class="error-text">{{ errors.pds }}</span>
            <div class="info-box">
              <i class="fas fa-info-circle"></i>
              <span
                >This file will be processed using OCR to extract your personal
                information automatically.</span
              >
            </div>
          </div>
        </div>

        <!-- Step 3: Extracted Documents (Certificates) -->
        <div v-if="currentStep === 3" class="form-step">
          <div class="step-header">
            <i class="fas fa-certificate step-icon"></i>
            <h3>Certificates & Credentials</h3>
            <p>Upload your certificates for verification</p>
          </div>

          <div class="certificates-grid">
            <!-- Graduation Certificate -->
            <div class="form-group">
              <label for="graduation_cert">Graduation Certificate</label>
              <div class="file-upload-compact">
                <input
                  ref="graduation_certInput"
                  type="file"
                  accept=".pdf,.jpg,.jpeg,.png"
                  @change="handleExtractedDoc($event, 'graduation_cert')"
                  class="file-input"
                  id="graduation_cert"
                />
                <label for="graduation_cert" class="file-upload-compact-label">
                  <i class="fas fa-upload"></i>
                  <span v-if="!extractedDocs.graduation_cert">Upload</span>
                  <span v-else>Change</span>
                </label>
              </div>

              <div
                v-if="extractedDocs.graduation_cert"
                class="uploaded-file-compact"
              >
                <i class="fas fa-file"></i>
                <span class="file-name-compact">{{
                  extractedDocs.graduation_cert.name
                }}</span>
                <button
                  @click="removeExtractedDoc('graduation_cert')"
                  class="btn-remove-compact"
                >
                  <i class="fas fa-times"></i>
                </button>
              </div>
              <span v-if="errors.graduation_cert" class="error-text">{{
                errors.graduation_cert
              }}</span>
            </div>

            <!-- Eligibility Certificate -->
            <div class="form-group">
              <label for="eligibility_cert">Eligibility Certificate</label>
              <div class="file-upload-compact">
                <input
                  ref="eligibility_certInput"
                  type="file"
                  accept=".pdf,.jpg,.jpeg,.png"
                  @change="handleExtractedDoc($event, 'eligibility_cert')"
                  class="file-input"
                  id="eligibility_cert"
                />
                <label for="eligibility_cert" class="file-upload-compact-label">
                  <i class="fas fa-upload"></i>
                  <span v-if="!extractedDocs.eligibility_cert">Upload</span>
                  <span v-else>Change</span>
                </label>
              </div>

              <div
                v-if="extractedDocs.eligibility_cert"
                class="uploaded-file-compact"
              >
                <i class="fas fa-file"></i>
                <span class="file-name-compact">{{
                  extractedDocs.eligibility_cert.name
                }}</span>
                <button
                  @click="removeExtractedDoc('eligibility_cert')"
                  class="btn-remove-compact"
                >
                  <i class="fas fa-times"></i>
                </button>
              </div>
              <span v-if="errors.eligibility_cert" class="error-text">{{
                errors.eligibility_cert
              }}</span>
            </div>

            <!-- Training Certificate -->
            <div class="form-group">
              <label for="training_cert">Training Certificate</label>
              <div class="file-upload-compact">
                <input
                  ref="training_certInput"
                  type="file"
                  accept=".pdf,.jpg,.jpeg,.png"
                  @change="handleExtractedDoc($event, 'training_cert')"
                  class="file-input"
                  id="training_cert"
                />
                <label for="training_cert" class="file-upload-compact-label">
                  <i class="fas fa-upload"></i>
                  <span v-if="!extractedDocs.training_cert">Upload</span>
                  <span v-else>Change</span>
                </label>
              </div>

              <div
                v-if="extractedDocs.training_cert"
                class="uploaded-file-compact"
              >
                <i class="fas fa-file"></i>
                <span class="file-name-compact">{{
                  extractedDocs.training_cert.name
                }}</span>
                <button
                  @click="removeExtractedDoc('training_cert')"
                  class="btn-remove-compact"
                >
                  <i class="fas fa-times"></i>
                </button>
              </div>
              <span v-if="errors.training_cert" class="error-text">{{
                errors.training_cert
              }}</span>
            </div>
          </div>

          <div class="info-box">
            <i class="fas fa-info-circle"></i>
            <span
              >Upload at least one certificate. These documents will be
              extracted and verified.</span
            >
          </div>
        </div>

        <!-- Step 4: Non-Extracted Documents (Supporting Documents) -->
        <div v-if="currentStep === 4" class="form-step">
          <div class="step-header">
            <i class="fas fa-folder-open step-icon"></i>
            <h3>Additional Documents</h3>
            <p>Upload any supporting documents (resume, references, etc.)</p>
          </div>

          <div class="form-group">
            <label>Supporting Documents (Optional)</label>
            <div class="file-upload-area">
              <input
                type="file"
                multiple
                @change="handleNonExtractedDocs"
                class="file-input"
                id="non-extracted-docs"
              />
              <label for="non-extracted-docs" class="file-upload-label">
                <i class="fas fa-cloud-upload-alt"></i>
                <span>Click to upload documents (Multiple files allowed)</span>
              </label>
            </div>

            <div v-if="nonExtractedDocs.length > 0" class="uploaded-files-list">
              <div
                v-for="(file, index) in nonExtractedDocs"
                :key="index"
                class="uploaded-file"
              >
                <div class="file-info">
                  <i class="fas fa-file"></i>
                  <div class="file-details">
                    <span class="file-name">{{ file.name }}</span>
                    <span class="file-size">{{
                      formatFileSize(file.size)
                    }}</span>
                  </div>
                </div>
                <button
                  @click="removeNonExtractedDoc(index)"
                  class="btn-remove"
                >
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </div>

            <span v-if="errors.nonExtracted" class="error-text">{{
              errors.nonExtracted
            }}</span>
            <span class="helper-text"
              >Accepted formats: PDF, DOC, DOCX, JPG, PNG, ZIP</span
            >
          </div>

          <!-- Review Summary -->
          <div class="review-summary">
            <h4>Application Summary</h4>
            <div class="summary-item">
              <i class="fas fa-check-circle"></i>
              <span>Cover Letter: Completed</span>
            </div>
            <div class="summary-item">
              <i
                :class="
                  pdsFile ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'
                "
              ></i>
              <span>PDS File: {{ pdsFile ? "Uploaded" : "Missing" }}</span>
            </div>
            <div class="summary-item">
              <i class="fas fa-check-circle"></i>
              <span
                >Certificates:
                {{ Object.values(extractedDocs).filter((d) => d).length }}
                uploaded</span
              >
            </div>
            <div class="summary-item">
              <i class="fas fa-check-circle"></i>
              <span
                >Supporting Documents: {{ nonExtractedDocs.length }} files</span
              >
            </div>
          </div>
        </div>
      </div>

      <!-- Footer Actions -->
      <div class="modal-footer">
        <button
          v-if="currentStep > 1"
          @click="prevStep"
          class="btn-secondary"
          :disabled="isSubmitting"
        >
          <i class="fas fa-arrow-left"></i>
          Previous
        </button>

        <button
          v-if="currentStep < totalSteps"
          @click="nextStep"
          class="btn-primary"
          :disabled="!canProceed"
        >
          Next
          <i class="fas fa-arrow-right"></i>
        </button>

        <button
          v-if="currentStep === totalSteps"
          @click="submitApplication"
          class="btn-submit"
          :disabled="isSubmitting || !pdsFile"
        >
          <i class="fas fa-paper-plane"></i>
          {{ isSubmitting ? "Submitting..." : "Submit Application" }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 15px;
  width: 100%;
  max-width: 800px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.modal-header {
  padding: 25px 30px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.header-content h2 {
  color: #2b3e75;
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 5px;
}

.step-indicator {
  color: #666;
  font-size: 14px;
  font-weight: 500;
}

.btn-close {
  width: 40px;
  height: 40px;
  border: none;
  background: #f5f5f5;
  border-radius: 50%;
  cursor: pointer;
  font-size: 18px;
  color: #666;
  transition: all 0.3s;
}

.btn-close:hover {
  background: #e0e0e0;
}

.progress-bar {
  height: 4px;
  background: #e0e0e0;
  position: relative;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s ease;
}

.modal-body {
  padding: 30px;
  overflow-y: auto;
  flex: 1;
}

.form-step {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.step-header {
  text-align: center;
  margin-bottom: 30px;
}

.step-icon {
  font-size: 48px;
  color: #667eea;
  margin-bottom: 15px;
}

.step-header h3 {
  color: #2b3e75;
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 8px;
}

.step-header p {
  color: #666;
  font-size: 14px;
}

.form-group {
  margin-bottom: 25px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 600;
  font-size: 14px;
}

.form-group textarea {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-family: inherit;
  font-size: 14px;
  resize: vertical;
  transition: all 0.3s;
}

.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group textarea.error {
  border-color: #f44336;
}

.file-input {
  display: none;
}

.file-upload-area {
  margin-bottom: 15px;
}

.file-upload-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  border: 2px dashed #667eea;
  border-radius: 12px;
  background: #f8f9fd;
  cursor: pointer;
  transition: all 0.3s;
}

.file-upload-label:hover {
  background: #eef1fc;
  border-color: #5568d3;
}

.file-upload-label i {
  font-size: 36px;
  color: #667eea;
  margin-bottom: 10px;
}

.file-upload-label span {
  color: #666;
  font-size: 14px;
  font-weight: 500;
}

.uploaded-file {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 15px;
  background: #f8f9fd;
  border-radius: 8px;
  margin-bottom: 10px;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.file-info i {
  font-size: 24px;
  color: #667eea;
}

.file-details {
  display: flex;
  flex-direction: column;
}

.file-name {
  color: #333;
  font-weight: 600;
  font-size: 14px;
}

.file-size {
  color: #999;
  font-size: 12px;
}

.btn-remove {
  width: 32px;
  height: 32px;
  border: none;
  background: #ffebee;
  color: #f44336;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-remove:hover {
  background: #f44336;
  color: white;
}

.certificates-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.file-upload-compact-label {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 20px;
  border: 2px solid #667eea;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
  color: #667eea;
  font-weight: 600;
}

.file-upload-compact-label:hover {
  background: #667eea;
  color: white;
}

.uploaded-file-compact {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: #f8f9fd;
  border-radius: 6px;
  margin-top: 10px;
}

.uploaded-file-compact i {
  color: #667eea;
}

.file-name-compact {
  flex: 1;
  font-size: 12px;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.btn-remove-compact {
  width: 24px;
  height: 24px;
  border: none;
  background: transparent;
  color: #999;
  cursor: pointer;
  transition: color 0.3s;
}

.btn-remove-compact:hover {
  color: #f44336;
}

.uploaded-files-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.info-box {
  display: flex;
  align-items: start;
  gap: 10px;
  padding: 12px 15px;
  background: #e3f2fd;
  border-radius: 8px;
  margin-top: 15px;
}

.info-box i {
  color: #1976d2;
  margin-top: 2px;
}

.info-box span {
  color: #1565c0;
  font-size: 13px;
  line-height: 1.5;
}

.review-summary {
  background: #f8f9fd;
  border-radius: 12px;
  padding: 20px;
  margin-top: 25px;
}

.review-summary h4 {
  color: #2b3e75;
  font-size: 16px;
  margin-bottom: 15px;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid #e0e0e0;
}

.summary-item:last-child {
  border-bottom: none;
}

.summary-item i {
  color: #4caf50;
  font-size: 18px;
}

.summary-item i.fa-exclamation-circle {
  color: #ff9800;
}

.summary-item span {
  color: #333;
  font-size: 14px;
}

.error-text {
  display: block;
  color: #f44336;
  font-size: 12px;
  margin-top: 5px;
}

.helper-text {
  display: block;
  color: #999;
  font-size: 12px;
  margin-top: 5px;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px;
  background: #ffebee;
  border-left: 4px solid #f44336;
  border-radius: 8px;
  margin-bottom: 20px;
  color: #c62828;
  font-size: 14px;
}

.success-message {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px;
  background: #e8f5e9;
  border-left: 4px solid #4caf50;
  border-radius: 8px;
  margin-bottom: 20px;
  color: #2e7d32;
  font-size: 14px;
}

.modal-footer {
  padding: 20px 30px;
  border-top: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  gap: 15px;
}

.btn-secondary,
.btn-primary,
.btn-submit {
  padding: 12px 30px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-secondary {
  background: #f5f5f5;
  color: #333;
}

.btn-secondary:hover {
  background: #e0e0e0;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  margin-left: auto;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
  background: #ccc;
  cursor: not-allowed;
  transform: none;
}

.btn-submit {
  background: linear-gradient(135deg, #4caf50 0%, #45a049 100%);
  color: white;
  margin-left: auto;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
}

.btn-submit:disabled {
  background: #ccc;
  cursor: not-allowed;
  transform: none;
}

@media (max-width: 768px) {
  .modal-content {
    max-width: 100%;
    max-height: 100vh;
    border-radius: 0;
  }

  .certificates-grid {
    grid-template-columns: 1fr;
  }

  .modal-footer {
    flex-direction: column;
  }

  .btn-primary,
  .btn-submit {
    margin-left: 0;
  }
}
</style>
