// The learning map: free, reputable sources from first letters to university and trades.
// Checked October 2026. Each entry says plainly what is free and what costs money.
export type Stage = "foundations" | "school" | "university" | "skills" | "life" | "meaning";
export type Source = { id: string; name: string; by: string; url: string; stages: Stage[]; topics: string[]; free: string; certificate: string; languages: string; offline?: string };

export const STAGES: { id: Stage; title: string; blurb: string }[] = [
  { id: "foundations", title: "First steps", blurb: "Reading, writing, numbers and using a phone or computer." },
  { id: "school", title: "School", blurb: "Primary and secondary subjects, at your own pace." },
  { id: "university", title: "University", blurb: "Courses, textbooks and full degrees that cost little or nothing." },
  { id: "skills", title: "Skills and trades", blurb: "Job skills, coding, health work and trades." },
  { id: "life", title: "Life skills", blurb: "Money, health, rights and staying safe online." },
  { id: "meaning", title: "Meaning", blurb: "The bigger questions: purpose, conscience and how to live." }
];

export const SOURCES: Source[] = [
  { id: "storyweaver", name: "StoryWeaver", by: "Pratham Books", url: "https://storyweaver.org.in/", stages: ["foundations"], topics: ["reading"],
    free: "Thousands of illustrated stories for children, free to read, download and translate.", certificate: "None", languages: "Hundreds of languages" },
  { id: "gdl", name: "Global Digital Library", by: "Norad (Norway)", url: "https://digitallibrary.io/", stages: ["foundations"], topics: ["reading"],
    free: "Quality-checked early-grade reading books, free.", certificate: "None", languages: "Dozens of languages" },
  { id: "gcf", name: "GCFGlobal", by: "Goodwill Community Foundation", url: "https://edu.gcfglobal.org/", stages: ["foundations", "life", "skills"], topics: ["digital", "reading", "maths", "work"],
    free: "Every tutorial free: using a computer and phone, email, internet safety, reading, maths, office software, job search.", certificate: "None", languages: "English, Spanish, Portuguese" },
  { id: "khan", name: "Khan Academy", by: "Khan Academy (non-profit)", url: "https://www.khanacademy.org/", stages: ["foundations", "school", "university"], topics: ["maths", "science", "reading", "economics", "computing"],
    free: "Everything free: lessons, practice and progress tracking, from early maths to early university.", certificate: "None", languages: "Many languages" },
  { id: "ck12", name: "CK-12", by: "CK-12 Foundation", url: "https://www.ck12.org/", stages: ["school"], topics: ["maths", "science"],
    free: "Free interactive textbooks (FlexBooks), simulations and practice for school maths and science.", certificate: "None", languages: "English, some Spanish" },
  { id: "bitesize", name: "BBC Bitesize", by: "BBC", url: "https://www.bbc.co.uk/bitesize", stages: ["school"], topics: ["all subjects"],
    free: "Free lessons and revision for every school subject (UK curriculum).", certificate: "None", languages: "English, Welsh, Gaelic" },
  { id: "openstax", name: "OpenStax", by: "Rice University", url: "https://openstax.org/", stages: ["school", "university"], topics: ["maths", "science", "business", "humanities"],
    free: "Peer-reviewed university and high-school textbooks, free online and as PDFs, openly licensed.", certificate: "None", languages: "English, some Spanish and Polish", offline: "Download the PDFs" },
  { id: "ocw", name: "MIT OpenCourseWare", by: "Massachusetts Institute of Technology", url: "https://ocw.mit.edu/", stages: ["university"], topics: ["engineering", "science", "maths", "humanities"],
    free: "Materials from over 2,400 MIT courses, free: lecture notes, videos, problem sets and exams.", certificate: "None", languages: "English (some translations)", offline: "Many courses can be downloaded whole" },
  { id: "openlearn", name: "OpenLearn", by: "The Open University", url: "https://www.open.edu/openlearn/", stages: ["university", "skills", "life"], topics: ["all subjects"],
    free: "Hundreds of free short courses at university level.", certificate: "Free statement of participation; some courses give a free digital badge", languages: "English" },
  { id: "saylor", name: "Saylor University", by: "Saylor Foundation", url: "https://www.saylor.org/", stages: ["university", "skills"], topics: ["business", "computing", "maths", "science", "humanities"],
    free: "Over 300 college-level courses, free. Renamed from Saylor Academy in 2026.", certificate: "Free certificate on passing the final exam; some courses carry college credit recommendations", languages: "English" },
  { id: "uopeople", name: "University of the People", by: "University of the People", url: "https://www.uopeople.edu/", stages: ["university"], topics: ["business", "computing", "health", "education"],
    free: "Accredited degrees with no tuition. There is a US$60 application fee and a fee for each course assessment; scholarships can cover them.", certificate: "Accredited associate, bachelor's and master's degrees", languages: "English" },
  { id: "edx", name: "edX (including MITx and HarvardX)", by: "edX", url: "https://www.edx.org/", stages: ["university", "skills"], topics: ["all subjects"],
    free: "Most courses can be audited free, but audit access is now usually time-limited and graded work may need payment.", certificate: "Paid", languages: "Mostly English" },
  { id: "coursera", name: "Coursera", by: "Coursera", url: "https://www.coursera.org/", stages: ["university", "skills"], topics: ["all subjects"],
    free: "Since August 2025 only the first module of most courses is free to preview. Financial aid is available on application.", certificate: "Paid (or by financial aid)", languages: "Many languages" },
  { id: "fcc", name: "freeCodeCamp", by: "freeCodeCamp (non-profit)", url: "https://www.freecodecamp.org/", stages: ["skills"], topics: ["computing"],
    free: "A complete programming curriculum, free.", certificate: "Free certifications", languages: "Several languages" },
  { id: "alison", name: "Alison", by: "Alison", url: "https://alison.com/", stages: ["skills"], topics: ["work", "health", "trades", "business"],
    free: "Thousands of short workplace courses, free to study (with advertising).", certificate: "Paid certificates", languages: "English and others" },
  { id: "openwho", name: "OpenWHO", by: "World Health Organization", url: "https://openwho.org/", stages: ["skills", "life"], topics: ["health"],
    free: "Free courses on health emergencies, disease control and care, written for health workers.", certificate: "Free records of achievement on many courses", languages: "Many languages" },
  { id: "hesperian", name: "Hesperian Health Guides", by: "Hesperian (non-profit)", url: "https://en.hesperian.org/", stages: ["life", "skills"], topics: ["health"],
    free: "Where There Is No Doctor and other community health books, free to read online.", certificate: "None", languages: "Many languages" },
  { id: "gutenberg", name: "Project Gutenberg", by: "Project Gutenberg", url: "https://www.gutenberg.org/", stages: ["school", "university", "meaning"], topics: ["reading", "literature"],
    free: "Over 70,000 free e-books whose copyright has expired.", certificate: "None", languages: "Mostly English, many others", offline: "Download any book" },
  { id: "openlibrary", name: "Open Library", by: "Internet Archive", url: "https://openlibrary.org/", stages: ["school", "university", "meaning"], topics: ["reading"],
    free: "Read free public-domain books, and borrow many others, online.", certificate: "None", languages: "Many languages" },
  { id: "wikipedia", name: "Wikipedia", by: "Wikimedia Foundation", url: "https://www.wikipedia.org/", stages: ["school", "university", "life"], topics: ["reference"],
    free: "The free encyclopedia.", certificate: "None", languages: "Over 300 languages", offline: "With Kiwix" },
  { id: "kiwix", name: "Kiwix", by: "Kiwix (non-profit)", url: "https://kiwix.org/", stages: ["foundations", "school", "university"], topics: ["offline"],
    free: "Free, open-source reader that carries Wikipedia and other libraries on a device with no internet.", certificate: "None", languages: "Many languages", offline: "Made for offline use" },
  { id: "kolibri", name: "Kolibri", by: "Learning Equality", url: "https://learningequality.org/kolibri/", stages: ["foundations", "school"], topics: ["offline"],
    free: "Free, offline-first learning platform for schools and learning centres, installed in over 220 countries and territories.", certificate: "None", languages: "Many languages", offline: "Made for offline use: ideal for Poverty Elimination Centers" },
  { id: "tensteps", name: "Ten Steps for Humanity", by: "People of the World", url: "https://peopleoftheworld.net/ten-steps.html", stages: ["meaning", "life"], topics: ["purpose"],
    free: "Ten practical steps toward a better life and a better world.", certificate: "None", languages: "English" },
  { id: "search", name: "The Search for Meaning", by: "People of the World", url: "https://peopleoftheworld.net/seekers.html", stages: ["meaning"], topics: ["purpose"],
    free: "Free weekly teachings on the voice within and the thread that runs through every faith.", certificate: "None", languages: "English" }
];

