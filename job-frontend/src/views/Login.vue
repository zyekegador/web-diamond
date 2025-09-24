<template>
  <div class="login-container">
    <div class="login-card">
      <h2>HR Login</h2>

      <form @submit.prevent="loginUser" class="login-form">
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <div v-if="successMessage" class="success-message">
          {{ successMessage }}
        </div>

        <div class="form-group">
          <label>Username</label>
          <input
            type="text"
            v-model="formData.username"
            required
            placeholder="Enter username"
            :disabled="isLoading"
          />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input
            type="password"
            v-model="formData.password"
            required
            placeholder="Enter password"
            :disabled="isLoading"
          />
        </div>

        <button type="submit" :disabled="isLoading" class="login-btn">
          <span v-if="isLoading">Logging in...</span>
          <span v-else>Login</span>
        </button>

        <p class="register-link">
          Don't have an account?
          <router-link to="/register">Register here</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Login",
  data() {
    return {
      formData: {
        username: "",
        password: "",
      },
      isLoading: false,
      errorMessage: "",
      successMessage: "",
    };
  },
  methods: {
    async loginUser() {
      this.errorMessage = "";
      this.successMessage = "";
      this.isLoading = true;

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/api/auth/login/",
          {
            username: this.formData.username,
            password: this.formData.password,
          }
        );

        if (response.data.success) {
          this.successMessage = response.data.message;

          // Store user data (you might want to use Vuex or localStorage)
          localStorage.setItem("user", JSON.stringify(response.data.user));

          // Redirect to dashboard or home page
          setTimeout(() => {
            this.$router.push("/dashboard"); // Adjust route as needed
          }, 1500);
        }
      } catch (error) {
        if (
          error.response &&
          error.response.data &&
          error.response.data.error
        ) {
          this.errorMessage = error.response.data.error;
        } else {
          this.errorMessage =
            "Login failed. Please check your connection and try again.";
        }
      } finally {
        this.isLoading = false;
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 400px;
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333;
  font-weight: 600;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
}

.form-group input {
  padding: 0.75rem;
  border: 2px solid #e1e5e9;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.error-message {
  background-color: #ffe6e6;
  color: #d63031;
  padding: 0.75rem;
  border-radius: 6px;
  border: 1px solid #ffcccc;
  text-align: center;
  font-weight: 500;
}

.success-message {
  background-color: #e8f5e8;
  color: #2d8c2d;
  padding: 0.75rem;
  border-radius: 6px;
  border: 1px solid #4caf50;
  text-align: center;
  font-weight: 500;
}

.login-btn {
  padding: 0.875rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  margin-top: 0.5rem;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.login-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.register-link {
  text-align: center;
  margin-top: 1.5rem;
  color: #666;
}

.register-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
}

.register-link a:hover {
  text-decoration: underline;
}
</style>
