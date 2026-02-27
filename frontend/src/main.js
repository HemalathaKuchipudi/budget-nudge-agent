

import "./style.css";
import { renderLogin, renderDashboard } from "./ui.js";

const app = document.getElementById("app");

renderLogin(app, (userId) => {
  renderDashboard(app, userId);
});