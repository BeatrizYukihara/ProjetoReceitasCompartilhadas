document.addEventListener("DOMContentLoaded", function () {
  // Pegando o ID do usuário do atributo 'data-id' no elemento com id 'usuarioTitulo'
  const usuarioId = document.getElementById('usuarioTitulo').getAttribute('data-id');

  if (!usuarioId) {
    console.error("ID do usuário não encontrado.");
    return;  // Se o ID não for encontrado, interrompe a execução
  }

  console.log("ID do usuário:", usuarioId);  // Verifique se o ID está correto no console

  const editarPerfilBtn = document.getElementById('editarPerfilBtn');
  const excluirPerfilBtn = document.getElementById('excluirPerfilBtn');
  const modalEditarPerfil = document.getElementById('modalEditarPerfil');
  const fecharModalBtn = document.getElementById('fecharModalBtn');
  const formEditarPerfil = document.getElementById('formEditarPerfil');
  const modalSucessoPerfil = document.getElementById('modalSucessoPerfil');
  const modalConfirmarExclusao = document.getElementById('modalConfirmarExclusao');
  const confirmarExclusaoBtn = document.getElementById('confirmarExclusaoBtn');
  const cancelarExclusaoBtn = document.getElementById('cancelarExclusaoBtn');

  //========================= EDIÇÃO DE PERFIL =========================
  editarPerfilBtn.addEventListener('click', () => {
    modalEditarPerfil.classList.remove('hidden');
  });

  fecharModalBtn.addEventListener('click', () => {
    modalEditarPerfil.classList.add('hidden');
  });

  formEditarPerfil.addEventListener('submit', (event) => {
    event.preventDefault();

    const dados = new FormData(formEditarPerfil);
    const usuarioData = {
      nome: dados.get('nomeUsuario'),
      email: dados.get('emailUsuario'),
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
          // Fecha o modal de edição
          modalEditarPerfil.classList.add('hidden');

          // Exibe o modal de sucesso
          modalSucessoPerfil.classList.remove('hidden');
          modalSucessoPerfil.style.display = 'block';

          setTimeout(() => {
            modalSucessoPerfil.style.display = 'none';
            modalSucessoPerfil.classList.add('hidden');
            // Recarrega a página
            window.location.reload();
          }, 1000);
        }
      })
      .catch(error => console.error('Erro ao atualizar perfil:', error));
  });

  //========================= EXCLUIR PERFIL =========================
  excluirPerfilBtn.addEventListener('click', () => {
    modalConfirmarExclusao.classList.remove('hidden');
  });

  cancelarExclusaoBtn.addEventListener('click', () => {
    modalConfirmarExclusao.classList.add('hidden');
  });

  confirmarExclusaoBtn.addEventListener('click', () => {
    // Verifique se o ID está sendo passado corretamente
    console.log("Excluindo conta do ID:", usuarioId);

    fetch('/excluir_conta', {
      method: 'POST',
      body: JSON.stringify({ usuario_id: usuarioId }),  // Envia o ID corretamente
      headers: {
        'Content-Type': 'application/json',
      }
    })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'conta excluída') {
          window.location.href = '/login';  // Redireciona para o login após a exclusão
        }
      })
      .catch(error => console.error('Erro ao excluir conta:', error));
  });
});
