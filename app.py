import hashlib
import hmac
import os

from flask import Flask, jsonify, request

app = Flask(__name__, static_folder="static", static_url_path="")

# Banco de dados simulado em memória (Dicionário)
# Salva { "usuario": (salt, hash_da_senha) }
banco_de_dados = {}


def gerar_hash(senha, salt=None):
    # 1. Se não recebeu salt (cadastro), gera um novo aleatório
    if salt is None:
        salt = os.urandom(16)

    # 2. Transforma a senha em bytes e gera o hash com PBKDF2
    senha_bytes = senha.encode("utf-8")
    hash_senha = hashlib.pbkdf2_hmac("sha256", senha_bytes, salt, 600_000)

    # 3. Devolve o salt e o hash
    return salt, hash_senha


def cadastrar_usuario(usuario, senha):
    # 1. Gera o salt e o hash da senha
    salt, hash_senha = gerar_hash(senha)

    # 2. Salva no "banco de dados"
    banco_de_dados[usuario] = (salt, hash_senha)
    print(f"✅ Usuário '{usuario}' cadastrado com sucesso!")
    return salt, hash_senha


def verificar_login(usuario, senha_digitada):
    # 1. Verifica se o usuário existe
    if usuario not in banco_de_dados:
        print("❌ Usuário ou senha inválidos.")
        return False, None

    # 2. Pega o salt e o hash que estão salvos
    salt, hash_salvo = banco_de_dados[usuario]

    # 3. Gera o hash da senha digitada usando o MESMO salt
    _, hash_digitado = gerar_hash(senha_digitada, salt)

    # 4. Compara os dois hashes de forma segura
    if hmac.compare_digest(hash_digitado, hash_salvo):
        print("🔓 Login realizado com sucesso!")
        return True, hash_digitado
    else:
        print("❌ Usuário ou senha inválidos.")
        return False, hash_digitado


# --- Rotas que a tela (HTML/JS) chama ---

@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/cadastrar", methods=["POST"])
def rota_cadastrar():
    dados = request.get_json()
    usuario = dados.get("usuario", "").strip()
    senha = dados.get("senha", "")

    if not usuario or not senha:
        return jsonify(ok=False, mensagem="Preencha usuário e senha.")

    salt, hash_senha = cadastrar_usuario(usuario, senha)
    return jsonify(
        ok=True,
        mensagem=f"Usuário '{usuario}' cadastrado com sucesso!",
        salt=salt.hex(),
        hash=hash_senha.hex(),
    )


@app.route("/login", methods=["POST"])
def rota_login():
    dados = request.get_json()
    usuario = dados.get("usuario", "").strip()
    senha = dados.get("senha", "")

    ok, hash_digitado = verificar_login(usuario, senha)
    resposta = {
        "ok": ok,
        "mensagem": "Login realizado com sucesso!" if ok else "Usuário ou senha inválidos.",
    }
    # Mostra os hashes na tela só para fins de estudo
    if hash_digitado is not None:
        resposta["hash_digitado"] = hash_digitado.hex()
        resposta["hash_salvo"] = banco_de_dados[usuario][1].hex()
    return jsonify(resposta)


if __name__ == "__main__":
    app.run(debug=True)
