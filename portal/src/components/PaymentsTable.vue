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
              <p style="font-weight: bolder">Costos: </p>
              <li>Base: ${{item.detalle.base}}</li>
              <li>Recargo: ${{item.detalle.recargo}}</li>
              <div v-if="item.detalle.disciplinas.length === 0">
                <li>Disciplinas: </li>
                <div v-for="value, key in item.detalle.disciplinas">
                  <p>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp- {{key}}: ${{value}}</p>
                </div>
              </div>
              <div v-else>
                <li>Disciplinas: $0</li>
              </div>
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
import { useAuthStore } from "../stores/auth";
import { usePaymentsStore } from "../stores/payments";
import { apiCall } from "../api";

export default defineComponent({
  name: 'TablaPagos',
  setup() {
    const headers: Header[] = [
      { text: "Número", value: "id" },
      { text: "Mes", value: "created_at" },
      { text: "Monto", value: "monto" },
      { text: "Estado", value: "estado" },
    ];
    let items: Item[] = []
    
    const authStore = useAuthStore()
    const paymentsStore = usePaymentsStore()
    const loading = ref(true)
    const sortBy = "id";
    const sortType = "asc";
    const msg = "Elementos por página";
    const msg2 = "de"
    const rows = [10, 25, 50]
    const tableHeight = 400
    const empty = "No dispone de pagos"
    
    return {
      headers,
      items,
      loading,
      sortBy,
      sortType,
      msg,
      msg2,
      rows,
      tableHeight,
      empty,
      authStore,
      paymentsStore,
    };
  },
  beforeMount() {
    apiCall('/api/me/payments/' + this.authStore.getUser['id'], this.setData, "GET")
  },
  methods: {
    setData(data){
      this.items = data
      let unpaid = this.items.some(payment => {
        return payment.estado == "Impaga"
        })
      this.paymentsStore.assignUnpaid(unpaid)
      this.loading = false
    }
  }
});

</script>