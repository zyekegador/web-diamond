<template>
  <div class="home-container">
    <section class="hero-section">
      <div class="header-in-hero">
        <div class="logo-section">
          <img src="@/assets/logo.jpg" alt="Company Logo" class="logo" />
          <span class="company-name clickable" @click="showAbout = true"
            >ABOUT BUTUAN</span
          >
        </div>
      </div>
      <div class="hero-overlay">
        <div class="hero-content">
          <div class="social-icons">
            <a href="#" class="social-icon instagram">
              <font-awesome-icon :icon="['fab', 'instagram']" />
            </a>
            <a href="#" class="social-icon facebook">
              <font-awesome-icon :icon="['fab', 'facebook']" />
            </a>
            <a href="#" class="social-icon whatsapp">
              <font-awesome-icon :icon="['fab', 'whatsapp']" />
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- Access Type Section -->
    <section class="access-section">
      <div class="access-container">
        <div class="access-box">
          <h2>CHOOSE YOUR ACCESS TYPE</h2>
          <div class="access-buttons">
            <router-link
              to="/login?role=applicant"
              class="access-btn applicant-btn"
            >
              <div class="btn-icon">
                <font-awesome-icon :icon="['fas', 'user']" />
              </div>
              <div class="btn-text">
                <span class="btn-title">APPLICANT</span>
                <span class="btn-subtitle">Fill out the application form</span>
              </div>
            </router-link>

            <router-link to="/login?role=hr" class="access-btn hr-btn">
              <div class="btn-icon">
                <font-awesome-icon :icon="['fas', 'briefcase']" />
              </div>
              <div class="btn-text">
                <span class="btn-title">EMPLOYEE</span>
                <span class="btn-subtitle">Log in to manage</span>
              </div>
            </router-link>
          </div>

          <div class="register-link">
            <p>
              Don't have an account?
              <router-link to="/register">Register as Applicant</router-link>
            </p>
          </div>
        </div>

        <div class="quick-links">
          <h3>QUICK LINKS</h3>
          <div class="link-cards">
            <a
              href="https://jobstreet.com"
              target="_blank"
              class="link-card jobstreet"
            >
              <img src="@/assets/jobstreet-logo.png" alt="JobStreet" />
            </a>
            <a
              href="https://outlook.com"
              target="_blank"
              class="link-card outlook"
            >
              <img src="@/assets/outlook-logo.png" alt="Outlook" />
            </a>
            <a href="https://csc.gov.ph" target="_blank" class="link-card csc">
              <img src="@/assets/csc-logo.png" alt="Civil Service Commission" />
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <p>&copy; 2024 Company Name. All Rights Reserved.</p>
    </footer>

    <About :isVisible="showAbout" @close="showAbout = false" />
  </div>
</template>

<script>
import About from "./About.vue";
export default {
  name: "Home",
  components: {
    About,
  },
  data() {
    return {
      showAbout: false,
    };
  },
  mounted() {
    // Check if user is already logged in
    const token = localStorage.getItem("token");
    const userType = localStorage.getItem("userType");

    if (token && userType) {
      // Redirect based on user type
      if (userType === "admin") {
        this.$router.push("/admin/dashboard");
      } else if (userType === "hr") {
        this.$router.push("/hr/dashboard");
      } else if (userType === "applicant") {
        this.$router.push("/applicant/dashboard");
      }
    }
  },
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.home-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  display: none;
}

/* Hero Section */
.hero-section {
  position: relative;
  height: 400px;
  background: url("@/assets/company-logo.png") center/cover;
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  background-color: #f5f5f5;
  overflow: hidden;
}

.header-in-hero {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  z-index: 10;
  padding: 15px 40px;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 0px;
}

.logo {
  width: 100px;
  height: 50px;
  object-fit: contain;
}

.company-name {
  font-weight: 700;
  font-size: 16px;
  color: #1a237e;
  letter-spacing: 0.5px;
  margin-left: 0px;
}

.company-name.clickable {
  cursor: pointer;
  transition: all 0.3s;
}

