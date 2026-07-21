# Databricks Free Edition — what you can and can't do

A condensed version of the [official limitations page](https://docs.databricks.com/aws/en/getting-started/free-edition-limitations),
covering the parts that matter for this guide. Check the official page if something here
seems out of date — Databricks changes these.

## The one that will actually bite you

**Exceed your daily quota and your compute shuts down for the rest of the day.** In extreme
cases, the rest of the month. There's no warning and no way to pay your way out.

Two habits that avoid it:

- `LIMIT 100` on exploratory queries — you're looking at the shape of the data, not reading
  all of it
- Don't leave things running

## Compute

| | |
|---|---|
| **Serverless only** | You cannot create classic or all-purpose compute clusters. This is why several official tutorials won't work — they start with "create a cluster" |
| **SQL warehouse** | One, at the smallest size (2X-Small) |
| **Concurrent jobs** | Up to 5 job tasks |
| **Pipelines** | One active pipeline per type |
| **Apps** | Up to 3, each running up to 24 hours after start or redeploy |

## Languages

**Python and SQL only.** No Scala, no R. Tutorials often show tabs for those — ignore them.

## AI and machine learning

| | |
|---|---|
| **Model serving** | Limited endpoints, CPU only |
| **No GPU serving** | No provisioned throughput, no custom GPU models, no batch inference |
| **Vector Search** | One endpoint, one search unit. Direct Vector Access not supported |
| **AI functions** | `ai_query()` and friends may or may not work depending on region |

This is why the project in Part 3 does its embedding and search in local Python rather than
using Databricks Vector Search — fewer moving parts, no quota risk, and you learn more.

## Networking

**Outbound internet access is restricted to a limited set of trusted domains.**

This shapes the whole project. A notebook probably cannot reach `api.openai.com`, which is
why Part 3 calls the model from a local script instead of from inside Databricks. As it
turns out, that's also closer to how real systems are built — see Part 3's architecture
notes.

Connecting *into* Databricks from your laptop is a normal client connection and is
unaffected.

## Storage

| | |
|---|---|
| **Volume uploads** | Any file format. 5 GB per file through the interface |
| **Sample data** | The `samples` catalog is available — `samples.nyctaxi.trips` and others |

## Other

- **Non-commercial use only.** It's for learning; don't run a business on it.
- **Personal access tokens work** — Settings → Developer → Access tokens. You'll need one
  in Part 3. Note that Databricks now considers these a legacy authentication method and
  recommends OAuth for production use, and that unused tokens are automatically revoked
  after 90 days.

## Free Edition vs. free trial

Not the same thing:

- **Free trial** — full platform, about $400 in credits, expires in roughly two weeks
- **Free Edition** — limited platform, free forever

You want Free Edition. See [the comparison](https://docs.databricks.com/aws/en/getting-started/free-trial-vs-free-edition).
