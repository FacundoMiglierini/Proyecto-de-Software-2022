<script setup>
  import NavBar from "./components/NavBar.vue";
  import NavBarLanding from "./components/NavBarLanding.vue";
  import Footer from "./components/Footer.vue";
  import FooterLanding from "./components/FooterLanding.vue"
  import { useAuthStore } from "./stores/auth";
  import { storeToRefs } from "pinia";

  const authStore = useAuthStore()
  const { isLoggedIn } = storeToRefs(authStore)
</script>

<template>
  <body class="d-flex flex-column min-vh-100"> 
    <header>
      <div v-if="isLoggedIn">
        <NavBar />
      </div>
      <div v-else>
        <NavBarLanding />
      </div>
    </header>
    <main class="mt-auto d-flex align-items-center justify-content-center"> 
      <RouterView />
    </main>
    <div class="w-100 mt-auto">
      <div v-if="isLoggedIn">
        <Footer />
      </div>
      <div v-else-if="$route.matched.some(({ name }) => name !== 'login')">
        <FooterLanding />
      </div>
    </div>
  </body>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css?family=Montserrat:400,600,700');
body {
  background-color: #0a0909;
}
header {
  line-height: 1.5;
  max-height: 100vh;
}

html, body {
  font-family: 'Montserrat', Helvetica, sans-serif;
}

#app {
  font-family: 'Montserrat', Helvetica, sans-serif;
}
</style>
