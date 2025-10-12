import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add token to all requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Token ${token}`;
      console.log("Sending token:", token); // Debug line
    } else {
      console.log("⚠️ No token found in localStorage"); // Debug line
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle response errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Check if this is NOT a logout request AND NOT a login request
      const isLogoutRequest = error.config.url.includes("/logout/");
      const isLoginRequest = error.config.url.includes("/login/");

      // Only redirect if it's not a login or logout request
      if (!isLogoutRequest && !isLoginRequest) {
        console.log("❌ 401 Unauthorized - clearing storage");
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        localStorage.removeItem("userType");

        // Preserve query parameters when redirecting
        const currentParams = new URLSearchParams(window.location.search);
        const role = currentParams.get("role");

        if (role) {
          window.location.href = `/login?role=${role}`;
        } else {
          window.location.href = "/login";
        }
      }
    }
    return Promise.reject(error);
  }
);

export default {
  // Auth endpoints
  login(credentials) {
    return api.post("/accounts/login/", credentials);
  },

  registerApplicant(data) {
    return api.post("/accounts/register/applicant/", data);
  },

  async logout() {
    try {
      await api.post("/accounts/logout/");
    } catch (error) {
      // Ignore errors - if token is already invalid, that's fine
      console.log("Logout API call failed, but clearing local session");
    } finally {
      // Always clear local storage regardless of API response
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      localStorage.removeItem("userType");
    }
  },

  getCurrentUser() {
    return api.get("/accounts/current-user/");
  },

  // Admin endpoints
  createHR(data) {
    return api.post("/accounts/create/hr/", data);
  },

  getHRList() {
    return api.get("/accounts/hr/list/");
  },

  // Job endpoints
  getJobs() {
    return api.get("/jobs/");
  },

  getJobDetail(id) {
    return api.get(`/jobs/${id}/`);
  },

  // HR Job management
  getHRJobs() {
    return api.get("/hr/jobs/");
  },

  createJob(data) {
    return api.post("/hr/jobs/create/", data);
  },

  updateJob(id, data) {
    return api.put(`/hr/jobs/${id}/update/`, data);
  },

  updateJobDates(id, data) {
    return api.patch(`/hr/jobs/${id}/update-dates/`, data);
  },

  deleteJob(id) {
    return api.delete(`/hr/jobs/${id}/delete/`);
  },

  // Application endpoints
  applyJob(data) {
    const formData = new FormData();
    for (const key in data) {
      formData.append(key, data[key]);
    }
    return api.post("/applications/apply/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  },

  getMyApplications() {
    return api.get("/applications/my-applications/");
  },

  getApplicationDetail(id) {
    return api.get(`/applications/${id}/`);
  },

  getJobApplications(jobId) {
    return api.get(`/hr/jobs/${jobId}/applications/`);
  },

  updateApplicationStatus(id, data) {
    return api.patch(`/hr/applications/${id}/update-status/`, data);
  },

  getEducationOptions() {
    return api.get("/options/education/");
  },

  getEligibilityOptions() {
    return api.get("/options/eligibility/");
  },

  submitApplication(formData) {
    return api.post("/applications/submit-complete/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  },
};
