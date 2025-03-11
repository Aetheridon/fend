const express = require("express");

const app = express();
const PORT = 8000;

app.get("/api", (req, res) => {
    res.end("Hello, World 2!");
});

app.listen(PORT, () => {
    console.log(`listening on port: ${PORT}`);
});

