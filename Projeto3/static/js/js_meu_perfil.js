document.addEventListener("DOMContentLoaded", function () {
  const editarPerfilBtn = document.getElementById('editarPerfilBtn');
  const excluirPerfilBtn = document.getElementById('excluirPerfilBtn');
  const modalEditarPerfil = document.getElementById('modalEditarPerfil');
  const fecharModalBtn = document.getElementById('fecharModalBtn');
  const formEditarPerfil = document.getElementById('formEditarPerfil');
  const modalSucessoPerfil = document.getElementById('modalSucessoPerfil');
  const modalConfirmarExclusao = document.getElementById('modalConfirmarExclusao');
  const confirmarExclusaoBtn = document.getElementById('confirmarExclusaoBtn');
  const cancelarExclusaoBtn = document.getElementById('cancelarExclusaoBtn');


//=======================================EDIÇÃO DE PERFIL============================
  // Exibir modal para edição de perfil
  editarPerfilBtn.addEventListener('click', () => {
    modalEditarPerfil.classList.remove('hidden');
  });

  // Fechar o modal de edição
  fecharModalBtn.addEventListener('click', () => {
    modalEditarPerfil.classList.add('hidden');
  }); 

  // Enviar as alterações para o servidor
  formEditarPerfil.addEventListener('submit', (event) => {
    event.preventDefault();
    
    const dados = new FormData(formEditarPerfil);
    const usuarioData = {
      nome: dados.get('nomeUsuario'),
      email: dados.get('emailUsuario'),
      telefone: dados.get('telefoneUsuario'),
      prato: dados.get('pratoFavorito'),
      foto: dados.get('fotoPerfil')
    };

    fetch('/atualizar_usuario', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(usuarioData),
    })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'sucesso') {
          modalEditarPerfil.classList.add('hidden'); // Fecha o modal
          modalSucessoPerfil.classList.remove('hidden'); // Mostra a mensagem de sucesso

          // Aguarda 1,5 segundo e recarrega a página
          setTimeout(() => {
            window.location.reload();
          }, 500);
        }
      })
      .catch(error => console.error('Erro ao atualizar perfil:', error));
  });


  //=======================================EXCLUIR PERFIL============================

  // Excluir perfil
  excluirPerfilBtn.addEventListener('click', () => {
    modalConfirmarExclusao.classList.remove('hidden');
  });

  cancelarExclusaoBtn.addEventListener('click', () => {
    modalConfirmarExclusao.classList.add('hidden');
  });

  confirmarExclusaoBtn.addEventListener('click', () => {
    fetch('/excluir_conta', {
      method: 'POST',
      body: JSON.stringify({ usuario_id: 1 }),  // Substitua o ID pelo valor real
      headers: {
        'Content-Type': 'application/json',
      }
    })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'conta excluída') {
          window.location.href = '/login';  // Redireciona para login
        }
      })
      .catch(error => console.error('Erro ao excluir conta:', error));
  });
});
