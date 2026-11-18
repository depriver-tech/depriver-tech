// Life story chapters. Source notes: STORY.md. Keep company names out (personal brand rule),
// and keep family events in the gentle wording agreed with Privatus.

export type Fact = { value: string; label: string };

export type Chapter = {
  id: string;
  year: string; // big number shown on the rail
  when: string; // small date line
  place: string;
  title: string;
  accent: string; // second, orange line of the title
  body: string[];
  facts?: Fact[];
  quote?: string;
  tone?: "dark";
  feature?: "rank" | "memory" | "robbed" | "results";
};

export const chapters: Chapter[] = [
  {
    id: "born",
    year: "2006",
    when: "Monday, 14 August 2006",
    place: "Kitwe village · Kyerwa · Kagera",
    title: "Where it",
    accent: "all began",
    body: [
      "I was born on a Monday, 14 August 2006, in Kitwe village, Kyerwa District, in Kagera. I'm the second born in our family and the first son.",
      "My dad, Patrick, and my mom, Christer, were both primary school teachers: Dad at Rulama Primary School and Mom at Nyerere Primary School. Life was simple, normal village life. In a teachers' home, school was never far from the dinner table.",
    ],
    facts: [
      { value: "14.08", label: "Born in 2006" },
      { value: "2nd", label: "Born · first son" },
      { value: "2", label: "Teachers as parents" },
    ],
  },
  {
    id: "primary",
    year: "2011",
    when: "2011 to 6 September 2018",
    place: "Nyerere Primary School",
    title: "A village",
    accent: "classroom",
    body: [
      "I started school in 2011 at Nyerere Primary, the same school where Mom taught. Like every “St Kayumba” kid (that's what we call our local government schools), I learnt everything in Kiswahili. English was a subject, not a language I lived in.",
      "I finished primary school on 6 September 2018. I had no idea how much that English gap was about to cost me.",
    ],
  },
  {
    id: "katoke",
    year: "2018",
    when: "15 September 2018 to April 2021",
    place: "Katoke Seminary",
    title: "Learning in a",
    accent: "new language",
    body: [
      "On 15 September 2018 I joined Katoke Seminary for pre-form one. Overnight, every lesson was in English. Through pre-form one and Form One I fought just to understand my teachers, chasing the 60% average we needed to stay.",
      "In Form Two stomach ulcers started, and the pain followed me until late Form Three. COVID closed schools from March to July 2020. Soon after we returned, in September, just before the Form Two national exam, I was admitted at Bugando Hospital for an endoscopy. I still sat the exam, and scored Division I with 11 points.",
      "Katoke also gave me music: it's where I started learning the piano. And I had Nelius Nickson, more than a friend, who taught me so much and took care of me whenever I was sick.",
      "In April 2021, in Form Three, my time at Katoke came to an end. I had to leave and start again somewhere new.",
    ],
    facts: [
      { value: "I", label: "Division · Form Two (11 pts)" },
      { value: "60%", label: "The average I chased" },
      { value: "♪", label: "Where I learnt the piano" },
    ],
  },
  {
    id: "kaisho",
    year: "2021",
    when: "2021 to 2022",
    place: "Kaisho Secondary School",
    title: "Starting again",
    accent: "from the bottom",
    feature: "rank",
    body: [
      "Kaisho was a whole new world: from a boys' seminary to a mixed school, new faces and new rules. At the first-semester break I was second from last in my class.",
      "So I focused. By the September break I was second in class with a 78% average. Maths, Chemistry and Physics became my strongest subjects. Biology… well, in one essay I confidently wrote that cholera is a sexually transmitted disease. We still laugh about that one.",
      "I became the Sports Prefect, played the piano at morning Mass and was the DJ at school events. In Form Four I studied through the night, hiding in the laboratory to practise experiments. I solved so many physics practicals that I learnt every shortcut for sketching the graphs, and scored 45 or more out of 50 in every physics practical exam.",
      "Not everything was perfect. In the Lake Zone exams I got F in Kiswahili and History, and I was punished for “ignoring” non-science subjects. My friends Gabriel and Polycarp were true life savers through all of it.",
    ],
  },
  {
    id: "graduation",
    year: "2022",
    when: "25 October 2022",
    place: "Form Four graduation · Kaisho",
    title: "The day Mom",
    accent: "smiled the most",
    feature: "results",
    body: [
      "On 25 October 2022, Dad, Mom, my young brother Alan and my young sister Agape all came to my Form Four graduation. I received certificates for leadership and for academic excellence in Mathematics and Physics. Mom's joy that day is a picture I still carry.",
      "Then the national results came: Division I, 7 points. A boy who once couldn't follow an English lesson was now among the best. That changed how I saw myself.",
    ],
    quote: "Where you start is not where you finish.",
  },
  {
    id: "choice",
    year: "2023",
    when: "November 2022 to September 2023",
    place: "Kagera → Mbeya",
    title: "The road",
    accent: "less taken",
    body: [
      "While waiting for selections, I went back to Kaisho as an intern teacher until after Easter, then did side hustles around home. From June to August I worked far from home with a family research organisation, then freelanced for a mobile network until September.",
      "I had made a choice many people didn't understand: I didn't want A-level. Teachers, parents and relatives said it was a mistake. When selections came, I was chosen for a Diploma in Computer Science at Mbeya University of Science and Technology (MUST), fully government sponsored.",
      "Some said that college was “for students who failed.” I went anyway.",
    ],
  },
  {
    id: "must",
    year: "2023",
    when: "October 2023",
    place: "MUST · Mbeya",
    title: "A fresher",
    accent: "with a toolkit",
    body: [
      "In October 2023 I joined MUST. University freedom was nothing like O-level, and I had to learn to manage everything on my own. I already knew my way around computers, so I stayed curious and busy: repairing computers and installing software and operating systems to survive.",
      "At the hostel I started reselling Wi-Fi. I didn't know then that this small business would carry me through the hardest years of my life.",
      "In my first year I took my work to MAKISATU, the national science, technology and innovation competition, in Morogoro.",
    ],
    facts: [
      { value: "CS", label: "Diploma in Computer Science" },
      { value: "Wi-Fi", label: "My first business" },
      { value: "MAKISATU", label: "Morogoro · Year one" },
    ],
  },
  {
    id: "robbed",
    year: "2024",
    when: "After my first semester",
    place: "Dodoma, around 3 a.m.",
    title: "Losing everything",
    accent: "in one night",
    feature: "robbed",
    body: [
      "On my way home after my first semester, I was robbed in Dodoma at around three in the morning. My laptop, my phone, my Sony FX3 camera and all my certificates were gone in minutes. It was my hardest setback yet.",
      "At home, my parents counselled me and helped me stand again. After the holiday I went back to university with nothing but a small feature phone, and started again.",
    ],
  },
  {
    id: "season",
    year: "2024",
    when: "October 2024 to June 2025",
    place: "Home",
    title: "The hardest",
    accent: "season",
    tone: "dark",
    feature: "memory",
    body: [
      "On 21 October 2024, we lost Dad suddenly, and our family went through its hardest season.",
      "For months I became the one holding home together: looking after my elder sister Coline and my young brother and sister while trying to stay in university. I came very close to dropping out, and my grades fell. The support of good people, my side hustles and that Wi-Fi business kept us going.",
      "In June 2025 our family was reunited when Mom came back home. Slowly, life found its rhythm again.",
    ],
  },
  {
    id: "building",
    year: "2025",
    when: "2025 to 2026",
    place: "Mbeya",
    title: "Building",
    accent: "while studying",
    body: [
      "I kept going: the second-year field attachment, then third year. As a side job I served as Lead Technical Officer at a tech innovation company, where I learnt a lot about hardware. I presented my work at exhibitions and earned certificates and prizes along the way.",
      "In March 2026 I joined a campus media startup as its technical person. We were paid in shares. I gave it my best, but my family's needs were real, so I resigned to find work that could support them.",
      "In June 2026 I interviewed at a software company in Mbeya and got the job as a Software Engineer while still a student. Thank God. Soon after, I graduated from MUST with my Diploma in Computer Science. After the diploma, I continued into the Bachelor of Computer Science programme at MUST. I’m now in my first year, first semester of the 2026/2027 academic year, studying alongside my work.",
    ],
    facts: [
      { value: "Lead", label: "Technical officer · Year two" },
      { value: "06.2026", label: "Hired as Software Engineer" },
      { value: "Diploma", label: "Graduated from MUST" },
    ],
  },
];

