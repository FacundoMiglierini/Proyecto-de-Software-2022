<template>
  <div class="container text-center my-5">
    <h1 class="mb-5 fw-bolder">Listado de mis pagos</h1>
    <div v-if="!this.getLoading">
      <div v-if="this.getUnpaid">
        <form method="POST" action @submit.prevent="uploadPayment" enctype="multipart/form-data">
            <div class="input-group mb-3">
                <input ref="file" type="file" class="form-control" required>
                <button class="btn btn-dark">Pagar</button>
            </div>
        </form>
      </div>

    </div>
    <div class="mb-3">
        <PaymentsTable :key="componentKey"/>
    </div>
    <div class="toast" ref="toast" role="alert" aria-live="assertive" aria-atomic="true" data-bs-delay="15000">
        <div class="toast-header">
          <img src="@/assets/logo.png" height="32" width="32" class="rounded me-2" alt="Logo del club">
          <strong class="me-auto">Pago realizado</strong>
          <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
          Se ha realizado el pago con éxito!
        </div>
      </div>
  </div>
</template>
  
<script>
import { ref, defineComponent } from 'vue';
import { storeToRefs } from 'pinia';
import { useAuthStore } from '../stores/auth';
import PaymentsTable from '../components/PaymentsTable.vue';
import { apiCall } from '../api';
import { usePaymentsStore } from '../stores/payments';
import { Toast } from 'bootstrap'

export default defineComponent({
  name: "PaymentsView",
  components: {
    PaymentsTable,
  },
  setup(){
    const file = ref(null)
    const componentKey = ref(0)
    const authStore = useAuthStore()
    const { getUser } = storeToRefs(authStore) 
    const paymentsStore = usePaymentsStore()
    const { getUnpaid, getLoading } = storeToRefs(paymentsStore)
    return { getUser, getUnpaid, getLoading, componentKey }
  },
  methods: {
    async uploadPayment(){
      
      let formData = new FormData();
      formData.append('file', this.$refs.file.files[0])
      formData.append('id', this.getUser['id'])

      const headers = {
        'Content-Type': 'multipart/form-data',
      }
      apiCall('/api/me/payments', this.updateKey, "POST", formData, headers)
    },
    updateKey(data){
      this.componentKey += 1;
      const toast = new Toast(this.$refs.toast)
      toast.show()
    }
  }
})
</script>
