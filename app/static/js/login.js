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
    window.location.href = "/inicio";
    return;
  }

  e.target.reset();

  try {
    const body = await response.json();

    if (response.status === 400) {
      const errorList = Object.values(body.errors).flat();
      for (const error of errorList) {
        alert(error);
      }
      return;
    }

    if ([401, 409, 500].includes(response.status)) {
      alert(body.message);
      return;
    }

    throw new Error("Unexpected response status: " + response.status);
  } catch (error) {
    console.error("Erro ao processar a resposta:", error);
    alert("Ocorreu um erro inesperado. Por favor, tente novamente mais tarde.");
  }
});
