<template>
  <div class="login-container">
    <div class="login-box">
      <h2>Login</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Username</label>
          <input
            type="text"
            v-model="credentials.username"
            required
            placeholder="Enter username"
          />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input
            type="password"
            v-model="credentials.password"
            required
            placeholder="Enter password"
          />
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? "Logging in..." : "Login" }}
        </button>
      </form>

      <div class="register-link">
        <p>
          Don't have an account?
          <router-link to="/register">Register as Applicant</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "Login",
  data() {
    return {
      credentials: {
        username: "",
        password: "",
      },
      error: "",
      loading: false,
    };
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      this.error = "";

      try {
        const response = await api.login(this.credentials);

        // Store token and user data
        localStorage.setItem("token", response.data.token);
        localStorage.setItem("user", JSON.stringify(response.data.user));
        localStorage.setItem("userType", response.data.user.user_type);

        // Redirect based on user type
        const userType = response.data.user.user_type;
        if (userType === "admin") {
          this.$router.push("/admin/dashboard");
        } else if (userType === "hr") {
          this.$router.push("/hr/dashboard");
        } else if (userType === "applicant") {
          this.$router.push("/applicant/dashboard");
        }
      } catch (error) {
        this.error =
          error.response?.data?.error || "Login failed. Please try again.";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 20px;
}

.login-box {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
  color: #555;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

input:focus {
  outline: none;
  border-color: #4caf50;
}

.btn-primary {
  width: 100%;
  padding: 12px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 10px;
}

.btn-primary:hover {
  background-color: #45a049;
}

.btn-primary:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.error-message {
  color: #f44336;
  padding: 10px;
  background-color: #ffebee;
  border-radius: 4px;
  margin-bottom: 10px;
  text-align: center;
}

.register-link {
  text-align: center;
  margin-top: 20px;
}

.register-link a {
  color: #4caf50;
  text-decoration: none;
  font-weight: 500;
}

.register-link a:hover {
  text-decoration: underline;
}
</style>
