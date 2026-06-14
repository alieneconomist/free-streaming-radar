#!/usr/bin/env python3
"""Generate the legal free streaming dashboard data file."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "public" / "free-streaming-dashboard" / "data.json"


SERVICES = [
    {
        "name": "Tubi",
        "url": "https://tubitv.com/",
        "domain": "tubitv.com",
        "rank": 1,
        "rating": 96,
        "movieDepth": 96,
        "tvDepth": 92,
        "liveDepth": 76,
        "freshness": 94,
        "signup": "Optional",
        "bestFor": "Movies, big TV library, recent free arrivals",
        "country": "US, Canada, Australia, Mexico, UK, Latin America availability varies",
        "tags": ["movies", "tv", "live", "no-required-signup"],
        "latestSignals": [
            "Official site exposes Recently Added, Most Popular, Movies, TV Shows, and Live TV sections.",
            "Current homepage includes 2025-2026 titles and active FOX sports/event hubs.",
        ],
        "watchNotes": "Strong first stop for free on-demand movies and recognizable TV. Ads are the tradeoff.",
        "sources": [
            {
                "label": "Tubi official catalog",
                "url": "https://tubitv.com/",
            },
            {
                "label": "Tom's Guide free streaming roundup",
                "url": "https://www.tomsguide.com/best-picks/best-free-streaming-services",
            },
            {
                "label": "JustWatch Tubi provider page",
                "url": "https://www.justwatch.com/us/provider/tubi-tv",
            },
        ],
    },
    {
        "name": "The Roku Channel",
        "url": "https://therokuchannel.roku.com/",
        "domain": "therokuchannel.roku.com",
        "rank": 2,
        "rating": 94,
        "movieDepth": 92,
        "tvDepth": 91,
        "liveDepth": 95,
        "freshness": 92,
        "signup": "Optional on web; device account often used",
        "bestFor": "FAST channels, broad household viewing, originals",
        "country": "US, Canada, Mexico, UK availability varies",
        "tags": ["movies", "tv", "live"],
        "latestSignals": [
            "Roku recently added 22 free live channels according to Tom's Guide.",
            "Public references show 500+ free channels and a large free movie/show catalog.",
        ],
        "watchNotes": "A top cable-like free option, especially if the viewer already uses Roku hardware.",
        "sources": [
            {
                "label": "Roku Channel official site",
                "url": "https://therokuchannel.roku.com/",
            },
            {
                "label": "Tom's Guide Roku channel update",
                "url": "https://www.tomsguide.com/entertainment/streaming/roku-just-got-22-new-free-channels-heres-what-you-can-watch-now",
            },
        ],
    },
    {
        "name": "Pluto TV",
        "url": "https://pluto.tv/",
        "domain": "pluto.tv",
        "rank": 3,
        "rating": 92,
        "movieDepth": 86,
        "tvDepth": 88,
        "liveDepth": 98,
        "freshness": 89,
        "signup": "Optional",
        "bestFor": "Live TV grid, channel surfing, Paramount-backed library",
        "country": "Americas and Europe, catalog varies by country",
        "tags": ["movies", "tv", "live", "no-required-signup"],
        "latestSignals": [
            "Official site positions Pluto as free movies, TV shows, and live TV.",
            "Public references show hundreds of FAST channels and a cable-style grid model.",
        ],
        "watchNotes": "Best when the viewer wants to turn something on now instead of searching a catalog.",
        "sources": [
            {"label": "Pluto TV official site", "url": "https://pluto.tv/"},
            {
                "label": "FAST category reference",
                "url": "https://en.wikipedia.org/wiki/Free_ad-supported_streaming_television",
            },
        ],
    },
    {
        "name": "Plex",
        "url": "https://watch.plex.tv/",
        "domain": "watch.plex.tv",
        "rank": 4,
        "rating": 88,
        "movieDepth": 87,
        "tvDepth": 82,
        "liveDepth": 88,
        "freshness": 84,
        "signup": "Recommended",
        "bestFor": "Free movies plus personal media and discovery tools",
        "country": "Global availability varies by title",
        "tags": ["movies", "tv", "live"],
        "latestSignals": [
            "Official watch site lists free movies, TV shows, and live TV.",
            "Editorial roundups continue to rank Plex as a major free streaming option.",
        ],
        "watchNotes": "Good for people who also want watchlists and personal-library tooling.",
        "sources": [
            {"label": "Plex official watch site", "url": "https://watch.plex.tv/"},
            {
                "label": "TechRadar free streaming guide",
                "url": "https://www.techradar.com/streaming/draft-best-free-streaming-service-2024-tubi-pluto-tv-the-roku-channel-and-more",
            },
        ],
    },
    {
        "name": "Sling Freestream",
        "url": "https://www.sling.com/freestream",
        "domain": "sling.com",
        "rank": 5,
        "rating": 86,
        "movieDepth": 83,
        "tvDepth": 86,
        "liveDepth": 94,
        "freshness": 86,
        "signup": "Free account improves experience",
        "bestFor": "Large live channel bundle and free on-demand backup",
        "country": "US",
        "tags": ["movies", "tv", "live"],
        "latestSignals": [
            "Official Sling page markets Freestream as free live TV, shows, movies, and news.",
            "Recent buying guides cite hundreds of free live channels and tens of thousands of on-demand titles.",
        ],
        "watchNotes": "A strong live-TV complement to Tubi or Plex.",
        "sources": [
            {
                "label": "Sling Freestream official site",
                "url": "https://www.sling.com/freestream",
            },
            {
                "label": "TechRadar Sling trial and Freestream guide",
                "url": "https://www.techradar.com/deals/sling-tv-free-trial",
            },
        ],
    },
    {
        "name": "YouTube Free",
        "url": "https://www.youtube.com/feed/storefront?bp=ogUCKAI%3D",
        "domain": "youtube.com",
        "rank": 6,
        "rating": 84,
        "movieDepth": 86,
        "tvDepth": 72,
        "liveDepth": 68,
        "freshness": 82,
        "signup": "Optional",
        "bestFor": "Free movies, clips, creator-adjacent discovery",
        "country": "Global availability varies",
        "tags": ["movies", "tv", "no-required-signup"],
        "latestSignals": [
            "Major free-streaming roundups include YouTube as a free movies and series source.",
            "JustWatch tracks YouTube Free as a separate free provider.",
        ],
        "watchNotes": "Huge reach, but the free movie catalog can be noisier than dedicated FAST apps.",
        "sources": [
            {
                "label": "Tom's Guide free streaming roundup",
                "url": "https://www.tomsguide.com/best-picks/best-free-streaming-services",
            },
            {
                "label": "JustWatch provider directory",
                "url": "https://www.justwatch.com/us/provider/tubi-tv",
            },
        ],
    },
    {
        "name": "Fandango at Home Free",
        "url": "https://www.vudu.com/content/movies/free",
        "domain": "vudu.com",
        "rank": 7,
        "rating": 82,
        "movieDepth": 84,
        "tvDepth": 70,
        "liveDepth": 45,
        "freshness": 78,
        "signup": "Required",
        "bestFor": "Free-with-ads movies next to rentals and purchases",
        "country": "US",
        "tags": ["movies", "tv"],
        "latestSignals": [
            "Editorial roundups still include Fandango at Home/Vudu for free ad-supported movies.",
            "JustWatch tracks Fandango as a provider in the US catalog.",
        ],
        "watchNotes": "Useful when a viewer already uses Fandango/Vudu for rentals.",
        "sources": [
            {
                "label": "Tom's Guide free streaming roundup",
                "url": "https://www.tomsguide.com/best-picks/best-free-streaming-services",
            },
            {
                "label": "JustWatch provider directory",
                "url": "https://www.justwatch.com/us/provider/tubi-tv",
            },
        ],
    },
    {
        "name": "Kanopy",
        "url": "https://www.kanopy.com/",
        "domain": "kanopy.com",
        "rank": 8,
        "rating": 81,
        "movieDepth": 82,
        "tvDepth": 66,
        "liveDepth": 0,
        "freshness": 76,
        "signup": "Library or university card required",
        "bestFor": "Critically regarded cinema, documentaries, education",
        "country": "Library/university dependent",
        "tags": ["movies", "tv", "library-card"],
        "latestSignals": [
            "TechRadar ranks Kanopy as a distinct free option for educational and classic cinema.",
            "Access depends on a participating library or university, so it is not universal.",
        ],
        "watchNotes": "Highest signal-to-noise for film lovers if the user's library supports it.",
        "sources": [
            {"label": "Kanopy official site", "url": "https://www.kanopy.com/"},
            {
                "label": "TechRadar free streaming guide",
                "url": "https://www.techradar.com/streaming/draft-best-free-streaming-service-2024-tubi-pluto-tv-the-roku-channel-and-more",
            },
        ],
    },
    {
        "name": "Xumo Play",
        "url": "https://play.xumo.com/",
        "domain": "xumo.com",
        "rank": 9,
        "rating": 78,
        "movieDepth": 73,
        "tvDepth": 76,
        "liveDepth": 88,
        "freshness": 74,
        "signup": "Optional",
        "bestFor": "Live FAST channels and lean-back viewing",
        "country": "US, availability varies",
        "tags": ["movies", "tv", "live", "no-required-signup"],
        "latestSignals": [
            "FAST category references list Xumo as a major ad-supported platform.",
            "JustWatch tracks Xumo Play as a US provider.",
        ],
        "watchNotes": "Good secondary live-TV option behind Pluto/Roku/Sling.",
        "sources": [
            {"label": "Xumo Play official site", "url": "https://play.xumo.com/"},
            {
                "label": "FAST category reference",
                "url": "https://en.wikipedia.org/wiki/Free_ad-supported_streaming_television",
            },
        ],
    },
    {
        "name": "Samsung TV Plus",
        "url": "https://www.samsungtvplus.com/",
        "domain": "samsungtvplus.com",
        "rank": 10,
        "rating": 76,
        "movieDepth": 70,
        "tvDepth": 75,
        "liveDepth": 90,
        "freshness": 72,
        "signup": "Device/web availability varies",
        "bestFor": "Samsung-device live channels",
        "country": "Selected countries",
        "tags": ["movies", "tv", "live"],
        "latestSignals": [
            "FAST references list Samsung TV Plus as a major device-owned platform.",
            "Recent free-movie roundups cite Samsung TV Plus for rotating free titles.",
        ],
        "watchNotes": "Best if the viewer already has a Samsung TV or Galaxy device.",
        "sources": [
            {
                "label": "Samsung TV Plus official site",
                "url": "https://www.samsungtvplus.com/",
            },
            {
                "label": "FAST category reference",
                "url": "https://en.wikipedia.org/wiki/Free_ad-supported_streaming_television",
            },
        ],
    },
]


EXCLUDED = [
    {
        "name": "Amazon Freevee",
        "reason": "Retired as a standalone service; free content moved into Prime Video's free-with-ads area.",
        "source": "https://www.theverge.com/2024/11/12/24295129/amazon-shutting-down-freevee-prime-video",
    },
    {
        "name": "Peacock free tier",
        "reason": "No longer broadly available to new customers as a free standalone tier.",
        "source": "https://en.wikipedia.org/wiki/Peacock_(streaming_service)",
    },
    {
        "name": "Unlicensed mirror sites",
        "reason": "Excluded intentionally. This dashboard only lists legitimate ad-supported, library, or official free sources.",
        "source": "https://en.wikipedia.org/wiki/Free_ad-supported_streaming_television",
    },
]


def check_url(url: str) -> dict[str, str | int | None]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "MoneyballOS-FreeStreamingDashboard/1.0 (+https://github.com/alieneconomist/moneyball-os)"
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=8) as response:
            return {"ok": True, "status": response.status, "error": None}
    except urllib.error.HTTPError as exc:
        return {"ok": 200 <= exc.code < 400, "status": exc.code, "error": str(exc.reason)}
    except Exception as exc:  # noqa: BLE001 - status capture should never break deploy.
        return {"ok": False, "status": None, "error": exc.__class__.__name__}


def build_payload(check_live: bool) -> dict:
    now = datetime.now(timezone.utc).replace(microsecond=0)
    services = []

    for service in SERVICES:
        item = dict(service)
        item["legality"] = "Official/legal free source"
        item["price"] = "Free with ads or institution access"
        item["scoreBreakdown"] = {
            "catalog": round((item["movieDepth"] + item["tvDepth"]) / 2),
            "live": item["liveDepth"],
            "freshness": item["freshness"],
            "friction": 95 if "no-required-signup" in item["tags"] else 78,
        }
        item["health"] = {"checked": check_live, "ok": None, "status": None, "error": None}
        if check_live:
            item["health"].update(check_url(item["url"]))
        services.append(item)

    return {
        "generatedAt": now.isoformat().replace("+00:00", "Z"),
        "refreshCadence": "Daily via GitHub Actions schedule and workflow dispatch",
        "scope": "Legal free movie and TV streaming sites only",
        "method": {
            "rating": "0-100 editorial utility score combining catalog breadth, TV depth, live channel usefulness, recent-source freshness, and access friction.",
            "latest": "Daily generator refreshes timestamp and optional source reachability; source list is curated from official pages, JustWatch provider discovery, and current editorial roundups.",
        },
        "services": services,
        "excluded": EXCLUDED,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-live", action="store_true", help="Check source URL reachability.")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    payload = build_payload(check_live=args.check_live)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
