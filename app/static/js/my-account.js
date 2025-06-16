import {
  addCustomValidity,
  displayBadRequestErrors,
  setSubmitting,
} from "./request-utils.js";

document.getElementById("name-form").addEventListener("submit", async (e) => {
  if (!e.target.checkValidity()) {
    return;
  }

  e.preventDefault();

  try {
    const name = document.getElementById("name").value;
    const response = await fetch("/api/my-account/name", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    });

    if (response.ok) {
      alert("Nome atualizado com sucesso!");
      window.location.replace("/minha-conta");
      return;
    }

    const body = await response.json();

    if (response.status === 400) {
      displayBadRequestErrors(body.errors);
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
  }
});

document.getElementById("email-form").addEventListener("submit", async (e) => {
  if (!e.target.checkValidity()) {
    return;
  }

  e.preventDefault();

  try {
    const email = document.getElementById("email").value;
    const response = await fetch("/api/my-account/email", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email }),
    });

    if (response.ok) {
      alert("E-mail atualizado com sucesso!");
      window.location.replace("/minha-conta");
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
    alert("Ocorreu um erro inesperado. Por favor, tente novamente mais tarde.");
  }
});

document
  .getElementById("password-form")
  .addEventListener("submit", async (e) => {
    if (!e.target.checkValidity()) {
      return;
    }

    e.preventDefault();
    const unsetSubmitting = setSubmitting(e, "Atualizando...");

    try {
      const currentPassword = document.getElementById("current-password").value;
      const newPassword = document.getElementById("new-password").value;
      const confirmNewPassword = document.getElementById(
        "confirm-new-password"
      ).value;

      if (newPassword !== confirmNewPassword) {
        addCustomValidity("confirm-new-password", "As senhas não coincidem.");
        return;
      }

      const response = await fetch("/api/my-account/password", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword,
        }),
      });

      if (response.ok) {
        alert("Senha atualizada com sucesso!");
        window.location.replace("/minha-conta");
        return;
      }

      const body = await response.json();

      if (response.status === 400) {
        displayBadRequestErrors(body.errors);
        return;
      }

      if (response.status === 401) {
        addCustomValidity("current-password", body.message);
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
