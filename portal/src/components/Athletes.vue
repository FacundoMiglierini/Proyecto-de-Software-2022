<template>
    <Bar v-if="loaded"
    :chart-options="chartOptions"
    :chart-data="chartData" />
    <div v-else class="spinner-border text-dark" role="status">
      <span class="visually-hidden">Cargando...</span>
    </div>
</template>
  
<script>
  import { Bar } from 'vue-chartjs'
  import { apiService } from '../api'
  
  export default {
    name: 'AthletesChart',
    components: { Bar },
    data: () => ({
      loaded: false,
      chartData: null,
      chartOptions: {
        responsive: true,
        mantainAspectRatio: false
      }
    }),
    async mounted () {
      this.loaded = false
      try {
            await apiService.get('/api/club/stats/deportistas')
            .then(( { data } ) => {
              this.chartData = {
              labels: data.labels,
              datasets: [
                {
                  label:'Deportistas por disciplina',
                  backgroundColor: ['#41B883', '#E46651', '#00D8FF'],
                  data: data.data
                }
              ]
              }
            this.loaded = true
          })
      } catch (e) {
        console.error(e)
      }
    }
  }
</script>
