# peopleoftheworld.net — website

The new People of the World website: a hub with six doors, starting with the Seekers door and the free online edition of *The Portal Opens*.

## What's in this folder

| Path | What it is |
|---|---|
| `docs/` | **The website itself.** Every file here is published as-is. |
| `docs/assets/site.js` | **Your settings:** buying links, review link, email sign-up address. Edit the lines at the top. |
| `docs/assets/site.css` | Colours, fonts and layout for every page. |
| `docs/assets/logo.webp` | The POW logo. |
| `build.py` | Rebuilds the pages in `docs/` (headers, footers, the online book). |
| `src/portal.txt` | The text of *The Portal Opens* that the online reader is built from. |

## Everyday changes

**Add a buying link, review link or audiobook link.** Open `docs/assets/site.js` and paste the address between the quotes, for example:

```js
portalKindle: "https://www.amazon.com.au/dp/XXXXXXXXXX",
```

A button whose link is empty stays hidden, so nothing broken ever shows.

**Connect the email sign-up.** Create a free list at MailerLite or Buttondown, copy the form's "action" address, and paste it into `POW_SIGNUP_ENDPOINT` in the same file.

**Change page text or the book text.** Edit `build.py` (page text) or `src/portal.txt` (book text), then run:

```
python build.py
```

This rewrites the pages in `docs/`. Don't edit the `.html` files in `docs/` by hand, because the next build would overwrite them. (`docs/assets/` is never overwritten.)

## Publishing with GitHub Pages (free)

1. Install **GitHub Desktop** and sign in.
2. *File → Add local repository* → choose this folder → *create a repository* when asked → **Publish repository** (name it `pow-website`; untick "Keep this code private" if you want it public).
3. On github.com, open the repository → **Settings → Pages** → *Source: Deploy from a branch* → branch `main`, folder **`/docs`** → Save.
4. After a minute the site is live at `https://<your-username>.github.io/pow-website/`. Check it there first.

## Moving peopleoftheworld.net to the new site (do this last)

The plan is: **peopleoftheworld.net** = this site, **shop.peopleoftheworld.net** = the Wix shop and members area.

1. In Wix, connect the subdomain `shop.peopleoftheworld.net` to your Wix site, and check the shop works there.
2. Update the shop link in `docs/assets/site.js` to `https://shop.peopleoftheworld.net`.
3. In GitHub → Settings → Pages → *Custom domain*, enter `peopleoftheworld.net` and save.
4. Where your domain's DNS is managed, point the main domain at GitHub Pages:
   - `A` records for `@` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `CNAME` for `www` → `<your-username>.github.io`
5. Back in GitHub Pages settings, tick **Enforce HTTPS** once it becomes available (can take up to a day).

Steps 3–4 move the main address away from Wix, so do them only after the shop is working on its subdomain.
