<template>
  <b-container fluid="sm">
    <b-row v-show="false">
      <video ref="video" id="video" :width="width" :height="height" autoplay muted playsinline></video>
      <canvas ref="canvas" id="canvas" :width="width" :height="height" />
    </b-row>
    <b-row>
      <button color="info" v-on:click="onClickTakePhoto()">撮影</button>
      <button color="info" v-on:click="onClickDeletePhoto()">削除</button>
    </b-row>
    <b-row>
      <b-img class="m1" fluid v-if="photo" v-bind:src="photo" width="250" />
    </b-row>
  </b-container>
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
      facingMode: !process.env.HAMCAM_PRODUCTION
        ? "user"
        : { exact: "environment" },
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
      return this.canvas.toDataURL("image/jpeg");
    },
    onClickTakePhoto() {
      this.photo = this.getPhoto();
    },
    onClickDeletePhoto() {
      this.photo = null;
    },
  },
};
</script>
