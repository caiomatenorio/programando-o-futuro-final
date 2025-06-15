class AppHeader extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this.data = {
      home: this.getAttribute("data-home"),
      back: this.hasAttribute("data-back"),
      login: this.getAttribute("data-login"),
      register: this.getAttribute("data-register"),
    };

    if (!this.data.home) {
      throw new Error("Header component 'data-home' attribute is mandatory.");
    }
  }

  async connectedCallback() {
    this.shadowRoot.innerHTML = `
      <link rel="stylesheet" href="/static/css/app-header.css"/ >
      <header class="header">
        <a href="${
          this.data.home
        }"><img src="/static/images/logo/logo-transparent.png" /></a>
        <nav>
          <ul>
              ${
                this.data.back
                  ? `<li><a href="${this.data.home}">Voltar</a></li>`
                  : ""
              }
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
