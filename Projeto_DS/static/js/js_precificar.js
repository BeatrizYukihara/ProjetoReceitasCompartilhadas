// ========================== VARIÁVEIS E USUÁRIO ===========================
let receitas = []; // Lista de receitas será preenchida via fetch
let receitaAtual = null; // Receita sendo precificada

// Buscar nome do usuário pelo flask
const usuario = document.getElementById('usuarioTitulo').dataset.nome || "Usuário";
document.getElementById('usuarioTitulo').textContent = `Olá, ${usuario}!`;

const icons = {
  doce: '/static/imagens/bolo.png',
  salgado: '/static/imagens/coxa_frango.png',
  outros: '/static/imagens/outros.png'
};

const searchInput = document.getElementById('searchInput');
const typeFilter = document.getElementById('typeFilter');
const recipesList = document.getElementById('recipesList');

// ========================== CARREGAR RECEITAS DO BACKEND ===========================
async function carregarReceitas() {
  try {
    const resposta = await fetch('/api/receitas');
    receitas = await resposta.json();
    renderReceitas(); // Corrigido: agora chama sem argumentos
  } catch (erro) {
    console.error('Erro ao carregar receitas:', erro);
  }
}

carregarReceitas();

// ========================== RENDERIZAR LISTA DE RECEITAS ===========================
function renderReceitas() {
  recipesList.innerHTML = '';
  const searchTerm = searchInput.value.toLowerCase();
  const selectedType = typeFilter.value;

  const filtradas = receitas.filter(r =>
    r.titulo.toLowerCase().includes(searchTerm) &&
    (selectedType === 'todos' || r.tipo === selectedType)
  );

  if (filtradas.length === 0) {
    recipesList.innerHTML = '<p>Nenhuma receita encontrada.</p>';
    return;
  }

  filtradas.forEach(r => {
    const card = document.createElement('div');
    card.className = 'recipe-card';
    card.innerHTML = `
      <h2 class="recipe-title">${r.titulo}</h2>
      <div class="recipe-bottom">
        <div class="recipe-type">
          <img src="${icons[r.tipo]}" alt="${r.tipo}">
          <span>${r.tipo.charAt(0).toUpperCase() + r.tipo.slice(1)}</span>
        </div>
        <div class="recipe-price">
          <img class="price-icon" src="/static/imagens/cifrao.png" alt="Ícone de preço">
          <span class="price-value">R$ ${r.preco || 'N/A'}</span>
        </div>
      </div>
    `;
    card.onclick = () => abrirModalPrecificar(r);
    recipesList.appendChild(card);
  });
}

// ========================== MODAL DE PRECIFICAR RECEITA ===========================
function abrirModalPrecificar(receita) {
  receitaAtual = receita;
  document.getElementById('tituloReceitaModal').textContent = receita.titulo;

  const container = document.getElementById('ingredientesFormulario');
  container.innerHTML = '';

  // Usa diretamente os ingredientes que já vêm na receita
  receita.ingredientes.forEach((ingrediente, i) => {
    const row = document.createElement('div');
    row.className = 'ingredient-row';
    row.innerHTML = `
      <div class="ingredient-name">${ingrediente.produto}</div>
      <div class="ingredient-price">
        <input type="number" min="0" step="0.01" placeholder="Preço" class="price-input" id="valor-${i}">
      </div>
      <div class="equal-sign"></div>
      <div class="ingredient-quantity">
        <input type="number" min="0" placeholder="Qtd" class="quantity-input" id="quantidade-${i}">
        <span class="unit-text">${ingrediente.unidade}</span>
      </div>
    `;
    container.appendChild(row);
  });

  document.getElementById('modalPrecificar').style.display = 'flex';
}


function confirmarPreco() {
  let total = 0;
  receitaAtual.ingredientes.forEach((ingrediente, i) => {
    const valorPorUnidade = parseFloat(document.getElementById(`valor-${i}`).value) || 0;
    const quantidadeNaReceita = ingrediente.quantidade;
    const quantidadeInserida = parseFloat(document.getElementById(`quantidade-${i}`).value) || 1;

    const precoIngrediente = (valorPorUnidade / quantidadeInserida) * quantidadeNaReceita;
    total += precoIngrediente;
  });

  const precoFinal = total.toFixed(2);
  receitaAtual.preco = precoFinal;

  fetch('/atualizar_preco', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ receita_id: receitaAtual.id, preco_total: precoFinal })
  })
    .then(res => res.json())
    .then(data => {
      fecharModal();
      renderReceitas();

      const caixa = document.getElementById('precoCaixa');
      const mensagem = document.getElementById('mensagemPreco');
      mensagem.textContent = `Preço total da receita: R$ ${precoFinal}`;
      caixa.style.display = 'flex';

      setTimeout(() => {
        caixa.style.display = 'none';
      }, 4000);
    });
}

function fecharModal() {
  document.getElementById('modalPrecificar').style.display = 'none';
}

// ========================== EVENTOS DE FILTRO E BUSCA ===========================
searchInput.addEventListener('input', () => renderReceitas());
typeFilter.addEventListener('change', () => renderReceitas());
