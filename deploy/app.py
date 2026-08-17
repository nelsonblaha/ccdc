"""Chucodata: the site and its signup list.

The machinery this runs on was written here and then lifted out into its own
package, so that the next person with something to propose does not have to
rebuild it: https://github.com/nelsonblaha/campaignlanding

What is left in this file is only what is about Chucodata. Everything below is a
statement about this campaign, not about how a campaign works. If something here
starts looking like machinery again, it belongs upstream instead.

Signups land in $CHUCODATA_DATA/signups.jsonl and can always be read over SSH. There
is also one authenticated HTTP view of them at /admin, gated by a password whose
hash lives only in the deploy environment. Without both CHUCODATA_SECRET_KEY and that
hash, those routes 404 and the page carries no admin markup at all.
"""

import os
from pathlib import Path

from campaignlanding import Config, Language, create_app

SITE_DIR = Path(os.environ.get("CHUCODATA_SITE", "/app/site"))
DATA_DIR = Path(os.environ.get("CHUCODATA_DATA", "/data"))

app = create_app(
    Config(
        name="Chucodata",
        site_dir=SITE_DIR,
        data_dir=DATA_DIR,
        # English is at "/", which negotiates, and at "/en/", which does not.
        # Spanish is at "/es/", which always means Spanish: in a metro where the
        # sender's language says nothing about the recipient's, the link people
        # paste into a group chat should be the one that lets each reader's own
        # browser decide.
        languages=[
            Language(
                code="en",
                page="index.html",
                strings={
                    "thanks_body": (
                        "That's the whole thing. We'll email when there's something "
                        "real to report — a board, a filing, a service you can "
                        "actually use."
                    ),
                    "back": "Back to the proposal",
                },
            ),
            Language(
                code="es",
                page="es/index.html",
                prefix="es",
                thanks_path="/es/gracias",
                strings={
                    "thanks_body": (
                        "Eso es todo. Te escribiremos cuando haya algo real que "
                        "contar: una junta directiva, un trámite, un servicio que "
                        "de veras puedas usar."
                    ),
                    "back": "Volver a la propuesta",
                },
            ),
        ],
        # chucodata.org is the permanent home (doc 06, item 9). ccdc.blaha.io is a
        # personal hostname that served the proposal while it had no domain of its
        # own, and epcdc.blaha.io predates the rename; both are kept so links
        # shared before the move still resolve.
        canonical_host="chucodata.org",
        legacy_hosts=frozenset(
            {"ccdc.blaha.io", "epcdc.blaha.io", "www.chucodata.org"}
        ),
        # ...and the redirect itself comes from CHUCODATA_CANONICAL_REDIRECT in the
        # deploy environment, so it can be turned on only once the new name is
        # verified serving end to end. A 301 is the response browsers cache
        # hardest, and pointing one at a name that does not resolve yet is not
        # something you can take back.
        help_choices=frozenset({"updates", "board", "legal", "technical", "spread"}),
        # The rail's own labels, hyphen-spaced, in both languages, so a Spanish
        # reader can share /hoja-de-ruta and an English one /roadmap and both land
        # in the same place in whichever language the reader's browser asks for.
        sections={
            "why": "why",
            "the-proposal": "proposal",
            "roadmap": "roadmap",
            "why-here": "border",
            "how-to-help": "help",
            "por-que": "why",
            "la-propuesta": "proposal",
            "hoja-de-ruta": "roadmap",
            "por-que-aqui": "border",
            "como-ayudar": "help",
        },
        # The four reasons are tabs inside the "why" section, keyed by the tab's
        # element id, which is the same in both languages while the labels are not.
        tabs={
            "environment": "tab-env",
            "privacy": "tab-privacy",
            "ownership": "tab-own",
            "services": "tab-svc",
            "medio-ambiente": "tab-env",
            "privacidad": "tab-privacy",
            "propiedad": "tab-own",
            "servicios": "tab-svc",
        },
        tabs_section="why",
        # Counts the founder, who is on the list in every sense except having
        # submitted the form. /admin shows the stored rows and says so, so the two
        # numbers never look like a discrepancy.
        founder_offset=1,
        # Below this the invitation is not shown at all. A small number is worse
        # than no number: "join 2 others" tells a reader the list is nearly empty
        # at the moment they are deciding whether to be on it. The administrator
        # still sees it at any count, because for them it is not social proof, it
        # is the notification and the way to the list.
        show_count_above=16,
        # CHUCODATA_SECRET_KEY, CHUCODATA_ADMIN_HASH_FILE, CHUCODATA_CANONICAL_REDIRECT.
        env_prefix="CHUCODATA",
        # Unchanged across the extraction on purpose: a new cookie name would sign
        # out every device that is already signed in.
        session_cookie_name="ccdc_admin",
    )
)
