/*=============== MENU SHOW/HIDE ===============*/
const showMenu = (toggleId, navId) => {
  const toggle = document.getElementById(toggleId),
        nav = document.getElementById(navId);

  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      nav.classList.toggle('show');
    });
  }
};
showMenu('nav-toggle','nav-menu');

/*=============== CLOSE MENU ON LINK CLICK (MOBILE) ===============*/
const navLinks = document.querySelectorAll('.nav__link');
navLinks.forEach(link => link.addEventListener('click', () => {
  document.getElementById('nav-menu').classList.remove('show');
}));

/*=============== MOBILE DROPDOWN TOGGLE ===============*/
document.querySelectorAll('.nav__dropdown > a').forEach(trigger => {
  trigger.addEventListener('click', e => {
    if (window.innerWidth <= 1024) {   // tablet & mobile
      e.preventDefault();
      trigger.parentElement.classList.toggle('open');
    }
  });
});

/*=============== SCROLL SECTIONS ACTIVE LINK ===============*/
const sections = document.querySelectorAll('section[id]');

function scrollActive() {
  const scrollY = window.pageYOffset;

  document.querySelectorAll('.nav__menu a').forEach(link =>
    link.classList.remove('active-link')
  );

  sections.forEach(current => {
    const sectionHeight = current.offsetHeight;
    const sectionTop = current.offsetTop - 60;
    const sectionId = current.getAttribute('id');

    if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
      const navLink = document.querySelector(`.nav__menu a[href*="${sectionId}"]`);
      if (navLink) navLink.classList.add('active-link');
    }
  });
}
window.addEventListener('scroll', scrollActive);

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
  if (!contactForm) return;

  contactForm.addEventListener("submit", function(e) {
    e.preventDefault();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const message = document.getElementById("message").value.trim();
    const honeypot = document.getElementById("honeypot").value;

    if (honeypot !== "") {
      console.warn("Spam detected, ignoring submission.");
      return;
    }

    const namePattern = /^[A-Za-z\s]{2,50}$/;
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}$/;
    const messagePattern = /^(?!.*(test|dummy|asdf|qwerty)).*[A-Za-z0-9]{3,}.*$/i;

    if (!namePattern.test(name)) {
      alert("⚠️ Please enter a valid full name (letters only).");
      return;
    }
    if (!emailPattern.test(email) || /(test|example|dummy)/i.test(email)) {
      alert("⚠️ Please enter a valid email.");
      return;
    }
    if (message.length < 10 || !messagePattern.test(message)) {
      alert("⚠️ Please enter a meaningful message (min 10 characters).");
      return;
    }

    emailjs.send("service_2fr3lod", "template_9a33lc3", {title: "Portfolio Contact", name, email, message})
      .then(() => { alert("✅ Message sent successfully!"); contactForm.reset(); })
      .catch((err) => { console.error("EmailJS error:", err); alert("❌ Failed to send message. Please try again later."); });
  });
});

/*=============== FLIPBOOK INIT ===============*/
const flipBook = (elBook) => {
  elBook.style.setProperty("--c", 0);
  elBook.querySelectorAll(".page").forEach((page, idx) => {
    page.style.setProperty("--i", idx);
    page.addEventListener("click", (evt) => {
      if (evt.target.closest("a")) return;
      const curr = evt.target.closest(".back") ? idx : idx + 1;
      elBook.style.setProperty("--c", curr);
    });
  });
};
document.querySelectorAll(".flipbook-section .book").forEach(flipBook);
