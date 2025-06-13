document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const response = await fetch("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  if (response.ok) {
    window.location.href = "/entrar";
    return;
  }

  // Handle errors
  e.target.reset();
  const body = await response.json();

  if (response.status === 400) {
    const errorList = Object.values(body.errors).flat();

    for (const error of errorList) {
      alert(error);
    }

    return;
  }

  // For 401 Unauthorized, 409 Conflict, 500 Internal Server Error

  alert(body.message);
});
