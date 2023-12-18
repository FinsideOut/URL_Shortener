// Function to switch between modals
function switch_to_create_account() {
    $('#loginModal').modal('hide');
    $('#createAccountModal').modal('show');
}
function switch_to_login() {
    $('#createAccountModal').modal('hide');
    $('#loginModal').modal('show');
}