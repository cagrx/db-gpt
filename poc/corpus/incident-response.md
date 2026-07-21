# Incident Response

## Severity levels

| Level | Meaning | Response |
|---|---|---|
| SEV1 | Complete outage, or customer data at risk | Immediate, 24/7 |
| SEV2 | Major feature unavailable, no workaround | Within 30 minutes, working hours extended |
| SEV3 | Degraded performance, workaround exists | Next working day |
| SEV4 | Minor issue, no customer impact | Scheduled with normal work |

## Declaring an incident

Anyone can declare an incident. You do not need permission and you will not be criticised
for declaring one that turns out to be minor. Use the `/incident` command in chat, which
creates a channel and pages the on-call engineer.

## Roles

The **incident commander** coordinates and makes decisions. They do not debug. The
**communications lead** handles updates to stakeholders and customers. Responders
investigate and fix.

For SEV1 and SEV2, these must be three different people.

## On-call

On-call rotations are one week, handed over on Wednesday mornings. On-call engineers
receive a weekly allowance and time off in lieu for out-of-hours pages.

## Afterwards

Every SEV1 and SEV2 gets a written review within 5 working days. Reviews are blameless:
they examine what made the failure possible, not who typed the command.
