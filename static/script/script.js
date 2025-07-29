function setCookie(mode) {
        const route_str = mode ? '/accept_cookies' : '/reject_cookies';
        fetch(route_str, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        }
                    })
                    .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    document.getElementById('cookie-consent-banner').style.display = 'none';
                    return response.json();
                })
                .catch(error => {
                });
}

function changeLanguage(lang) {
        window.location.href = '/language/' + lang;
}

        function createParticle() {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + 'vw';
            particle.style.animationDuration = (Math.random() * 4 + 6) + 's';
            particle.style.animationDelay = Math.random() * 2 + 's';
            document.getElementById('particles').appendChild(particle);

            setTimeout(() => {
                if (particle.parentNode) {
                    particle.remove();
                }
            }, 10000);
        }

        // Create particles continuously
        setInterval(createParticle, 200);

       // const cv = document.getElementById('CV');
       // cv.onclick(function)

const en_text = [
    "I'm a Full Stack Developer",
    "I'm an Informatic Technician",
    "I'm a System Specialist",
    "I'm a Software Engineer"
];

const pt_text = [
    "Sou um Desenvolvedor Full Stack",
    "Sou técnico de Informatica",
    "Sou analista de sistemas",
    "Sou Desenvolvedor de software"
];

texts = en_text

function set_text(lang) {
    texts = lang ? en_text : pt_text;
}

let textIndex = 0;
let charIndex = 0;
let isDeleting = false;
let isPaused = false;
const typewriterElement = document.getElementById('typewriter');

function typeWriter() {
    if (isPaused) {
        setTimeout(typeWriter, 100); // Espera e tenta de novo
        return;
    }

    const current = texts[textIndex];

    if (isDeleting) {
        typewriterElement.textContent = current.substring(0, charIndex - 1);
        charIndex--;

        if (charIndex === 0) {
            isDeleting = false;
            textIndex = (textIndex + 1) % texts.length;
            setTimeout(typeWriter, 500);
            return;
        }
    } else {
        typewriterElement.textContent = current.substring(0, charIndex + 1);
        charIndex++;

        if (charIndex === current.length) {
            isDeleting = true;
            setTimeout(typeWriter, 2000);
            return;
        }
    }

    setTimeout(typeWriter, isDeleting ? 50 : 100);
}

// Começa após 1 segundo
setTimeout(typeWriter, 1000);

// Observer para pausar/resumir
const animateState = new IntersectionObserver(
    (entries) => {
        entries.forEach(entry => {
            isPaused = !entry.isIntersecting;
        });
    },
    { threshold: 0.1 }
);

animateState.observe(typewriterElement);

