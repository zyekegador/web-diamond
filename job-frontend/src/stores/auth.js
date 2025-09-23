import { ref, computed } from "vue";
import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api";
axios.defaults.baseURL = API_BASE_URL;

const user = ref(null);
const token = ref(localStorage.getItem("access_token"));
const refreshToken = ref(localStorage.getItem("refresh_token"));

if (token.value) {
  axios.defaults.headers.common["Authorization"] = `Bearer ${token.value}`;
}

axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const response = await axios.post("/auth/token/refresh/", {
          refresh: refreshToken.value,
        });

        const newToken = response.data.access;
        setToken(newToken);
        originalRequest.headers.Authorization = `Bearer ${newToken}`;

        return axios(originalRequest);
      } catch (refreshError) {
        logout();
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export function setToken(newToken) {
  token.value = newToken;
  localStorage.setItem("access_token", newToken);
  axios.defaults.headers.common["Authorization"] = `Bearer ${newToken}`;
}

export function setRefreshToken(newRefreshToken) {
  refreshToken.value = newRefreshToken;
  localStorage.setItem("refresh_token", newRefreshToken);
}

export function clearTokens() {
  token.value = null;
  refreshToken.value = null;
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  delete axios.defaults.headers.common["Authorization"];
}

export async function login(credentials) {
  try {
    const response = await axios.post("/auth/login/", credentials);
    const { access, refresh, user: userData } = response.data;

    user.value = userData;
    setToken(access);
    setRefreshToken(refresh);

    return { success: true, user: userData };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.non_field_errors?.[0] || "Login failed",
    };
  }
}

export async function register(userData) {
  try {
    const response = await axios.post("/auth/register/", userData);
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      errors: error.response?.data || { general: "Registration failed" },
    };
  }
}

export async function logout() {
  try {
    if (refreshToken.value) {
      await axios.post("/auth/logout/", { refresh: refreshToken.value });
    }
  } catch (error) {
    console.log("Logout error:", error);
  }

  user.value = null;
  clearTokens();
}

export async function fetchProfile() {
  try {
    const response = await axios.get("/auth/profile/");
    user.value = response.data;
    return response.data;
  } catch (error) {
    logout();
    throw error;
  }
}

export const isAuthenticated = computed(() => !!token.value && !!user.value);
export const isAdmin = computed(() => user.value?.user_type === "admin");
export const isHR = computed(() => user.value?.user_type === "hr");
export const currentUser = computed(() => user.value);

export { user, token, refreshToken };
