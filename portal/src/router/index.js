import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/auth";
import LoginView from "../views/LoginView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "login",
      meta: {
        hideForAuth: true
      },
      component: LoginView,
    },
    {
      path: "/disciplines",
      name: "disciplines",
      meta: {
        hideForAuth: true
      },
      component: () => import("../views/AllDisciplinesView.vue"),
    },
    {
      path: "/about",
      name: "about",
      meta: {
        hideForAuth: true
      },
      component: () => import("../views/AboutView.vue"),
    },
    {
      path: "/home",
      name: "home",
      meta: {
        requiresAuth: true
      },
      component: () => import("../views/HomeView.vue"),
    },
    {
      path: "/payments",
      name: "payments",
      meta: {
        requiresAuth: true
      },
      component: () => import("../views/PaymentsView.vue"),
    },
    {
      path: "/license",
      name: "license",
      meta: {
        requiresAuth: true
      },
      component: () => import("../views/LicenseView.vue"),
    },
    {
      path: "/stats",
      name: "stats",
      meta: {
        requiresAuth: true
      },
      component: () => import("../views/StatsView.vue"),
    },
  ],
});

router.beforeEach(async(to) => {

  const authStore = useAuthStore()
  if( to.meta.requiresAuth && !authStore.isLoggedIn ) { return { name: 'login' } }
  if( to.meta.hideForAuth && authStore.isLoggedIn) { return { name: 'home' } }
}) 

export default router;
