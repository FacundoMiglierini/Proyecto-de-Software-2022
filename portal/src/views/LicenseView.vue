<template>
  <div v-if="hasCarnet()" class="container-fluid text-center my-5">
      <h1 class="mb-5 fw-bolder">Carnet digital</h1>
      <Carnet />
      <div class="mb-5"></div>
  </div>
  <div v-else>
    <div class="container-fluid text-center my-5">
      <h1 class="fw-bolder">No posee Carnet digital</h1>
      <h4 class="fw-bolder" style="color:white;">Solicite uno en la sede del Club.</h4>
    </div>
  </div>
</template>

<script lang="ts">
import Carnet from '../components/Carnet.vue'
export default {
  name: 'CarnetView',
  components: {
    Carnet
  },
  setup() {
    const data = JSON.parse(sessionStorage.user)

    function hasCarnet() {
      return data.image
    }

    return {
      data,
      hasCarnet
    }
  }
}
</script>