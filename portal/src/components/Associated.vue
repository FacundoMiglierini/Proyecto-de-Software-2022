<template>
    <Line v-if="loaded"
    :chart-options="chartOptions"
    :chart-data="chartData" />
    <div v-else class="spinner-border text-dark" role="status">
      <span class="visually-hidden">Cargando...</span>
    </div>
</template>
  
<script>
  import { Line } from 'vue-chartjs'
  import { apiService } from '../api'
  import Chart from 'chart.js/auto'
  
  export default {
    name: 'AssociatedChart',
    components: { Line },
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
            await apiService.get('/api/club/stats/socios')
            .then(( { data } ) => {
              this.chartData = {
                labels: data.labels,
                datasets: [
                  {
                    label : 'Socios inscriptos',
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
