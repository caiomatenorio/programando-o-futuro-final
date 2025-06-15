function formatMultipleValidityErrorMessages(errors) {
  return errors
    .map((e, i) => {
      if (i !== 0) e = e.charAt(0).toLowerCase() + e.slice(1);
      if (i !== errors.length - 1) e = e.replace(/\.$/, ",");
      return e;
    })
    .join(" ");
}

function formatMultipleAlertErrorMessages(errors) {
  return errors.map((e) => `- ${e}`).join("\n");
}

function clearCustomValidity(input) {
  clear = () => {
    input.setCustomValidity("");
    input.reportValidity();
  };

  input.addEventListener("input", clear, { once: true });
  input.addEventListener("change", clear, { once: true });
}

function addCustomValidity(inputId, errorMessage) {
  const input = document.getElementById(inputId);

  if (input) {
    input.setCustomValidity(errorMessage);
    input.reportValidity();
    clearCustomValidity(input);
  }
}

function displayBadRequestErrors(errors) {
  Object.entries(errors).forEach(([field, errors]) => {
    const input = document.getElementById(field);

    if (input) {
      addCustomValidity(field, formatMultipleValidityErrorMessages(errors));
      return;
    }

    alert(
      `Erros no campo ${field}: \n${formatMultipleAlertErrorMessages(errors)}`
    );
  });
}

function setSubmitting(e, message) {
  const submitBtn = e.submitter;
  const previousContent = submitBtn.textContent;
  submitBtn.disabled = true;
  submitBtn.textContent = message;
  return () => {
    submitBtn.disabled = false;
    submitBtn.textContent = previousContent;
  };
}

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

    if ([401, 409, 500].includes(response.status)) {
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
