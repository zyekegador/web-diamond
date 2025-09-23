import { createRouter, createWebHistory } from "vue-router";
import { isAuthenticated, isAdmin, isHR, fetchProfile } from "@/stores/auth";

const routes = [
  {
    path: "/",
    name: "Home",
    component: () => import("@/views/Home.vue"),
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("@/views/Login.vue"),
    meta: { requiresGuest: true },
  },
  {
    path: "/register",
    name: "Register",
    component: () => import("@/views/Register.vue"),
    meta: { requiresGuest: true },
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: () => import("@/views/Dashboard.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/admin",
    name: "AdminPanel",
    component: () => import("@/views/AdminPanel.vue"),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  if (localStorage.getItem("access_token") && !isAuthenticated.value) {
    try {
      await fetchProfile();
    } catch (error) {
      // Token invalid
    }
  }

  if (to.meta.requiresAuth && !isAuthenticated.value) {
    next("/login");
  } else if (to.meta.requiresGuest && isAuthenticated.value) {
    next("/dashboard");
  } else if (to.meta.requiresAdmin && !isAdmin.value) {
    next("/dashboard");
  } else {
    next();
  }
});

export default router;
