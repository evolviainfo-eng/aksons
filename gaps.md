# AK & Sons: what we still need from Keiron

1. **Opening hours.** Facebook says "always open", so the site shows no hours.
2. **Domain.** A .co.uk was promised. The sitemap, canonical links and social previews assume `aksonsbespokejoinery.co.uk` (`SITE` in `data.py`). Change it there once the name is chosen, then run `python3 gen.py`.
3. **Activating the form.** The form posts to FormSubmit at ak.sonsbespokejoinery@gmail.com. The first real enquiry triggers a one-time activation email to that inbox, and Keiron has to click it. Nothing has been sent from here. Photo upload takes one photo of up to 5 MB.
4. **Vector logo.** The logo comes from the 1440 px Instagram post (P18_00), split into the mark and the wordmark. It is sharp enough for the site. A vector file would still be better for print and the favicon.
5. **Customer and builder names.** The Harthill post names Lindrick Construction, and the Sheffield roof was done for AGE builders. Neither name is on the site; both say "a local builder". Ask whether we can name them.
6. **Project scope to confirm:**
   - Worksop glazed doors (Instagram, March 2026): the caption has no text, so the description was written from the photos.
   - Banbury: are the two media walls one job?
   - Kilton garage conversion and Harworth pergola: is anything to add?
7. **Number of jobs completed and the area covered.** The site shows the project places only. It gives no radius and no count.
8. **Reviews.** All 8 Facebook recommendations were scraped word for word (`assets/reviews.json`). Three are on the home page, with the first name and the initial of the surname. Check this is OK with the reviewers' wishes.
9. **Photos.** These are phone photos from Instagram, and most are sharp originals (3024 px). Five small frames were super-resolved. Five more failed the fidelity check, so they are used at their original size. A proper shoot of two or three finished jobs would lift the site further.
10. **Hosting.** Vercel Hobby forbids commercial use. Use Cloudflare Pages (free) or the client's own host.
