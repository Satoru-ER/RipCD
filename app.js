const byId = (id) => document.getElementById(id);

async function postAction(action, payload = {}) {
  const response = await fetch(`/api/${action}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const data = await response.json();
  renderStatus(data);
}

function renderStatus(data) {
  byId("track").textContent = `Track: ${data.track}`;
  byId("state").textContent = `State: ${data.state}`;
  byId("meta").textContent = `${Math.max(0, data.index + 1)} / ${data.total} (${data.source})`;
  byId("message").textContent = data.message || "";
}

async function refreshStatus() {
  const response = await fetch("/api/status");
  renderStatus(await response.json());
}

document.addEventListener("click", (event) => {
  const action = event.target.closest("[data-api]")?.dataset.api;
  if (!action) {
    return;
  }

  if (action === "load-folder") {
    postAction(action, { path: byId("folderPath").value });
    return;
  }

  if (action === "load-cd") {
    postAction(action, { path: byId("cdPath").value });
    return;
  }

  postAction(action);
});

refreshStatus();
setInterval(refreshStatus, 4000);
