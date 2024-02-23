<template>
    <div v-if="!loading">
      <EasyDataTable
          theme-color="#b5a369"
          buttons-pagination
          :rows-per-page-message="msg"
          :rows-of-page-separator-message="msg2"
          :rows-items="rows" 
          :table-min-height="tableHeight"
          :headers="headers"
          :items="items"
          :sort-by="sortBy"
          :sort-type="sortType"
          :empty-message="empty"
          alternating
      >
          <template #expand="item">
          <div style="padding: 15px; text-align: left;">
              <p style="font-weight: bolder">Instructores: </p>
              <p v-for="profesor in item.instructores"> - {{profesor.nombre_instructor}} {{profesor.apellido_instructor}}</p>
          </div>
          </template> 
      </EasyDataTable>
    </div>
    <div v-else class="spinner-border text-light" role="status">
      <span class="visually-hidden">Cargando...</span>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { Header, Item } from "vue3-easy-data-table";
import { apiCall } from "../api";

export default defineComponent({
  name: 'TablaTodasDisciplinas',
  setup() {
    const headers: Header[] = [
      { text: "Nombre", value: "nombre_disciplina" },
      { text: "Horarios", value: "detalle" },
      { text: "Costo", value: "costo" },
    ];
    let items: Item[] = []
    const loading = ref(true)
    const sortBy = "nombre_disciplina";
    const sortType = "asc";
    const msg = "Elementos por página";
    const msg2 = "de"
    const rows = [10, 25, 50]
    const tableHeight = 400
    const empty = "No existen disciplinas cargadas en el sistema."
    
    return {
      headers,
      items,
      loading,
      sortBy,
      sortType,
      msg,
      msg2,
      rows,
      empty,
      tableHeight,
    };
  },
  beforeMount() {
    apiCall('api/club/disciplinas', this.setData, "GET")
  },
  methods: {
    setData(data){
      this.items = data
      this.loading = false
    }
  }
});

</script>