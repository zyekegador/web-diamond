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
          <font-awesome-icon :icon="['fas', 'check-circle']" />
          {{ successMessage }}
        </div>

        <!-- Error Message -->
        <div v-if="errors.submit" class="error-message">
          <font-awesome-icon :icon="['fas', 'exclamation-circle']" />
          {{ errors.submit }}
        </div>

        <!-- Step 1: Application Letter -->
        <div v-if="currentStep === 1" class="form-step">
          <div class="step-header">
            <font-awesome-icon :icon="['fas', 'envelope']" class="step-icon" />
            <h3>Application Letter</h3>
            <p>Indicate position, item number, and place of assignment</p>
          </div>

          <div class="form-group">
            <label>Upload Application Letter *</label>
            <div class="file-upload-area">
              <input
                ref="applicationLetterInput"
                type="file"
                accept=".pdf,.doc,.docx"
                @change="handleDocument($event, 'application_letter')"
                class="file-input"
                id="application-letter-file"
              />
              <label for="application-letter-file" class="file-upload-label">
                <font-awesome-icon :icon="['fas', 'cloud-upload-alt']" />
                <span v-if="!documents.application_letter"
                  >Click to upload Application Letter (PDF or Word)</span
                >
                <span v-else>Change Application Letter file</span>
              </label>
            </div>

            <div v-if="documents.application_letter" class="uploaded-file">
              <div class="file-info">
                <font-awesome-icon :icon="['fas', 'file-alt']" />
                <div class="file-details">
                  <span class="file-name">{{
                    documents.application_letter.name
                  }}</span>
                  <span class="file-size">{{
                    formatFileSize(documents.application_letter.size)
                  }}</span>
                </div>
              </div>
              <button
                @click="removeDocument('application_letter')"
                class="btn-remove"
              >
                <font-awesome-icon :icon="['fas', 'trash']" />
              </button>
            </div>

            <span v-if="errors.application_letter" class="error-text">{{
              errors.application_letter
            }}</span>
            <div class="info-box">
              <font-awesome-icon :icon="['fas', 'info-circle']" />
              <span
                >Your letter should clearly state the position, item number, and
                place of assignment you're applying for.</span
              >
            </div>
          </div>
        </div>

        <!-- Step 2: Personal Data Sheet (PDS) - CS Form 212 -->
        <div v-if="currentStep === 2" class="form-step">
          <div class="step-header">
            <font-awesome-icon :icon="['fas', 'file-alt']" class="step-icon" />
            <h3>Personal Data Sheet (PDS)</h3>
            <p>
              CS Form No. 212, Revised 2017 with recent passport-sized picture
            </p>
          </div>

          <div class="form-group">
            <label>Upload PDS (CS Form 212) *</label>
            <div class="file-upload-area">
              <input
                ref="pdsInput"
                type="file"
                accept=".pdf"
                @change="handleDocument($event, 'pds')"
                class="file-input"
                id="pds-file"
              />
              <label for="pds-file" class="file-upload-label">
                <font-awesome-icon :icon="['fas', 'cloud-upload-alt']" />
                <span v-if="!documents.pds"
                  >Click to upload PDS (PDF only)</span
                >
                <span v-else>Change PDS file</span>
              </label>
            </div>

            <div v-if="documents.pds" class="uploaded-file">
              <div class="file-info">
                <font-awesome-icon :icon="['fas', 'file-pdf']" />
                <div class="file-details">
                  <span class="file-name">{{ documents.pds.name }}</span>
                  <span class="file-size">{{
                    formatFileSize(documents.pds.size)
                  }}</span>
                </div>
              </div>
              <button @click="removeDocument('pds')" class="btn-remove">
                <font-awesome-icon :icon="['fas', 'trash']" />
              </button>
            </div>

            <span v-if="errors.pds" class="error-text">{{ errors.pds }}</span>
            <div class="info-box">
              <font-awesome-icon :icon="['fas', 'info-circle']" />
              <span
                >Download the PDS form at www.csc.gov.ph. Must include recent
                passport-sized picture.</span
              >
            </div>
          </div>
        </div>

        <!-- Step 3: Work Experience Sheet (WES) -->
        <div v-if="currentStep === 3" class="form-step">
          <div class="step-header">
            <font-awesome-icon :icon="['fas', 'briefcase']" class="step-icon" />
            <h3>Work Experience Sheet (WES)</h3>
            <p>Fully accomplished Work Experience Sheet</p>
          </div>

          <div class="form-group">
            <label>Upload Work Experience Sheet *</label>
            <div class="file-upload-area">
              <input
                ref="wesInput"
                type="file"
                accept=".pdf,.jpg,.jpeg,.png"
                @change="handleDocument($event, 'wes')"
                class="file-input"
                id="wes-file"
              />
              <label for="wes-file" class="file-upload-label">
                <font-awesome-icon :icon="['fas', 'cloud-upload-alt']" />
                <span v-if="!documents.wes"
                  >Click to upload WES (PDF, JPG, PNG)</span
                >
                <span v-else>Change WES file</span>
              </label>
            </div>

            <div v-if="documents.wes" class="uploaded-file">
              <div class="file-info">
                <font-awesome-icon :icon="['fas', 'file']" />
                <div class="file-details">
                  <span class="file-name">{{ documents.wes.name }}</span>
                  <span class="file-size">{{
                    formatFileSize(documents.wes.size)
                  }}</span>
                </div>
              </div>
              <button @click="removeDocument('wes')" class="btn-remove">
                <font-awesome-icon :icon="['fas', 'trash']" />
              </button>
            </div>

            <span v-if="errors.wes" class="error-text">{{ errors.wes }}</span>
            <div class="info-box">
              <font-awesome-icon :icon="['fas', 'info-circle']" />
              <span>Download the WES form at www.csc.gov.ph</span>
            </div>
          </div>
        </div>

        <!-- Step 4: Required Documents -->
        <div v-if="currentStep === 4" class="form-step">
          <div class="step-header">
            <font-awesome-icon
              :icon="['fas', 'folder-open']"
              class="step-icon"
            />
            <h3>Required Documents</h3>
            <p>Upload eligibility certificate and transcript of records</p>
          </div>

          <!-- Performance Rating (if applicable) -->
          <div class="form-group">
            <label for="performance_rating"
              >Performance Rating (if applicable)</label
            >
            <div class="file-upload-area">
              <input
                ref="performanceInput"
                type="file"
                accept=".pdf,.jpg,.jpeg,.png"
                @change="handleDocument($event, 'performance_rating')"
                class="file-input"
                id="performance-file"
              />
              <label for="performance-file" class="file-upload-label">
                <font-awesome-icon :icon="['fas', 'cloud-upload-alt']" />
                <span v-if="!documents.performance_rating"
                  >Click to upload Performance Rating</span
                >
                <span v-else>Change file</span>
              </label>
            </div>

            <div v-if="documents.performance_rating" class="uploaded-file">
              <div class="file-info">
                <font-awesome-icon :icon="['fas', 'file']" />
                <div class="file-details">
                  <span class="file-name">{{
                    documents.performance_rating.name
                  }}</span>
                  <span class="file-size">{{
                    formatFileSize(documents.performance_rating.size)
                  }}</span>
                </div>
              </div>
              <button
                @click="removeDocument('performance_rating')"
                class="btn-remove"
              >
                <font-awesome-icon :icon="['fas', 'trash']" />
              </button>
            </div>
          </div>

          <!-- Eligibility Certificate -->
          <div class="form-group">
            <label for="eligibility_license"
              >Eligibility Certificate / Board License *</label
            >
            <div class="file-upload-area">
              <input
                ref="eligibilityInput"
                type="file"
                accept=".pdf,.jpg,.jpeg,.png"
                @change="handleDocument($event, 'eligibility_license')"
                class="file-input"
                id="eligibility-file"
              />
              <label for="eligibility-file" class="file-upload-label">
                <font-awesome-icon :icon="['fas', 'cloud-upload-alt']" />
                <span v-if="!documents.eligibility_license"
                  >Click to upload Eligibility/License</span
                >
                <span v-else>Change file</span>
              </label>
            </div>

            <div v-if="documents.eligibility_license" class="uploaded-file">
              <div class="file-info">
                <font-awesome-icon :icon="['fas', 'certificate']" />
                <div class="file-details">
                  <span class="file-name">{{
                    documents.eligibility_license.name
                  }}</span>
                  <span class="file-size">{{
                    formatFileSize(documents.eligibility_license.size)
                  }}</span>
                </div>
              </div>
              <button
                @click="removeDocument('eligibility_license')"
                class="btn-remove"
              >
                <font-awesome-icon :icon="['fas', 'trash']" />
              </button>
            </div>

            <span v-if="errors.eligibility_license" class="error-text">{{
              errors.eligibility_license
            }}</span>
          </div>

          <!-- Transcript of Records -->
          <div class="form-group">
            <label for="transcript">Transcript of Records *</label>
            <div class="file-upload-area">
              <input
                ref="transcriptInput"
                type="file"
                accept=".pdf,.jpg,.jpeg,.png"
                @change="handleDocument($event, 'transcript')"
                class="file-input"
                id="transcript-file"
              />
              <label for="transcript-file" class="file-upload-label">
                <font-awesome-icon :icon="['fas', 'cloud-upload-alt']" />
                <span v-if="!documents.transcript"
                  >Click to upload Transcript</span
                >
                <span v-else>Change file</span>
              </label>
            </div>

            <div v-if="documents.transcript" class="uploaded-file">
              <div class="file-info">
                <font-awesome-icon :icon="['fas', 'file-alt']" />
                <div class="file-details">
                  <span class="file-name">{{ documents.transcript.name }}</span>
                  <span class="file-size">{{
                    formatFileSize(documents.transcript.size)
                  }}</span>
                </div>
              </div>
              <button @click="removeDocument('transcript')" class="btn-remove">
                <font-awesome-icon :icon="['fas', 'trash']" />
              </button>
            </div>

            <span v-if="errors.transcript" class="error-text">{{
              errors.transcript
            }}</span>
          </div>
        </div>

        <!-- Step 5: Training Certificates & Other Documents -->
        <div v-if="currentStep === 5" class="form-step">
          <div class="step-header">
            <font-awesome-icon
              :icon="['fas', 'certificate']"
              class="step-icon"
            />
            <h3>Training Certificates & Other Documents</h3>
            <p>
              Upload training certificates and any other supporting documents
            </p>
          </div>

          <!-- Training Certificates -->
          <div class="form-group">
            <label>Training Certificates (Optional)</label>
            <div class="file-upload-area">
              <input
                type="file"
                multiple
                accept=".pdf,.jpg,.jpeg,.png"
                @change="
                  handleMultipleDocuments($event, 'training_certificates')
                "
                class="file-input"
                id="training-files"
              />
              <label for="training-files" class="file-upload-label">
                <font-awesome-icon :icon="['fas', 'cloud-upload-alt']" />
                <span
                  >Click to upload Training Certificates (Multiple files
                  allowed)</span
                >
              </label>
            </div>

            <div
              v-if="documents.training_certificates.length > 0"
              class="uploaded-files-list"
            >
              <div
                v-for="(file, index) in documents.training_certificates"
                :key="index"
                class="uploaded-file"
              >
                <div class="file-info">
                  <font-awesome-icon :icon="['fas', 'file']" />
                  <div class="file-details">
                    <span class="file-name">{{ file.name }}</span>
                    <span class="file-size">{{
                      formatFileSize(file.size)
                    }}</span>
                  </div>
                </div>
                <button
                  @click="removeFromArray('training_certificates', index)"
                  class="btn-remove"
                >
                  <font-awesome-icon :icon="['fas', 'trash']" />
                </button>
              </div>
            </div>
          </div>

          <!-- Other Documents -->
          <div class="form-group">
            <label>Other Supporting Documents (Optional)</label>
            <div class="file-upload-area">
              <input
                type="file"
                multiple
                accept=".pdf,.jpg,.jpeg,.png"
                @change="handleMultipleDocuments($event, 'other')"
                class="file-input"
                id="other-files"
              />
              <label for="other-files" class="file-upload-label">
                <font-awesome-icon :icon="['fas', 'cloud-upload-alt']" />
                <span
                  >Click to upload Other Documents (Multiple files
                  allowed)</span
                >
              </label>
            </div>

            <div v-if="documents.other.length > 0" class="uploaded-files-list">
              <div
                v-for="(file, index) in documents.other"
                :key="index"
                class="uploaded-file"
              >
                <div class="file-info">
                  <font-awesome-icon :icon="['fas', 'file']" />
                  <div class="file-details">
                    <span class="file-name">{{ file.name }}</span>
                    <span class="file-size">{{
                      formatFileSize(file.size)
                    }}</span>
                  </div>
                </div>
                <button
                  @click="removeFromArray('other', index)"
                  class="btn-remove"
                >
                  <font-awesome-icon :icon="['fas', 'trash']" />
                </button>
              </div>
            </div>

            <span class="helper-text"
              >Accepted formats: PDF, JPG, PNG. Max 10MB per file.</span
            >
          </div>

          <!-- Review Summary -->
          <div class="review-summary">
            <h4>Application Summary</h4>
            <div class="summary-item">
              <font-awesome-icon
                :icon="[
                  'fas',
                  documents.application_letter
                    ? 'check-circle'
                    : 'exclamation-circle',
                ]"
              />
              <span
                >Application Letter:
                {{
                  documents.application_letter ? "Uploaded" : "Missing"
                }}</span
              >
            </div>
            <div class="summary-item">
              <font-awesome-icon
                :icon="[
                  'fas',
                  documents.pds ? 'check-circle' : 'exclamation-circle',
                ]"
              />
              <span>PDS: {{ documents.pds ? "Uploaded" : "Missing" }}</span>
            </div>
            <div class="summary-item">
              <font-awesome-icon
                :icon="[
                  'fas',
                  documents.wes ? 'check-circle' : 'exclamation-circle',
                ]"
              />
              <span>WES: {{ documents.wes ? "Uploaded" : "Missing" }}</span>
            </div>
            <div class="summary-item">
              <font-awesome-icon
                :icon="[
                  'fas',
                  documents.eligibility_license
                    ? 'check-circle'
                    : 'exclamation-circle',
                ]"
              />
              <span
                >Eligibility/License:
                {{
                  documents.eligibility_license ? "Uploaded" : "Missing"
                }}</span
              >
            </div>
            <div class="summary-item">
              <font-awesome-icon
                :icon="[
                  'fas',
                  documents.transcript ? 'check-circle' : 'exclamation-circle',
                ]"
              />
              <span
                >Transcript:
                {{ documents.transcript ? "Uploaded" : "Missing" }}</span
              >
            </div>
            <div class="summary-item">
              <font-awesome-icon :icon="['fas', 'info-circle']" />
              <span
                >Performance Rating:
                {{
                  documents.performance_rating
                    ? "Uploaded"
                    : "Not provided (if applicable)"
                }}</span
              >
            </div>
            <div class="summary-item">
              <font-awesome-icon :icon="['fas', 'check-circle']" />
              <span
                >Training Certificates:
                {{ documents.training_certificates.length }} files</span
              >
            </div>
            <div class="summary-item">
              <font-awesome-icon :icon="['fas', 'check-circle']" />
              <span>Other Documents: {{ documents.other.length }} files</span>
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
          <font-awesome-icon :icon="['fas', 'arrow-left']" />
          Previous
        </button>

        <button
          v-if="currentStep < totalSteps"
          @click="nextStep"
          class="btn-primary"
          :disabled="!canProceed"
        >
          Next
          <font-awesome-icon :icon="['fas', 'arrow-right']" />
        </button>

        <button
          v-if="currentStep === totalSteps"
          @click="submitApplication"
          class="btn-submit"
          :disabled="isSubmitting || !canSubmit"
        >
          <font-awesome-icon :icon="['fas', 'paper-plane']" />
          {{ isSubmitting ? "Submitting..." : "Submit Application" }}
        </button>
      </div>
    </div>
  </div>
