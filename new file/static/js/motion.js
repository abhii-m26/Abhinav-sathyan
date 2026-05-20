const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

function setupPageMotion() {
    document.body.classList.add("is-loading");
    requestAnimationFrame(() => document.body.classList.add("is-ready"));

    window.addEventListener("load", () => {
        setTimeout(() => document.body.classList.add("loader-complete"), 450);
    });

    document.querySelectorAll("a[href]").forEach((link) => {
        const url = new URL(link.href, window.location.href);
        const isSameSite = url.origin === window.location.origin;
        const isHash = link.getAttribute("href").startsWith("#");
        if (!isSameSite || isHash || link.target) return;

        link.addEventListener("click", (event) => {
            if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
            event.preventDefault();
            document.body.classList.add("page-leaving");
            setTimeout(() => {
                window.location.href = link.href;
            }, prefersReducedMotion ? 0 : 260);
        });
    });
}

function setupRevealMotion() {
    const targets = document.querySelectorAll(
        ".hero-copy, .hero-panel, .luxury-strip span, .showcase-copy, .showcase-stage, .floating-product, .section-heading, .product-card, .craft-card, .filters, .summary, .form-panel, .cart-row"
    );
    targets.forEach((target) => target.classList.add("motion-reveal"));

    if (prefersReducedMotion || !("IntersectionObserver" in window)) {
        targets.forEach((target) => target.classList.add("is-visible"));
        return;
    }

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.14, rootMargin: "0px 0px -8% 0px" }
    );

    targets.forEach((target, index) => {
        target.style.setProperty("--reveal-delay", `${Math.min(index * 34, 260)}ms`);
        observer.observe(target);
    });
}

function setupCursorLight() {
    const light = document.querySelector(".cursor-light");
    if (!light || prefersReducedMotion) return;

    let targetX = window.innerWidth / 2;
    let targetY = window.innerHeight / 2;
    let currentX = targetX;
    let currentY = targetY;

    window.addEventListener("pointermove", (event) => {
        targetX = event.clientX;
        targetY = event.clientY;
        document.documentElement.style.setProperty("--cursor-x", `${targetX}px`);
        document.documentElement.style.setProperty("--cursor-y", `${targetY}px`);
    });

    function animate() {
        currentX += (targetX - currentX) * 0.12;
        currentY += (targetY - currentY) * 0.12;
        light.style.transform = `translate3d(${currentX}px, ${currentY}px, 0) translate(-50%, -50%)`;
        requestAnimationFrame(animate);
    }

    animate();
}

function setupParallax() {
    if (prefersReducedMotion) return;

    const parallaxItems = document.querySelectorAll(".paper-layer, .metal-line, .glass-orbit, .hero-panel");
    let ticking = false;

    function update() {
        const y = window.scrollY;
        parallaxItems.forEach((item, index) => {
            const depth = (index + 1) * 0.018;
            item.style.setProperty("--scroll-lift", `${y * depth}px`);
        });
        ticking = false;
    }

    window.addEventListener(
        "scroll",
        () => {
            if (!ticking) {
                requestAnimationFrame(update);
                ticking = true;
            }
        },
        { passive: true }
    );
}

function setupProductPhysics() {
    if (prefersReducedMotion) return;

    document.querySelectorAll(".product-card").forEach((card) => {
        card.addEventListener("pointermove", (event) => {
            const rect = card.getBoundingClientRect();
            const x = (event.clientX - rect.left) / rect.width - 0.5;
            const y = (event.clientY - rect.top) / rect.height - 0.5;
            card.style.setProperty("--tilt-x", `${(-y * 5).toFixed(2)}deg`);
            card.style.setProperty("--tilt-y", `${(x * 6).toFixed(2)}deg`);
            card.style.setProperty("--shine-x", `${((x + 0.5) * 100).toFixed(1)}%`);
            card.style.setProperty("--shine-y", `${((y + 0.5) * 100).toFixed(1)}%`);
        });

        card.addEventListener("pointerleave", () => {
            card.style.setProperty("--tilt-x", "0deg");
            card.style.setProperty("--tilt-y", "0deg");
            card.style.setProperty("--shine-x", "50%");
            card.style.setProperty("--shine-y", "20%");
        });
    });
}

document.addEventListener("DOMContentLoaded", () => {
    setupPageMotion();
    setupRevealMotion();
    setupCursorLight();
    setupParallax();
    setupProductPhysics();
});
