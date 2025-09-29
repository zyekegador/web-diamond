import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Token ${token}`;
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
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      localStorage.removeItem("userType");
      window.location.href = "/login";
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

  logout() {
    return api.post("/accounts/logout/");
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

  // HR Application management
  getJobApplications(jobId) {
    return api.get(`/hr/jobs/${jobId}/applications/`);
  },

  updateApplicationStatus(id, data) {
    return api.patch(`/hr/applications/${id}/update-status/`, data);
  },
};
