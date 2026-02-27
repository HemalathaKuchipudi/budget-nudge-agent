const BASE = "http://127.0.0.1:5000";

export async function createUser(data) {
  const res = await fetch(`${BASE}/create-user`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(data)
  });

  return res.json();
}

export async function addTransaction(userId, transaction) {
  await fetch(`${BASE}/add-transaction/${userId}`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(transaction)
  });
}

export async function getDashboard(userId) {
  const res = await fetch(`${BASE}/dashboard/${userId}`);
  return res.json();
}