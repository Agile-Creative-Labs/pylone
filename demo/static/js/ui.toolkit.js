class PyloneUI 
{
    constructor()
    {
        this.init();
    }

    init() 
    {
        // Create the container for notifications/dialogs
        this.container = document.createElement("div");
        this.container.id = "pylone-ui-container";
        document.body.appendChild(this.container);
        // Apply Apple-style aesthetics
        Object.assign(this.container.style, {
            position: "fixed",
            top: "20px",
            right: "20px",
            display: "flex",
            flexDirection: "column",
            gap: "10px",
            zIndex: "9999",
            pointerEvents: "none" // Prevent interference with other UI elements
        });
    }

    showToast(message, { type = "info", duration = 3000 } = {})
    {
        const toast = document.createElement("div");
        toast.classList.add("pylone-toast", `pylone-toast-${type}`);
        toast.innerText = message;
        
        Object.assign(toast.style, {
            background: this.getColor(type),
            color: "white",
            padding: "12px 16px",
            borderRadius: "12px",
            fontSize: "14px",
            fontWeight: "500",
            boxShadow: "0 8px 16px rgba(0, 0, 0, 0.15)",
            opacity: "0",
            transform: "translateY(-10px)",
            transition: "opacity 0.3s ease, transform 0.3s ease",
            pointerEvents: "auto", // Allow interaction with notifications
            maxWidth: "300px"
        });
        
        this.container.appendChild(toast);
        
        // Trigger fade-in effect
        requestAnimationFrame(() => {
            toast.style.opacity = "1";
            toast.style.transform = "translateY(0)";
        });

        // Auto-remove after duration
        setTimeout(() => this.removeToast(toast), duration);
    }

    removeToast(toast) 
    {
        toast.style.opacity = "0";
        toast.style.transform = "translateY(-10px)";
        setTimeout(() => toast.remove(), 300); // Allow transition time before removal
    }

    getColor(type) 
    {
        switch (type) 
        {
            case "success": return "#4CAF50"; // Apple-style green
            case "error": return "#FF3B30"; // Apple-style red
            case "warning": return "#FF9500"; // Apple-style orange
            default: return "#007AFF"; // Apple-style blue
        }
    }
    
    xshowNotification(message, type = "info", duration = 3000) 
    {
        const notification = document.createElement("div");
        notification.className = `pylone-notification pylone-${type}`;
        notification.textContent = message;
        
        this.container.appendChild(notification);

        setTimeout(() => {
            notification.classList.add("fade-out");
            setTimeout(() => notification.remove(), 500);
        }, duration);
    }

    showNotification(message, type = "info", duration = 3000) 
    {
        let container = document.getElementById("pylone-ui-container");

        // Create container if not exists
        if (!container) {
            container = document.createElement("div");
            container.id = "pylone-ui-container";
            document.body.appendChild(container);
        }

        // Create notification element
        let notification = document.createElement("div");
        notification.classList.add("pylone-toast", `pylone-toast-${type}`);
        notification.innerText = message;

        // Append to container
        container.appendChild(notification);

        // Animate into view
        setTimeout(() => {
            notification.style.opacity = "1";
            notification.style.transform = "translateY(0)";
        }, 10);

        // Auto-remove notification
        setTimeout(() => {
            notification.style.opacity = "0";
            notification.style.transform = "translateY(-10px)";
            setTimeout(() => notification.remove(), 300); // Ensure smooth removal
        }, duration);
    }

    showAlert(message, callback = null) 
    {
        this.createDialog("Alert", message, [{ text: "OK", action: callback }]);
    }

    showConfirm(message, onConfirm, onCancel = null) 
    {
        this.createDialog("Confirm", message, [
            { text: "Cancel", action: onCancel },
            { text: "OK", action: onConfirm }
        ]);
    }

    showPrompt(message, onSubmit, placeholder = "") 
    {
        this.createDialog("Prompt", message, [
            { text: "Cancel", action: null },
            { text: "Submit", action: (input) => onSubmit(input) }
        ], true, placeholder);
    }

    createDialog(title, message, buttons, hasInput = false, placeholder = "") 
    {
        const overlay = document.createElement("div");
        overlay.className = "pylone-dialog-overlay";
        
        const dialog = document.createElement("div");
        dialog.className = "pylone-dialog";
        
        const header = document.createElement("h3");
        header.textContent = title;
        
        const body = document.createElement("p");
        body.textContent = message;
        
        let inputField = null;
        if (hasInput) {
            inputField = document.createElement("input");
            inputField.type = "text";
            inputField.placeholder = placeholder;
            dialog.appendChild(inputField);
        }
        
        const buttonContainer = document.createElement("div");
        buttonContainer.className = "pylone-dialog-buttons";
        
        buttons.forEach(({ text, action }) => {
            const button = document.createElement("button");
            button.textContent = text;
            button.onclick = () => {
                if (action) action(inputField ? inputField.value : null);
                overlay.remove();
            };
            buttonContainer.appendChild(button);
        });
        
        dialog.append(header, body, buttonContainer);
        overlay.appendChild(dialog);
        document.body.appendChild(overlay);
    }
}
// Auto-initialize PyloneUI
//const Pylone = new PyloneUI();
document.addEventListener("DOMContentLoaded", () => 
{
    window.Pylone = new PyloneUI(); // Ensure global access
});
