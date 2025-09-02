/*===== MENU SHOW =====*/ 
const showMenu = (toggleId, navId) => {
  const toggle = document.getElementById(toggleId),
        nav = document.getElementById(navId);

  if(toggle && nav){
    toggle.addEventListener('click', () => {
      nav.classList.toggle('show');
    });
  }
}
showMenu('nav-toggle','nav-menu');

/*==================== REMOVE MENU MOBILE ====================*/
const navLink = document.querySelectorAll('.nav__link');

function linkAction(){
  const navMenu = document.getElementById('nav-menu');
  // When we click on each nav__link, we remove the show class
  navMenu.classList.remove('show');
}
navLink.forEach(n => n.addEventListener('click', linkAction));

/*==================== MOBILE DROPDOWN TOGGLE ====================*/
document.querySelectorAll('.nav__lin').forEach(link => {
  link.addEventListener('click', function(e) {
    if(window.innerWidth <= 767){
      e.preventDefault(); // prevent jump
      const dropdown = this.nextElementSibling;
      dropdown.classList.toggle('active'); // toggle class instead of style
    }
  });
});

/*==================== SCROLL SECTIONS ACTIVE LINK ====================*/
const sections = document.querySelectorAll('section[id]');

function scrollActive() {
  const scrollY = window.pageYOffset;

  document.querySelectorAll('.nav__link').forEach(link =>
    link.classList.remove('active-link')
  );

  sections.forEach(current => {
    const sectionHeight = current.offsetHeight;
    const sectionTop = current.offsetTop - 60;
    const sectionId = current.getAttribute('id');

    if(scrollY >= sectionTop && scrollY < sectionTop + sectionHeight){
      const navLink = document.querySelector('.nav__menu a[href*=' + sectionId + ']');
      if(navLink){
        navLink.classList.add('active-link');
      }
    }
  });
}
window.addEventListener('scroll', scrollActive);

/*==================== DROPDOWN MOBILE CLICK ====================*/
// Select all dropdown parent links
const dropdowns = document.querySelectorAll('.nav__dropdown > .nav__link');

dropdowns.forEach(drop => {
  drop.addEventListener('click', function(e) {
    e.preventDefault(); // Prevent the default link action

    // Toggle the dropdown menu
    const menu = this.nextElementSibling;
    menu.classList.toggle('show-dropdown');
  });
});


/*=============== SCROLL REVEAL ANIMATION ===============*/
const sr = ScrollReveal({
  origin: 'top',
  distance: '40px',
  duration: 1000,
  delay: 150,
  reset: false
});

sr.reveal('.section-title', {origin: 'top'});
sr.reveal('.home__data, .home__img, .about__subtitle, .about__text', {interval: 100});
sr.reveal('.skills__data', {interval: 100, origin: 'bottom'});
sr.reveal('.timeline-item', {interval: 150, origin: 'left'});
sr.reveal('.testimonial-card', {interval: 150, origin: 'right'});

/*=============== CONTACT FORM VALIDATION + EMAILJS ===============*/
document.addEventListener("DOMContentLoaded", () => {
  const contactForm = document.getElementById("contact-form");
  if(contactForm){
    contactForm.addEventListener("submit", function(e){
      e.preventDefault();

      const name = document.getElementById("name").value.trim();
      const email = document.getElementById("email").value.trim();
      const message = document.getElementById("message").value.trim();
      const honeypot = document.getElementById("honeypot").value;

      if(honeypot !== ""){
        console.warn("Spam detected, ignoring submission.");
        return;
      }

      const namePattern = /^[A-Za-z\s]{2,50}$/;
      const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}$/;
      const messagePattern = /^(?!.*(test|dummy|asdf|qwerty)).*[A-Za-z0-9]{3,}.*$/i;

      if(!namePattern.test(name)){
        alert("⚠️ Please enter a valid full name (letters only).");
        return;
      }
      if(!emailPattern.test(email) || /(test|example|dummy)/i.test(email)){
        alert("⚠️ Please enter a valid email.");
        return;
      }
      if(message.length < 10 || !messagePattern.test(message)){
        alert("⚠️ Please enter a meaningful message (min 10 characters).");
        return;
      }

      emailjs.send("*", "*", {title: "Portfolio Contact", name, email, message})
        .then(() => { alert("✅ Message sent successfully!"); contactForm.reset(); })
        .catch((err) => { console.error("EmailJS error:", err); alert("❌ Failed to send message. Please try again later."); });
    });
  }
});
const flipBook = (elBook) => {
  // Initialize current page
  elBook.style.setProperty("--c", 0);

  // Set index for each page and add click listener
  elBook.querySelectorAll(".page").forEach((page, idx) => {
    page.style.setProperty("--i", idx);

    page.addEventListener("click", (evt) => {
      // Ignore clicks on links
      if (evt.target.closest("a")) return;

      // If back side clicked, set current to idx, else idx + 1
      const curr = evt.target.closest(".back") ? idx : idx + 1;
      elBook.style.setProperty("--c", curr);
    });
  });
};

// Only target books inside .flipbook-section
document.querySelectorAll(".flipbook-section .book").forEach(flipBook);
