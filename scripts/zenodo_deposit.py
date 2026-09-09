#!/usr/bin/env python3
"""
zenodo_deposit.py -- Zenodo deposition helper for this repository (stdlib only).

Adapted from ~/ANSE.ASIA/glosa/scripts/zenodo_deposit.py (this workspace's own reusable
Zenodo-deposit pattern) for a standalone single-paper repo with no glosa-style
registry/ apparatus of its own.

Tier: Dr (tooling, not a research claim). Readout-not-truth applies to every printed field:
HTTP responses are readouts from Zenodo's API, not truth about the deposition's final state --
always re-run `status` after a mutating call.

Subcommands:
  create-draft      POST /api/deposit/depositions (metadata from .zenodo.json + prereserve_doi)
  upload <files...> PUT files into the deposition's bucket (default: git-archive tarball +
                     paper/main.pdf)
  update-metadata   PUT metadata again (version from CITATION.cff)
  status            GET the deposition and print a summary
  new-version       POST actions/newversion (documents the concept DOI for later updates)
  publish           GUARDED -- requires --i-have-founder-approval (a file
                     registry/RELEASE_APPROVAL.txt containing APPROVED) OR --founder-instructed
                     "<verbatim instruction + date>" for a same-session explicit founder chat
                     instruction, logged into registry/zenodo_uploads/<id>.json so the bypass is
                     auditable, never silent.

Secrets: never read from argv, never printed. Token comes from the environment (ZENODO_TOKEN /
ZENODO_SANDBOX_TOKEN), sourced from this workspace's shared secret file:
    set -a; . ~/.config/araya/zenodo.env; set +a
    python3 scripts/zenodo_deposit.py status

--sandbox switches to sandbox.zenodo.org and ZENODO_SANDBOX_TOKEN.
"""
import argparse
import datetime
import json
import os
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = REPO_ROOT / "registry" / "zenodo_state.json"
ZENODO_JSON_PATH = REPO_ROOT / ".zenodo.json"
CITATION_PATH = REPO_ROOT / "CITATION.cff"
RELEASE_APPROVAL_PATH = REPO_ROOT / "registry" / "RELEASE_APPROVAL.txt"
ZENODO_UPLOADS_DIR = REPO_ROOT / "registry" / "zenodo_uploads"


def founder_approval_gate(args, script_name: str):
    """Hard-refuse a publish action unless founder approval is present.

    Two auditable routes, no silent third path:
      1. --i-have-founder-approval AND registry/RELEASE_APPROVAL.txt containing APPROVED.
      2. --founder-instructed "<verbatim instruction + date>" -- a same-session explicit chat
         instruction that bypasses the file check but is logged (via `log_founder_instruction`,
         called by the caller once a deposition id is known) so the bypass is never silent.
    Exits 1 with a message on refusal; returns None on success. Never makes a network call.
    """
    instructed = getattr(args, "founder_instructed", None)
    if instructed:
        if len(instructed.strip()) < 15:
            print(
                f"{script_name}: refused -- --founder-instructed must be the verbatim founder "
                "instruction plus a date, not a short placeholder",
                file=sys.stderr,
            )
            sys.exit(1)
        print(f"{script_name}: proceeding under --founder-instructed (will be logged): {instructed}")
        return
    if not getattr(args, "i_have_founder_approval", False):
        print(f"{script_name}: refused -- publish requires --i-have-founder-approval "
              "(or --founder-instructed \"<verbatim instruction + date>\")", file=sys.stderr)
        sys.exit(1)
    if not RELEASE_APPROVAL_PATH.exists():
        print(f"{script_name}: refused -- {RELEASE_APPROVAL_PATH} does not exist", file=sys.stderr)
        sys.exit(1)
    text = RELEASE_APPROVAL_PATH.read_text()
    if "APPROVED" not in text:
        print(f"{script_name}: refused -- {RELEASE_APPROVAL_PATH} does not contain APPROVED", file=sys.stderr)
        sys.exit(1)


