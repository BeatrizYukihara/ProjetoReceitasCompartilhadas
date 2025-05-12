// Definir o usuário e exibir a mensagem de boas-vindas
const usuario = document.getElementById('usuarioTitulo').dataset.nome || "Usuário";
document.getElementById('usuarioTitulo').textContent = `Olá, ${usuario}!`;
const usuario_id = document.getElementById('usuarioTitulo').dataset.id;

// Função que representa o planejamento do menu
function menuPlanner() {
  return {
    dias: ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'],

    // Cardápio com IDs das receitas
    cardapio: {
      Segunda: { 'Café da Manhã': [], Almoço: [], Jantar: [] },
      Terça: { 'Café da Manhã': [], Almoço: [], Jantar: [] },
      Quarta: { 'Café da Manhã': [], Almoço: [], Jantar: [] },
      Quinta: { 'Café da Manhã': [], Almoço: [], Jantar: [] },
      Sexta: { 'Café da Manhã': [], Almoço: [], Jantar: [] },
      Sábado: { 'Café da Manhã': [], Almoço: [], Jantar: [] },
      Domingo: { 'Café da Manhã': [], Almoço: [], Jantar: [] }
    },

    mostrarModal: false,
    mostrarModalCompras: false,
    novoDia: 'Segunda',
    novaRefeicao: 'Café da Manhã',
    novasReceitas: [''], // Array com IDs (string) das receitas

    listaDeCompras: [],
    receitasUsuario: [],// Carregado do servidor
    
    
    obterTituloPorId(id) {
      const receita = this.receitasUsuario.find(r => r.id.toString() === id.toString());
      return receita ? receita.titulo : '';
    },
    
    atualizarReceitaDigitada(titulo, index) {
      const receita = this.receitasUsuario.find(r => r.titulo.toLowerCase() === titulo.toLowerCase());
      if (receita) {
        this.novasReceitas[index] = receita.id.toString();
      }
    },
    
//============================= MODAL ====================================
abrirModalAdicionar() {
      this.mostrarModal = true;
},
adicionarLinhaReceita() {
      this.novasReceitas.push('');
},
removerLinhaReceita(index) {
      this.novasReceitas.splice(index, 1);
},

//===================== RECEITAS NO CARDÁPIO =============================
async adicionarReceita() {
  for (const receitaId of this.novasReceitas) {
    if (!receitaId.trim()) continue;

    const dia = this.novoDia;
    const refeicao = this.novaRefeicao;

    // Verifica se já existe no cardápio local
    if (!this.cardapio[dia][refeicao].includes(receitaId)) {
      const res = await fetch('/cardapio', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ receita_id: receitaId, dia, refeicao, usuario_id })
      });

      if (res.ok) {
        const dados = await res.json();
        if (dados.sucesso) {
          this.cardapio[dia][refeicao].push(receitaId);
        } else {
          alert("Erro ao adicionar receita.");
        }
      } else {
        alert("Erro na comunicação com o servidor.");
      }
    }
  }

  this.novasReceitas = [''];
  this.mostrarModal = false;
},



async removerReceita(dia, refeicao, index) {
  const receitaId = this.cardapio[dia][refeicao][index];
  const res = await fetch('/cardapio/remover', {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ receita_id: receitaId, dia, refeicao, usuario_id })
  });
  const dados = await res.json();
  if (dados.sucesso) {
    this.cardapio[dia][refeicao].splice(index, 1);
  }
},


//=========================== AUTOCOMPLETE ======================================
filtrarReceitas(index) {
      const termo = this.novasReceitas[index].toLowerCase();
      return this.receitasUsuario.filter(r => {
        return (
          r.titulo.toLowerCase().includes(termo) &&
          !this.novasReceitas.includes(r.id.toString())
        );
      });
    },

//=========================LISTA DE COMPRAS ======================================
gerarListaCompras() {
      const ingredientesTotais = {};

      for (const dia of this.dias) {
        for (const refeicao of ['Café da Manhã', 'Almoço', 'Jantar']) {
          for (const id of this.cardapio[dia][refeicao]) {
            const receita = this.receitasUsuario.find(r => r.id === parseInt(id));
            if (!receita) continue;

            for (const ingrediente of receita.ingredientes) {
              const chave = `${ingrediente.produto}|${ingrediente.unidade}`;
              const qtd = parseFloat(ingrediente.quantidade.replace(',', '.')) || 0;
              ingredientesTotais[chave] = (ingredientesTotais[chave] || 0) + qtd;
            }
          }
        }
      }

      return Object.entries(ingredientesTotais).map(([chave, qtd]) => {
        const [produto, unidade] = chave.split('|');
        return `${qtd} ${unidade} de ${produto}`;
      });
    },

    abrirModalCompras() {
      this.listaDeCompras = this.gerarListaCompras();
      this.mostrarModalCompras = true;
    },

//========================== INICIALIZAÇÃO ====================================
    async carregarCardapio() {
      const res = await fetch(`/cardapio?usuario_id=${usuario_id}`);
      if (res.ok) {
        this.cardapio = await res.json();
      } else {
        alert("Erro ao carregar o cardápio.");
      }
    }
    ,
    

async init() {
      await this.carregarCardapio();
    }
  };
}
