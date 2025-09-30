<template>
  <div class="home-container">
    <section class="hero-section">
      <div class="logo-section">
        <img src="@/assets/logo.png" alt="Company Logo" class="logo" />
        <span class="company-name">About Butuan</span>
      </div>
      <div class="hero-overlay">
        <div class="hero-content">
          <div class="company-branding">
            <img
              src="@/assets/company-logo.png"
              alt="Company Branding"
              class="brand-logo"
            />
          </div>

          <div class="social-icons">
            <a href="#" class="social-icon instagram">
              <i class="fab fa-instagram"></i>
            </a>
            <a href="#" class="social-icon facebook">
              <i class="fab fa-facebook"></i>
            </a>
            <a href="#" class="social-icon whatsapp">
              <i class="fab fa-whatsapp"></i>
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
            <router-link to="/login" class="access-btn applicant-btn">
              <div class="btn-icon">
                <i class="fas fa-user"></i>
              </div>
              <div class="btn-text">
                <span class="btn-title">APPLICANT</span>
                <span class="btn-subtitle">Fill out the application form</span>
              </div>
            </router-link>

            <router-link to="/login" class="access-btn hr-btn">
              <div class="btn-icon">
                <i class="fas fa-briefcase"></i>
              </div>
              <div class="btn-text">
                <span class="btn-title">HR STAFF</span>
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

        <!-- Quick Links Section -->
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
  </div>
</template>

<script>
export default {
  name: "Home",
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

/* Header Styles */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 40px;
  background-color: white;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 15px;
}

.logo {
  width: 100px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
  padding: 10px;
}

.company-name {
  font-weight: 600;
  font-size: 18px;
  color: #333;
}

.nav-links a {
  color: #333;
  text-decoration: none;
  font-weight: 500;
  font-size: 14px;
  transition: color 0.3s;
}

.nav-links a:hover {
  color: #4caf50;
}

/* Hero Section */
.hero-section {
  position: relative;
  height: 400px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background-image: url("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1200");
  background-size: cover;
  background-position: center;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    135deg,
    rgba(102, 126, 234, 0.8) 0%,
    rgba(118, 75, 162, 0.8) 100%
  );
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-content {
  text-align: center;
  color: white;
}

.company-branding {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.brand-logo {
  width: 200px;
  height: auto;
  filter: brightness(0) invert(1);
}

.tagline {
  font-size: 36px;
  font-weight: 700;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.social-icons {
  display: flex;
  gap: 15px;
  margin-top: 30px;
  justify-content: center;
}

.social-icon {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
  transition: transform 0.3s;
  text-decoration: none;
}

.social-icon:hover {
  transform: scale(1.1);
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
  padding: 60px 20px;
  background: linear-gradient(to bottom, #f5f7fa 0%, #c3cfe2 100%);
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
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.access-box h2 {
  text-align: center;
  color: #333;
  font-size: 22px;
  margin-bottom: 30px;
  font-weight: 600;
}

.access-buttons {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.access-btn {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px 25px;
  border-radius: 12px;
  text-decoration: none;
  transition: all 0.3s;
  cursor: pointer;
}

.applicant-btn {
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  color: white;
}

.applicant-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(30, 60, 114, 0.3);
}

.hr-btn {
  background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
  color: white;
}

.hr-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(86, 171, 47, 0.3);
}

.btn-icon {
  width: 50px;
  height: 50px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.btn-text {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.btn-title {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.btn-subtitle {
  font-size: 13px;
  opacity: 0.9;
}

.register-link {
  text-align: center;
  margin-top: 25px;
  padding-top: 25px;
  border-top: 1px solid #eee;
}

.register-link a {
  color: #4caf50;
  text-decoration: none;
  font-weight: 600;
}

.register-link a:hover {
  text-decoration: underline;
}

/* Quick Links */
.quick-links {
  background: white;
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.quick-links h3 {
  text-align: center;
  color: #333;
  font-size: 18px;
  margin-bottom: 25px;
  font-weight: 600;
}

.link-cards {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.link-card {
  display: block;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
  text-align: center;
  text-decoration: none;
  transition: all 0.3s;
}

.link-card:hover {
  transform: translateX(5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.link-card img {
  max-width: 100%;
  height: 50px;
  object-fit: contain;
}

.jobstreet {
  background: linear-gradient(135deg, #ff0084 0%, #ff6b9d 100%);
}

.outlook {
  background: linear-gradient(135deg, #0078d4 0%, #50a3e8 100%);
}

.csc {
  background: linear-gradient(135deg, #c41e3a 0%, #e63946 100%);
}

/* Footer */
.footer {
  background: #2c3e50;
  color: white;
  text-align: center;
  padding: 20px;
  font-size: 14px;
}

/* Responsive */
@media (max-width: 968px) {
  .access-container {
    grid-template-columns: 1fr;
  }

  .header {
    padding: 15px 20px;
  }

  .hero-section {
    height: 300px;
  }

  .tagline {
    font-size: 28px;
  }

  .brand-logo {
    width: 150px;
  }
}

@media (max-width: 600px) {
  .access-box {
    padding: 25px;
  }

  .access-btn {
    padding: 15px 20px;
  }

  .btn-icon {
    width: 40px;
    height: 40px;
    font-size: 20px;
  }

  .btn-title {
    font-size: 16px;
  }

  .btn-subtitle {
    font-size: 12px;
  }
}
</style>
