// The DEMONSTRATION issuer: in a pilot, a Poverty Elimination Center would hold its own private keys in secure hardware.
// These keys are deliberately public so any copy of the prototype can issue and verify demo credentials.
// Anything they sign proves nothing in real life, and the app says so wherever they appear.
export const DEMO_ISSUER = {
  iss: "https://peopleoftheworld.net/lifelink/demo-issuer",
  name: "LifeLink demonstration issuer (not a real authority)",
  kid: "demo-pec-1",
  publicJwk: { kty: "EC", crv: "P-256", x: "ZAKu4Q7VEGh9YfhGV-w1ndWwxrnVIR9K81JsUUZCZ7I", y: "WKh_GT2sWIVqliqe4_rvEzvyU1Lg65V7asUdMiVi2yA" },
  privateJwk: { kty: "EC", crv: "P-256", x: "ZAKu4Q7VEGh9YfhGV-w1ndWwxrnVIR9K81JsUUZCZ7I", y: "WKh_GT2sWIVqliqe4_rvEzvyU1Lg65V7asUdMiVi2yA", d: "8hUzx2B266a6sd6pYlhCfKfMPmkcMF2-hq-aoe6rymc" },
  pqSeedHex: "169b73412942484873500e606d508001e46eab9015dfd6cdb91717424da6b9be"
};
