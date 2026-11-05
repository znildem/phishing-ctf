# Phishing Infrastructure Investigation CTF

A self-contained OSINT and network security CTF. Participants investigate a
look-alike domain used against the fictional company Quillmarsh Logistics.

All domains use the reserved `.test` TLD, and the lab runs on an isolated,
internal Docker network with no internet access and no ports published to the host.

## Requirements
- Docker Desktop (with Docker Compose)

## Start the lab

cd infra
docker compose up -d --build
docker exec -it qm-analyst bash

The challenge files are in `~/challenge`. Start with `BRIEF.md`.

## Stop the lab
cd infra
docker compose down


## Repository layout
- `challenge/` - files given to participants
- `infra/` - Docker lab (analyst workstation and target server)
- `solution/` - answer key (do not give to participants)
- `docs/` - supporting material
