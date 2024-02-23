<template>
<div class="container text-center my-5">
    <div class="row row-cols-lg-3 mx-2 gap-3 gap-lg-0">
    <div class="card mx-auto px-0">
        <div class="card-header fs-5">Géneros</div>
        <div class="card-body">
            <GendersChart />
        </div>
    </div>
    <div class="card mx-auto px-0">
        <div class="card-header fs-5">Deportistas</div>
        <div class="card-body">
            <AthletesChart />
        </div>
    </div>
    <div class="card mx-auto px-0">
        <div class="card-header fs-5">Altas de socios</div>
        <div class="card-body">
            <AssociatedChart />
        </div>
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
  components: { GendersChart, AthletesChart, AssociatedChart }
}
</script>
