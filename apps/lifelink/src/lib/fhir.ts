// Export the health record as an International Patient Summary (HL7 FHIR R4 IPS), the international standard
// for a portable summary that a doctor anywhere can read. Required sections (medications, allergies, problems)
// are always present, using the IPS "no known ..." codes when the list is empty.
import type { Health } from "./model";

const uuid = () => crypto.randomUUID();
const LOINC = "http://loinc.org";
const ABSENT = "http://hl7.org/fhir/uv/ips/CodeSystem/absent-unknown-uv-ips";
const text = (s: string) => ({ text: s });
const absent = (code: string, display: string) => ({ coding: [{ system: ABSENT, code, display }], text: display });

export function ipsBundle(name: string, birthDate: string | undefined, h: Health): object {
  const pid = `urn:uuid:${uuid()}`, now = new Date().toISOString();
  const entries: { fullUrl: string; resource: Record<string, unknown> }[] = [];
  const add = (resource: Record<string, unknown>) => { const fullUrl = `urn:uuid:${uuid()}`; entries.push({ fullUrl, resource }); return fullUrl; };
  const subject = { reference: pid };
  const [given, ...family] = name.trim().split(/\s+/);

  const meds = h.medications.length ? h.medications.map(m => add({ resourceType: "MedicationStatement", status: "active", subject, medicationCodeableConcept: text(m.name), dosage: m.dose ? [{ text: m.dose }] : undefined }))
    : [add({ resourceType: "MedicationStatement", status: "active", subject, medicationCodeableConcept: absent("no-known-medications", "No known medications") })];
  const allergies = h.allergies.length ? h.allergies.map(a => add({ resourceType: "AllergyIntolerance", patient: subject, code: text(a.name), criticality: a.severe ? "high" : "low",
      clinicalStatus: { coding: [{ system: "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical", code: "active" }] } }))
    : [add({ resourceType: "AllergyIntolerance", patient: subject, code: absent("no-known-allergies", "No known allergies") })];
  const problems = h.conditions.length ? h.conditions.map(c => add({ resourceType: "Condition", subject, code: text(c.name), onsetDateTime: c.since || undefined,
      clinicalStatus: { coding: [{ system: "http://terminology.hl7.org/CodeSystem/condition-clinical", code: "active" }] } }))
    : [add({ resourceType: "Condition", subject, code: absent("no-known-problems", "No known problems") })];
  const imms = h.immunizations.map(i => add({ resourceType: "Immunization", status: "completed", patient: subject, vaccineCode: text(i.name), occurrenceDateTime: i.date }));
  const VIT: Record<string, [string, string, string]> = { hr: ["8867-4", "Heart rate", "/min"], temp: ["8310-5", "Body temperature", "Cel"], weight: ["29463-7", "Body weight", "kg"], spo2: ["59408-5", "Oxygen saturation by pulse oximetry", "%"] };
  const vitals = h.vitals.slice(-20).map(v => v.kind === "bp"
    ? add({ resourceType: "Observation", status: "final", subject, effectiveDateTime: v.at, category: [{ coding: [{ system: "http://terminology.hl7.org/CodeSystem/observation-category", code: "vital-signs" }] }],
        code: { coding: [{ system: LOINC, code: "85354-9", display: "Blood pressure panel" }] },
        component: [{ code: { coding: [{ system: LOINC, code: "8480-6", display: "Systolic blood pressure" }] }, valueQuantity: { value: v.value, unit: "mmHg", system: "http://unitsofmeasure.org", code: "mm[Hg]" } },
                    { code: { coding: [{ system: LOINC, code: "8462-4", display: "Diastolic blood pressure" }] }, valueQuantity: { value: v.value2, unit: "mmHg", system: "http://unitsofmeasure.org", code: "mm[Hg]" } }] })
    : add({ resourceType: "Observation", status: "final", subject, effectiveDateTime: v.at, category: [{ coding: [{ system: "http://terminology.hl7.org/CodeSystem/observation-category", code: "vital-signs" }] }],
        code: { coding: [{ system: LOINC, code: VIT[v.kind][0], display: VIT[v.kind][1] }] }, valueQuantity: { value: v.value, unit: v.unit, system: "http://unitsofmeasure.org", code: VIT[v.kind][2] } }));

  const ref = (urls: string[]) => urls.map(reference => ({ reference }));
  const section = (title: string, code: string, display: string, urls: string[]) => ({ title, code: { coding: [{ system: LOINC, code, display }] }, entry: ref(urls) });
  const sections = [section("Medication Summary", "10160-0", "History of Medication use Narrative", meds),
                    section("Allergies and Intolerances", "48765-2", "Allergies and adverse reactions Document", allergies),
                    section("Problem List", "11450-4", "Problem list - Reported", problems)];
  if (imms.length) sections.push(section("History of Immunizations", "11369-6", "History of Immunization Narrative", imms));
  if (vitals.length) sections.push(section("Vital Signs", "8716-3", "Vital signs", vitals));

  const patient = { fullUrl: pid, resource: { resourceType: "Patient", name: [{ text: name, given: [given], family: family.join(" ") || undefined }], birthDate: birthDate || undefined } };
  const composition = { fullUrl: `urn:uuid:${uuid()}`, resource: { resourceType: "Composition", status: "final",
    type: { coding: [{ system: LOINC, code: "60591-5", display: "Patient summary Document" }] }, subject, date: now, author: [subject],
    title: `Patient summary for ${name} (self-reported, LifeLink prototype)`, section: sections } };
  return { resourceType: "Bundle", identifier: { system: "urn:ietf:rfc:3986", value: `urn:uuid:${uuid()}` }, type: "document", timestamp: now,
           entry: [composition, patient, ...entries] };
}
