# RT Kitchen (staging)

Staging site for RT Kitchen, Raju & Trupti's Kitchen: Gujarati snacks, sweets, biscuits and catering at 15714 Pioneer Blvd, Norwalk, CA.

A single `index.html` with no build step. Pages: home, about, menu by category, product pages, cart, checkout (pickup or shipping), catering and contact.

## Settings to confirm before launch
At the top of the `<script>` in `index.html`:
- `SHIP_FEE`: flat shipping under $65 is a placeholder ($12)
- Product list (`P`): prices, sizes and stock flags (`oos`, `store`, `call`)

## Not wired up yet
- Orders and form messages are not sent anywhere, and there is no online payment.
- Product photos load from the old rtkitchen.com WordPress uploads, with a drawn illustration as fallback. Replace with the client's photos (and host them in this repo) before the old site is shut down.
