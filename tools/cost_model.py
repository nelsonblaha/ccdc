#!/usr/bin/env python3
"""Runnable cost model for the Chuco Community Data Center MVP.

The prose in docs/03-cost-model.md is generated from these assumptions. Change
the numbers here and re-run rather than editing tables by hand.

    python3 tools/cost_model.py
    python3 tools/cost_model.py --members 500 --turns 300 --model gemini-3.7-flash

Prices researched 2026-08-16. Re-verify before quoting to a donor or a board.
"""

import argparse
from dataclasses import dataclass

# --------------------------------------------------------------------------
# Assumptions you should argue about
# --------------------------------------------------------------------------

# Tokens per average chat turn. Input dominates because the whole conversation
# history is resent every turn; this is the number that most affects the answer.
INPUT_TOKENS_PER_TURN = 6_000
OUTPUT_TOKENS_PER_TURN = 700

# Fraction of input tokens that are unchanged history and therefore cacheable.
# Set CACHE_ENABLED = True to model the single biggest cost lever.
CACHEABLE_INPUT_FRACTION = 0.80
CACHE_ENABLED = False

DEFAULT_MEMBERS = 200
DEFAULT_TURNS_PER_MEMBER_PER_MONTH = 150


@dataclass(frozen=True)
class Model:
    name: str
    input_per_mtok: float
    output_per_mtok: float
    cached_input_per_mtok: float | None = None
    note: str = ''


# Per 1M tokens, USD. See docs/03-cost-model.md for sourcing.
MODELS = [
    Model('gemini-2.5-flash-lite', 0.10, 0.40, 0.01),
    Model('gpt-5-nano', 0.05, 0.40),
    Model('gpt-5-mini', 0.25, 2.00),
    Model('gemini-2.5-flash', 0.30, 2.50, 0.03),
    Model('gemini-3.7-flash', 0.75, 3.75, 0.075, 'doubles to 1.50/7.50 on 2027-01-01'),
    Model('claude-haiku-4.5', 1.00, 5.00, 0.10),
    Model('gemini-2.5-pro', 1.25, 10.00, 0.125),
    Model('gpt-5.1', 1.25, 10.00),
    Model('claude-sonnet-5', 3.00, 15.00, 0.30, 'post-2026-09-01 standard rate'),
    Model('claude-opus-5', 5.00, 25.00, 0.50),
]

# Infrastructure, USD/month. See docs/03-cost-model.md.
HOSTING = {
    'gce-vm-on-demand': 65.00,      # e2-standard-2 + 100GB balanced PD + egress
    'gce-vm-1yr-cud': 46.00,        # same with committed use discount
    'gce-vm-plus-cloudsql': 100.00,  # + smallest Cloud SQL Postgres
    'cloud-run-always-warm': 150.00,  # 2 vCPU / 4 GiB pinned, upper bound
    'hetzner-cpx31': 30.00,
}

MISC_MONTHLY = 15.00              # domain, transactional email, monitoring
NONPROFIT_CREDIT_ANNUAL = 10_000  # Google for Nonprofits ceiling

# Stripe 501(c)(3) donation rate.
STRIPE_PCT = 0.022
STRIPE_FIXED = 0.30


def cost_per_turn(m: Model) -> float:
    """USD for one average chat turn."""
    if CACHE_ENABLED and m.cached_input_per_mtok is not None:
        cached = INPUT_TOKENS_PER_TURN * CACHEABLE_INPUT_FRACTION
        fresh = INPUT_TOKENS_PER_TURN - cached
        input_cost = (cached * m.cached_input_per_mtok + fresh * m.input_per_mtok) / 1e6
    else:
        input_cost = INPUT_TOKENS_PER_TURN * m.input_per_mtok / 1e6
    output_cost = OUTPUT_TOKENS_PER_TURN * m.output_per_mtok / 1e6
    return input_cost + output_cost


