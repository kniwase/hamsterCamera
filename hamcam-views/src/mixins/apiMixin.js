export default {
  apiUrl: ({ websocket = false } = {}) => {
    const subDirectory = "/hamcam/api";
    let protocol = "";
    if (websocket) {
      protocol = location.protocol === "https:" ? "wss:" : "ws:";
    } else {
      protocol = location.protocol;
    }
    let port;
    switch (process.env.VUE_APP_PRODUCTION) {
      case "1":
        // Production
        port = "";
        break;
      case "0":
        // Staging
        port = ":20334";
        break;
      default:
        // Development
        port = ":9080";
    }
    const url = protocol + location.hostname + port + subDirectory;
    return url;
  },
};
