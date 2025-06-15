class AppHeader extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this.data = {
      index: this.getAttribute("data-index"),
      login: this.getAttribute("data-login"),
      register: this.getAttribute("data-register"),
    };

    if (!this.data.index) {
      throw new Error("Header component 'data-home' attribute is mandatory.");
    }
  }

  async connectedCallback() {
    this.shadowRoot.innerHTML = `
      <link rel="stylesheet" href="/static/css/header.css">
      <header class="header">
        <div><a href="${this.data.index}"></a></div>
        <nav>
          <ul>
              ${
                this.data.login
                  ? `<li><a href="${this.data.login}">Entrar</a></li>`
                  : ""
              }
              ${
                this.data.register
                  ? `<li><a href="${this.data.register}">Criar conta</a></li>`
                  : ""
              }
          </ul>
        </nav>
      </header>
    `;
  }
}

customElements.define("app-header", AppHeader);
