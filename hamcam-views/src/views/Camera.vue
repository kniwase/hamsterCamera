<template>
  <b-container fluid="sm">
    <b-row>
      <RpcWorker ref="rpc" />
    </b-row>
  </b-container>
</template>


<script>
import { RpcWorker } from "../components";

export default {
  components: { RpcWorker },
  data() {
    return new Object();
      },
  mounted() {},
  beforeDestroy() {},
  computed: {},
  methods: {},
};
</script>
