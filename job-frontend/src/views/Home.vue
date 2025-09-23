<template>
  <div class="home">
    <h1>Job Application System</h1>
    <p>Find your dream job or manage your hiring process</p>

    <div class="sections">
      <!-- For Applicants -->
      <div class="applicant-section">
        <h2>Looking for a Job?</h2>
        <p>Browse available positions and apply online</p>
        <router-link to="/jobs" class="btn primary">
          🔍 Browse Jobs
        </router-link>
      </div>

      <!-- For Staff -->
      <div class="staff-section">
        <h2>Staff Portal</h2>
        <p>HR and Admin login</p>
        <div class="staff-buttons">
          <router-link to="/login" class="btn">Login</router-link>
          <router-link to="/register" class="btn">Register</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
}

.home h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  text-align: center;
}

.home > p {
  font-size: 1.2rem;
  margin-bottom: 3rem;
  text-align: center;
}

.sections {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 3rem;
  max-width: 800px;
  width: 100%;
}

.applicant-section,
.staff-section {
  background: rgba(255, 255, 255, 0.1);
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  backdrop-filter: blur(10px);
}

.applicant-section h2,
.staff-section h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.staff-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1rem;
}

.btn {
  padding: 1rem 2rem;
  background: white;
  color: #667eea;
  text-decoration: none;
  border-radius: 8px;
  font-weight: bold;
  transition: all 0.2s;
  display: inline-block;
}

.btn.primary {
  background: #28a745;
  color: white;
  font-size: 1.1rem;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.btn.primary:hover {
  background: #218838;
}
</style>
