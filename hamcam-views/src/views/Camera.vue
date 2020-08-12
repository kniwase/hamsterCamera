<template>
  <b-container fluid="sm">
    <b-row>
      <CameraWorker ref="camera" />
    </b-row>
  </b-container>
</template>


<script>
import { CameraWorker } from "../components";

export default {
  components: { CameraWorker },
  data() {
    return new Object();
      },
  mounted() {},
  beforeDestroy() {},
  computed: {},
  methods: {},
};
</script>
