"""Post to LinkedIn when a blog post is published.

Required environment variables:
  LINKEDIN_ACCESS_TOKEN  — OAuth 2.0 token with w_member_social scope
  LINKEDIN_PERSON_ID     — LinkedIn person URN (e.g. "abc123def")

Usage:
  python post_to_linkedin.py blog/posts/my-post/
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

API_BASE = "https://api.linkedin.com/v2"
SITE_URL = "https://mauroloprete.github.io/mauroloprete/blog/posts"


def linkedin_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
        "LinkedIn-Version": "202401",
    }


def upload_image(token: str, person_id: str, image_path: Path) -> str:
    """Upload image to LinkedIn and return the asset URN."""
    # Step 1: Register upload
    register_body = {
        "registerUploadRequest": {
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "owner": f"urn:li:person:{person_id}",
            "serviceRelationships": [
                {
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent",
                }
            ],
        }
    }

    req = urllib.request.Request(
        f"{API_BASE}/assets?action=registerUpload",
        data=json.dumps(register_body).encode(),
        headers=linkedin_headers(token),
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())

    upload_url = result["value"]["uploadMechanism"][
        "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"
    ]["uploadUrl"]
    asset = result["value"]["asset"]

    # Step 2: Upload binary
    with open(image_path, "rb") as f:
        image_data = f.read()

    req = urllib.request.Request(
        upload_url,
        data=image_data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/octet-stream",
        },
        method="PUT",
    )
    urllib.request.urlopen(req)

    return asset


def create_post(token: str, person_id: str, text: str, image_asset: str) -> str:
    """Create a LinkedIn post with image. Returns post URN."""
    body = {
        "author": f"urn:li:person:{person_id}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "IMAGE",
                "media": [
                    {
                        "status": "READY",
                        "media": image_asset,
                    }
                ],
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }

    req = urllib.request.Request(
        f"{API_BASE}/ugcPosts",
        data=json.dumps(body).encode(),
        headers=linkedin_headers(token),
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())

    return result["id"]


def add_comment(token: str, post_urn: str, comment_text: str) -> None:
    """Add a comment to a LinkedIn post (for the link)."""
    body = {
        "actor": post_urn.split(":ugcPost:")[0].replace("ugcPost", "person"),
        "message": {"text": comment_text},
    }

    # Extract the activity URN from post URN
    # urn:li:ugcPost:123 -> urn:li:activity:123
    activity_urn = post_urn.replace("ugcPost", "activity")
    encoded_urn = urllib.parse.quote(activity_urn, safe="")

    req = urllib.request.Request(
        f"{API_BASE}/socialActions/{encoded_urn}/comments",
        data=json.dumps(body).encode(),
        headers=linkedin_headers(token),
        method="POST",
    )
    urllib.request.urlopen(req)


def main() -> int:
    token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    person_id = os.environ.get("LINKEDIN_PERSON_ID")

    if not token or not person_id:
        print("Error: LINKEDIN_ACCESS_TOKEN and LINKEDIN_PERSON_ID must be set")
        return 1

    if len(sys.argv) < 2:
        print("Usage: python post_to_linkedin.py <post_dir> [post_dir2 ...]")
        return 1

    import urllib.parse

    for post_dir in sys.argv[1:]:
        post_path = Path(post_dir)
        linkedin_txt = post_path / "linkedin.txt"
        linkedin_img = post_path / "linkedin.png"
        linkedin_comment = post_path / "linkedin_comment.txt"

        if not linkedin_txt.exists():
            print(f"Skip {post_dir}: no linkedin.txt")
            continue
        if not linkedin_img.exists():
            print(f"Skip {post_dir}: no linkedin.png")
            continue

        text = linkedin_txt.read_text(encoding="utf-8").strip()
        comment = (
            linkedin_comment.read_text(encoding="utf-8").strip()
            if linkedin_comment.exists()
            else f"📖 Leelo acá: {SITE_URL}/{post_path.name}/"
        )

        print(f"Uploading image for {post_dir}...")
        asset = upload_image(token, person_id, linkedin_img)

        print(f"Creating post for {post_dir}...")
        post_urn = create_post(token, person_id, text, asset)
        print(f"Post created: {post_urn}")

        # Wait a bit before commenting
        time.sleep(3)

        print(f"Adding comment with link...")
        add_comment(token, post_urn, comment)
        print(f"Comment added for {post_dir}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