def stripe_net(gross: float) -> float:
    """What actually lands in the bank from one donation of `gross`."""
    return gross - (gross * STRIPE_PCT + STRIPE_FIXED)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--members', type=int, default=DEFAULT_MEMBERS)
    p.add_argument('--turns', type=int, default=DEFAULT_TURNS_PER_MEMBER_PER_MONTH,
                   help='chat turns per member per month')
    p.add_argument('--model', default='gemini-3.7-flash')
    p.add_argument('--hosting', default='gce-vm-on-demand', choices=sorted(HOSTING))
    p.add_argument('--cache', action='store_true', help='model context caching on cacheable history')
    args = p.parse_args()

    global CACHE_ENABLED
    CACHE_ENABLED = args.cache

    print(f'Assumptions: {INPUT_TOKENS_PER_TURN:,} in / {OUTPUT_TOKENS_PER_TURN:,} out per turn, '
          f'{args.turns} turns/member/month, caching {"ON" if CACHE_ENABLED else "OFF"}')
    print()

    print(f'{"model":<24}{"$/turn":>10}{"$/member/mo":>14}{"$/mo @ " + str(args.members):>16}{"$/yr":>12}')
    print('-' * 76)
    for m in MODELS:
        per_turn = cost_per_turn(m)
        per_member = per_turn * args.turns
        monthly = per_member * args.members
        marker = ' <-' if m.name == args.model else ''
        print(f'{m.name:<24}{per_turn:>10.4f}{per_member:>14.2f}{monthly:>16.2f}{monthly * 12:>12.0f}{marker}')
    print()

    chosen = next((m for m in MODELS if m.name == args.model), None)
    if chosen is None:
        raise SystemExit(f'unknown model {args.model!r}; pick one of {[m.name for m in MODELS]}')

    inference_monthly = cost_per_turn(chosen) * args.turns * args.members
    hosting_monthly = HOSTING[args.hosting]
    total_monthly = inference_monthly + hosting_monthly + MISC_MONTHLY
    total_annual = total_monthly * 12

    print(f'Budget: {args.members} members on {chosen.name}, hosting = {args.hosting}')
    print('-' * 76)
    print(f'{"inference":<40}{inference_monthly:>12.2f}/mo{inference_monthly * 12:>12.0f}/yr')
    print(f'{"hosting":<40}{hosting_monthly:>12.2f}/mo{hosting_monthly * 12:>12.0f}/yr')
    print(f'{"misc (domain, email, monitoring)":<40}{MISC_MONTHLY:>12.2f}/mo{MISC_MONTHLY * 12:>12.0f}/yr')
    print(f'{"TOTAL":<40}{total_monthly:>12.2f}/mo{total_annual:>12.0f}/yr')

    covered = min(total_annual, NONPROFIT_CREDIT_ANNUAL)
    print(f'{"Google for Nonprofits credit (max 10k)":<40}{"":>12}   {-covered:>12.0f}/yr')
    print(f'{"NET CASH":<40}{"":>12}   {total_annual - covered:>12.0f}/yr')
    print()

    if total_annual > NONPROFIT_CREDIT_ANNUAL:
        headroom_members = int(NONPROFIT_CREDIT_ANNUAL / 12 / (cost_per_turn(chosen) * args.turns))
        print(f'Credit is exhausted. It covers roughly {headroom_members} members at this usage.')
    else:
        headroom_members = int((NONPROFIT_CREDIT_ANNUAL / 12 - hosting_monthly - MISC_MONTHLY)
                               / (cost_per_turn(chosen) * args.turns))
        print(f'Credit covers this comfortably: room for about {headroom_members} members '
              f'at {args.turns} turns/month before cash is needed.')

    print()
    print('Dues required to break even (annual, after Stripe fees):')
    per_member_annual = total_annual / args.members
    for dues in (25, 50, 60, 100, 120):
        print(f'  ${dues:>4}/yr dues -> ${stripe_net(dues):>6.2f} net vs ${per_member_annual:>6.2f} cost '
              f'per member  {"OK" if stripe_net(dues) >= per_member_annual else "SHORT"}')


if __name__ == '__main__':
    main()
