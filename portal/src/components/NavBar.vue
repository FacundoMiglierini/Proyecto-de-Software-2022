<template>
  <nav class="navbar sticky-top navbar-expand-md bg-light mt-0" role="navigation">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">
          <img src="@/assets/logo.png" height="50" width="50" class="rounded me-2" alt="Logo del club">
      </a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="navbar-collapse collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mx-md-auto mt-3 mt-md-0"> 
          <li class="nav-item"> 
            <a class="nav-link"><router-link to="/home">Home</router-link></a>
          </li>
          <li class="nav-item">
            <a class="nav-link"><router-link to="/stats">Estadísticas</router-link></a>
          </li>
          <li class="nav-item">
            <a class="nav-link"><router-link to="/payments">Pagos</router-link></a>
          </li>
          <li class="nav-item">
            <a class="nav-link"><router-link to="/license">Carnet</router-link></a>
          </li>
          <li class="nav-item">
            <a class="nav-link"><router-link to="/" @click="logout">Cerrar sesión</router-link></a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script lang="ts">
import { useAuthStore } from "../stores/auth";
import { defineComponent } from "vue";
import { RouterLink } from "vue-router";
import $ from 'jquery'
window.jQuery = window.$ = $

export default defineComponent({
  name: "NavBar",
  setup(){
    const authStore = useAuthStore()
    return { authStore };
  },
  watch: {
    '$route' (){
      $('#navbarSupportedContent').collapse('hide');
    }
  },
  methods: {
    async logout() {
      await this.authStore.logoutUser().catch((err) => {
        console.log(err);
      });
      this.$router.push('/');
    },
  }
});

</script>

<style>
@media (min-width: 768px){
  .navbar-brand {
    display: none
  }
}
nav {
  width: 100%;
  font-size: 15px;
  text-align: left;
}

nav a.router-link-exact-active {
  color:black; /* var(--color-text); */
  font-weight: bolder;
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
  color: black;
}

nav a:first-of-type {
  border: 0;
}

</style>
