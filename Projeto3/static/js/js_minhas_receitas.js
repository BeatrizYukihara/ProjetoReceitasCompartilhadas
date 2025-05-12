// ========================== VARIÁVEIS E USUÁRIO ===========================
let receitas = []; // Lista de receitas será preenchida via fetch

// Buscar nome do usuário autenticado via sessão (Flask deve fornecer isso no HTML renderizado)
const usuario = document.getElementById('usuarioTitulo').dataset.nome || "Usuário";
document.getElementById('usuarioTitulo').textContent = `Olá, ${usuario}!`;

const icons = {
  doce: '/static/imagens/bolo.png',
  salgado: '/static/imagens/coxa_frango.png',
  outros: '/static/imagens/outros.png'
};

// ========================== CARREGAR RECEITAS DO BACKEND ===========================
async function carregarReceitas() {
  try {
    const resposta = await fetch('/api/receitas');
    receitas = await resposta.json();
    renderReceitas();
  } catch (erro) {
    console.error('Erro ao carregar receitas:', erro);
  }
}

carregarReceitas();

// ========================== RENDERIZAR LISTA DE RECEITAS ===========================
function renderReceitas() {
  const searchTerm = searchInput.value.toLowerCase();
  const selectedType = typeFilter.value;

  recipesList.innerHTML = '';

  const filtradas = receitas.filter(r => {
    const matchTitulo = r.titulo.toLowerCase().includes(searchTerm);
    const matchTipo = selectedType === 'todos' || r.tipo === selectedType;
    return matchTitulo && matchTipo;
  });

  if (filtradas.length === 0) {
    recipesList.innerHTML = '<p>Nenhuma receita encontrada.</p>';
    return;
  }

  filtradas.forEach(r => {
    const card = document.createElement('div');
    card.className = 'recipe-card';
    card.innerHTML = `
      <h2 class="recipe-title">${r.titulo}</h2>
      <div class="recipe-type">
        <img src="${icons[r.tipo]}" alt="${r.tipo}">
        <span>${r.tipo.charAt(0).toUpperCase() + r.tipo.slice(1)}</span>
      </div>
    `;

    card.addEventListener('click', () => exibirDetalhesReceita(r));
    recipesList.appendChild(card);
  });
}

// ========================== DETALHES DE UMA RECEITA ===========================
function exibirDetalhesReceita(receita) {
  modalTitle.textContent = receita.titulo;
  modalPortions.textContent = receita.porcoes;
  modalPrepTime.textContent = receita.tempoPreparo;

  modalIngredients.innerHTML = '';
  receita.ingredientes.forEach(i => {
    const li = document.createElement('li');
    li.textContent = `${i.quantidade} ${i.unidade} de ${i.produto}`;
    modalIngredients.appendChild(li);
  });

  modalPreparation.innerHTML = '';
  receita.modoPreparo.forEach(p => {
    const li = document.createElement('li');
    li.textContent = p;
    modalPreparation.appendChild(li);
  });

  recipeModal.style.display = 'flex';
}

closeModal.addEventListener('click', () => {
  recipeModal.style.display = 'none';
});

// ========================== EXCLUSÃO DE RECEITA ===========================
function abrirModalExcluir() {
  document.getElementById("modalExcluir").classList.remove("hidden");
  document.getElementById("pesquisaExcluir").value = "";
  atualizarListaExcluir();
}

function fecharModalExcluir() {
  document.getElementById("modalExcluir").classList.add("hidden");
  document.getElementById("confirmarExclusao").classList.add("hidden");
  document.getElementById("confirmarExclusao").disabled = true;
}

function atualizarListaExcluir() {
  const termo = document.getElementById("pesquisaExcluir").value.toLowerCase();
  const lista = document.getElementById("listaReceitasExcluir");
  lista.innerHTML = "";

  const filtradas = receitas.filter(r => r.titulo.toLowerCase().includes(termo));

  filtradas.forEach((r, index) => {
    const item = document.createElement("div");
    item.className = "item-receita";
    item.textContent = r.titulo;
    item.dataset.index = index;

    item.addEventListener("click", () => {
      document.querySelectorAll('.item-receita').forEach(el => el.classList.remove("selecionado"));
      item.classList.add("selecionado");
      const btn = document.getElementById("confirmarExclusao");
      btn.dataset.index = index;
      btn.classList.remove("hidden");
      btn.disabled = false;
    });

    lista.appendChild(item);
  });

  const btn = document.getElementById("confirmarExclusao");
  btn.classList.add("hidden");
  btn.disabled = true;
}

document.getElementById("confirmarExclusao").addEventListener("click", async () => {
  const index = parseInt(document.getElementById("confirmarExclusao").dataset.index);
  if (!isNaN(index)) {
    const receitaId = receitas[index].id;
    try {
      const resposta = await fetch(`/api/receitas/${receitaId}`, {
        method: 'DELETE'
      });
      if (!resposta.ok) throw new Error('Erro ao excluir receita');

      await carregarReceitas();
      fecharModalExcluir();

      const modalSucesso = document.getElementById("modalSucessoExcluir");
      modalSucesso.style.display = "flex";
      setTimeout(() => { modalSucesso.style.display = "none"; }, 2000);
    } catch (erro) {
      console.error('Erro ao excluir receita:', erro);
    }
  }
});