</template>

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
      formData: {},
      documents: {
        application_letter: null,
        pds: null,
        wes: null,
        performance_rating: null,
        eligibility_license: null,
        transcript: null,
        training_certificates: [],
        other: [],
      },
      currentStep: 1,
      totalSteps: 5,
      isSubmitting: false,
      errors: {},
      successMessage: "",
    };
  },
  computed: {
    canProceed() {
      if (this.currentStep === 1)
        return this.documents.application_letter !== null;
      if (this.currentStep === 2) return this.documents.pds !== null;
      if (this.currentStep === 3) return this.documents.wes !== null;
      if (this.currentStep === 4)
        return (
          this.documents.eligibility_license !== null &&
          this.documents.transcript !== null
        );
      return true;
    },
    canSubmit() {
      return (
        this.documents.application_letter !== null &&
        this.documents.pds !== null &&
        this.documents.wes !== null &&
        this.documents.eligibility_license !== null &&
        this.documents.transcript !== null
      );
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
    handleDocument(event, docType) {
      const file = event.target.files[0];
      if (!file) return;

      // Validate file type based on document type
      let validTypes = ["application/pdf", "image/jpeg", "image/png"];

      // Allow Word documents for application letter
      if (docType === "application_letter") {
        validTypes = [
          "application/pdf",
          "application/msword",
          "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ];
      }

      if (!validTypes.includes(file.type)) {
        if (docType === "application_letter") {
          this.errors[docType] =
            "Please upload PDF or Word document (.doc, .docx)";
        } else {
          this.errors[docType] = "Please upload PDF, JPG, or PNG file";
        }
        this.documents[docType] = null;
        return;
      }

      // Validate file size (10MB)
      if (file.size > 10 * 1024 * 1024) {
        this.errors[docType] = "File size must be less than 10MB";
        this.documents[docType] = null;
        return;
      }

      this.documents[docType] = file;
      this.errors[docType] = null;
    },
    handleMultipleDocuments(event, docType) {
      const files = Array.from(event.target.files);
      const validFiles = [];

      for (const file of files) {
        if (file.size > 10 * 1024 * 1024) {
          this.errors[docType] = "Each file must be less than 10MB";
          continue;
        }
        validFiles.push(file);
      }

      this.documents[docType] = [...this.documents[docType], ...validFiles];
      if (validFiles.length > 0) {
        this.errors[docType] = null;
      }
    },
    removeDocument(docType) {
      this.documents[docType] = null;
      const refName = `${docType}Input`;
      if (this.$refs[refName]) {
        this.$refs[refName].value = "";
      }
    },
    removeFromArray(docType, index) {
      this.documents[docType].splice(index, 1);
    },
    async submitApplication() {
      this.isSubmitting = true;
      this.errors = {};
      this.successMessage = "";

      try {
        const formData = new FormData();

        // Add job ID
        formData.append("job_id", this.jobId);

        // Add application letter file
        if (this.documents.application_letter) {
          formData.append(
            "application_letter",
            this.documents.application_letter
          );
        }

        // Add required documents
        if (this.documents.pds) {
          formData.append("pds_file", this.documents.pds);
        }
        if (this.documents.wes) {
          formData.append("wes_file", this.documents.wes);
        }
        if (this.documents.eligibility_license) {
          formData.append(
            "eligibility_license_file",
            this.documents.eligibility_license
          );
        }
        if (this.documents.transcript) {
          formData.append("transcript_file", this.documents.transcript);
        }

        // Add optional documents
        if (this.documents.performance_rating) {
          formData.append(
            "performance_rating_file",
            this.documents.performance_rating
          );
        }

        // Add training certificates
        this.documents.training_certificates.forEach((file) => {
          formData.append("training_certificates_files", file);
        });

        // Add other documents
        this.documents.other.forEach((file) => {
          formData.append("other_files", file);
        });

        // Submit application
        const response = await api.submitApplication(formData);

        this.successMessage = "Application submitted successfully!";

        // Redirect after 2 seconds
        setTimeout(() => {
          this.$emit("application-submitted");
          this.$router.push("/applicant/dashboard");
        }, 2000);
      } catch (error) {
        console.error("Submission error:", error);
        console.error(
          "ERROR DETAILS:",
          JSON.stringify(error.response?.data, null, 2)
        );

        if (error.response?.data) {
          const errorData = error.response.data;

          // Show non_field_errors prominently (like "Job is closed")
          if (
            errorData.non_field_errors &&
            errorData.non_field_errors.length > 0
          ) {
            this.errors.submit = errorData.non_field_errors[0];
          }
          // Show field-specific errors
          else if (typeof errorData === "object") {
            // Copy all field errors
            Object.keys(errorData).forEach((key) => {
              if (Array.isArray(errorData[key])) {
                this.errors[key] = errorData[key][0];
              } else {
                this.errors[key] = errorData[key];
              }
            });
            this.errors.submit = "Please check the form for errors";
          }
          // Show generic error message
          else {
            this.errors.submit = errorData.toString();
          }
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

<style scoped>
.summary-item i.fa-exclamation-circle {
  color: #ff9800;
}

.summary-item i.fa-info-circle {
  color: #2196f3;
}

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

  .modal-footer {
    flex-direction: column;
  }

  .btn-primary,
  .btn-submit {
    margin-left: 0;
  }
}
</style>
