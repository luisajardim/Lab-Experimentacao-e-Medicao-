"use strict";

const { createApp } = require("./app");

const port = Number(process.env.PORT || 3000);
createApp().listen(port, () => console.log(`lab05 express-api em http://localhost:${port}`));
