<template>
  <div class="container text-center my-5">
    <div class="card">
      <ul class="nav nav-tabs mx-auto">
        <li class="nav-item">
          <a :class="value==1?'active':''" class="nav-link" aria-current="page" @click="setOne">Géneros</a>
        </li>
        <li class="nav-item">
          <a :class="value==2?'active':''" class="nav-link" @click="setTwo">Deportistas por disiplina</a>
        </li>
        <li class="nav-item">
          <a :class="value==3?'active':''" class="nav-link" @click="setThree">Altas de socios en los ultimos 24 meses</a>
        </li>
      </ul>
      <div v-show="value === 1" style="margin:0px auto">
        <GendersChart />
      </div>
      <div v-show="value === 2">
        <AthletesChart style= "height: 600px; width: 900x; padding: 4px;"/>
      </div>
      <div v-show="value === 3">
        <AssociatedChart style="height: 600px; width: 900x; padding: 4px;"/>
      </div>
    </div>
  </div>
</template>

<script>
import GendersChart from '../components/Genders.vue'
import AthletesChart from '../components/Athletes.vue'
import AssociatedChart from '../components/Associated.vue'

export default {
  name: 'Charts',
  components: { GendersChart, AthletesChart, AssociatedChart },
  data() {
    return {
      value: 1
    }
  }, 
  methods: {
    setOne() {
      this.value = 1
    },
    setTwo(){
      this.value = 2
    },
    setThree() {
      this.value = 3
    }
  }
}
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
