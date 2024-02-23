import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";


import "./assets/main.css";
import "bootstrap/dist/css/bootstrap.min.css"
import 'bootstrap-icons/font/bootstrap-icons.css'
import "bootstrap"
import Logo from "./components/Logo.vue"
import Vue3EasyDataTable from 'vue3-easy-data-table';
import 'vue3-easy-data-table/dist/style.css'



const app = createApp(App);

app.component('Logo', Logo)
app.component('EasyDataTable', Vue3EasyDataTable)

app.use(createPinia());
app.use(router);

app.mount("#app");
