<template>
  <div class="card mb-3 mx-auto" style="max-width: 540px;"> 
    <h5 class="card-header fw-semibold mb-4 text-center">Club Deportivo de Villa Elisa</h5>
    <div class="row g-0 px-4">
      <div class="col-md-5 mx-auto d-flex align-items-center">
          <div class="container">
            <div class="row row-cols-2">
                <div class="col-12 pb-4 text-center">
                  <img :src="image" class="img-fluida" alt="Imagen de perfil">
                </div>
                <div class="col-12 text-center">
                    <span class="fw-semibold">Estado: {{estado}}</span>
                </div>
            </div>
          </div>
      </div>
      <div class="col-md-6 d-flex flex-column">
        <div class="card-body ms-md-auto text-md-start text-center">
            <h5 class="card-title">Socio: {{data.nombre}} {{data.apellido}}</h5> 
            <p class="card-text">{{data.tipo_identificacion}}: {{ data.identificacion }}</p>
            <p class="card-text">Nro socio: #{{ data.id }}</p>
            <p class="card-text">Fecha alta: {{ data.fecha_alta }}</p>
            <qrcode-vue class="qr" :value="value" :size="100" level="H" />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import QrcodeVue from 'qrcode.vue'

export default defineComponent({
  name: 'Carnet',
  components: {
    QrcodeVue,
  },
  setup() {
    const data = JSON.parse(sessionStorage.user)
    const image = `data:image/png;base64,${data.image.data}`;
    const estado = data.estado_act_block ? 'Activo' : 'Bloqueado';
    const value = `https://admin-grupo19.proyecto2022.linti.unlp.edu.ar/socio/${data.id}/carnet`;

    return {
      data,
      image,
      estado,
      value
    }
  },
});

</script>

<style>
.img-fluida {
  max-width: 100%;
  height: auto;
  clip-path: circle();
}
.qr {
  max-width: 100%;
  height: auto;
}
</style>