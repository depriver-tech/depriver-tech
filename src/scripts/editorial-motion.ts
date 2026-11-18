import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.registerPlugin(ScrollTrigger);

// Progressive enhancement: content stays visible if scripts or motion are unavailable.
const media = gsap.matchMedia();
media.add("(prefers-reduced-motion: no-preference)", () => {
  const lines = document.querySelectorAll("[data-hero-line]");
  if (lines.length) gsap.from(lines, { yPercent: 115, rotate: 2, duration: 1.15, stagger: .13, ease: "power4.out", delay: .12 });
  gsap.utils.toArray<HTMLElement>("[data-photo-reveal]").forEach((photo) => {
    gsap.from(photo, { clipPath: "inset(10% 0 10% 0 round 12px)", opacity: 0, y: 35, duration: 1.2, ease: "power3.out", scrollTrigger: { trigger: photo, start: "top 94%", once: true } });
  });
  const groups = [".start-here", ".journal-heading", ".details", ".service-grid"];
  groups.forEach((selector) => document.querySelectorAll(selector).forEach((group) => {
    gsap.from(group.children, { opacity: 0, y: 28, duration: .85, stagger: .12, ease: "power3.out", scrollTrigger: { trigger: group, start: "top 90%", once: true } });
  }));
  // Small depth changes only on devices with a precise pointer.
  if (matchMedia("(hover: hover) and (pointer: fine)").matches) {
    document.querySelectorAll<HTMLElement>(".portrait-frame, .journal-photos figure").forEach((photo) => {
      const img = photo.querySelector("img");
      if (!img) return;
      gsap.fromTo(img, { scale: 1.06, yPercent: -2 }, { yPercent: 2, ease: "none", scrollTrigger: { trigger: photo, start: "top bottom", end: "bottom top", scrub: 1 } });
      photo.addEventListener("pointermove", (event) => {
        const rect = photo.getBoundingClientRect();
        gsap.to(photo, { rotateY: ((event.clientX - rect.left) / rect.width - .5) * 3, rotateX: -((event.clientY - rect.top) / rect.height - .5) * 3, transformPerspective: 1000, duration: .6, ease: "power2.out" });
      });
      photo.addEventListener("pointerleave", () => gsap.to(photo, { rotateY: 0, rotateX: 0, duration: .8, ease: "power3.out" }));
    });
  }
});

// Photographic chapters overlap through native sticky layout; scrolling remains native.
media.add("(prefers-reduced-motion: no-preference)", () => {
  const home = document.querySelector(".cosmic-home");
  if (!home) return;
  gsap.from("[data-launch-copy]", { opacity: 0, y: 22, duration: 1, stagger: .12, delay: .35, ease: "power3.out" });
  gsap.from(".launch-person", { scale: 1.12, opacity: 0, duration: 1.8, ease: "power2.out" });
  gsap.to(".launch-glow", { scale: 1.15, xPercent: 4, duration: 8, repeat: -1, yoyo: true, ease: "sine.inOut" });
  gsap.to(".launch-copy", { y: -65, opacity: .2, ease: "none", scrollTrigger: { trigger: ".launch-hero", start: "top top", end: "bottom 25%", scrub: true } });
  const scenes = gsap.utils.toArray<HTMLElement>("[data-scene]");
  scenes.forEach((scene, index) => {
    const image = scene.querySelector(".scene-media img");
    const copy = scene.querySelector(".scene-copy");
    gsap.fromTo(image, { scale: 1.15 }, { scale: 1, ease: "none", scrollTrigger: { trigger: scene, start: "top bottom", end: "top top", scrub: 1 } });
    gsap.from(copy, { opacity: 0, y: 65, duration: 1.2, ease: "power3.out", scrollTrigger: { trigger: scene, start: "top 65%", once: true } });
    if (index > 0) {
      gsap.fromTo(scene, { clipPath: "inset(10% 3% 0 round 30px)" }, { clipPath: "inset(0% 0% 0 round 0px)", ease: "none", scrollTrigger: { trigger: scene, start: "top 85%", end: "top top", scrub: true } });
    }
  });
  gsap.from(".build-paths > a", { y: 35, opacity: 0, stagger: .12, duration: .9, ease: "power3.out", scrollTrigger: { trigger: ".build-paths", start: "top 90%", once: true } });
});

// Tactile cards: a small tilt and local specular highlight, never on touch devices.
media.add("(prefers-reduced-motion: no-preference) and (hover: hover) and (pointer: fine)", () => {
  const disposers: Array<() => void> = [];
  document.querySelectorAll<HTMLElement>(".post, .duo-card, .build-paths > a, .launch-tracks > a").forEach((card) => {
    const move = (event: PointerEvent) => {
      const rect = card.getBoundingClientRect();
      const x = (event.clientX - rect.left) / rect.width;
      const y = (event.clientY - rect.top) / rect.height;
      card.style.setProperty("--shine-x", `${x * 100}%`);
      card.style.setProperty("--shine-y", `${y * 100}%`);
      gsap.to(card, { rotateX: (0.5 - y) * 7, rotateY: (x - 0.5) * 7, y: -5, transformPerspective: 1000, duration: .45, ease: "power2.out", overwrite: "auto" });
    };
    const leave = () => gsap.to(card, { rotateX: 0, rotateY: 0, y: 0, duration: .7, ease: "elastic.out(1, .55)", overwrite: "auto" });
    card.addEventListener("pointermove", move);
    card.addEventListener("pointerleave", leave);
    disposers.push(() => { card.removeEventListener("pointermove", move); card.removeEventListener("pointerleave", leave); });
  });
  return () => disposers.forEach((dispose) => dispose());
});

media.add("(prefers-reduced-motion: no-preference)", () => {
  gsap.from(".nav-in", { y: -30, duration: .9, ease: "power3.out", delay: .1 });
  gsap.utils.toArray<HTMLElement>(".service-sculpture").forEach((sculpture, index) => {
    gsap.from(sculpture.children, { y: 35, opacity: 0, rotateY: -25, duration: 1.1, stagger: .12, ease: "back.out(1.4)", scrollTrigger: { trigger: sculpture, start: "top 93%", once: true } });
    gsap.to(sculpture, { y: -8, duration: 2.8 + index * .4, yoyo: true, repeat: -1, ease: "sine.inOut", scrollTrigger: { trigger: sculpture, start: "top bottom", end: "bottom top", toggleActions: "play pause resume pause" } });
  });
});
