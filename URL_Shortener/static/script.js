import validator from 'validator';

const btn_switch_to_register = document.getElementById("switch_to_register_modal")
const btn_switch_to_login = document.getElementById("switch_to_login_modal")
const login_modal = document.getElementById("loginModal")
const register_modal = document.getElementById("createAccountModal")


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


    var valid = validator.isEmail("hello")
    console.log(valid)

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
btn_switch_to_register.addEventListener("click", function () {
    $("#loginModal").modal("hide");
    $("#createAccountModal").modal("show");
});

btn_switch_to_login.addEventListener("click", function () {
    $("#createAccountModal").modal("hide");
    $("#loginModal").modal("show");
});

