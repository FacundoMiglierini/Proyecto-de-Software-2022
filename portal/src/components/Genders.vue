<template>
    <Pie v-if="loaded"
    :chart-options="chartOptions"
    :chart-data="chartData" />
    <div v-else class="spinner-border text-dark" role="status">
      <span class="visually-hidden">Cargando...</span>
    </div>
</template>
  
<script>
  import { Pie } from 'vue-chartjs'
  import { apiService } from '../api'
  import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, CategoryScale } from 'chart.js'
  
  ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale)
  
  export default {
    name: 'GendersChart',
    components: { Pie },
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
        await apiService.get('/api/club/stats/gender_all')
          .then(( { data } ) => {
            this.chartData = {
              labels: data.labels,
              datasets: [
                {
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
