// Envia usuário e senha para uma rota do Python e devolve a resposta
async function enviar(rota) {
    const usuario = document.getElementById("usuario").value;
    const senha = document.getElementById("senha").value;

    document.getElementById("mensagem").textContent = "Processando...";
    document.getElementById("resultado").textContent = "";

    const resposta = await fetch(rota, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ usuario, senha }),
    });

    return resposta.json();
}

// Mostra a mensagem verde (sucesso) ou vermelha (erro)
function mostrarMensagem(dados) {
    const mensagem = document.getElementById("mensagem");
    mensagem.textContent = dados.mensagem;
    mensagem.className = dados.ok ? "sucesso" : "erro";
}

async function cadastrar() {
    const dados = await enviar("/cadastrar");
    mostrarMensagem(dados);

    if (dados.ok) {
        document.getElementById("resultado").textContent =
            "Salt:\n" + dados.salt + "\n\nHash salvo:\n" + dados.hash;
    }
}

async function entrar() {
    const dados = await enviar("/login");
    mostrarMensagem(dados);

    if (dados.hash_digitado) {
        document.getElementById("resultado").textContent =
            "Hash da senha digitada:\n" + dados.hash_digitado +
            "\n\nHash salvo no banco:\n" + dados.hash_salvo;
    }
}