def log_founder_instruction(deposition_id, instruction: str, extra: dict = None) -> None:
    ZENODO_UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = ZENODO_UPLOADS_DIR / f"{deposition_id}.json"
    record = {}
    if out_path.exists():
        try:
            record = json.loads(out_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            record = {}
    record["deposition_id"] = deposition_id
    record["founder_instructed_bypass"] = {
        "instruction": instruction,
        "logged_at": datetime.datetime.now().isoformat(timespec="seconds"),
    }
    if extra:
        record.update(extra)
    out_path.write_text(json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"logged --founder-instructed bypass to {out_path}")


def api_base(sandbox: bool) -> str:
    return "https://sandbox.zenodo.org/api" if sandbox else "https://zenodo.org/api"


def get_token(sandbox: bool) -> str:
    var = "ZENODO_SANDBOX_TOKEN" if sandbox else "ZENODO_TOKEN"
    tok = os.environ.get(var, "")
    if not tok:
        print(
            f"zenodo_deposit: {var} not set in environment. "
            f"Run `set -a; . ~/.config/araya/zenodo.env; set +a` first "
            f"(never pass tokens on argv).",
            file=sys.stderr,
        )
        sys.exit(2)
    return tok


def load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {}


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")


def http_request(method: str, url: str, token: str, data=None, headers=None, raw=False):
    hdrs = dict(headers or {})
    hdrs["Authorization"] = f"Bearer {token}"
    body = None
    if data is not None:
        if raw:
            body = data
        else:
            body = json.dumps(data).encode("utf-8")
            hdrs.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            status = resp.status
            payload = resp.read()
    except urllib.error.HTTPError as e:
        status = e.code
        payload = e.read()
    except urllib.error.URLError as e:
        print(f"zenodo_deposit: network error contacting Zenodo: {e.reason}", file=sys.stderr)
        sys.exit(3)
    if not payload:
        return status, {}
    try:
        return status, json.loads(payload)
    except json.JSONDecodeError:
        return status, {"_raw_text": payload.decode("utf-8", errors="replace")}


def die_on_error(status: int, resp: dict, context: str):
    if status >= 300:
        print(f"zenodo_deposit: {context} failed -- HTTP {status}", file=sys.stderr)
        print(json.dumps(resp, indent=2), file=sys.stderr)
        sys.exit(1)


def load_zenodo_json() -> dict:
    return json.loads(ZENODO_JSON_PATH.read_text())


def load_citation_version() -> str:
    text = CITATION_PATH.read_text()
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("version:"):
            return line.split(":", 1)[1].strip().strip('"')
    return "0.0.0-draft"


def git_short_sha() -> str:
    out = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], cwd=REPO_ROOT, capture_output=True, text=True
    )
    return out.stdout.strip() if out.returncode == 0 else "nogit"


def build_metadata(version: str) -> dict:
    base = load_zenodo_json()
    metadata = {
        "title": base["title"],
        "upload_type": base.get("upload_type", "publication"),
        "license": base.get("license", "CC-BY-4.0"),
        "creators": base.get("creators", []),
        "description": base.get("description", ""),
        "keywords": base.get("keywords", []),
        "version": version,
        "related_identifiers": base.get("related_identifiers", []),
    }
    if base.get("upload_type") == "publication" and base.get("publication_type"):
        metadata["publication_type"] = base["publication_type"]
    return metadata


def cmd_create_draft(args):
    token = get_token(args.sandbox)
    base = api_base(args.sandbox)
    version = load_citation_version()
    metadata = build_metadata(version)
    payload = {"metadata": metadata}
    status, resp = http_request("POST", f"{base}/deposit/depositions?prereserve_doi=true", token, data=payload)
    if status >= 300:
        payload2 = {"metadata": {**metadata, "prereserve_doi": True}}
        status, resp = http_request("POST", f"{base}/deposit/depositions", token, data=payload2)
    die_on_error(status, resp, "create-draft")

    dep_id = resp.get("id")
    prereserved = (resp.get("metadata", {}).get("prereserve_doi") or {})
    conceptrecid = resp.get("conceptrecid")
    state = {
        "deposition_id": dep_id,
        "prereserved_doi": prereserved.get("doi"),
        "conceptrecid": conceptrecid,
        "created": resp.get("created"),
        "status": "draft",
        "sandbox": bool(args.sandbox),
        "bucket_url": (resp.get("links") or {}).get("bucket"),
    }
    save_state(state)
    print(f"deposition id: {dep_id}")
    print(f"prereserved DOI: {state['prereserved_doi']}")
    print(f"conceptrecid: {conceptrecid}")
    print(f"state written: {STATE_PATH}")


def default_upload_files() -> list:
    files = []
    tmpdir = Path(tempfile.mkdtemp(prefix="ns-readout-archive-"))
    version = load_citation_version()
    sha = git_short_sha()
    archive_name = f"readout-problem-navier-stokes-{version}-{sha}.tar.gz"
    archive_path = tmpdir / archive_name
    out = subprocess.run(
        ["git", "archive", "--format=tar.gz", "-o", str(archive_path), "HEAD"],
        cwd=REPO_ROOT, capture_output=True, text=True,
    )
    if out.returncode != 0:
        print(f"zenodo_deposit: git archive failed: {out.stderr}", file=sys.stderr)
        sys.exit(1)
    files.append(archive_path)

    main_pdf = REPO_ROOT / "paper" / "main.pdf"
    if main_pdf.exists():
        files.append(main_pdf)

    return files


def cmd_upload(args):
    token = get_token(args.sandbox)
    state = load_state()
    bucket_url = state.get("bucket_url")
    if not bucket_url:
        print("zenodo_deposit: no bucket_url in registry/zenodo_state.json -- run create-draft first", file=sys.stderr)
        sys.exit(1)

    files = [Path(f) for f in args.files] if args.files else default_upload_files()
    if not files:
        print("zenodo_deposit: no files to upload", file=sys.stderr)
        sys.exit(1)

    uploaded = []
    for f in files:
        if not f.exists():
            print(f"zenodo_deposit: skip missing file {f}", file=sys.stderr)
            continue
        url = f"{bucket_url}/{f.name}"
        data = f.read_bytes()
        status, resp = http_request("PUT", url, token, data=data, raw=True,
                                     headers={"Content-Type": "application/octet-stream"})
        die_on_error(status, resp, f"upload {f.name}")
        uploaded.append(f.name)
        print(f"uploaded: {f.name} ({len(data)} bytes)")

    state["files_uploaded"] = sorted(set(state.get("files_uploaded", []) + uploaded))
    save_state(state)
    print(f"total files uploaded this run: {len(uploaded)}")


