# AutoCV

Gere currículos modernos automaticamente a partir do seu GitHub e/ou LinkedIn CSV, edite visualmente e baixe em PDF.

---

## ✨ Funcionalidades

- Importação automática de dados do GitHub e LinkedIn (CSV).
- Geração de bio e descrições de projetos com IA (Gemini).
- Escolha entre múltiplos templates de currículo.
- Editor visual (GrapesJS) para personalização.
- Exportação em PDF com design fiel ao template.

---

## 🚀 Como usar

1. **Clone o repositório:**
   ```sh
   git clone https://github.com/seu-usuario/AutoCV.git
   cd AutoCV
   ```

2. **Instale as dependências:**
   ```sh
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure o `.env`:**
   ```
   SECRET_KEY=sua_chave_secreta
   ```
   > Para usar a IA Gemini, insira sua chave de API no arquivo `app/services/gemini.py`.

4. **Execute o servidor:**
   ```sh
   python server.py
   ```
   Acesse [http://localhost:1111](http://localhost:1111) no navegador.

---

## 📝 Como funciona

1. Escolha um template.
2. Preencha seu usuário do GitHub e/ou faça upload do CSV do LinkedIn.
3. Gere e edite visualmente seu currículo.
4. Baixe o PDF pronto.

---

## 📁 Estrutura

- `app/` - Backend Flask, templates e serviços.
- `data/` - Uploads temporários.
- `output/` - PDFs gerados.
- `requirements.txt` - Dependências.
- `server.py` - Inicialização do servidor.

---

## 🛠️ Tecnologias

- Python 3.10+
- Flask
- WeasyPrint
- GrapesJS
- Google Gemini API
- Pandas

---

## 📦 Exportando CSV do LinkedIn

1. Vá em Configurações > Obtenha uma cópia dos seus dados.
2. Exporte "Dados do perfil" em CSV.
3. Faça upload na página do AutoCV.

---

## 📄 Licença

MIT

---

Desenvolvido por
