<template>
  <div class="w-100 mt-auto">
    <!-- Footer -->
    <footer class="text-center text-lg-start bg-dark text-muted">
      <!-- Section: Links  -->
      <section class="pt-1">
        <div class="container text-center text-md-start mt-5">
          <!-- Grid row -->
            <!-- Grid column -->
            <div class="col-md-6 col-lg-4 col-xl-4 mx-auto mb-md-0 mb-4">
              <!-- Links -->
              <h6 class="text-uppercase fw-bold mb-4">CONTACTO</h6>
              <p><i class="bi bi-house-fill me-3 text-secondary"></i> {{getAddress}}</p>
              <p class="fs-7">
                <i class="bi bi-envelope-fill me-3 text-secondary"></i>
                {{getEmail}}
              </p>
              <p><i class="bi bi-telephone-fill me-3 text-secondary"></i> {{getPhone}}</p>
            </div>
            <!-- Grid column -->
        </div>
        <!-- Grid row -->
      </section>
      <!-- Section: Links  -->

      <!-- Copyright -->
      <div class="text-center p-4" style="background-color: rgba(0, 0, 0, 0.025);">
        Proyecto de software:
        <a class="text-reset fw-bold" href="https://gitlab.catedras.linti.unlp.edu.ar/proyecto2022/Proyectos/grupo19" target="_blank">Grupo 19</a>
      </div>
      <!-- Copyright -->
    </footer>
    <!-- Footer -->
  </div>
</template>

<script>
  import { storeToRefs } from "pinia";
  import { defineComponent } from "vue";
  import { useContactStore } from "../stores/contact";

  export default defineComponent({
    name: "FooterLanding",
    setup(){
      const contactStore = useContactStore()
      const { getEmail } = storeToRefs(contactStore);
      const { getPhone } = storeToRefs(contactStore);
      const { getAddress } = storeToRefs(contactStore);
      return { contactStore, getEmail, getPhone, getAddress };
    },
    beforeMount(){
      this.contactStore.fetchInfo();
    },
  })
</script>

<style>
p{
  word-break: break-all;
}
</style>