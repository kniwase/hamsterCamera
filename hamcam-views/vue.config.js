module.exports = { publicPath: "/hamcam/" };

if (
  process.env.VUE_APP_PRODUCTION !== "1" &&
  process.env.VUE_APP_PRODUCTION !== "0"
) {
  const fs = require("fs");
  module.exports["devServer"] = {
    disableHostCheck: true,
    host: "0.0.0.0",
    https: {
      key: fs.readFileSync("../dev-env/cert/key.pem"),
      cert: fs.readFileSync("../dev-env/cert/cert.pem"),
    },
  };
}
