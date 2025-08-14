document.addEventListener('DOMContentLoaded', function () {
    console.log("Script carregado e DOM pronto!");

    // ===== Limitar a data de entrada entre amanhã e 5 dias após hoje =====
    const inputData = document.getElementById('data');

    const hoje = new Date();
    const amanha = new Date(hoje);
    amanha.setDate(hoje.getDate() + 1);

    const limite = new Date(hoje);
    limite.setDate(hoje.getDate() + 5);

    const formatarData = (data) => {
        const ano = data.getFullYear();
        const mes = String(data.getMonth() + 1).padStart(2, '0');
        const dia = String(data.getDate()).padStart(2, '0');
        return `${ano}-${mes}-${dia}`;
    };

    inputData.min = formatarData(amanha);
    inputData.max = formatarData(limite);

    // ========== Lógica do formulário ==========
    const form = document.getElementById('form-previsao');
    const resultadoDiv = document.getElementById('resultado');

    form.addEventListener('submit', async function (e) {
        e.preventDefault(); // impede o envio normal do formulário (sem recarregar a página)

        const dataSelecionada = document.getElementById('data').value;

        try {
            const response = await fetch('/bike_rentals/prever', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: new URLSearchParams({ data: dataSelecionada })
            });

            const json = await response.json();

            if (response.ok) {
                resultadoDiv.innerHTML = `
                    <p><strong>Previsão de aluguéis:</strong> ${json.previsao}</p>
                    <p><strong>Margem de erro:</strong> ±${json.margem_erro}</p>
                `;
            } else {
                resultadoDiv.innerHTML = `<p class="erro">Erro: ${json.erro}</p>`;
            }

        } catch (err) {
            resultadoDiv.innerHTML = `<p class="erro">Erro ao conectar com a API.</p>`;
            console.error(err);
        }
    });

    // Função para obter o CSRF token do cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
