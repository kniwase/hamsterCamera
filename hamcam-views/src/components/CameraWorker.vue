<template>
  <div>
    <div v-show="false">
      <video ref="video" :width="width" :height="height" autoplay muted playsinline></video>
      <canvas ref="canvas" :width="width" :height="height" />
    </div>
    <button v-on:click="onClickTakePhoto()">撮影</button>
    <button v-on:click="onClickDeletePhoto()">削除</button>
    <br />
    <img v-if="photo" v-bind:src="photo" width="250" />
  </div>
</template>

<script>
export default {
  name: "CameraWorker",
  props: {
    width: {
      type: String,
      require: false,
      default: () => "1280",
    },
    height: {
      type: String,
      require: false,
      default: () => "720",
    },
  },
  data() {
    return {
      facingMode:
        process.env.VUE_APP_PRODUCTION === "1"
          ? { exact: "environment" }
          : "user",
      video: {},
      canvas: {},
      photo: null,
    };
  },
  mounted() {
    this.video = this.$refs.video;
    navigator.mediaDevices
      .getUserMedia({
        video: {
          width: this.width,
          height: this.height,
          facingMode: this.facingMode,
        },
      })
      .then((stream) => {
        this.video.srcObject = stream;
        this.video.play();
      });
  },
  methods: {
    getPhoto() {
      this.canvas = this.$refs.canvas;
      this.canvas
        .getContext("2d")
        .drawImage(this.video, 0, 0, this.width, this.height);
      return {
        photo: this.canvas.toDataURL("image/jpeg"),
        datetime: new Date().toISOString(),
      };
    },
    onClickTakePhoto() {
      this.photo = this.getPhoto().photo;
    },
    onClickDeletePhoto() {
      this.photo = null;
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
