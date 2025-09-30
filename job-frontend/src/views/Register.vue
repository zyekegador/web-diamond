<template>
  <div class="register-container">
    <div class="register-box">
      <h2>Applicant Registration</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-row">
          <div class="form-group">
            <label>First Name *</label>
            <input
              type="text"
              v-model="formData.first_name"
              required
              placeholder="Enter first name"
            />
          </div>

          <div class="form-group">
            <label>Last Name *</label>
            <input
              type="text"
              v-model="formData.last_name"
              required
              placeholder="Enter last name"
            />
          </div>
        </div>

        <div class="form-group">
          <label>Username *</label>
          <input
            type="text"
            v-model="formData.username"
            required
            placeholder="Choose a username"
          />
        </div>

        <div class="form-group">
          <label>Email *</label>
          <input
            type="email"
            v-model="formData.email"
            required
            placeholder="Enter email"
          />
        </div>

        <div class="form-group">
          <label>Phone Number</label>
          <input
            type="tel"
            v-model="formData.phone_number"
            placeholder="Enter phone number"
          />
        </div>

        <div class="form-group">
          <label>Date of Birth</label>
          <input type="date" v-model="formData.date_of_birth" />
        </div>

        <div class="form-group">
          <label>Address</label>
          <textarea
            v-model="formData.address"
            rows="3"
            placeholder="Enter address"
          ></textarea>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Password *</label>
            <input
              type="password"
              v-model="formData.password"
              required
              placeholder="Enter password"
            />
          </div>

          <div class="form-group">
            <label>Confirm Password *</label>
            <input
              type="password"
              v-model="formData.password2"
              required
              placeholder="Confirm password"
            />
          </div>
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <div v-if="success" class="success-message">
          {{ success }}
        </div>

        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? "Creating Account..." : "Register" }}
        </button>
      </form>

      <div class="login-link">
        <p>
          Already have an account? <router-link to="/login">Login</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "ApplicantRegister",
  data() {
    return {
      formData: {
        username: "",
        email: "",
        password: "",
        password2: "",
        first_name: "",
        last_name: "",
        phone_number: "",
        address: "",
        date_of_birth: "",
      },
      error: "",
      success: "",
      loading: false,
    };
  },
  methods: {
    async handleRegister() {
      this.loading = true;
      this.error = "";
      this.success = "";

      if (this.formData.password !== this.formData.password2) {
        this.error = "Passwords do not match";
        this.loading = false;
        return;
      }

      try {
        const response = await api.registerApplicant(this.formData);
        this.success =
          "Account created successfully! Redirecting to dashboard...";

        // Store token and user data
        localStorage.setItem("token", response.data.token);
        localStorage.setItem("user", JSON.stringify(response.data.user));
        localStorage.setItem("userType", response.data.user.user_type);

        // Redirect to applicant dashboard
        setTimeout(() => {
          this.$router.push("/applicant/dashboard");
        }, 1500);
      } catch (error) {
        if (error.response?.data) {
          const errors = error.response.data;
          this.error = Object.values(errors).flat().join(" ");
        } else {
          this.error = "Registration failed. Please try again.";
        }
      } finally {
        this.loading = false;
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
  padding: 20px;
  background-color: #f5f5f5;
}

.register-box {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 600px;
}

h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
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

input,
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  font-family: inherit;
}

input:focus,
textarea:focus {
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

.success-message {
  color: #4caf50;
  padding: 10px;
  background-color: #e8f5e9;
  border-radius: 4px;
  margin-bottom: 10px;
  text-align: center;
}

.login-link {
  text-align: center;
  margin-top: 20px;
}

.login-link a {
  color: #4caf50;
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
}
</style>
