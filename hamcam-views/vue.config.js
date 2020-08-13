const fs = require("fs");

let https_setting;
switch (process.env.HAMCAM_PRODUCTION) {
  case "0": // Staging
  case "1": // Production
    https_setting = false;
    break;
  default:
    // Development
    https_setting = {
      key: fs.readFileSync("../dev-env/cert/key.pem"),
      cert: fs.readFileSync("../dev-env/cert/cert.pem"),
    };
}

module.exports = {
  publicPath: "/hamcam/views/",
  devServer: {
    disableHostCheck: true,
    host: "0.0.0.0",
    https: https_setting,
  },
};
