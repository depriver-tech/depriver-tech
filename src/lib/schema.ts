// Structured data (schema.org JSON-LD) so search engines and AI assistants understand who Privatus is.
import { services, contact } from "../data/story";

const SITE = "https://depriver.tech";

export const personJsonLd = {
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": `${SITE}/#person`,
  name: "Privatus Cosmas",
  alternateName: ["Priver", "Privatus", "depriver", "@_depriver"],
  url: `${SITE}/about/`,
  image: `${SITE}/img/me-cut.webp`,
  jobTitle: "Software Engineer",
  description:
    "Privatus Cosmas, also known as Priver, is a software engineer from Kagera, based in Mbeya, Tanzania. Builds web and mobile apps, SaaS and business systems, systems integrations and data dashboards, and uses technology to solve community problems.",
  birthPlace: { "@type": "Place", name: "Kyerwa, Kagera, Tanzania" },
  homeLocation: { "@type": "Place", address: { "@type": "PostalAddress", addressLocality: "Mbeya", addressRegion: "Mbeya", addressCountry: "TZ" } },
  nationality: { "@type": "Country", name: "Tanzania" },
  alumniOf: [
    { "@type": "CollegeOrUniversity", name: "Mbeya University of Science and Technology (MUST)", sameAs: "https://www.must.ac.tz" },
    { "@type": "HighSchool", name: "Kaisho Secondary School" },
  ],
  hasCredential: { "@type": "EducationalOccupationalCredential", credentialCategory: "Diploma", name: "Diploma in Computer Science" },
  knowsLanguage: ["English", "Swahili"],
  knowsAbout: [
    "Software engineering", "Web development", "Mobile app development", "SaaS", "Business systems", "Systems integration",
    "Data analysis", "Dashboards", "Cloud computing", "DevOps", "Artificial intelligence", "Python", "JavaScript", "React",
    "Flutter", "Django", "AWS", "Computer hardware", "Multimedia", "Digital innovation", "Technology for social good",
  ],
  makesOffer: services.map((s) => ({ "@type": "Offer", itemOffered: { "@type": "Service", name: s.title, description: s.body, areaServed: ["Tanzania", "East Africa", "Remote"] } })),
  telephone: contact.phone,
  sameAs: [contact.githubHref, contact.instagramHref],
};

export const websiteJsonLd = {
  "@context": "https://schema.org",
  "@type": "WebSite",
  "@id": `${SITE}/#website`,
  url: SITE,
  name: "Privatus Cosmas",
  alternateName: ["Priver", "depriver.tech"],
  description: "Software engineering and practical tech lessons by Privatus Cosmas (Priver), a software engineer in Mbeya, Tanzania.",
  inLanguage: "en",
  author: { "@id": `${SITE}/#person` },
  publisher: { "@id": `${SITE}/#person` },
};
