<template>
  <div>
    <button v-on:click="onClickTakePhoto()">撮影</button>
    <button v-on:click="onClickDeletePhoto()">削除</button>
    <div v-if="photo">
      <br />
      <img v-bind:src="photo" width="250" />
    </div>
  </div>
</template>

<script>
export default {
  name: "CameraWorker",
  props: {
    width: {
      type: String,
      require: false,
      default: () => "1280"
    },
    height: {
      type: String,
      require: false,
      default: () => "720"
    }
  },
  data() {
    return {
      video: {},
      canvas: {},
      getUserMediaArgs: {
        audio: false,
        video: {
          width: this.width,
          height: this.height,
          facingMode:
            process.env.VUE_APP_PRODUCTION === "1" ? "environment" : "user"
        }
      },
      photo: null
    };
  },
  mounted() {
    this.canvas = document.createElement("canvas");
    this.canvas.setAttribute("width", this.width);
    this.canvas.setAttribute("height", this.height);

    this.video = document.createElement("video");
    this.video.setAttribute("width", this.width);
    this.video.setAttribute("height", this.height);
    this.video.setAttribute("playsinline", true);
    navigator.mediaDevices.getUserMedia(this.getUserMediaArgs).then(stream => {
      this.video.srcObject = stream;
    });
  },
  methods: {
    getPhoto() {
      this.video.play();
      this.canvas
        .getContext("2d")
        .drawImage(this.video, 0, 0, this.width, this.height);
      return {
        photo: this.canvas.toDataURL("image/jpeg"),
        datetime: new Date().toISOString()
      };
    },
    onClickTakePhoto() {
      this.photo = this.getPhoto().photo;
    },
    onClickDeletePhoto() {
      this.photo = null;
    }
  }
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
