<template>
  <body class="text-center form-signin w-100 m-auto">
    <div class="row">
      <form action class="form col-12" @submit.prevent="login">
        <Logo />
        <h1 class="h3 mb-3 fw-semibold">Club deportivo Villa Elisa</h1>

        <div class="form-floating">
          <input v-model="user.username" placeholder="Nombre de usuario" class="form-control" type="username" id="username" required>
          <label class="form-label" for="#user.username">Nombre de usuario</label>
        </div>
        <div class="form-floating">
          <input v-model="user.password" placeholder="Contraseña" autocomplete="on" class="form-control" type="password" id="password" required>
          <label class="form-label" for="#user.password">Contraseña</label>
        </div>
        <div class="mb-4 col-12">
          <p v-if="error" class="error">Nombre de usuario o contraseña inválidos</p>
        </div>
        
        <button class="w-100 btn btn-lg btn-light" type="submit">Iniciar sesión</button>
        <p class="mt-5 mb-3 text-muted">&copy; Proyecto de software - Grupo 19</p>
      </form>
    </div>
  </body>
</template>

<script>
  import { useAuthStore } from "../stores/auth";
  import { defineComponent } from "vue";
  import { storeToRefs } from "pinia";

  export default defineComponent({
    name: "LoginView",
    setup(){
      const authStore = useAuthStore()
      const { isLoggedIn } = storeToRefs(authStore);
      return { authStore, isLoggedIn };
    },
    data() {
      return {
        error:false,
        user: {
          username: null,
          password: null
        }
      };
    },
    created(){
      this.isLoggedIn;
    },
    methods: {
      async login() {
        await this.authStore.loginUser(this.user)
          .catch(() => {
              // Handle error
              this.error=true;
            }
          );
          //Cleaning
          this.user = {
                username: null,
                password: null
              }
          
          if (this.isLoggedIn) {
              this.$router.push('/home')
          }
      },
      async logout() {
        await this.authStore.logoutUser().catch((err) => {
          console.log(err);
        });
        this.error=false;
        this.user = {
          username: null,
          password: null
        }
        this.$router.push('/');
      },
    }
  });
</script>

<style lang="scss" scoped>
html,
body {
  height: 100%;
}

body {
  align-items: center;
  padding-top: 40px;
  padding-bottom: 40px;
}

.form-signin {
  max-width: 330px;
  padding: 15px;
}

.form-signin .form-floating:focus-within {
  z-index: 2;
}

.form-signin input[type="username"] {
  margin-bottom: -1px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}

.form-signin input[type="password"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}

label {
  color: black;
}
.error {
  color: red;
  font-weight: 400;
}
</style>