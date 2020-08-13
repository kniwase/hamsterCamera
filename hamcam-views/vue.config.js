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
      key: fs.readFileSync("../dev-env/cert/pem/key.pem"),
      cert: fs.readFileSync("../dev-env/cert/pem/cert.pem"),
    };
}

module.exports = {
  publicPath: "/hamcam/",
  devServer: {
    disableHostCheck: true,
    host: "0.0.0.0",
    https: https_setting,
  },
};
