<template>
  <transition name="modal-fade">
    <div v-if="isVisible" class="modal-overlay" @click="closeModal">
      <div class="modal-container" @click.stop>
        <button class="modal-close" @click="closeModal">
          <font-awesome-icon icon="times" />
        </button>

        <div class="modal-header">
          <img
            src="@/assets/logo.png"
            alt="Butuan City Logo"
            class="city-logo"
          />
          <h1>BUTUAN CITY</h1>
          <div class="social-links">
            <a href="#" class="social-link instagram">
              <font-awesome-icon :icon="['fab', 'instagram']" />
            </a>
            <a href="#" class="social-link facebook">
              <font-awesome-icon :icon="['fab', 'facebook']" />
            </a>
            <a href="#" class="social-link twitter">
              <font-awesome-icon :icon="['fab', 'twitter']" />
            </a>
          </div>
        </div>

        <div class="modal-content">
          <div class="info-grid">
            <div class="info-item">
              <strong>Category:</strong>
              <p>
                Highly Urbanized City in the Philippines and the regional center
                of Caraga Region.
              </p>
            </div>

            <div class="info-item">
              <strong>Location:</strong>
              <p>
                Northeastern part of Agusan Valley, Mindanao, sprawling across
                the Agusan River.
              </p>
            </div>

            <div class="info-item">
              <strong>Population:</strong>
              <p>372,910 people (according to 2020 census)</p>
            </div>

            <div class="info-item">
              <strong>Charter Day:</strong>
              <p>Every 2nd day of August (known as Adlaw Hong Butuan)</p>
            </div>

            <div class="info-item">
              <strong>Festival:</strong>
              <p>Balangay Festival (celebrated every month of May)</p>
            </div>
          </div>

          <div class="history-section">
            <h2>Origin:</h2>
            <p>
              Butuan City was originally located in Pinamanculan by the banks of
              Masao River but due to flooding, the settlers moved to Bood, now
              the Municipality of Magallanes. They again transferred to Bancao,
              now known as Linungusuran in Banza, five kilometers inland of
              Agusan River. But flooding was still a problem, so the people
              settled some 80 years ago permanently at a higher place called
              Agsao, now the present site of the City proper. Butuan City then
              was known to be The Timber City of the South during the booming
              logging industry. The city is blessed with rich fertile soil
              provided by the periodic flood coming from the Agusan River and
              its tributaries.
            </p>

            <p>
              The Agusan River provided the people with easy means of
              transportation for trade and commerce. The city is also enclosed
              with fertile flat lands and gently sloping hills, with Mt Mayapay
              over at the South West. The city's strategic location and rich
              natural resources have contributed to its economic growth. Butuan
              was The Timber City of the South during the boom of the logging
              industry. This boom prompted Congressman Marcos M. Calo to file a
              bill creating the City of Butuan. It became a city by virtue of
              Republic Act No. 523 also known as the City Charter of Butuan on
              August 2, 1950. From a Chartered City, Butuan was reclassified
              into a Highly Urbanized City on February 7, 1985, pursuant to the
              provisions of Memorandum Circular No. 83-49 of the Ministry of
              Local Government.
            </p>

            <p>
              The reclassification was based on its income and population as
              certified by the Ministry of Finance and National Census and
              Statistics Office. On February 23, 1985 a Republic Act 790 was
              approved by the National Assembly which created the administrative
              Region XIII, now known as the Caraga Region. Butuan City is
              considered as the regional center of Caraga Region. It's known for
              its historical significance as a trading hub in ancient times and
              its current role as a center for commerce, industry, and
              administration in the region. The city's strategic location and
              well-connected road network make it a key point of access to other
              major cities in Northern Mindanao, such as Davao, Cagayan de Oro,
              Malaybalay, Surigao, and Tandag. This connectivity enhances
              Butuan's importance as a hub for trade and economic activities in
              the region.
            </p>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: "AboutModal",
  props: {
    isVisible: {
      type: Boolean,
      required: true,
    },
  },
  methods: {
    closeModal() {
      this.$emit("close");
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 20px;
  overflow-y: auto;
}

.modal-container {
  background: white;
  border-radius: 16px;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    transform: translateY(-50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-close {
  position: absolute;
  top: 15px;
  right: 15px;
  width: 40px;
  height: 40px;
  border: none;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: #333;
  transition: all 0.3s;
  z-index: 10;
}

.modal-close:hover {
  background: rgba(0, 0, 0, 0.2);
  transform: rotate(90deg);
}

.modal-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 40px 30px;
  text-align: center;
  color: white;
  border-radius: 16px 16px 0 0;
}

.city-logo {
  width: 80px;
  height: 80px;
  object-fit: contain;
  margin-bottom: 15px;
  background: white;
  padding: 10px;
  border-radius: 50%;
}

.modal-header h1 {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 15px;
  letter-spacing: 2px;
}

.social-links {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-top: 20px;
}

.social-link {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
  transition: all 0.3s;
  text-decoration: none;
  background: rgba(255, 255, 255, 0.2);
}

.social-link:hover {
  transform: translateY(-3px);
  background: rgba(255, 255, 255, 0.3);
}

.modal-content {
  padding: 40px 30px;
}

.info-grid {
  display: grid;
  gap: 20px;
  margin-bottom: 40px;
}

.info-item {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
  border-left: 4px solid #667eea;
}

.info-item strong {
  display: block;
  color: #333;
  font-size: 16px;
  margin-bottom: 8px;
  font-weight: 600;
}

.info-item p {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
  margin: 0;
}

.history-section {
  margin-top: 30px;
}

.history-section h2 {
  color: #333;
  font-size: 24px;
  margin-bottom: 20px;
  font-weight: 700;
  border-bottom: 3px solid #667eea;
  padding-bottom: 10px;
}

.history-section p {
  color: #555;
  font-size: 15px;
  line-height: 1.8;
  text-align: justify;
  margin-bottom: 20px;
}

/* Scrollbar styling */
.modal-container::-webkit-scrollbar {
  width: 8px;
}

.modal-container::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.modal-container::-webkit-scrollbar-thumb {
  background: #667eea;
  border-radius: 4px;
}

.modal-container::-webkit-scrollbar-thumb:hover {
  background: #764ba2;
}

/* Modal transitions */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .modal-container {
    max-height: 95vh;
    margin: 10px;
  }

  .modal-header {
    padding: 30px 20px;
  }

  .modal-header h1 {
    font-size: 24px;
  }

  .city-logo {
    width: 60px;
    height: 60px;
  }

  .modal-content {
    padding: 30px 20px;
  }

  .info-item {
    padding: 15px;
  }

  .info-item strong {
    font-size: 14px;
  }

  .info-item p {
    font-size: 13px;
  }

  .history-section h2 {
    font-size: 20px;
  }

  .history-section p {
    font-size: 14px;
  }
}
</style>
