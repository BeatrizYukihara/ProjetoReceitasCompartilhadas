// Definir o usuário e exibir a mensagem de boas-vindas
const usuario = document.getElementById('usuarioTitulo').dataset.nome || "Usuário";
document.getElementById('usuarioTitulo').textContent = `Olá, ${usuario}!`;

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
    receitasUsuario: [], // Carregado do servidor

    obterTituloPorId(id) {
      const receita = this.receitasUsuario.find(r => r.id.toString() === id.toString());
      return receita ? receita.titulo : '';
    },

    agruparReceitas(receitas) {
      const grupos = {};
      for (const id of receitas) {
        const titulo = this.obterTituloPorId(id);
        if (!grupos[titulo]) {
          grupos[titulo] = [];
        }
        grupos[titulo].push(id);
      }
      return grupos;
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
          if (!receitaId.trim()) continue; // Ignora se o ID da receita estiver vazio
  
          const dia = this.novoDia;
          const refeicao = this.novaRefeicao;
  
          // Evita duplicidade local
          if (!this.cardapio[dia][refeicao].includes(receitaId)) {
              try {
                  const res = await fetch('/cardapio/adicionar', {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({ receita_id: receitaId, dia, refeicao })
                  });
                  
                  // Verifica se a resposta foi bem-sucedida
                  if (res.ok) {
                      const dados = await res.json(); // Obtém os dados da resposta
                      if (dados.sucesso) {
                          this.cardapio[dia][refeicao].push(receitaId); // Adiciona a receita ao cardápio
                          this.exibirCardapio(); // Atualiza a visualização do cardápio
                      } else {
                          alert("Erro ao adicionar receita: " + dados.erro); // Exibe a mensagem de erro retornada
                      }
                  } else {
                      alert("Erro ao adicionar receita: " + res.statusText); // Exibe o status da resposta
                  }
              } catch (error) {
                  console.error("Erro ao adicionar receita:", error);
                  alert("Erro ao adicionar receita. Tente novamente.");
              }
          } else {
              alert("Receita já adicionada ao cardápio."); // Mensagem se a receita já estiver no cardápio
          }
      }
  
      this.novasReceitas = ['']; // Reseta o array de novas receitas
      this.mostrarModal = false; // Fecha o modal
  
      // Renderiza a página novamente ou atualiza a seção do cardápio
      await this.carregarCardapio(); // Recarrega o cardápio
  }
  ,

    //=========================== REMOVER CARDAPIO ======================================
    async removerReceita(dia, refeicao, index) {
      const receitaId = this.cardapio[dia][refeicao][index];
      console.log("Remover:", { receita_id: receitaId, dia, refeicao });
    
      try {
        const res = await fetch('/api/cardapio/excluir', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ receita_id: receitaId, dia, refeicao })
        });
    
        const dados = await res.json();
        if (dados.sucesso) {
          this.cardapio[dia][refeicao].splice(index, 1);
          this.exibirCardapio();
        } else {
          alert("Erro ao remover receita: " + (dados.mensagem || "Erro desconhecido"));
        }
      } catch (error) {
        console.error("Erro ao remover receita:", error);
        alert("Erro ao remover receita. Tente novamente.");
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
                  const receita = this.receitasUsuario.find(r => r.id.toString() === id.toString());
                  if (!receita) continue;

                  const ingredientes = receita.ingredientes || [];
                  console.log(`Ingredientes da receita ${receita.titulo}:`, ingredientes); // Verifique os ingredientes
                  for (const ingrediente of ingredientes) {
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
  }
  ,
    

    abrirModalCompras() {
      this.listaDeCompras = this.gerarListaCompras();
      this.mostrarModalCompras = true;
    },

    //========================== INICIALIZAÇÃO ====================================
    async carregarReceitas() {
      try {
          const res = await fetch('/api/receitas');
          if (res.ok) {
              this.receitasUsuario = await res.json();
              console.log("Receitas carregadas:", this.receitasUsuario); // Verifique se as receitas estão corretas
          } else {
              alert("Erro ao carregar receitas.");
          }
      } catch (error) {
          console.error("Erro ao carregar receitas:", error);
          alert("Erro ao carregar receitas. Tente novamente.");
      }
  }
  
    ,

    async carregarCardapio() {
      try {
        const res = await fetch('/api/cardapio');
        if (res.ok) {
          const dadosCardapio = await res.json();
          console.log("Cardápio recebido:", dadosCardapio);  // Verifique se os dados estão corretos
          this.cardapio = dadosCardapio;
          this.exibirCardapio(); // Exibe o cardápio ao carregar
        } else {
          alert("Erro ao carregar o cardápio {1}.");
        }
      } catch (error) {
        console.error("Erro ao carregar o cardápio {2}:", error);
        alert("Erro ao carregar o cardápio. Tente novamente.");
      }
    },

    exibirCardapio() {
      const normalizarTipo = tipo => tipo.normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/\s+/g, '');
    
      for (const dia in this.cardapio) {
        for (const tipo in this.cardapio[dia]) {
          const tipoNormalizado = normalizarTipo(tipo);
          const idElemento = `${dia}-${tipoNormalizado}`;
          const container = document.getElementById(idElemento);
    
          if (!container) {
            console.warn(`Elemento com id ${idElemento} não encontrado no DOM.`);
            continue;
          }
    
          const receitas = this.cardapio[dia][tipo];
          container.innerHTML = ''; // Limpa antes de adicionar
    
          if (receitas.length === 0) {
            container.innerHTML = '<span> </span>'; // Mensagem para receitas vazias
          } else {
            const contagem = {};
            receitas.forEach(receita => {
                contagem[receita.id] = (contagem[receita.id] || 0) + 1;
            });

            // Exibir cada receita apenas uma vez
            for (const receitaId in contagem) {
                const receita = receitas.find(r => r.id === parseInt(receitaId));
                if (receita) { // Verifica se a receita existe
                    const item = document.createElement('div');
                    item.textContent = `${contagem[receitaId]} x ${receita.nome}`; // Exibe a contagem e o nome da receita

                    // Criar botão de exclusão
                    const btnExcluir = document.createElement('button');
                    btnExcluir.textContent = 'X'; // Texto do botão
                    btnExcluir.className = 'botao-excluir'; // Classe para estilização
                    btnExcluir.onclick = () => {
                        this.removerReceita(dia, tipo, receitas.indexOf(receita)); // Chama a função de remoção
                    };

                    item.appendChild(btnExcluir); // Adiciona o botão ao item
                    container.appendChild(item); // Adiciona o item ao container
                } else {
                    console.warn(`Receita com ID ${receitaId} não encontrada.`);
                }
            }
          }
        }
      }
    },
    
    async init() {
      await this.carregarReceitas();
      await this.carregarCardapio();
    }
  };
}
