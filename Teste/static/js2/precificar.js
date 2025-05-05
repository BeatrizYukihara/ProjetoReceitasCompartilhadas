const usuario = "João"; //TEM QUE MUDAR ISSO
const usuario_id = 1 //TEM QUE MUDAR ISSO



document.getElementById('usuarioTitulo').textContent = `Olá, ${usuario}!`;

const icons = {
  doce: 'static/imagens/bolo.png',
  salgado: 'static/imagens/coxa_frango.png',
  outros: 'static/imagens/outros.png'
};

const recipesList = document.getElementById('recipesList');
const searchInput = document.getElementById('searchInput');
const typeFilter = document.getElementById('typeFilter');

let receitas = [];
let receitaAtual = null;

function renderReceitas(receitas) {
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
          <img class="price-icon" src="static/imagens/cifrao.png" alt="Ícone de preço">
          <span class="price-value">R$ ${r.preco || 'N/A'}</span>
        </div>
      </div>
    `;
    card.onclick = () => abrirModalPrecificar(r);
    recipesList.appendChild(card);
  });
}

function abrirModalPrecificar(receita) {
  receitaAtual = receita;
  document.getElementById('tituloReceitaModal').textContent = receita.titulo;
  const container = document.getElementById('ingredientesFormulario');
  container.innerHTML = '';

  fetch(`/get_ingredientes/${receita.id}`)
    .then(res => res.json())
    .then(ingredientes => {
      receitaAtual.ingredientes = ingredientes;
      ingredientes.forEach((ingrediente, i) => {
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
            <span class="unit-text">${ingrediente.unidade_de_medida}</span>
          </div>
        `;
        container.appendChild(row);
      });
    });

  document.getElementById('modalPrecificar').style.display = 'flex';
}

function confirmarPreco() {
  let total = 0;
  receitaAtual.ingredientes.forEach((ingrediente, i) => {
    const valorPorUnidade = parseFloat(document.getElementById(`valor-${i}`).value) || 0;
    const quantidadeNaReceita = ingrediente.quantidade;
    const quantidadeInserida = parseFloat(document.getElementById(`quantidade-${i}`).value) || 1;

    // Regra de 3
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
    renderReceitas(receitas);

    // Mostra a caixinha com o preço
    const caixa = document.getElementById('precoCaixa');
    const mensagem = document.getElementById('mensagemPreco');
    mensagem.textContent = `Preço total da receita: R$ ${precoFinal}`;
    caixa.style.display = 'flex';

    // Esconde a caixinha depois de 4 segundos
    setTimeout(() => {
      caixa.style.display = 'none';
    }, 4000);
  });
} 

function fecharModal() {
  document.getElementById('modalPrecificar').style.display = 'none';
}

searchInput.addEventListener('input', () => renderReceitas(receitas));
typeFilter.addEventListener('change', () => renderReceitas(receitas));

fetch(`/get_receitas/${usuario_id}`)
  .then(res => res.json())
  .then(data => {
    receitas = data;
    renderReceitas(receitas);
  })
  .catch(err => console.error('Erro ao carregar as receitas:', err));
