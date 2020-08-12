<template>
  <b-container fluid="sm">
    <b-row>接続先: {{wsUrl}}</b-row>
    <b-row>状態: {{wsState}}</b-row>
    <b-row>
      <button color="info" v-on:click="getConnection()">接続</button>
      <button color="info" v-on:click="closeConnection()">切断</button>
    </b-row>
    <button color="info" v-on:click="getBatteryStatus()">バッテリー</button>

    <b-row>
      <CameraWorker ref="camera" />
    </b-row>
  </b-container>
</template>

<script>
import { CameraWorker } from "./";
import { ApiMixin } from "../mixins";
import ReconnectingWebSocket from "reconnecting-websocket";
const msgpack = require("msgpack-lite");
import { useBattery } from "vue-use-web";

export default {
  name: "RpcWorker",
  components: { CameraWorker },
  data() {
    return {
      ws: { readyState: null },
      wsUrl: ApiMixin.apiUrl({ websocket: true }) + "/camera/ws",
      wsState: "未接続",
      rpcMethods: {
        getPhoto: this.getPhoto,
        getBatteryStatus: this.getBatteryStatus,
      },
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
          this.ws.onmessage = this.recieveRequest;
        };
      }
    },
    closeConnection: function () {
      if (this.ws && this.ws.readyState != null) {
        this.ws.close();
      }
      this.ws = { readyState: null };
    },
    sendResponse: function (res) {
      this.ws.send(msgpack.encode(res));
    },
    recieveRequest: function (event) {
      this.convMspackObj(event.data)
        .then((req) => {
          const ret_data = this.executeReqestedTask(req);
          this.sendResponse(ret_data);
        })
        .catch(() => {
          const ret_data = {
            id: null,
            error: { code: -32700, message: "Parse error" },
          };
          this.sendResponse(ret_data);
        });
    },
    convMspackObj: function (mspackBlob) {
      const fr = new FileReader();
      fr.readAsArrayBuffer(mspackBlob);
      return new Promise((resolve, reject) => {
        fr.onload = () => {
          resolve(msgpack.decode(new Uint8Array(fr.result)));
        };
        fr.onerror = () => {
          reject(fr.error);
        };
      });
    },
    executeReqestedTask: function (req) {
      if (req.method in this.rpcMethods) {
        try {
          let result;
          if (req.params != null) {
            result = this.rpcMethods[req.method](req.params);
          } else {
            result = this.rpcMethods[req.method]();
          }
          return {
            id: req.id,
            result: result,
          };
        } catch (err) {
          const detail = {
            name: err.name,
            message: err.message,
            stack: err.stack ? err.stack : null,
          };
          console.error(detail);
          return {
            id: req.id,
            error: { code: -32603, message: "Internal error", detail: detail },
          };
        }
      } else {
        return {
          id: req.id,
          error: {
            code: -32601,
            message: "Method not found",
          },
        };
      }
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
