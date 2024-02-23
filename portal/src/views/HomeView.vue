<template>
  <div class="container my-5">
    <div class="card text-center">
      <ul class="nav nav-tabs mx-auto">
        <li class="nav-item">
          <a :class="!all?'active':''" class="nav-link" @click="unsetAll">Mis disciplinas</a>
        </li>
        <li class="nav-item">
          <a :class="all?'active':''" class="nav-link" aria-current="page" @click="setAll">Todas las disciplinas</a>
        </li>
      </ul>
    <div v-show="!all">
      <DisciplinesTable/>
    </div>
    <div v-show="all">
      <AllDisciplinesTable/>
    </div>
    </div>
  </div>
</template>

<script lang="ts">
  import { defineComponent } from 'vue';
  import AllDisciplinesTable from '../components/AllDisciplinesTable.vue';
  import DisciplinesTable from '../components/DisciplinesTable.vue';

  export default defineComponent({
    name: "HomeView",
    components: {
      AllDisciplinesTable,
      DisciplinesTable
    },
    data(){
      return { 
        all: false 
      }
    },
    methods: {
      setAll(){
        this.all = true
      },
      unsetAll(){
        this.all = false
      }
    }
  })
</script>

<style>
a.nav-link {
  color: black;
}

a.nav-link:hover{
  color: black !important;
}

a.active {
  font-weight: 600;
  color: black;
}
</style>