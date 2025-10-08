<template>
  <div class="login-container">
    <div class="login-box">
      <h1 class="back-link">
        <router-link to="/" class="back-link">
          <font-awesome-icon :icon="['fas', 'home']" />
          <span>Back to Home</span>
        </router-link>
      </h1>
      <div class="role-indicator" :class="expectedRole">
        <font-awesome-icon
          :icon="
            expectedRole === 'applicant'
              ? ['fas', 'user']
              : ['fas', 'briefcase']
          "
        />
        <span
          >{{
            expectedRole === "applicant" ? "APPLICANT" : "EMPLOYEE"
          }}
          LOGIN</span
        >
      </div>

      <form @submit.prevent="handleLogin">
        <!-- Show role dropdown only for HR staff login -->
        <div v-if="expectedRole === 'hr'" class="form-group">
          <label>Login As</label>
          <select v-model="selectedRole" required>
            <option value="">Select Role</option>
            <option value="hr">HR Staff</option>
            <option value="admin">Admin</option>
          </select>
        </div>

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
      selectedRole: "",
      error: "",
      loading: false,
      expectedRole: "", // Will be set in created hook
    };
  },
  created() {
    // Set the expected role from query parameter only once when component is created
    this.expectedRole = this.$route.query.role || "applicant";

    // Validate role parameter
    if (!["applicant", "hr", "admin"].includes(this.expectedRole)) {
      this.expectedRole = "applicant";
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      this.error = "";

      // Validate role selection for HR staff
      if (this.expectedRole === "hr" && !this.selectedRole) {
        this.error = "Please select your role (HR Staff or Admin)";
        this.loading = false;
        return;
      }

      try {
        const response = await api.login(this.credentials);

        const actualUserType = response.data.user.user_type;

        // Validate that the user's role matches what they selected
        if (this.expectedRole === "hr") {
          // Check if user type matches the selected role
          if (this.selectedRole === "admin" && actualUserType !== "admin") {
            this.error = "Access denied. This account is not an Admin account.";
            this.loading = false;
            return;
          }

          if (this.selectedRole === "hr" && actualUserType !== "hr") {
            this.error =
              "Access denied. This account is not an HR Staff account.";
            this.loading = false;
            return;
          }

          // General validation - must be hr or admin
          if (actualUserType !== "hr" && actualUserType !== "admin") {
            this.error =
              "Access denied. This account is not authorized for HR access.";
            this.loading = false;
            return;
          }
        }

        if (
          this.expectedRole === "applicant" &&
          actualUserType !== "applicant"
        ) {
          this.error =
            "Access denied. Please use the HR Staff login if you are an HR user.";
          this.loading = false;
          return;
        }

        // Store token and user data
        localStorage.setItem("token", response.data.token);
        localStorage.setItem("user", JSON.stringify(response.data.user));
        localStorage.setItem("userType", actualUserType);

        // Redirect based on actual user type
        if (actualUserType === "admin") {
          this.$router.push("/admin/dashboard");
        } else if (actualUserType === "hr") {
          this.$router.push("/hr/dashboard");
        } else if (actualUserType === "applicant") {
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
  min-height: 100vh;
  padding: 20px;
  background: linear-gradient(to bottom, #e3f2fd 0%, #bbdefb 100%);
}

.login-box {
  background: white;
  padding: 0 40px 40px 40px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 420px;
}

.role-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 12px 20px;
  border-radius: 8px;
  margin-bottom: 25px;
  font-weight: 600;
  font-size: 14px;
  letter-spacing: 0.5px;
}

.role-indicator.applicant {
  background: #1a237e;
  color: white;
}

.role-indicator.hr {
  background: #4caf50;
  color: white;
}

.role-indicator.admin {
  background: #ff5722;
  color: white;
}

h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
  font-size: 24px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #555;
  font-weight: 500;
  font-size: 14px;
}

input,
select {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.3s;
  background-color: white;
}

input:focus,
select:focus {
  outline: none;
  border-color: #4caf50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

select {
  cursor: pointer;
}

.btn-primary {
  width: 100%;
  padding: 14px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 10px;
  transition: background-color 0.3s, transform 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background-color: #45a049;
  transform: translateY(-1px);
}

.btn-primary:disabled {
  background-color: #ccc;
  cursor: not-allowed;
  transform: none;
}

.error-message {
  color: #d32f2f;
  padding: 12px;
  background-color: #ffebee;
  border-left: 4px solid #d32f2f;
  border-radius: 4px;
  margin-bottom: 15px;
  font-size: 14px;
}

.register-link {
  text-align: center;
  margin-top: 25px;
  padding-top: 20px;
  border-top: 1px solid #e0e0e0;
}

.register-link p {
  margin-bottom: 10px;
  font-size: 14px;
  color: #666;
}

.register-link a {
  color: #4caf50;
  text-decoration: none;
  font-weight: 600;
}

.register-link a:hover {
  text-decoration: underline;
}

.back-link {
  padding: 20px 0px 20px 0px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #791f1f;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s;
}

.back-link:hover {
  color: #4caf50;
}

.back-link svg {
  font-size: 16px;
}

.back-link a {
  color: #666;
  font-size: 13px;
}

@media (max-width: 480px) {
  .login-box {
    padding: 30px 20px;
  }

  h2 {
    font-size: 20px;
  }

  .role-indicator {
    font-size: 13px;
    padding: 10px 16px;
  }
}
</style>
