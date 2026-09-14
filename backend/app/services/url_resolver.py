import httpx
from typing import List, Dict, Any

DEFAULT_TIMEOUT = 5.0
MAX_REDIRECTS = 10


async def unroll_url(url: str) -> Dict[str, Any]:
    """
    Traces HTTP redirects (e.g., shortlinks like bit.ly) asynchronously
    and returns the hop chain along with the final destination URL.
    """
    hops: List[str] = [url]
    current_url = url

    headers = {
        "User-Agent": "Mozilla/5.0 (Android Mobile; PhishGuard/1.0)",
    }

    async with httpx.AsyncClient(
        headers=headers, timeout=DEFAULT_TIMEOUT, follow_redirects=False
    ) as client:
        for _ in range(MAX_REDIRECTS):
            try:
                # Use HEAD first to save bandwidth; fallback to GET on 405/400
                response = await client.head(current_url)
                if response.status_code in (405, 400):
                    response = await client.get(current_url)

                if response.is_redirect or "location" in response.headers:
                    next_url = response.headers["location"]
                    # Handle relative URLs in redirect headers
                    if next_url.startswith("/"):
                        parsed_base = httpx.URL(current_url)
                        next_url = f"{parsed_base.scheme}://{parsed_base.netloc}{next_url}"

                    hops.append(next_url)
                    current_url = next_url
                else:
                    break
            except (httpx.RequestError, httpx.HTTPStatusError):
                # Reachable limit or connection failure; return best effort
                break

    return {
        "initial_url": url,
        "final_destination_url": current_url,
        "redirect_count": len(hops) - 1,
        "hops": hops,
    }