.company-name.clickable:hover {
  color: #667eea;
  text-decoration: underline;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    to right,
    rgba(255, 255, 255, 0.3) 0%,
    rgba(255, 255, 255, 0.1) 60%,
    transparent 100%
  );
  display: flex;
  align-items: flex-end;
  justify-content: flex-end;
  padding: 30px 40px;
}

.hero-content {
  position: relative;
  z-index: 3;
}

.social-icons {
  display: flex;
  gap: 12px;
  padding-right: 25px;
}

.social-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
  transition: transform 0.3s, box-shadow 0.3s;
  text-decoration: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.social-icon:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.instagram {
  background: linear-gradient(
    45deg,
    #f09433 0%,
    #e6683c 25%,
    #dc2743 50%,
    #cc2366 75%,
    #bc1888 100%
  );
}

.facebook {
  background: #1877f2;
}

.whatsapp {
  background: #25d366;
}

/* Access Section */
.access-section {
  flex: 1;
  padding: 50px 20px;
  background: linear-gradient(to bottom, #e3f2fd 0%, #bbdefb 100%);
}

.access-container {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  align-items: start;
}

.access-box {
  background: white;
  padding: 40px 35px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.access-box h2 {
  text-align: center;
  color: #1a237e;
  font-size: 18px;
  margin-bottom: 30px;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.access-buttons {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.access-btn {
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 18px 22px;
  border-radius: 30px;
  text-decoration: none;
  transition: all 0.3s ease;
  cursor: pointer;
}

.applicant-btn {
  background: #1a237e;
  color: white;
}

.applicant-btn:hover {
  background: #0d1642;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(26, 35, 126, 0.25);
}

.hr-btn {
  background: #4caf50;
  color: white;
}

.hr-btn:hover {
  background: #43a047;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(76, 175, 80, 0.25);
}

.btn-icon {
  width: 45px;
  height: 45px;
  background: rgba(255, 255, 255, 0.25);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  flex-shrink: 0;
}

.btn-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
  text-align: left;
}

.btn-title {
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.btn-subtitle {
  font-size: 12px;
  opacity: 0.95;
  font-weight: 400;
}

.register-link {
  text-align: center;
  margin-top: 25px;
  padding-top: 25px;
  border-top: 1px solid #e0e0e0;
  font-size: 14px;
  color: #666;
}

.register-link a {
  color: #1976d2;
  text-decoration: none;
  font-weight: 600;
}

.register-link a:hover {
  text-decoration: underline;
}

/* Quick Links */
.quick-links {
  background: white;
  padding: 35px 30px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.quick-links h3 {
  text-align: center;
  color: #1a237e;
  font-size: 18px;
  margin-bottom: 25px;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.link-cards {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.link-card {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.link-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.link-card img {
  max-width: 100%;
  height: 45px;
  object-fit: contain;
}

.jobstreet {
  background: linear-gradient(135deg, #e91e63 0%, #f06292 100%);
}

.outlook {
  background: linear-gradient(135deg, #0078d4 0%, #4ba3e8 100%);
}

.csc {
  background: linear-gradient(135deg, #1565c0 0%, #1976d2 100%);
}

/* Footer */
.footer {
  background: #263238;
  color: white;
  text-align: center;
  padding: 20px;
  font-size: 13px;
}

/* Responsive */
@media (max-width: 968px) {
  .access-container {
    grid-template-columns: 1fr;
  }

  .header-in-hero {
    padding: 15px 20px;
  }

  .hero-section {
    height: 300px;
  }

  .hero-overlay {
    padding: 20px;
  }

  .social-icons {
    gap: 10px;
  }

  .social-icon {
    width: 36px;
    height: 36px;
    font-size: 16px;
  }
}

@media (max-width: 600px) {
  .access-box {
    padding: 30px 20px;
  }

  .access-btn {
    padding: 16px 18px;
  }

  .btn-icon {
    width: 40px;
    height: 40px;
    font-size: 18px;
  }

  .btn-title {
    font-size: 15px;
  }

  .btn-subtitle {
    font-size: 11px;
  }

  .hero-section {
    height: 250px;
  }

  .link-card img {
    height: 38px;
  }
}
</style>