export const lessons = [
  { n: "01", from: "kaisho", title: "A bad start is not the final result", then: "Second from last", now: "Division I", body: "Second from last became second in class. Division I followed." },
  { n: "02", from: "choice", title: "Your path can look wrong and still be right", then: "“Diploma is for those who failed”", now: "My way into tech", body: "They said a diploma was for those who failed. It became my way into tech." },
  { n: "03", from: "robbed", title: "Skills are what they can't steal", then: "Laptop, phone, certificates", now: "Everything I knew", body: "I lost my laptop, phone and certificates in one night. What I knew came with me." },
];

// Each service is a file in the "today" editor. Code lines are small, trusted HTML: k keyword, f function, s string, p property, n number.
export const services = [
  { title: "Web & mobile apps", body: "From idea to launch: products people enjoy using.", file: "web-mobile.tsx",
    code: ['<k>export default function</k> <f>App</f>() {', '  <k>return</k> &lt;<f>Product</f> <p>users</p>=<s>"happy"</s> <p>platforms</p>={[<s>"web"</s>, <s>"android"</s>, <s>"ios"</s>]} /&gt;;', '}'] },
  { title: "SaaS & business systems", body: "Tools that help businesses work smarter.", file: "business.ts",
    code: ['<k>const</k> shop = <k>await</k> <f>system</f>({ <p>sales</p>: <n>true</n>, <p>stock</p>: <n>true</n>, <p>staff</p>: <n>true</n> });', 'shop.<f>work</f>({ <p>smarter</p>: <n>true</n>, <p>paperwork</p>: <n>0</n> });'] },
  { title: "Systems integration", body: "Making different systems talk to each other.", file: "integrations.ts",
    code: ['mobileMoney.<f>on</f>(<s>"payment"</s>, <k>async</k> (tx) =&gt; {', '  <k>await</k> accounting.<f>record</f>(tx);', '  <k>await</k> sms.<f>send</f>(tx.phone, <s>"Asante! Tumepokea malipo."</s>);', '});'] },
  { title: "Data for business", body: "Dashboards, reports and insights that drive decisions.", file: "insights.sql",
    code: ['<k>SELECT</k> month, <f>SUM</f>(sales) <k>AS</k> revenue', '<k>FROM</k> orders', '<k>GROUP BY</k> month', '<k>ORDER BY</k> revenue <k>DESC</k>;  <c>-- decide with numbers, not guesses</c>'] },
  { title: "Multimedia & content", body: "Video, photography and visuals that tell a story.", file: "story.json",
    code: ['{', '  <p>"shoot"</p>: [<s>"video"</s>, <s>"photo"</s>],', '  <p>"edit"</p>: <s>"until it feels right"</s>,', '  <p>"goal"</p>: <s>"a story people remember"</s>', '}'] },
  { title: "Tech for social good", body: "Using technology to solve real community problems.", file: "README.md",
    code: ['<k>#</k> Tech for the community', '', 'Works on cheap phones. Works offline.', 'Speaks <s>Kiswahili</s>. Solves a <f>real</f> problem.'] },
];

