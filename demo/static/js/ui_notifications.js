class PyloneUI {
    constructor() {
        this.initContainer();
    }

    initContainer() {
        this.container = document.createElement("div");
        this.container.id = "pylone-toast-container";
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

    showToast(message, { type = "info", duration = 3000 } = {}) {
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

    removeToast(toast) {
        toast.style.opacity = "0";
        toast.style.transform = "translateY(-10px)";
        setTimeout(() => toast.remove(), 300); // Allow transition time before removal
    }

    getColor(type) {
        switch (type) {
            case "success": return "#4CAF50"; // Apple-style green
            case "error": return "#FF3B30"; // Apple-style red
            case "warning": return "#FF9500"; // Apple-style orange
            default: return "#007AFF"; // Apple-style blue
        }
    }
}

// Initialize the UI system
document.addEventListener("DOMContentLoaded", () => {
    window.pyloneUI = new PyloneUI();
});
