function formatMultipleValidityErrorMessages(errors) {
  return errors
    .map((e, i) => {
      e = i !== 0 ? e.charAt(0).toLowerCase() + e.slice(1) : e;
      e = i !== errors.length - 1 ? e.replace(/\.$/, ",") : e;
      return e;
    })
    .join(" ");
}

function formatMultipleAlertErrorMessages(errors) {
  return errors.map((e) => `- ${e}`).join("\n");
}

function clearCustomValidity(input) {
  let clear = () => {
    input.setCustomValidity("");
    input.reportValidity();
  };

  input.addEventListener("input", clear, { once: true });
  input.addEventListener("change", clear, { once: true });
}

export function addCustomValidity(inputId, errorMessage) {
  const input = document.getElementById(inputId);

  if (input) {
    input.setCustomValidity(errorMessage);
    input.reportValidity();
    clearCustomValidity(input);
  }
}

export function displayBadRequestErrors(errors) {
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

export function setSubmitting(e, message) {
  const submitBtn = e.submitter;
  const previousContent = submitBtn.textContent;
  submitBtn.disabled = true;
  submitBtn.textContent = message;
  return () => {
    submitBtn.disabled = false;
    submitBtn.textContent = previousContent;
  };
}
