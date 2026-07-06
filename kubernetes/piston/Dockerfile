FROM ghcr.io/engineer-man/piston:latest

# We use Node to send HTTP POST requests
RUN echo 'const http = require("http"); \n\
const install = (lang, ver) => new Promise((resolve) => { \n\
  const req = http.request("http://localhost:2000/api/v2/packages", { \n\
    method: "POST", \n\
    headers: { "Content-Type": "application/json" } \n\
  }, (res) => { \n\
    let data = ""; \n\
    res.on("data", chunk => data += chunk); \n\
    res.on("end", () => { console.log(data); resolve(); }); \n\
  }); \n\
  req.write(JSON.stringify({ language: lang, version: ver })); \n\
  req.end(); \n\
}); \n\
async function run() { \n\
  await new Promise(r => setTimeout(r, 5000)); \n\
  console.log("Installing Python 3.12.0..."); \n\
  await install("python", "3.12.0"); \n\
  console.log("Installing Node 20.11.1..."); \n\
  await install("node", "20.11.1"); \n\
} \n\
run();' > /tmp/install.js

# Give piston user ownership of /piston
RUN mkdir -p /piston && chown -R piston:piston /piston

USER piston
CMD ["node", "/piston_api/src/index.js"]
RUN node /piston_api/src/index.js & \
    PID=$! && \
    node /tmp/install.js && \
    echo "Stopping Piston API..." && \
    kill $PID && \
    wait $PID || true

USER root
