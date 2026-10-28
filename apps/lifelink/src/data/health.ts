// Where to get care, by country, and where to find trustworthy health information. Checked October 2026.
export type Line = { label: string; number?: string; url?: string; note: string };
export type Country = { code: string; name: string; emergency: string; lines: Line[] };

export const COUNTRIES: Country[] = [
  { code: "AU", name: "Australia", emergency: "000", lines: [
    { label: "healthdirect nurse line", number: "1800 022 222", url: "https://www.healthdirect.gov.au/", note: "Free health advice from a registered nurse, 24 hours. In Victoria the call goes to NURSE-ON-CALL." },
    { label: "Lifeline", number: "13 11 14", url: "https://www.lifeline.org.au/", note: "Crisis support and suicide prevention, 24 hours, also by text and online chat." },
    { label: "Kids Helpline", number: "1800 55 1800", url: "https://kidshelpline.com.au/", note: "Free counselling for young people aged 5 to 25, 24 hours." },
    { label: "Poisons Information Centre", number: "13 11 26", note: "24 hours." } ] },
  { code: "US", name: "United States", emergency: "911", lines: [
    { label: "988 Suicide & Crisis Lifeline", number: "988", url: "https://988lifeline.org/", note: "Call or text, 24 hours." },
    { label: "Poison Help", number: "1-800-222-1222", note: "24 hours." },
    { label: "MedlinePlus", url: "https://medlineplus.gov/", note: "Trusted health information from the US National Library of Medicine, in English and Spanish." } ] },
  { code: "GB", name: "United Kingdom", emergency: "999", lines: [
    { label: "NHS 111", number: "111", url: "https://111.nhs.uk/", note: "Urgent medical help that isn't an emergency, 24 hours." },
    { label: "Samaritans", number: "116 123", url: "https://www.samaritans.org/", note: "Free, 24 hours, whatever you're going through." } ] },
  { code: "IE", name: "Ireland", emergency: "112 or 999", lines: [
    { label: "Samaritans", number: "116 123", url: "https://www.samaritans.org/ireland/", note: "Free, 24 hours." },
    { label: "HSE health A to Z", url: "https://www2.hse.ie/conditions/", note: "Health information from the Health Service Executive." } ] },
  { code: "NZ", name: "New Zealand", emergency: "111", lines: [
    { label: "Healthline", number: "0800 611 116", url: "https://www.healthline.govt.nz/", note: "Free health advice from a registered nurse, 24 hours." },
    { label: "Need to talk?", number: "1737", note: "Free call or text to a trained counsellor, 24 hours." } ] },
  { code: "CA", name: "Canada", emergency: "911", lines: [
    { label: "9-8-8 Suicide Crisis Helpline", number: "988", url: "https://988.ca/", note: "Call or text, 24 hours." },
    { label: "Provincial health line", number: "811", note: "Nurse advice in most provinces and territories." } ] },
  { code: "IN", name: "India", emergency: "112", lines: [
    { label: "Tele-MANAS", number: "14416", note: "Free national mental health helpline, 24 hours, in many languages." } ] },
  { code: "XX", name: "Another country", emergency: "112", lines: [
    { label: "Find a Helpline", url: "https://findahelpline.com/", note: "Free, confidential crisis lines in over 130 countries." },
    { label: "Emergency on a mobile phone", note: "112 connects to emergency services from most mobile phones in many countries, but check your local number." } ] }
];

export const INFO: { name: string; by: string; url: string; note: string }[] = [
  { name: "WHO fact sheets", by: "World Health Organization", url: "https://www.who.int/news-room/fact-sheets", note: "Short, reliable summaries of hundreds of health topics, in several languages." },
  { name: "MedlinePlus", by: "US National Library of Medicine", url: "https://medlineplus.gov/", note: "Conditions, tests and medicines in plain language, English and Spanish." },
  { name: "healthdirect", by: "Australian Government", url: "https://www.healthdirect.gov.au/", note: "Health information, a symptom checker and a service finder for Australia." },
  { name: "NHS health A to Z", by: "National Health Service (UK)", url: "https://www.nhs.uk/conditions/", note: "Conditions and treatments, written for the public." },
  { name: "Hesperian Health Guides", by: "Hesperian", url: "https://en.hesperian.org/", note: "Community health guides for places with few doctors, in many languages." },
  { name: "Find a Helpline", by: "Throughline", url: "https://findahelpline.com/", note: "Crisis lines around the world." }
];

export const MEDICINE_LINKS = [
  { name: "MedlinePlus: Drugs and supplements", url: "https://medlineplus.gov/druginformation.html" },
  { name: "healthdirect: Medicines", url: "https://www.healthdirect.gov.au/medicines" },
  { name: "NHS: Medicines A to Z", url: "https://www.nhs.uk/medicines/" }
];
