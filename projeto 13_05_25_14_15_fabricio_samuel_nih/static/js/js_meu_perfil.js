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
          // Atualiza o perfil na página
          document.querySelector('.perfil-info p strong:nth-of-type(1)').nextSibling.textContent = ` ${usuarioData.nome}`;
          document.querySelector('.perfil-info p strong:nth-of-type(2)').nextSibling.textContent = ` ${usuarioData.email}`;
          document.querySelector('.perfil-info p strong:nth-of-type(3)').nextSibling.textContent = ` ${usuarioData.telefone}`;
          document.querySelector('.perfil-info p strong:nth-of-type(4)').nextSibling.textContent = ` ${usuarioData.prato}`;

          modalSucessoPerfil.style.display = 'block';
          setTimeout(() => modalSucessoPerfil.style.display = 'none', 2000);
          modalEditarPerfil.classList.add('hidden');
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
