import { createUser, getDashboard, addTransaction } from "./api.js";
import Chart from "chart.js/auto";

/* =========================
   LOGIN PAGE
========================= */
export function renderLogin(app, onLogin) {
  app.innerHTML = `
    <div class="login-container">
      <h1>Budget Nudge Agent</h1>

      <input id="name" placeholder="Full Name" />
      <input id="salary" type="number" placeholder="Monthly Salary" />
      <input id="expenses" type="number" placeholder="Required Expenses" />
      <input id="emi" type="number" placeholder="Total EMI" />

      <button id="loginBtn">Start Smart Budgeting</button>
    </div>
  `;

  document.getElementById("loginBtn").addEventListener("click", async () => {
    const userData = {
      name: document.getElementById("name").value,
      salary: Number(document.getElementById("salary").value),
      expenses: Number(document.getElementById("expenses").value),
      emi: Number(document.getElementById("emi").value)
    };

    if (!userData.name || !userData.salary) {
      alert("Please fill required fields");
      return;
    }

    const response = await createUser(userData);
    onLogin(response.user_id);
  });
}

/* =========================
   DASHBOARD PAGE
========================= */
export async function renderDashboard(app, userId) {

  const data = await getDashboard(userId);

  app.innerHTML = `
    <div class="dashboard-container">

      <!-- TOP METRICS -->
      <div class="card-grid">
        <div class="dashboard-card">
          <h3>Monthly Limit</h3>
          <p class="big-value">₹${data.monthly_limit}</p>
        </div>

        <div class="dashboard-card">
          <h3>Food Delivery Spend</h3>
          <p class="big-value">₹${data.food_spend}</p>
        </div>

        <div class="dashboard-card">
          <h3>Addiction Score</h3>
          <p class="big-value">${data.addiction_score} / 100</p>
        </div>
      </div>

      <!-- MAIN SECTION -->
      <div class="middle-section">

        <!-- ADD EXPENSE -->
        <div class="add-expense-card">
          <h2>+ Add Expense</h2>

          <input id="merchantInput" placeholder="Merchant Name" />
          <input id="amountInput" type="number" placeholder="Amount" />

          <select id="categoryInput">
            <option>Food Delivery</option>
            <option>Groceries</option>
            <option>Shopping</option>
            <option>Transport</option>
          </select>

          <button id="addBtn" class="primary-btn">
            Add Transaction
          </button>
        </div>

        <!-- RECENT TRANSACTIONS -->
        <div class="transactions-card">
          <div class="transactions-header">
            <h2>Recent Transactions</h2>
            <span class="entries-badge">
              ${data.transactions.length} entries
            </span>
          </div>

          <div>
            ${
              data.transactions.length === 0
                ? "<p>No transactions found</p>"
                : data.transactions.map(tx => `
                  <div class="transaction-row">
                    <div>
                      <strong>${tx.merchant}</strong>
                      <div class="category">${tx.category}</div>
                    </div>
                    <div>₹${tx.amount}</div>
                  </div>
                `).join("")
            }
          </div>
        </div>

      </div>

      <!-- CHARTS SECTION -->
      <div class="charts-section">
        <div class="chart-card">
          <h3>Spending by Category</h3>
          <canvas id="categoryChart"></canvas>
        </div>

        <div class="chart-card">
          <h3>Cumulative Spending Trend</h3>
          <canvas id="trendChart"></canvas>
        </div>
      </div>

    </div>
  `;

  /* =========================
     ADD TRANSACTION
  ========================= */
  document.getElementById("addBtn").addEventListener("click", async () => {

    const merchant = document.getElementById("merchantInput").value;
    const amount = document.getElementById("amountInput").value;
    const category = document.getElementById("categoryInput").value;

    if (!merchant || !amount) {
      alert("Fill all fields");
      return;
    }

    await addTransaction(userId, {
      merchant,
      amount: Number(amount),
      category
    });

    renderDashboard(app, userId);
  });

  /* =========================
     CHART LOGIC
  ========================= */

  const transactions = data.transactions;

  if (transactions.length === 0) return;

  // Category aggregation
  const categoryTotals = {};
  transactions.forEach(tx => {
    if (!categoryTotals[tx.category]) {
      categoryTotals[tx.category] = 0;
    }
    categoryTotals[tx.category] += tx.amount;
  });

  const categoryLabels = Object.keys(categoryTotals);
  const categoryValues = Object.values(categoryTotals);

  // Cumulative trend
  let cumulative = 0;
  const trendValues = [];
  transactions.forEach(tx => {
    cumulative += tx.amount;
    trendValues.push(cumulative);
  });

  const trendLabels = transactions.map((_, i) => `Tx ${i + 1}`);

  // Doughnut chart
  new Chart(document.getElementById("categoryChart"), {
    type: "doughnut",
    data: {
      labels: categoryLabels,
      datasets: [{
        data: categoryValues,
        backgroundColor: [
          "#3b82f6",
          "#22c55e",
          "#f97316",
          "#6366f1",
          "#ef4444"
        ]
      }]
    },
    options: {
      plugins: {
        legend: { position: "bottom" }
      }
    }
  });

  // Line chart
  new Chart(document.getElementById("trendChart"), {
    type: "line",
    data: {
      labels: trendLabels,
      datasets: [{
        label: "Cumulative Spend",
        data: trendValues,
        borderColor: "#3b82f6",
        backgroundColor: "rgba(59,130,246,0.2)",
        fill: true,
        tension: 0.3
      }]
    },
    options: {
      scales: {
        y: { beginAtZero: true }
      }
    }
  });

}