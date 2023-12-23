// import validator from 'validator';

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

const login_form = document.getElementById("login_form")
const login_email = document.getElementById("login_email")
const login_password = document.getElementById("login_password")
const login_inputs = [login_email, login_password];

// URL FORM
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("url_form").addEventListener("submit", function (event) {
        event.preventDefault();
        var formData = new FormData(this);
        fetch("/url_submit", {
            method: "POST",
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log("Success!")
                    // window.location.href = "/";
                    document.getElementById("quote").textContent = data.quote;
                    document.getElementById("author").textContent = data.author;
                    document.getElementById("url_result").textContent = data.result;

                } else {
                    write_errors(this, data.errors);
                }
            })
            .catch(error => console.error("Error:", error));
    });
});

// REGISTER FORM
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("register_form").addEventListener("submit", function (event) {
        event.preventDefault();
        var formData = new FormData(this);
        fetch("/register_submit", {
            method: "POST",
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = "/";
                } else {
                    write_errors(this, data.errors);
                }
            })
            .catch(error => console.error("Error:", error));
    });
});

// LOGING FORM
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("login_form").addEventListener("submit", function (event) {
        event.preventDefault();
        var formData = new FormData(this);
        fetch("/login_submit", {
            method: "POST",
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                console.log(data)
                if (data.success) {
                    window.location.href = "/";
                } else {
                    write_errors(this, data.errors);
                }
            })
            .catch(error => console.error("Error:", error));
    });
});

function write_errors(form, errors) {
    form.querySelectorAll(".invalid-feedback").forEach(element => element.remove());
    form.querySelectorAll(".is-invalid").forEach(element => element.classList.remove("is-invalid"));
    Object.keys(errors).forEach(function (key) {
        var value = errors[key];
        if (value.length !== 0) {
            var input = document.getElementById(form.id.split("_")[0] + "_" + key);
            input.classList.add("is-invalid");
            value.forEach(item => {
                var new_error = document.createElement('div');
                new_error.classList.add("invalid-feedback");
                new_error.textContent = item;
                input.parentNode.insertBefore(new_error, input.nextSibling);
            })

        }
    });
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


// login_form.addEventListener("submit", async (event) => {
//     console.log("clicked")
//     event.preventDefault();
//     var errors = presence_check(login_inputs);
//     try {
//         // make call to flask route
//         var response = await fetch('/submit-login', {
//             method: "GET",
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//         });
//         if (!response.ok) {
//             throw new Error(`HTTP error! Status: ${response.status}`);
//         }

//         // get data and add errors if exist
//         var data = await response.json();
//         if (data.username === false) {
//             errors.push({ "input": login_email, "error": "There is no account with this email" })
//         }
//         else if (data.password === false) {
//             errors.push({ "input": login_password, "error": "Incorrect Password" })
//         }

//         // either write feedback elements or submit form
//         if (errors.length !== 0) {
//             event.preventDefault();
//             write_errors(register_form, errors);
//             return false;
//         } else {
//             event.currentTarget.submit();
//         }
//     }
//     catch (error) {
//         console.error('Error:', error);
//     };
// })

// register_form.addEventListener("submit", (event) => {
//     // presence check for all fields
//     var errors = presence_check(register_inputs);
//     // emails
//     if (!validator.isEmail(register_email.value)) {
//         errors.push({ "input": register_email, "error": "Please enter a valid email address" })
//     } else {
//         // CHeck if email exists in db
//         console.log("fetch database check")
//         fetch('/submit-registration', {
//             method: "GET",
//             headers: {
//                 'Content-Type': 'application/json'
//                 // You can add additional headers if needed
//             },
//         })
//             .then(response => response.json())
//             .then(data => {
//                 if (data.value === true) {
//                     errors.push({ "input": register_email, "error": "There is already an account with this email" })
//                 }
//             })
//             .catch(error => {
//                 console.error('Error:', error);
//             });
//     }

//     // passwords
//     if (!validator.isStrongPassword(register_password.value)) {
//         errors.push({ "input": register_password, "error": "Your password is not strong enough" })
//     }
//     if (register_password.value !== register_confirm_password.value) {
//         errors.push({ "input": register_confirm_password, "error": "Passwords must match exactly" })
//     }

//     // either write feedback elements or submit form
//     if (errors.length !== 0) {
//         event.preventDefault();
//         write_errors(register_form, errors);
//         return false;
//     } else {
//         event.currentTarget.submit();
//     }

// })



// function presence_check(inputs) {
//     var errors = []
//     inputs.forEach(input => {
//         if (input.value === "") {
//             var error = { "input": input, "error": "This field is required" }
//             errors.push(error);
//         }
//     })
//     return errors
// }

// function write_errors(form, errors) {
//     // remove previous errors
//     form.querySelectorAll(".invalid-feedback").forEach(element => element.remove());
//     register_form.querySelectorAll(".is-invalid").forEach(element => element.classList.remove("is-invalid"));

//     errors.forEach(error => {
//         // input styling
//         error.input.classList.add("is-invalid");
//         // add list of errors in divs
//         var new_error = document.createElement("div");
//         new_error.classList.add("invalid-feedback");
//         var new_error_text = document.createTextNode(error.error);
//         new_error.appendChild(new_error_text);
//         error.input.parentElement.appendChild(new_error);
//     })
// }



