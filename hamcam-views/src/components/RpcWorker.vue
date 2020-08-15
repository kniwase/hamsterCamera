<template>
  <b-container fluid="sm">
    <b-row>接続先: {{wsUrl}}</b-row>
    <b-row>状態: {{wsState}}</b-row>
    <b-row>
      <button color="info" v-on:click="getConnection()">接続</button>
      <button color="info" v-on:click="closeConnection()">切断</button>
    </b-row>
    <CameraWorker ref="camera" />
  </b-container>
</template>

<script>
import { CameraWorker } from "./";
import { ApiMixin } from "../mixins";
import ReconnectingWebSocket from "reconnecting-websocket";
const JsonRPC = require("simple-jsonrpc-js");
import { useBattery } from "vue-use-web";

export default {
  name: "RpcWorker",
  components: { CameraWorker },
  data() {
    return {
      ws: { readyState: null },
      wsUrl: ApiMixin.apiUrl({ websocket: true }) + "/camera/ws",
      wsState: "未接続",
      jrpc: {},
    };
  },
  mounted() {
    this.getConnection();
  },
  beforeDestroy() {
    this.closeConnection();
  },
  computed: {},
  methods: {
    getConnection: function () {
      if (this.ws && this.ws.readyState == null) {
        this.ws = new ReconnectingWebSocket(this.wsUrl);
        this.ws.onopen = () => {
          this.jrpc = new JsonRPC();
          this.jrpc.toStream = (msg) => {
            this.ws.send(msg);
          };
          this.ws.onmessage = (event) => {
            this.jrpc.messageHandler(event.data);
          };
          this.jrpc.on("getPhoto", [], this.getPhoto);
          this.jrpc.on("getBatteryStatus", [], this.getBatteryStatus);
        };
      }
    },
    closeConnection: function () {
      if (this.ws && this.ws.readyState != null) {
        this.ws.close();
      }
      this.ws = { readyState: null };
      this.jrpc = {};
    },
    getPhoto: function () {
      const photo = this.$refs.camera.getPhoto();
      console.log(photo);
      return photo;
    },
    getBatteryStatus: function () {
      const { isCharging, chargingTime, dischargingTime, level } = useBattery();
      const batteryStatus = {
        isCharging: isCharging.value,
        chargingTime: chargingTime.value,
        dischargingTime: dischargingTime.value,
        level: level.value,
      };
      console.log(batteryStatus);
      return batteryStatus;
    },
  },
  watch: {
    ws: {
      deep: true,
      handler: function () {
        switch (this.ws.readyState) {
          case 0:
            this.wsState = "接続中";
            break;
          case 1:
            this.wsState = "接続済み";
            break;
          case 2:
            this.wsState = "切断中";
            break;
          case 3:
            this.wsState = "切断済み";
            break;
          default:
            this.wsState = "未接続";
        }
      },
    },
  },
};
</script>

<style>
@media (prefers-color-scheme: dark) {
  body {
    background-color: #000;
    color: #aaa;
  }
}
</style>
