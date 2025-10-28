import { appWindow } from "@tauri-apps/api/window";

document.addEventListener("DOMContentLoaded", () => {
    const bubble = document.getElementById("bubble");

    if (bubble) {
        // A forma mais robusta de arrastar a janela no Tauri
        bubble.addEventListener("mousedown", (e) => {
            // Previne que o evento de mousedown do React seja interrompido
            e.preventDefault();

            // Usa a função nativa do Tauri para iniciar o arrasto da janela
            appWindow.startDragging();
        });

        // clique (mantido para a funcionalidade futura de abrir o chat)
        bubble.addEventListener("click", () => {
            console.log("Bolha clicada");
            // Aqui depois abrimos o chat
        });

    } else {
        console.error("Elemento #bubble não encontrado. Verifique se o componente React foi renderizado.");
    }
});
