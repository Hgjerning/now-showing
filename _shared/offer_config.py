# -*- coding: utf-8 -*-
"""One place for the 'test your own strategy' offer (fake-door test, 27 Nov 2026).

Change PRICE here, then run  python _shared/add_offer.py  (factsheets) and
python Articles/_map/build_game.py  (game). Both are idempotent and replace the old block.

No payment is taken. The button opens a short request; the reader copies it and sends it
to Henrik on LinkedIn (no e-mail address is published). If a form service is set up later
(Microsoft Forms, Tally, Formspree), put its URL in FORM_URL and the button goes there instead.
GoatCounter events: offer-seen-<place>, offer-click-<place>, offer-sent-<place>.
"""
PRICE = "from DKK 2,500"            # placeholder until Henrik sets it
CONTACT_URL = "https://www.linkedin.com/in/henrikgjerning/"
FORM_URL = ""                        # optional external form; empty = copy-and-message flow
HEADLINE = "Have a strategy of your own?"
PITCH = ("We run it through the same engine as this series: six point-in-time markets, 2013 to 2026, "
         "after trading costs, pre-registered before we look. You get one factsheet showing where it "
         "lands among 19 famous rules, including how it behaves in crash months.")
SMALL = ("Research, not investment advice. Your rule stays confidential unless you say otherwise, "
         "and you get the honest result, which is usually that the market is hard to beat.")
