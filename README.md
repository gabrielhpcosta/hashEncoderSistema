# hashEncoderSistema

Sistema simples de cadastro e login que mostra o hash de senhas funcionando (PBKDF2 + salt), com Python (Flask) e uma tela em HTML, CSS e JS.

## Como usar

1. Instale o Flask:
   ```
   pip install flask
   ```
2. Rode o projeto:
   ```
   python app.py
   ```
3. Abra **http://127.0.0.1:5000** no navegador.
4. Cadastre um usuário e faça login para ver o salt e os hashes.

> Os usuários ficam salvos só na memória e somem quando o programa é encerrado.
