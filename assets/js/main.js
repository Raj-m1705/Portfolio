/*===== MENU SHOW =====*/ 
const showMenu = (toggleId, navId) =>{
    const toggle = document.getElementById(toggleId),
    nav = document.getElementById(navId)

    if(toggle && nav){
        toggle.addEventListener('click', ()=>{
            nav.classList.toggle('show')
        })
    }
}
showMenu('nav-toggle','nav-menu')

/*==================== REMOVE MENU MOBILE ====================*/
const navLink = document.querySelectorAll('.nav__link')

function linkAction(){
    const navMenu = document.getElementById('nav-menu')
    // When we click on each nav__link, we remove the show class
    navMenu.classList.remove('show')
}
navLink.forEach(n => n.addEventListener('click', linkAction))

/*==================== SCROLL SECTIONS ACTIVE LINK ====================*/
const sections = document.querySelectorAll('section[id]')

function scrollActive() {
  const scrollY = window.pageYOffset;

  // Remove active class from all first
  document.querySelectorAll('.nav__link').forEach(link =>
    link.classList.remove('active-link')
  );

  sections.forEach(current => {
    const sectionHeight = current.offsetHeight;
    const sectionTop = current.offsetTop - 60;
    const sectionId = current.getAttribute('id');

    if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
      const navLink = document.querySelector('.nav__menu a[href*=' + sectionId + ']');
      if (navLink) {
        navLink.classList.add('active-link');
      }
    }
  });
}
window.addEventListener('scroll', scrollActive)

/*=============== SCROLL REVEAL ANIMATION ===============*/
/*=============== SCROLL REVEAL ANIMATION ===============*/
/*=============== SCROLL REVEAL ANIMATION ===============*/
const sr = ScrollReveal({
  origin: 'top',
  distance: '40px',
  duration: 1000,
  delay: 150,
  reset: false // one-time animation
});

/* Section headers */
sr.reveal('.section-title', {origin: 'top'});

/* Home/About */
sr.reveal('.home__data, .home__img, .about__subtitle, .about__text', {interval: 100});

/* Competencies (all cards in one scroll, small stagger) */
sr.reveal('.skills__data', {
  interval: 100,
  origin: 'bottom'
});

/* Journey Timeline */
sr.reveal('.timeline-item', {
  interval: 150,
  origin: 'left'
});

/* Testimonials */
sr.reveal('.testimonial-card', {
  interval: 150,
  origin: 'right'
});
// ================== CONTACT FORM VALIDATION + EMAILJS ==================
document.addEventListener("DOMContentLoaded", () => {
  const contactForm = document.getElementById("contact-form");

  if (contactForm) {
    contactForm.addEventListener("submit", function(e) {
      e.preventDefault();

      const name = document.getElementById("name").value.trim();
      const email = document.getElementById("email").value.trim();
      const message = document.getElementById("message").value.trim();
      const honeypot = document.getElementById("honeypot").value;

      // 🛑 If honeypot is filled → it's a bot
      if (honeypot !== "") {
        console.warn("Spam detected, ignoring submission.");
        return;
      }

      // === Regex Validation ===
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

      // === Send via EmailJS ===
      emailjs.send("*", "*", {
        title: "Portfolio Contact",
        name: name,
        email: email,
        message: message
      })
      .then(() => {
        alert("✅ Message sent successfully!");
        contactForm.reset();
      })
      .catch((err) => {
        console.error("EmailJS error:", err);
        alert("❌ Failed to send message. Please try again later.");
      });
    });
  }
});
