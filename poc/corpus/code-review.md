# Code Review

## Approvals required

All changes to production code require 2 approvals before merge. Changes to
infrastructure, authentication, or payment handling require 2 approvals, at least one
from the owning team.

Documentation-only changes require 1 approval.

## Response times

Reviewers are expected to give an initial response within 24 hours on working days. If a
review is urgent, say so explicitly and say why — "urgent" without a reason is not
actionable.

## What reviewers look for

- Correctness, and whether the tests actually demonstrate it
- Whether the change is understandable to someone who was not in the discussion
- Security implications, particularly around access to customer data
- Whether it is the smallest change that solves the problem

## Tone

Review comments address the code, not the author. Prefer questions to instructions where
there is genuine uncertainty. Approving with minor comments is encouraged — blocking a
change over formatting is not.

## Emergency changes

Production incidents may be resolved with a single approval, with a follow-up review
within 2 working days. Note the incident number in the change description.
