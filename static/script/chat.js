
const chatToggle = document.getElementById('chat-toggle');
    const chatWindow = document.getElementById('chat-window');
    const closeChat = document.getElementById('close-chat');
    const chatInput = document.getElementById('chat-input');
    const sendMessageBtn = document.getElementById('send-message');
    const speechBtn = document.getElementById('microphone-btn');
    const chatMessages = document.getElementById('chat-messages');

chatInput.addEventListener('keydown', function(event) {
      if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault(); // Impede quebras de linha
        sendMessage();
      }
    });

// Função para alternar a visibilidade do chat
    function toggleChat() {
      chatWindow.classList.toggle('active');
    }

    // Função para fechar o chat
    function closeChatWindow() {
      chatWindow.classList.remove('active');
    }

    // Função para enviar uma mensagem

    function compute_user_message(message, data) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', 'sent');

        const timeString = data.getHours().toString().padStart(2, '0') + ':' + data.getMinutes().toString().padStart(2, '0');

        messageElement.innerHTML = `
          <p>${message}</p>
          <span class="timestamp">${timeString}</span>
        `;

        chatMessages.appendChild(messageElement);
    }

    function compute_assistant_message(message, data) {
          const responseElement = document.createElement('div');
          responseElement.classList.add('message', 'received');

          const responseTimeString = data.getHours().toString().padStart(2, '0') + ':' + data.getMinutes().toString().padStart(2, '0');

          // Resposta simulada
          responseElement.innerHTML = `
            <p>${message}</p>
            <span class="timestamp">${responseTimeString}</span>
          `;

          chatMessages.appendChild(responseElement);
          chatMessages.scrollTop = chatMessages.scrollHeight; // Rolagem automática
    }

    async function sendMessage() {
      const messageText = chatInput.value.trim();
      if (messageText) {
        // Criar elemento da mensagem enviada

        const date = new Date();

        compute_user_message(messageText, date);


        // Limpar o campo de entrada
        chatInput.value = '';

        // Rolagem automática para a nova mensagem
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // --- Simulação de Resposta Automática ---
        // Em um cenário real, você chamaria uma API aqui.
       /* setTimeout(() => {
          compute_assistant_message("dsofhyisudf", new Date())
        }, 1000); // Simula um pequeno atraso na resposta */

        fetch('/api/get_response', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        // Enviamos o novo tema no corpo do pedido
                        body: JSON.stringify({ message: messageText, date: date })
                    })
                    .then(response => response.json())
                    .then(data => {
                  //  if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                        if (data.success) {
                            compute_assistant_message(
                            data.response,
                             new Date(data.timestamp) // <--- fallback seguro
                          );
                        } else {
                          compute_assistant_message(
                            "Erro: " + (data.response || "Resposta inválida"),
                            new Date()
                          );
                        }
                    })
                    .catch(error => {
                        compute_assistant_message(
                          "Erro de conexão com o servidor " + error,
                          new Date()
                        );
                    });

   /*     try {
        const response = await fetch('/api/get_response', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: messageText })
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const data = await response.json(); // <--- await adicionado aqui

        if (data.success) {
          compute_assistant_message(
            data.response,
             new Date(data.timestamp) // <--- fallback seguro
          );
        } else {
          compute_assistant_message(
            "Erro: " + (data.response || "Resposta inválida"),
            new Date()
          );
        }
      } catch (error) {
        compute_assistant_message(
          "Erro de conexão com o servidor " + error,
          new Date()
        );
      } */
      }
    }

function capture_audio() {
    const btn = document.getElementById('microphone-btn');
    //btn.disabled = true;
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US'; // Set language
    recognition.interimResults = false;

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      const chatInput = document.getElementById('chat-input');
      chatInput.value = transcript;
      //btn.disabled = false;
    };

    recognition.start();

}