export const outside = ["Basketball", "Inline skating (four-wheel skates)", "Cycling", "Calisthenics", "Content creation", "Nature", "Gaming", "Piano & music", "Data & cloud"];

export const dreams = [
  {
    group: "Faith & family",
    icon: "heart",
    items: [
      "Keep growing a close relationship with God",
      "Keep my family united and working together",
      "Build a healthy relationship and start my own family",
    ],
  },
  {
    group: "Work & purpose",
    icon: "rocket",
    items: [
      "Raise funds for my startup",
      "Solve real community problems with technology",
      "Grow in my career and keep learning how computers work, deeper",
      "Become financially free",
    ],
  },
  {
    group: "Life & adventure",
    icon: "road",
    items: [
      "Travel the world to places where tech is most advanced",
      "Live close to nature",
      "Ride: bikes and the open road",
    ],
  },
];

export const contact = {
  phone: "+255 752 747 681",
  phoneHref: "tel:+255752747681",
  instagram: "@_depriver",
  instagramHref: "https://instagram.com/_depriver",
  github: "Stark-Priver",
  githubHref: "https://github.com/Stark-Priver",
  whatsappHref: "https://wa.me/255752747681",
  email: "privercosmas@gmail.com",
  emailHref: "mailto:privercosmas@gmail.com",
  linkedin: "in/incpritech",
  linkedinHref: "https://www.linkedin.com/in/incpritech/",
};

// Gratitude. Named people come from Privatus; groups are drawn from the story. Add names here as he shares them.
export const gratitude = {
  // photo: optional, e.g. "/img/people/mom.jpg" (put files in public/img/people/). Without one, a designed monogram shows.
  people: [
    { name: "Patrick", relation: "Dad", note: "My first teacher at home. Your lessons still guide me. Forever in my heart.", memory: true, photo: "" },
    { name: "Christer", relation: "Mom", note: "Your strength held our family together. Your joy on my graduation day keeps me going.", photo: "" },
    { name: "Coline", relation: "Elder sister", note: "For walking through the hardest season with me, side by side.", photo: "" },
    { name: "Alan & Agape", relation: "Young brother & sister", note: "Everything I build is also for you.", photo: "" },
    { name: "Nelius Nickson", relation: "Friend · Katoke Seminary", note: "More than a friend. You taught me and cared for me when I was sick.", photo: "" },
    { name: "Gabriel & Polycarp", relation: "Friends · Kaisho Secondary", note: "My life savers when I had to start again from the bottom.", photo: "" },
  ],
  groups: [
    { title: "My teachers", note: "At Nyerere Primary, Katoke Seminary and Kaisho Secondary: for teaching, correcting and believing in me." },
    { title: "Kaisho Secondary", note: "For taking me in when I had to start again, and welcoming me back as an intern teacher." },
    { title: "Bugando Hospital", note: "The doctors and nurses who cared for me when my stomach wouldn't let me be." },
    { title: "MUST", note: "My lecturers and classmates, who made Mbeya a second home." },
    { title: "Our family's supporters", note: "Relatives, neighbours, friends and well-wishers who stood with us in the hardest season." },
    { title: "My customers", note: "Everyone who bought Wi-Fi, repairs or software from me. You kept me in school." },
    { title: "The teams I've worked with", note: "Everyone who gave me a chance, trusted me with real work and taught me along the way." },
    { title: "Everyone who prayed", note: "For every prayer, encouragement and simple “how are you?” that came at the right time." },
  ],
};
