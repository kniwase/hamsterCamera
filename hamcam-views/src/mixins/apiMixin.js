export default {
  apiUrl: ({ websocket = false } = {}) => {
    const subDirectory = "/hamcam/api";
    let protocol = "";
    if (websocket) {
      protocol = location.protocol === "https:" ? "wss:" : "ws:";
    } else {
      protocol = location.protocol;
    }
    let port = "";
    switch (process.env.HAMCAM_PRODUCTION) {
      case "0": // Staging
      case "1": // Production
        break;
      default:
        // Development
        port = ":9080";
    }
    const url = protocol + location.hostname + port + subDirectory;
    return url;
  },
};
