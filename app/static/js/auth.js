import {
  addCustomValidity,
  displayBadRequestErrors,
  setSubmitting,
} from "./request-utils";

document
  .getElementById("register-form")
  ?.addEventListener("submit", async (e) => {
    if (!e.target.checkValidity()) {
      return;
    }

    e.preventDefault();
    const unsetSubmitting = setSubmitting(e, "Criando conta...");

    try {
      const name = document.getElementById("name").value;
      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;
      const passwordConfirmation =
        document.getElementById("confirm-password").value;

      if (password !== passwordConfirmation) {
        addCustomValidity(
          "confirm-password",
          "As senhas não coincidem. Por favor, verifique."
        );
        return;
      }

      const response = await fetch("/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
      });

      if (response.ok) {
        alert("Cadastro realizado com sucesso!");
        window.location.replace("/inicio");
        return;
      }

      const body = await response.json();

      if (response.status === 400) {
        displayBadRequestErrors(body.errors);
        return;
      }

      if (response.status === 409) {
        addCustomValidity("email", body.message);
        return;
      }

      if (response.status === 500) {
        alert(body.message);
        return;
      }

      throw new Error("Unexpected response status: " + response.status);
    } catch (error) {
      console.error("Erro ao processar a resposta:", error);
      alert(
        "Ocorreu um erro inesperado. Por favor, tente novamente mais tarde."
      );
    } finally {
      unsetSubmitting();
    }
  });

document.getElementById("login-form")?.addEventListener("submit", async (e) => {
  if (!e.target.checkValidity()) {
    return;
  }

  e.preventDefault();
  const unsetSubmitting = setSubmitting(e, "Entrando...");

  try {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (response.ok) {
      window.location.replace("/inicio");
      return;
    }

    const body = await response.json();

    if (response.status === 400) {
      displayBadRequestErrors(body.errors);
      return;
    }

    if (response.status === 401) {
      addCustomValidity("password", body.message);
      return;
    }

    if (response.status === 500) {
      alert(body.message);
      return;
    }

    throw new Error("Unexpected response status: " + response.status);
  } catch (error) {
    console.error("Erro ao processar a resposta:", error);
    alert("Ocorreu um erro inesperado. Por favor, tente novamente mais tarde.");
  } finally {
    unsetSubmitting();
  }
});
