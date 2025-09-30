import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

// Font Awesome imports
import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

// Icons you want to use
import {
  faInstagram,
  faFacebook,
  faWhatsapp,
} from "@fortawesome/free-brands-svg-icons";
import { faUser, faBriefcase } from "@fortawesome/free-solid-svg-icons";

// Add icons to the library
library.add(faInstagram, faFacebook, faWhatsapp, faUser, faBriefcase);

const app = createApp(App);

app.component("font-awesome-icon", FontAwesomeIcon);

app.use(router);

app.mount("#app");
