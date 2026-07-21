function showToast(message, type = "success") {

    const toastElement = document.getElementById("app-toast");
    const toastBody = document.getElementById("app-toast-body");

    toastBody.textContent = message;

    toastElement.className =
        "toast align-items-center border-0 text-white";

    switch (type) {

        case "success":
            toastElement.classList.add("bg-success");
            break;

        case "warning":
            toastElement.classList.add("bg-warning");
            break;

        case "danger":
            toastElement.classList.add("bg-danger");
            break;

        default:
            toastElement.classList.add("bg-primary");

    }

    const toast = bootstrap.Toast.getOrCreateInstance(toastElement);

    toast.show();

}