def cmd_update_metadata(args):
    token = get_token(args.sandbox)
    base = api_base(args.sandbox)
    state = load_state()
    dep_id = state.get("deposition_id")
    if not dep_id:
        print("zenodo_deposit: no deposition_id in state -- run create-draft first", file=sys.stderr)
        sys.exit(1)
    version = load_citation_version()
    metadata = build_metadata(version)
    payload = {"metadata": metadata}
    status, resp = http_request("PUT", f"{base}/deposit/depositions/{dep_id}", token, data=payload)
    die_on_error(status, resp, "update-metadata")
    print(f"metadata updated for deposition {dep_id} (version={version})")


def cmd_status(args):
    token = get_token(args.sandbox)
    base = api_base(args.sandbox)
    state = load_state()
    dep_id = state.get("deposition_id")
    if not dep_id:
        print("zenodo_deposit: no deposition_id in state -- run create-draft first", file=sys.stderr)
        sys.exit(1)
    status, resp = http_request("GET", f"{base}/deposit/depositions/{dep_id}", token)
    die_on_error(status, resp, "status")
    print(f"deposition id: {resp.get('id')}")
    print(f"state: {resp.get('state')}")
    print(f"submitted (published): {resp.get('submitted')}")
    print(f"prereserved/DOI: {resp.get('metadata', {}).get('prereserve_doi') or resp.get('doi')}")
    print(f"conceptrecid: {resp.get('conceptrecid')}")
    files = resp.get("files", [])
    print(f"files ({len(files)}): {[f.get('filename') for f in files]}")


def cmd_new_version(args):
    token = get_token(args.sandbox)
    base = api_base(args.sandbox)
    state = load_state()
    dep_id = state.get("deposition_id")
    if not dep_id:
        print("zenodo_deposit: no deposition_id in state -- run create-draft first", file=sys.stderr)
        sys.exit(1)
    status, resp = http_request("POST", f"{base}/deposit/depositions/{dep_id}/actions/newversion", token)
    die_on_error(status, resp, "new-version")
    new_url = (resp.get("links") or {}).get("latest_draft")
    print(f"new version draft link: {new_url}")
    print(f"concept DOI (stable across versions): {resp.get('conceptdoi') or state.get('prereserved_doi')}")
    print("Update registry/zenodo_state.json manually with the new draft's deposition id if you continue with it.")


def cmd_publish(args):
    state = load_state()
    dep_id = state.get("deposition_id")
    if not dep_id:
        print("zenodo_deposit: no deposition_id in state -- run create-draft first", file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        print(json.dumps({
            "dry_run": True,
            "would_publish_deposition_id": dep_id,
            "sandbox": bool(args.sandbox),
            "founder_instructed": getattr(args, "founder_instructed", None),
        }, ensure_ascii=False))
        return

    founder_approval_gate(args, "zenodo_deposit")

    if getattr(args, "founder_instructed", None):
        log_founder_instruction(dep_id, args.founder_instructed)

    token = get_token(args.sandbox)
    base = api_base(args.sandbox)
    status, resp = http_request("POST", f"{base}/deposit/depositions/{dep_id}/actions/publish", token)
    die_on_error(status, resp, "publish")
    state["status"] = "published"
    save_state(state)
    print(f"PUBLISHED deposition {dep_id}. DOI: {resp.get('doi')}")


def main():
    parser = argparse.ArgumentParser(description="Zenodo deposition helper for this repository")
    parser.add_argument("--sandbox", action="store_true", help="use sandbox.zenodo.org + ZENODO_SANDBOX_TOKEN")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("create-draft")

    p_upload = sub.add_parser("upload")
    p_upload.add_argument("files", nargs="*", help="files to upload (default: git archive + paper/main.pdf)")

    sub.add_parser("update-metadata")
    sub.add_parser("status")
    sub.add_parser("new-version")

    p_publish = sub.add_parser("publish")
    p_publish.add_argument("--i-have-founder-approval", action="store_true")
    p_publish.add_argument(
        "--founder-instructed", metavar='"<verbatim instruction + date>"',
        help="bypass the RELEASE_APPROVAL.txt file check for an explicit same-session founder "
             "chat instruction; the instruction is logged to registry/zenodo_uploads/<id>.json",
    )
    p_publish.add_argument(
        "--dry-run", action="store_true",
        help="print what would be published and exit 0 -- no network call, no publish",
    )

    args = parser.parse_args()

    dispatch = {
        "create-draft": cmd_create_draft,
        "upload": cmd_upload,
        "update-metadata": cmd_update_metadata,
        "status": cmd_status,
        "new-version": cmd_new_version,
        "publish": cmd_publish,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
