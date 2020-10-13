const Toast = {
    initialized: false,
    types: {
        info: ["#00c4ff", "#007fa5"],
        warrning: ["#fbff00", "#afb202"],
        error: ["#ff0000", "#b60000"],
        success: ["#0be12f", "#079f20"],
    },
    // style for the shadow dom
    styleSheet: `
            * {
                font-family: san-serif;
                font-size: 18px
            }
            .toast-container {
                position: fixed;
                right: 1%;
                width: auto;
                top: 2%;

            }
            .toast {
                border: 2px solid black;
                width: 250px;
                margin-left: -125px;
                background-color: #ddd;
                color: #000;
                border-radius: 2px;
                padding: 10px;
                z-index: 1;
                margin-bottom: 20px;
                position: relative;
                box-shadow: 1px 1px 10px 0px #00000094;
                transform: translateX(200%);
                opacity: 0;
                transition: all 0.5s cubic-bezier(0.95, -0.06, 0, 1.09);
            }
            .toast-visible {
                opacity: 1;
                transform: translateX(0);
            }
            .close {
                position: absolute;
                top: 0;
                right: 0;
                margin: 5px;
                cursor: pointer;
            }
            .title {
                margin-bottom: 15px;
            }
            `,
    init() {
        // on callin a toast for the first time, set up shadow dom and container
        if (!this.initialized) {
            // creating element to hold shadow dom
            let shadow = document.createElement("div");
            shadow.style.position = "absolute";
            shadow.className = "shadow";
            shadow.attachShadow({ mode: "open" });

            // adding toast style to shadow dom
            let style = document.createElement("style");
            style.innerHTML = this.styleSheet;
            shadow.shadowRoot.appendChild(style);

            // adding the shadow comtainer to page
            document.body.appendChild(shadow);

            // creating and adding the toast container to the shadow element
            let newContainer = document.createElement("div");
            newContainer.className = "toast-container";
            shadow.shadowRoot.appendChild(newContainer);
            this.container = newContainer;
            this.initialized = true;
        }
    },
    show(type, message, duration) {
        // run only once
        this.init();

        // create a new toast with passed params and adds it to toast container
        let toast = this.newToast(type, message, duration);
        this.container.appendChild(toast);

        // timing of entrance animation for the toast
        setTimeout(() => {
            toast.classList.add("toast-visible");
        }, 0);
    },
    // create a new toast element and returns it
    newToast(type, message, duration) {
        // type of toast to set styling and title
        const toastType = type || "info";

        // duration of visibilty either as passed or infinite (-1)
        const toastDuration = duration || -1;

        let toast = document.createElement("div");
        toast.classList.add("toast");
        toast.innerHTML = `<div class="title">${toastType}!</div>
                <div class="close">&#10006;</div>
                <div>${message}</div>`;

        // adding close functionality to x button
        toast.querySelector(".close").addEventListener("click", () => {
            toast.classList.remove("toast-visible");
            this.removeToast(toast);
        });

        // applying type style
        toast.style.backgroundColor = this.types[type][0];
        toast.style.borderColor = this.types[type][1];

        if (toastDuration > 0) {
            setTimeout(() => {
                toast.classList.remove("toast-visible");
                this.removeToast(toast);
            }, duration * 1000);
        }
        return toast;
    },

    // animation timing for exiting toast
    removeToast(toast) {
        setTimeout(() => {
            toast.remove();
        }, 500);
    },
};
