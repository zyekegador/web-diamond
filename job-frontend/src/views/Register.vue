<template>
  <div class="register-container">
    <div class="register-card">
      <h2>HR Registration</h2>

      <!-- Success Message -->
      <div v-if="registrationSuccess" class="success-message">
        <div class="success-icon">✓</div>
        <h3>Registration Successful!</h3>
        <p>{{ successMessage }}</p>
        <p class="note">An admin will review and activate your account soon.</p>
        <div class="user-info">
          <p><strong>Username:</strong> {{ registeredUser.username }}</p>
          <p><strong>Email:</strong> {{ registeredUser.email }}</p>
        </div>
        <router-link to="/login" class="back-to-login">Go to Login</router-link>
      </div>

      <!-- Registration Form -->
      <form
        v-if="!registrationSuccess"
        @submit.prevent="registerUser"
        class="register-form"
      >
        <!-- Error Messages -->
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <div class="form-group">
          <label>Username *</label>
          <input
            type="text"
            v-model="formData.username"
            required
            placeholder="Enter username"
            :disabled="isLoading"
          />
        </div>

        <div class="form-group">
          <label>Email *</label>
          <input
            type="email"
            v-model="formData.email"
            required
            placeholder="Enter email"
            :disabled="isLoading"
          />
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>First Name</label>
            <input
              type="text"
              v-model="formData.first_name"
              placeholder="First name"
              :disabled="isLoading"
            />
          </div>
          <div class="form-group">
            <label>Last Name</label>
            <input
              type="text"
              v-model="formData.last_name"
              placeholder="Last name"
              :disabled="isLoading"
            />
          </div>
        </div>

        <div class="form-group">
          <label>Password *</label>
          <input
            type="password"
            v-model="formData.password"
            required
            placeholder="Enter password (min 6 characters)"
            :disabled="isLoading"
          />
        </div>

        <div class="form-group">
          <label>Confirm Password *</label>
          <input
            type="password"
            v-model="formData.confirmPassword"
            required
            placeholder="Confirm password"
            :disabled="isLoading"
          />
        </div>

        <button type="submit" :disabled="isLoading" class="register-btn">
          <span v-if="isLoading">Registering...</span>
          <span v-else>Register</span>
        </button>

        <p class="login-link">
          Already have an account?
          <router-link to="/login">Login here</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Register",
  data() {
    return {
      formData: {
        username: "",
        email: "",
        first_name: "",
        last_name: "",
        password: "",
        confirmPassword: "",
      },
      isLoading: false,
      errorMessage: "",
      registrationSuccess: false,
      successMessage: "",
      registeredUser: {},
    };
  },
  methods: {
    async registerUser() {
      // Reset messages
      this.errorMessage = "";

      // Validate passwords match
      if (this.formData.password !== this.formData.confirmPassword) {
        this.errorMessage = "Passwords do not match";
        return;
      }

      // Validate password strength
      if (this.formData.password.length < 6) {
        this.errorMessage = "Password must be at least 6 characters long";
        return;
      }

      this.isLoading = true;

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/api/auth/register/",
          {
            username: this.formData.username,
            email: this.formData.email,
            first_name: this.formData.first_name,
            last_name: this.formData.last_name,
            password: this.formData.password,
          }
        );

        if (response.data.success) {
          this.registrationSuccess = true;
          this.successMessage = response.data.message;
          this.registeredUser = {
            username: response.data.username,
            email: response.data.email,
          };

          // Clear form data
          this.formData = {
            username: "",
            email: "",
            first_name: "",
            last_name: "",
            password: "",
            confirmPassword: "",
          };
        }
      } catch (error) {
        console.error("Registration error:", error);
        if (
          error.response &&
          error.response.data &&
          error.response.data.error
        ) {
          this.errorMessage = error.response.data.error;
        } else {
          this.errorMessage =
            "Registration failed. Please check your connection and try again.";
        }
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.register-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 500px;
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333;
  font-weight: 600;
}

.success-message {
  text-align: center;
  padding: 2rem;
  border: 2px solid #4caf50;
  border-radius: 8px;
  background-color: #f8fff8;
}

.success-icon {
  font-size: 4rem;
  color: #4caf50;
  margin-bottom: 1rem;
  font-weight: bold;
}

.success-message h3 {
  color: #4caf50;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.success-message p {
  margin-bottom: 0.5rem;
  color: #666;
  line-height: 1.5;
}

.note {
  font-style: italic;
  font-size: 0.9rem;
  color: #888;
}

.user-info {
  background-color: #f0f0f0;
  padding: 1rem;
  border-radius: 6px;
  margin: 1rem 0;
  text-align: left;
}

.user-info p {
  margin: 0.25rem 0;
  font-size: 0.9rem;
}

.back-to-login {
  display: inline-block;
  margin-top: 1rem;
  padding: 12px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  border-radius: 6px;
  transition: transform 0.2s, box-shadow 0.2s;
  font-weight: 500;
}

.back-to-login:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
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
  font-size: 0.9rem;
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

.form-group input:disabled {
  background-color: #f8f9fa;
  cursor: not-allowed;
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

.register-btn {
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

.register-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.register-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.login-link {
  text-align: center;
  margin-top: 1.5rem;
  color: #666;
}

.login-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
}

.login-link a:hover {
  text-decoration: underline;
}

@media (max-width: 600px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .register-card {
    padding: 1.5rem;
    margin: 10px;
  }

  .success-icon {
    font-size: 3rem;
  }
}
</style>
