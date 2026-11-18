// Free guides and books (PDF). Files live in public/guides/: <slug>.pdf plus <slug>/cover.webp and preview pages,
// exported from studio/<slug>-guide or similar with the PIL book builder. Add a guide here to list it on /guides/.
export type Guide = {
  slug: string;
  title: string;
  subtitle: string;
  date: string; // YYYY-MM-DD, first edition
  description: string;
  pages: number;
  sizeMB: number;
  level: string;
  chapters: string[];
  previews: string[]; // page numbers with a <nn>.webp preview in public/guides/<slug>/
  companion?: string; // optional editable notes and practice package
  post?: string; // companion blog post slug, linked once it is live
};

export const guides: Guide[] = [
  {
    "slug": "computer-science-semester-one",
    "title": "Computer Science Foundations",
    "subtitle": "Semester One: notes, examples and practice",
    "date": "2026-11-18",
    "description": "An independent 39-page study book covering seven first-semester foundation modules: 56 lessons, worked examples, 84 practice questions and answer guides. Includes a twelve-week study pathway, with editable notes and tested C exercises in the companion ZIP. Match the material to your current lecturer outlines.",
    "pages": 39,
    "sizeMB": 0.11,
    "level": "First-year foundations",
    "chapters": [
        "Linear Algebra and Calculus",
        "Communication Skills",
        "Theory of Computation",
        "Operating Systems",
        "Programming Concepts in C",
        "Basics in Digital Circuit",
        "Electrical Fundamentals",
        "Study plan and practical work",
        "Resources and provenance"
    ],
    "previews": [
        "03",
        "12",
        "22",
        "32"
    ],
    "post": "c-integer-division-average",
    "companion": "/guides/computer-science-semester-one.zip"
},
  {
    slug: "python-daily",
    title: "Python Daily",
    subtitle: "From beginner to professional",
    date: "2026-10-09",
    description:
      "A free 43-page book that takes you from installing Python to working like a professional: six levels with explanations, real code, " +
      "practice exercises and a project at every step, all 20 areas where Python is used, a 12-month plan, free resources and a glossary.",
    pages: 43,
    sizeMB: 7,
    level: "Complete beginner and up",
    chapters: [
      "Why Python?",
      "Set up your tools",
      "The basics",
      "Intermediate Python",
      "Advanced Python",
      "Where Python is used",
      "Specialise",
      "Work like a professional",
      "Your 12-month plan",
      "Resources and glossary",
    ],
    previews: ["05", "12", "13", "27"],
    post: "python-roadmap",
  },
];

export const guideFile = (slug: string) => `/guides/${slug}.pdf`;
export const guideAsset = (slug: string, file: string) => `/guides/${slug}/${file}`;
