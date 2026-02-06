const screens = document.querySelectorAll(".screen");

const setActiveScreen = (target) => {
  screens.forEach((screen) => {
    const isActive = screen.dataset.screen === target;
    screen.classList.toggle("active", isActive);
  });
};

document.addEventListener("click", (event) => {
  const action = event.target.closest("[data-action]")?.dataset.action;
  if (!action) {
    return;
  }

  if (action === "enter-home") {
    setActiveScreen("home");
  }

  if (action === "back-setup") {
    setActiveScreen("setup");
  }
});