document.getElementById("deleteRecipeBtn").addEventListener("click", abrirModalExcluir);

// ========================== MODAL DE ADICIONAR RECEITA ===========================

// Definindo o modalAdicionar para o modal correto
const abrirModalBtn = document.getElementById("abrirModalBtn");
const modalAdicionar = document.getElementById("modalAdicionar");
const fecharModalBtn = document.getElementById("fecharModalBtn");
const addIngredienteBtn = document.getElementById("addIngredienteBtn");
const addPassoBtn = document.getElementById("addPassoBtn");


// Verifica se o botão de abrir existe antes de adicionar o evento
if (abrirModalBtn) {
  abrirModalBtn.addEventListener("click", () => {
    modalAdicionar.classList.remove("hidden"); // Exibe o modal
    modalAdicionar.classList.add("show"); // Adiciona a classe show para exibir com transição
    limparCamposFormulario();
  });
}

if (fecharModalBtn) {
  fecharModalBtn.addEventListener("click", () => {
    modalAdicionar.classList.add("hidden"); // Esconde o modal
    modalAdicionar.classList.remove("show"); // Remove a classe show
  });
}

if (addIngredienteBtn) {
  addIngredienteBtn.addEventListener("click", () => {
    adicionarIngrediente()
  });
}

if (addPassoBtn) {
  addPassoBtn.addEventListener("click", () => {
    adicionarPasso()
  });
}

function limparCamposFormulario() {
  document.getElementById('titulo').value = '';
  document.getElementById('tipo').value = 'doce';
  document.getElementById('tempo').value = '';
  document.getElementById('porcoes').value = '';
  ingredientesContainer.innerHTML = '';
  modoContainer.innerHTML = '';
  adicionarIngrediente();
  adicionarPasso();
}

const unidades = ['unidade', 'g', 'kg', 'ml', 'L', 'xícara', 'colher'];
const ingredientesContainer = document.getElementById("ingredientesContainer");
const modoContainer = document.getElementById("modoContainer");

function adicionarIngrediente() {
  const div = document.createElement("div");
  div.className = "ingrediente-item";
  div.innerHTML = `
    <div class="input-container">
      <input type="text" placeholder="Produto" class="input-ingrediente produto" required>
      <input type="text" placeholder="Quantidade" class="input-ingrediente quantidade" required>
      <select class="input-ingrediente unidade" required>
        ${unidades.map(u => `<option value="${u}">${u}</option>`).join('')}
      </select>
      <button type="button" class="botao-acao botao-lixeira" onclick="removerIngrediente(this)">
        <span class="x-vermelho">❌</span>
      </button>
    </div>
  `;
  ingredientesContainer.appendChild(div);
}

function removerIngrediente(botao) {
  const div = botao.closest(".ingrediente-item");
  div.remove();
}

function adicionarPasso() {
  const index = modoContainer.children.length + 1;
  const div = document.createElement("div");
  div.className = "passo-item";
  div.innerHTML = `
    <div class="input-container">
      <span>${index}.</span>
      <textarea placeholder="Descreva o passo..." required></textarea>
      <button type="button" class="botao-acao botao-lixeira" onclick="removerPasso(this)">
        <span class="x-vermelho">❌</span>
      </button>
    </div>
  `;
  modoContainer.appendChild(div);
}

function removerPasso(botao) {
  const div = botao.closest(".passo-item");
  div.remove();
  atualizarNumeracaoPassos();
}

function atualizarNumeracaoPassos() {
  const passos = modoContainer.querySelectorAll('.passo-item');
  passos.forEach((p, i) => {
    p.querySelector('span').textContent = i + 1;
  });
}

// ========================== ENVIO DO FORMULÁRIO DE RECEITA ===========================
const form = document.getElementById("formReceita"); // Definindo o formulário correto
form.addEventListener("submit", async function(event) {
  event.preventDefault();

  const titulo = document.getElementById('titulo').value;
  const tipo = document.getElementById('tipo').value;
  const tempoPreparo = document.getElementById('tempo').value;
  const porcoes = document.getElementById('porcoes').value;

  const ingredientes = [];
  ingredientesContainer.querySelectorAll('.ingrediente-item').forEach(item => {
    ingredientes.push({
      produto: item.querySelector('.produto').value,
      quantidade: item.querySelector('.quantidade').value,
      unidade: item.querySelector('.unidade').value
    });
  });

  const modoPreparo = [];
  modoContainer.querySelectorAll('.passo-item textarea').forEach(item => {
    modoPreparo.push(item.value);
  });

  const novaReceita = {
    titulo,
    tipo,
    tempoPreparo,
    porcoes,
    ingredientes,
    modoPreparo
  };

  try {
    const resposta = await fetch('/api/receitas', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(novaReceita)
    });

    if (!resposta.ok) throw new Error('Erro ao salvar receita');

    await carregarReceitas();
    modalAdicionar.classList.add("hidden"); // Fechar o modal após salvar
  } catch (erro) {
    console.error('Erro ao adicionar receita:', erro);
  }
});
