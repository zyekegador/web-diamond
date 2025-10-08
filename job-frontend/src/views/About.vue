<template>
  <transition name="modal-fade">
    <div v-if="isVisible" class="modal-overlay" @click="closeModal">
      <div class="modal-container" @click.stop>
        <button class="modal-close" @click="closeModal">
          <font-awesome-icon icon="times" />
        </button>

        <!-- Header with logo and title -->
        <div class="modal-header">
          <img
            src="@/assets/logo.jpg"
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

        <!-- Content Section -->
        <div class="modal-content">
          <!-- Info Table -->
          <div class="info-table">
            <div class="info-row">
              <div class="info-label">Category:</div>
              <div class="info-value">
                Highly Urbanized City in the Philippines and the regional center
                of Caraga Region.
              </div>
            </div>

            <div class="info-row">
              <div class="info-label">Location:</div>
              <div class="info-value">
                Northeastern part of Agusan Valley, Mindanao, sprawling across
                the Agusan River.
              </div>
            </div>

            <div class="info-row">
              <div class="info-label">Population:</div>
              <div class="info-value">
                372,910 people (according to 2020 census)
              </div>
            </div>

            <div class="info-row">
              <div class="info-label">Charter Day:</div>
              <div class="info-value">
                Every 2nd day of August (known as Adlaw Hong Butuan)
              </div>
            </div>

            <div class="info-row">
              <div class="info-label">Festival:</div>
              <div class="info-value">
                Balangay Festival (celebrated every month of May)
              </div>
            </div>

            <div class="info-row">
              <div class="info-label">Origin:</div>
              <div class="info-value origin-text">
                <p>
                  Butuan City was originally located in Pinamanculan by the
                  banks of Masao River but due to flooding, the settlers moved
                  to Bood, now the Municipality of Magallanes. They again
                  transferred to Bancao, now known as Linungusuran in Banza,
                  five kilometers inland of Agusan River. But flooding was still
                  a problem, so the people settled some 80 years ago permanently
                  at a higher place called Agsao, now the present site of the
                  City proper. Butuan City then was known to be The Timber City
                  of the South during the booming logging industry. The city is
                  blessed with rich fertile soil provided by the periodic flood
                  coming from the Agusan River and its tributaries.
                </p>

                <p>
                  The Agusan River provided the people with easy means of
                  transportation for trade and commerce. The city is also
                  endowed with fertile rice lands and gently sloping hills, with
                  Mt Mayapay over at the South West. The mountain that surround
                  the city protect the valley from fierce Pacific storms. The
                  city then was known as The Timber City of the South during the
                  boom of the logging industry. This boom prompted Congressman
                  Marcos M. Calo to file a bill creating the City of Butuan. It
                  became a city by virtue of Republic Act No. 523, also known as
                  the City Charter of Butuan on August 2, 1950. From a Chartered
                  City, Butuan was reclassified into a Highly Urbanized City on
                  February 7, 1985, pursuant to the provisions of Memorandum
                  Circular No. 83-49 of the Ministry of Local Government.
                </p>

                <p>
                  The reclassification was based on its income and population as
                  certified by the Ministry of Finance and National Census and
                  Statistics Office. On February 23, 1985 a Republic Act 7901
                  was approved by the National Assembly which created the
                  administrative Region XIII, now known as the Caraga Region.
                  Butuan City is considered as the regional center of Caraga
                  Region. It's known for its historical significance as a
                  trading hub in ancient times and its current role as a center
                  for commerce, industry, and administration in the region. The
                  city's strategic location and well-connected road network make
                  it a key point of access to other major cities in Northern
                  Mindanao, such as Davao, Cagayan de Oro, Malaybalay, Surigao,
                  and Tandag. This connectivity enhances Butuan's importance as
                  a hub for trade and economic activities in the region.
                </p>
              </div>
            </div>
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
  border-radius: 20px;
  max-width: 1000px;
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
  width: 36px;
  height: 36px;
  border: none;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: #333;
  transition: all 0.3s;
  z-index: 10;
}

.modal-close:hover {
  background: rgba(0, 0, 0, 0.2);
  transform: rotate(90deg);
}

.modal-header {
  background: white;
  padding: 30px 30px 20px 30px;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  align-items: center;
  gap: 15px;
}

.city-logo {
  width: 60px;
  height: 60px;
  object-fit: contain;
  flex-shrink: 0;
}

.modal-header h1 {
  font-size: 20px;
  font-weight: 700;
  color: #333;
  letter-spacing: 1px;
  flex: 1;
}

.social-links {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.social-link {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 14px;
  transition: all 0.3s;
  text-decoration: none;
}

.social-link:hover {
  transform: translateY(-2px);
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

.twitter {
  background: #1da1f2;
}

.modal-content {
  padding: 30px;
}

.info-table {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.info-row {
  display: grid;
  grid-template-columns: 130px 1fr;
  gap: 15px;
  padding: 18px 0;
  border-bottom: 1px solid #f0f0f0;
  align-items: start;
}

.info-row:last-child {
  border-bottom: none;
}

.info-label {
  font-weight: 600;
  color: #333;
  font-size: 14px;
  padding-top: 2px;
}

.info-value {
  color: #555;
  font-size: 14px;
  line-height: 1.6;
}

.origin-text p {
  margin: 0 0 15px 0;
  text-align: justify;
}

.origin-text p:last-child {
  margin-bottom: 0;
}

/* Scrollbar styling */
.modal-container::-webkit-scrollbar {
  width: 6px;
}

.modal-container::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.modal-container::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 3px;
}

.modal-container::-webkit-scrollbar-thumb:hover {
  background: #999;
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
    border-radius: 16px;
  }

  .modal-header {
    padding: 20px;
    flex-wrap: wrap;
  }

  .city-logo {
    width: 50px;
    height: 50px;
  }

  .modal-header h1 {
    font-size: 18px;
  }

  .social-links {
    width: 100%;
    justify-content: center;
    margin-top: 10px;
  }

  .modal-content {
    padding: 20px;
  }

  .info-row {
    grid-template-columns: 1fr;
    gap: 8px;
    padding: 15px 0;
  }

  .info-label {
    font-size: 13px;
  }

  .info-value {
    font-size: 13px;
  }
}
</style>
