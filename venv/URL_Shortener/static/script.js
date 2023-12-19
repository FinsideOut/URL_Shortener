const register_form = document.getElementById("register_form")
const register_username = document.getElementById("register_username")
const register_email = document.getElementById("register_email")
const register_password = document.getElementById("register_password")
const register_confirm_password = document.getElementById("register_confirm_password")

const register_inputs = [register_username, register_email, register_password, register_confirm_password];

register_form.addEventListener("submit", function check_form(event) {
    event.preventDefault();
    var errors = [];

    // presence check for all fields
    register_inputs.forEach(input => {
        if (input.value === "") {
            var error = { "input": input, "error": "This field is required" }
            errors.push(error);
        }
    })
    write_errors(errors);
})

function write_errors(errors) {
    // remove previous errors
    register_form.querySelectorAll(".invalid-feedback").forEach(element => element.remove());
    register_form.querySelectorAll(".is-invalid").forEach(element => element.classList.remove("is-invalid"));

    errors.forEach(error => {
        // input styling
        error.input.classList.add("is-invalid");
        // add list of errors in divs
        var new_error = document.createElement("div");
        new_error.classList.add("invalid-feedback");
        var new_error_text = document.createTextNode(error.error);
        new_error.appendChild(new_error_text);
        error.input.parentElement.appendChild(new_error);
    })
}


// Function to switch between modals
function switch_to_create_account() {
    $('#loginModal').modal('hide');
    $('#createAccountModal').modal('show');
}
function switch_to_login() {
    $('#createAccountModal').modal('hide');
    $('#loginModal').modal('show');
}

