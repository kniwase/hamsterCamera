<template>
  <div>
    <div>
      <video
        ref="video"
        id="video"
        :width="imageSize.width"
        :height="imageSize.height"
        autoplay
        muted
        playsinline
      ></video>
      <div>
        <button color="info" id="snap" v-on:click="capture()">Snap Photo</button>
  </div>
      <canvas
        v-show="false"
        ref="canvas"
        id="canvas"
        :width="imageSize.width"
        :height="imageSize.height"
      ></canvas>
      <ul>
        <li class="capture" v-for="c in captures" v-bind:key="c.d">
          <img v-bind:src="c" height="50" />
        </li>
      </ul>
    </div>
  </div>
</template>


<script>
export default {
  data() {
    return {
      imageSize: {
        width: 640,
        height: 480,
      },
      facingMode: !process.env.HAMCAM_PRODUCTION
        ? "user"
        : { exact: "environment" },
      video: {},
      canvas: {},
      captures: [],
    };
  },
  mounted() {
    this.video = this.$refs.video;
    navigator.mediaDevices
      .getUserMedia({
        video: {
          width: this.imageSize.width,
          height: this.imageSize.height,
          facingMode: this.facingMode,
        },
      })
      .then((stream) => {
        this.video.srcObject = stream;
        this.video.play();
      });
  },
  computed: {},
  methods: {
    capture() {
      this.canvas = this.$refs.canvas;
      this.canvas
        .getContext("2d")
        .drawImage(
          this.video,
          0,
          0,
          this.imageSize.height,
          this.imageSize.width
        );
      this.captures.push(this.canvas.toDataURL("image/png"));
      console.log(this.captures);
    },
  },
};
</script>
