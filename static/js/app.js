//  Login and Sign Up Modal JavaScript
const modal = document.getElementById("signup-modal");
const openBtn = document.querySelector(".main-btn");
const closeSignupBtn = document.querySelector(".close-btn");

const loginModal = document.getElementById("login-modal");
const openLoginBtn = document.querySelector(".modal-input-login");
const openSignupBtn = document.querySelector(".modal-input-signup");
const closeLoginBtn = document.querySelector(".close-login-btn");

const passModal = document.getElementById("pass-modal");
const openPassBtn = document.querySelector(".modal-input-pass");
const closePassBtn = document.querySelector(".close-pass-btn");

//CLick Events
openBtn.addEventListener("click", () => {
  modal.style.display = "block";
});

closeSignupBtn.addEventListener("click", () => {
  modal.style.display = "none";
});

window.addEventListener("click", (e) => {
  if (e.target == modal) {
    modal.style.display = "none";
  }
});

openLoginBtn.addEventListener("click", () => {
  modal.style.display = "none";
  loginModal.style.display = "block";
});

window.addEventListener("click", (e) => {
  if (e.target == loginModal) {
    loginModal.style.display = "none";
    modal.style.display = "none";
  }
});

openSignupBtn.addEventListener("click", () => {
  loginModal.style.display = "none";
  modal.style.display = "block";
});

closeLoginBtn.addEventListener("click", () => {
  loginModal.style.display = "none";
});

// Password Reset Modal
openPassBtn.addEventListener('click', () => {
  passModal.style.display = 'block';
});

closePassBtn.addEventListener("click", () => {
  passModal.style.display = "none";
});
