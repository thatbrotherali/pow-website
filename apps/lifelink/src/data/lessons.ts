// Short built-in lessons that work with no internet. Each ends with a few questions;
// questions you get wrong come back for review (spaced repetition), and finishing one earns a signed certificate.
export type Lesson = { id: string; title: string; stage: string; minutes: number; credits: number; cards: { h: string; p: string }[]; quiz: { q: string; options: string[]; answer: number; why: string }[]; more?: { label: string; url: string } };

export const LESSONS: Lesson[] = [
  { id: "scam", title: "Spot a scam", stage: "Staying safe online", minutes: 6, credits: 5,
    cards: [
      { h: "Scams play on feelings", p: "Most scams try to make you hurry, panic or feel lucky: a prize you didn't enter for, a parcel you didn't order, a bank or government 'problem' that must be fixed today. Urgency is the warning sign." },
      { h: "Check who is really asking", p: "A message can show any name. Don't use the link or phone number in the message. Contact the organisation yourself, using a number or website you already know is real." },
      { h: "Never share codes or PINs", p: "No genuine bank, government office or LifeLink worker will ever ask for your PIN, password or a one-time code sent to your phone. Anyone who asks is a scammer." },
      { h: "Payments that can't be undone", p: "Requests to pay with gift cards, cryptocurrency or wire transfers are almost always scams, because the money can't be traced or returned." },
      { h: "If it has happened", p: "Stop paying, call your bank on its known number, change any passwords you shared, and report it. Being scammed is not your fault: scammers are professionals." }
    ],
    quiz: [
      { q: "A text says your account will close today unless you tap a link. What should you do?", options: ["Tap the link quickly", "Reply asking if it's real", "Contact the organisation using a number you already know"], answer: 2, why: "Urgency is the classic sign of a scam. Use contact details you already trust, never the ones in the message." },
      { q: "Someone from 'the bank' asks for the code just sent to your phone. Is this safe?", options: ["Yes, they're from the bank", "No, never share it", "Only if they know your name"], answer: 1, why: "Genuine organisations never ask for one-time codes. Knowing your name proves nothing." },
      { q: "Which payment request is most likely a scam?", options: ["An invoice from your regular electrician", "A request to pay a fine in gift cards", "A bill from your water company"], answer: 1, why: "Gift cards can't be traced or refunded, which is why scammers ask for them." }
    ],
    more: { label: "GCFGlobal: Internet safety (free)", url: "https://edu.gcfglobal.org/en/internetsafety/" } },

  { id: "credits", title: "How Civic Credits work", stage: "Money and community", minutes: 5, credits: 5,
    cards: [
      { h: "Paid for serving the community", p: "In the Plan to End Poverty, Civic Credits are earned for work that serves everyone: teaching, nursing and caring, and also volunteering such as neighbourhood clean-ups." },
      { h: "Backed by what we own together", p: "Credits can be exchanged for money because they are backed by income from public resources and public works: the sale or licensing of public resources, utilities and similar sources." },
      { h: "Spent where it matters", p: "Credits pay for essentials at Poverty Elimination Centers and partner businesses: food, housing, training and care, at true cost plus a fair margin, with no profit on necessities." },
      { h: "Voluntary, and never a gate", p: "Taking part is a choice. No one is refused food, care or a payment because a device failed or they don't have one; a person can always step in." },
      { h: "Every credit can be traced", p: "Each payment carries a digital signature, and the record of payments is linked so that changing any past entry shows. That is how public money stays honest." }
    ],
    quiz: [
      { q: "Which of these would earn Civic Credits in the plan?", options: ["Volunteering at a neighbourhood clean-up", "Winning a lottery", "Selling a used car"], answer: 0, why: "Credits reward service to the community, paid or volunteer." },
      { q: "What backs the value of Civic Credits?", options: ["Nothing", "Income from public resources and public works", "A private bank's profits"], answer: 1, why: "In the plan, credits are backed by what the public owns together." },
      { q: "If your LifeLink device breaks, can you still get food at a Poverty Elimination Center?", options: ["No", "Yes, a person can always step in", "Only with a new device"], answer: 1, why: "No one is ever refused essentials because of technology." }
    ],
    more: { label: "End Poverty by Design: Civic Credits", url: "https://peopleoftheworld.net/plan-to-end-poverty/civic-credits/" } },

  { id: "data", title: "Your data, your rights", stage: "Staying safe online", minutes: 5, credits: 5,
    cards: [
      { h: "It's yours", p: "Under laws such as Europe's GDPR you can ask to see the data an organisation holds about you, have it corrected, take a copy with you, and in many cases have it deleted. LifeLink is designed to give everyone those rights, everywhere." },
      { h: "Share only what's needed", p: "A shop checking your age needs 'over 18', not your birth date, name or address. LifeLink credentials let you show one fact and nothing else." },
      { h: "Know who has looked", p: "Every time your record is opened or shared, LifeLink writes it in an access log you can read." },
      { h: "Consent can be taken back", p: "Agreeing to share something once doesn't mean forever. You can change your mind, and the sharing stops." }
    ],
    quiz: [
      { q: "A venue needs to know you're an adult. What's the least you should share?", options: ["Your full ID", "Only that you're over 18", "Your birth date and address"], answer: 1, why: "Share the one fact that's needed, nothing more." },
      { q: "You agreed to share your learning progress with a centre. Can you stop?", options: ["No, it's permanent", "Yes, consent can be withdrawn", "Only after a year"], answer: 1, why: "Consent can be withdrawn at any time." }
    ],
    more: { label: "European Commission: Your data protection rights", url: "https://commission.europa.eu/law/law-topic/data-protection/information-individuals_en" } },

  { id: "fractions", title: "Fractions in everyday life", stage: "Numbers", minutes: 7, credits: 5,
    cards: [
      { h: "A fraction is a share", p: "¾ means a whole split into 4 equal parts, and you have 3 of them. The bottom number says how many parts; the top says how many you have." },
      { h: "Same amount, different names", p: "½ = 2/4 = 4/8. Multiply or divide the top and bottom by the same number and the amount doesn't change." },
      { h: "Halving a recipe", p: "To halve ¾ cup, halve the amount: ¾ ÷ 2 = 3/8 cup. To double it: ¾ × 2 = 6/4 = 1½ cups." },
      { h: "Fractions and percentages", p: "Percent means 'out of 100'. ½ = 50%, ¼ = 25%, ¾ = 75%, 1/10 = 10%. A 25% discount takes a quarter off the price." }
    ],
    quiz: [
      { q: "Which is the same as ½?", options: ["2/3", "3/6", "1/4"], answer: 1, why: "3/6: three of six equal parts is half." },
      { q: "A $40 item has 25% off. What do you pay?", options: ["$10", "$30", "$35"], answer: 1, why: "25% is a quarter. A quarter of $40 is $10, so you pay $30." },
      { q: "Double ¾ cup of rice. How much?", options: ["1½ cups", "1¼ cups", "6/8 cup"], answer: 0, why: "¾ × 2 = 6/4 = 1½." }
    ],
    more: { label: "Khan Academy: Fractions (free)", url: "https://www.khanacademy.org/math/arithmetic/fraction-arithmetic" } },

  { id: "help", title: "When and how to call for help", stage: "Health and safety", minutes: 5, credits: 5,
    cards: [
      { h: "Know your number", p: "Emergency numbers differ: 000 in Australia, 911 in the United States and Canada, 999 in the United Kingdom, 111 in New Zealand, 112 across the European Union and India. On most mobile phones 112 also connects in many other countries." },
      { h: "Call for", p: "Someone who is unconscious, not breathing normally, has chest pain, severe bleeding, signs of a stroke (face drooping, arm weakness, slurred speech), a severe allergic reaction, or is in danger. When in doubt, call." },
      { h: "What to say", p: "Which service you need, where you are (an address or landmark), what happened, and how many people are hurt. Stay on the line and follow instructions." },
      { h: "Not an emergency, but worried?", p: "Many countries have free nurse or health lines that can tell you whether to see a doctor. LifeLink lists the ones for your country under Health." }
    ],
    quiz: [
      { q: "Someone's face is drooping and their speech is slurred. What should you do?", options: ["Wait and see if it passes", "Call the emergency number now", "Give them water"], answer: 1, why: "These are signs of a stroke. Every minute counts." },
      { q: "What's the first thing to tell the emergency operator?", options: ["Your life story", "Which service you need and where you are", "Your LifeLink number"], answer: 1, why: "The service and your location let help start moving." }
    ],
    more: { label: "Find your emergency number and nurse line under Health", url: "#/health/care" } },

  { id: "within", title: "The voice within", stage: "Meaning", minutes: 6, credits: 0,
    cards: [
      { h: "A question every faith asks", p: "Across religions and cultures people describe an inner guide: a quiet sense of what is right that sometimes argues with what we want. Many call it conscience." },
      { h: "More than habit?", p: "We share bodies and instincts with animals, yet only we wrestle with fairness, truth and goodness. Many traditions hold that this voice is more than habit: a portion of the Creator within each person." },
      { h: "A practice", p: "Once a day, sit quietly for a few minutes. Ask: what is the kindest, most honest thing I could do today? Notice what you hear before your wants answer for you." },
      { h: "Why it matters for LifeLink", p: "LifeLink counts every person because every person matters. If each of us carries that inner spark, then no one is a number, and no one should be left behind." }
    ],
    quiz: [
      { q: "This lesson has no right answers to test. Which practice would you like to try this week?", options: ["A few quiet minutes each day", "Writing down one kind act a day", "Reading one teaching a week"], answer: -1, why: "Any of these is a good beginning." }
    ],
    more: { label: "The Search for Meaning: why every faith points within", url: "https://peopleoftheworld.net/seekers.html#why" } }
];
