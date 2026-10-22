/* People of the World — site settings and small behaviours.
   EDIT THE LINKS BELOW. Any button whose link is left empty ("") is hidden automatically. */
// Shop links point at the Wix shop, which lives at shop.peopleoftheworld.net.
const POW_LINKS = {
  shop: "shop.html",                 // e.g. "https://shop.peopleoftheworld.net" once the Wix shop moves to its subdomain
  support: "support.html",  // the Support the mission page
  donate: "https://shop.peopleoftheworld.net/donations-1",               // donation payment link (Stripe, PayPal or Wix)
  portalPaperback: "https://shop.peopleoftheworld.net/product-page/the-portal-opens",      // Wix shop or Lulu link for The Portal Opens paperback
  portalHardcover: "https://shop.peopleoftheworld.net/product-page/the-portal-opens-hardback",      // Lulu link for the hardcover
  portalKindle: "",         // Amazon Kindle link for The Portal Opens
  powNovelKindle: "",       // Amazon Kindle link for People of the World (novel)
  powNovelPrint: "https://shop.peopleoftheworld.net/product-page/people-of-the-world-1",        // Lulu link for People of the World (novel)
  review: "https://literarytitan.com/2025/08/13/the-portal-opens/",               // Literary Titan review of The Portal Opens
  easeApple: "",            // Music to Ease Your Mind on Apple Music
  easeAmazon: "",           // Music to Ease Your Mind on Amazon Music
  anthologySpotify: "",     // Anthology Vol. 1 on Spotify
  anthologyApple: "",       // Anthology Vol. 1 on Apple Music
  anthologyAmazon: "",      // Anthology Vol. 1 on Amazon Music
  gptBook: "https://shop.peopleoftheworld.net/product-page/the-unified-framework-for-the-graviton-pressure-theory",              // Lulu link for The Unified Framework for the Graviton Pressure Theory
  easykeyBook: "",          // link to buy Learning to Play the EasyKey Way
  audiobook: "",            // YouTube playlist or audio page
  vision: "",               // full Vision document
};
// Email sign-up: paste the form address from your email service (MailerLite, Buttondown, etc.).
const POW_SIGNUP_ENDPOINT = "";
const POW_CONTACT = "shareef@peopleoftheworld.net";

// the site's root folder, worked out from where this script lives (assets/site.js), so links work from any sub-folder
const POW_ROOT = new URL("..", document.currentScript ? document.currentScript.src : location.href);

document.addEventListener("DOMContentLoaded", () => {
  // videos: show a thumbnail until the visitor presses play, then load the YouTube player in its place
  document.querySelectorAll(".video-play[data-yt]").forEach(btn => {
    btn.addEventListener("click", () => {
      const id = btn.dataset.yt, list = btn.dataset.list;
      const f = document.createElement("iframe");
      f.src = "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0" + (list ? "&playlist=" + list : "");
      f.title = btn.getAttribute("aria-label") || "Video";
      f.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
      f.allowFullscreen = true;
      f.className = "video-frame";
      btn.replaceWith(f);
    });
  });
  // fill links; hide buttons whose link isn't set yet
  document.querySelectorAll("[data-link]").forEach(el => {
    const url = POW_LINKS[el.dataset.link];
    if (url) { el.href = /^https?:|^mailto:/.test(url) ? url : new URL(url, POW_ROOT).href; if (/^https?:/.test(url)) { el.target = "_blank"; el.rel = "noopener"; } }
    else el.hidden = true;
  });

  // email sign-up forms
  document.querySelectorAll("form.signup").forEach(form => {
    const note = form.parentElement.querySelector(".form-note");
    form.addEventListener("submit", async e => {
      e.preventDefault();
      const email = form.querySelector("input[type=email]").value.trim();
      if (!email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) { note.textContent = "Please enter a full email address, like you@example.com."; return; }
      if (!POW_SIGNUP_ENDPOINT) { note.textContent = `Sign-up opens soon. Until then, write to ${POW_CONTACT} and you'll be added by hand.`; return; }
      try {
        const body = new FormData(); body.append("email", email); body.append("list", form.dataset.list || "teachings");
        const r = await fetch(POW_SIGNUP_ENDPOINT, { method: "POST", body });
        note.textContent = r.ok ? "You're signed up. Check your inbox to confirm." : "That didn't go through. Please try again in a minute.";
        if (r.ok) form.reset();
      } catch { note.textContent = "That didn't go through. Please check your connection and try again."; }
    });
  });

  // copy email address
  document.querySelectorAll(".copy-btn").forEach(btn => {
    btn.addEventListener("click", async () => {
      const text = btn.dataset.copy;
      try { await navigator.clipboard.writeText(text); btn.textContent = "Copied"; }
      catch { const r = document.createRange(); r.selectNodeContents(btn.previousElementSibling); const s = getSelection(); s.removeAllRanges(); s.addRange(r); btn.textContent = "Selected"; }
      setTimeout(() => (btn.textContent = "Copy"), 1800);
    });
  });

  // share a page: the phone's share sheet where there is one, otherwise copy the message and link
  document.querySelectorAll(".share-btn").forEach(btn => {
    const label = btn.textContent;
    btn.addEventListener("click", async () => {
      const url = btn.dataset.url, text = btn.dataset.text || "";
      if (navigator.share) { try { await navigator.share({ title: document.title, text, url }); return; } catch (e) { if (e && e.name === "AbortError") return; } }
      try { await navigator.clipboard.writeText(text ? text + " " + url : url); btn.textContent = "Link copied"; }
      catch { const n = document.querySelector(".share-note"); if (n) n.textContent = "Copy this link: " + url; }
      setTimeout(() => (btn.textContent = label), 2000);
    });
  });
});
