<template>
  <div class="register-container">
    <div class="register-form">
      <h2>Register</h2>

      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>Username:</label>
          <input
            v-model="formData.username"
            type="text"
            required
            :disabled="loading"
          />
          <div v-if="errors.username" class="field-error">
            {{ errors.username[0] }}
          </div>
        </div>

        <div class="form-group">
          <label>Email:</label>
          <input
            v-model="formData.email"
            type="email"
            required
            :disabled="loading"
          />
          <div v-if="errors.email" class="field-error">
            {{ errors.email[0] }}
          </div>
        </div>

        <div class="form-group">
          <label>User Type:</label>
          <select v-model="formData.user_type" required :disabled="loading">
            <option value="">Select user type</option>
            <option value="hr">HR</option>
            <option value="admin">Admin</option>
          </select>
        </div>

        <div class="form-group">
          <label>Password:</label>
          <input
            v-model="formData.password"
            type="password"
            required
            :disabled="loading"
          />
          <div v-if="errors.password" class="field-error">
            {{ errors.password[0] }}
          </div>
        </div>

        <div v-if="generalError" class="error">
          {{ generalError }}
        </div>

        <div v-if="successMessage" class="success">
          {{ successMessage }}
        </div>

        <button type="submit" :disabled="loading">
          {{ loading ? "Registering..." : "Register" }}
        </button>
      </form>

      <p>
        Already have an account?
        <router-link to="/login">Login here</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { register } from "@/stores/auth";

const formData = ref({
  username: "",
  email: "",
  user_type: "",
  password: "",
});

const loading = ref(false);
const errors = ref({});
const generalError = ref("");
const successMessage = ref("");

const handleRegister = async () => {
  loading.value = true;
  errors.value = {};
  generalError.value = "";
  successMessage.value = "";

  const result = await register(formData.value);

  if (result.success) {
    successMessage.value =
      formData.value.user_type === "hr"
        ? "Registration successful! Your account is pending admin approval."
        : "Registration successful! You can now login.";

    formData.value = {
      username: "",
      email: "",
      user_type: "",
      password: "",
    };
  } else {
    if (result.errors.general) {
      generalError.value = result.errors.general;
    } else {
      errors.value = result.errors;
    }
  }

  loading.value = false;
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.register-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box;
}

.field-error {
  color: #dc3545;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.error {
  color: #dc3545;
  margin-bottom: 1rem;
  padding: 0.5rem;
  background-color: #f8d7da;
  border-radius: 4px;
}

.success {
  color: #155724;
  margin-bottom: 1rem;
  padding: 0.5rem;
  background-color: #d4edda;
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 0.75rem;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
}

button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #218838;
}
</style>
