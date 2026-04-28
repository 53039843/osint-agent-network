"""
Seed script: populates the database with well-known APT groups
sourced from MITRE ATT&CK and public threat intelligence reports.

Usage:
    python scripts/seed_threat_actors.py
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from db.session import AsyncSessionLocal
from db.crud import upsert_threat_actor

KNOWN_THREAT_ACTORS = [
    {
        "name": "APT29",
        "aliases": ["Cozy Bear", "The Dukes", "Midnight Blizzard", "NOBELIUM"],
        "origin_country": "Russia",
        "motivation": "Espionage",
        "associated_malware": ["SUNBURST", "TEARDROP", "MiniDuke", "CosmicDuke"],
        "mitre_groups": ["G0016"],
        "description": "APT29 is a threat group attributed to Russia's Foreign Intelligence Service (SVR). Known for the SolarWinds supply chain attack (2020) and targeting government, healthcare, and energy sectors globally."
    },
    {
        "name": "APT28",
        "aliases": ["Fancy Bear", "Sofacy", "Pawn Storm", "Forest Blizzard"],
        "origin_country": "Russia",
        "motivation": "Espionage, Influence Operations",
        "associated_malware": ["X-Agent", "Sofacy", "CHOPSTICK", "GAMEFISH"],
        "mitre_groups": ["G0007"],
        "description": "APT28 is attributed to Russia's GRU military intelligence. Responsible for the 2016 DNC hack and numerous election interference campaigns."
    },
    {
        "name": "Lazarus Group",
        "aliases": ["HIDDEN COBRA", "Guardians of Peace", "ZINC", "Diamond Sleet"],
        "origin_country": "North Korea",
        "motivation": "Financial gain, Espionage",
        "associated_malware": ["WannaCry", "BLINDINGCAN", "HOPLIGHT", "ELECTRICFISH"],
        "mitre_groups": ["G0032"],
        "description": "Lazarus Group is a North Korean state-sponsored threat actor responsible for the 2017 WannaCry ransomware attack and numerous cryptocurrency exchange heists."
    },
    {
        "name": "APT41",
        "aliases": ["Double Dragon", "Winnti", "Barium", "Wicked Panda"],
        "origin_country": "China",
        "motivation": "Espionage, Financial gain",
        "associated_malware": ["POISONPLUG", "MESSAGETAP", "KEYPLUG"],
        "mitre_groups": ["G0096"],
        "description": "APT41 is a prolific Chinese state-sponsored threat actor that conducts both espionage and financially motivated intrusions, targeting healthcare, telecom, and gaming industries."
    },
    {
        "name": "APT32",
        "aliases": ["OceanLotus", "SeaLotus", "Canvas Cyclone"],
        "origin_country": "Vietnam",
        "motivation": "Espionage",
        "associated_malware": ["WINDSHIELD", "SOUNDBITE", "PHOREAL", "BEACON"],
        "mitre_groups": ["G0050"],
        "description": "APT32 is a Vietnamese threat actor targeting foreign governments, journalists, and private sector companies with interests in Vietnam."
    },
]

async def seed():
    print("Seeding threat actor database...")
    async with AsyncSessionLocal() as db:
        for actor_data in KNOWN_THREAT_ACTORS:
            actor = await upsert_threat_actor(db, **actor_data)
            print(f"  ✓ Upserted: {actor.name} (aliases: {', '.join(actor.aliases[:2])}...)")
    print(f"\nDone. Seeded {len(KNOWN_THREAT_ACTORS)} threat actors.")

if __name__ == "__main__":
    asyncio.run(seed())
