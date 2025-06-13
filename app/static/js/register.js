document
  .getElementById("register-form")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm-password").value;

    if (password !== confirmPassword) {
      alert("As senhas não coincidem.");
      return;
    }

    const response = await fetch("/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password }),
    });

    if (response.ok) {
      alert("Cadastro realizado com sucesso!");
      window.location.href = "/entrar";
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

      if ([409, 500].includes(response.status)) {
        alert(body.message);
        return;
      }

      throw new Error("Unexpected response status: " + response.status);
    } catch (error) {
      console.error("Erro ao processar a resposta:", error);
      alert(
        "Ocorreu um erro inesperado. Por favor, tente novamente mais tarde."
      );
    }
  });
