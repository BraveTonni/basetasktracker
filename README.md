# Base application

Kanban task tracker. Domain events go to the event bus.

## Event bus

Set env vars (see `.env.example`):

```bash
EVENT_BUS_URL=http://localhost:8000
EVENT_BUS_TOKEN=<jwt from bus cli>
EVENT_BUS_SENDER=kanban
```

Without `EVENT_BUS_TOKEN` the app runs standalone and publishes nothing.

Published kinds:

| Kind | When |
|---|---|
| `kanban.task.created` | task added to column |
| `kanban.task.moved` | task moved between columns |
| `kanban.task.deleted` | task removed |

## Run

```bash
uv run main.py
```
