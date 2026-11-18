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