// The guide's goals. Each maps to stages and sources, with the reason it gives.
export const GOALS: { id: string; label: string; stages: Stage[]; sources: string[]; lessons: string[]; why: string }[] = [
  { id: "read", label: "Read and write with confidence", stages: ["foundations"], sources: ["gcf", "storyweaver", "gdl", "khan"], lessons: ["scam"], why: "Reading opens every other door, so the plan starts here." },
  { id: "digital", label: "Use a phone or computer safely", stages: ["foundations", "life"], sources: ["gcf"], lessons: ["scam", "data"], why: "Staying safe online protects your money and identity." },
  { id: "school", label: "Finish school", stages: ["school"], sources: ["khan", "ck12", "bitesize", "openstax"], lessons: ["fractions"], why: "School subjects build step by step; these sources let you start where you are." },
  { id: "uni", label: "Study at university level", stages: ["university"], sources: ["ocw", "openstax", "openlearn", "saylor", "uopeople"], lessons: [], why: "These are genuinely free, and two of them lead to certificates or a degree." },
  { id: "job", label: "Get skills for work", stages: ["skills"], sources: ["fcc", "saylor", "openlearn", "alison", "gcf"], lessons: ["credits"], why: "Short courses with certificates you can show an employer or a Poverty Elimination Center." },
  { id: "health", label: "Care for my health and my family's", stages: ["life"], sources: ["hesperian", "openwho"], lessons: ["help"], why: "Knowing when and how to get help saves lives." },
  { id: "rights", label: "Understand money, rights and Civic Credits", stages: ["life"], sources: ["openlearn", "gcf"], lessons: ["credits", "data"], why: "Knowing how credits and your data work keeps you in control." },
  { id: "meaning", label: "Explore meaning and purpose", stages: ["meaning"], sources: ["search", "tensteps", "gutenberg"], lessons: ["within"], why: "Every faith asks the same questions; here you can explore them freely." }
];
