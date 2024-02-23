<template>
    <div class="container text-center my-5">
    <h1 class="mb-5 fw-bolder">Disciplinas</h1>
    <!-- The table component -->
    <AllDisciplinesTable />
    <div class="mb-5"></div>
</div>
</template>

<script lang="ts">
// Importing the table component
import AllDisciplinesTable from '../components/AllDisciplinesTable.vue'
export default {
  name: 'AllDisciplinesView',
  components: {
    AllDisciplinesTable
  },
}
</script>