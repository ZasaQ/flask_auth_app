document.addEventListener("DOMContentLoaded", function () {
    const flashMessagesElement = document.getElementById("flash-messages-data");
    if (!flashMessagesElement) {
        console.error("Flash messages element not found!");
        return;
    }

    const flashMessages = JSON.parse(flashMessagesElement.textContent || "[]");

    if (flashMessages.length > 0) {
        let flashContent = '';

        flashMessages.forEach(msg => {
            flashContent += `<div class="alert alert-${msg[0]}">${msg[1]}</div>`;
        });

        const modalBody = document.getElementById("flashModalBody");
        if (modalBody) {
            modalBody.innerHTML = flashContent;

            const flashModal = new bootstrap.Modal(document.getElementById("flashModal"));
            flashModal.show();
        } else {
            console.error("Flash modal body element not found!");
        }
    }
});
