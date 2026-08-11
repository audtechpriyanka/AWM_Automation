"""Persistent resume state for the confirmed engagement workflow."""
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from utilities.logger import get_logger

logger = get_logger("checkpoint")

STAGE_ORDER = [
    "engagement_created", "planning_complete", "fieldwork_complete",
    "completion_complete", "prepared_by_complete", "first_review_complete",
    "manager_signoff_complete", "partner_review_complete", "partner_signoff_complete",
]

_REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "reports")
CHECKPOINT_PATH = os.path.join(_REPORTS_DIR, "checkpoint.json")


def save_checkpoint(stage: str, engagement_id: str, extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Record a verified completed stage; reject stages outside the confirmed order."""
    if stage not in STAGE_ORDER:
        raise ValueError(f"Unknown workflow stage: {stage}")
    if not engagement_id:
        raise ValueError("engagement_id is required to save a checkpoint")
    checkpoint = {"stage": stage, "engagement_id": str(engagement_id),
                  "timestamp": datetime.now(timezone.utc).isoformat(), "extra": extra or {}}
    os.makedirs(_REPORTS_DIR, exist_ok=True)
    with open(CHECKPOINT_PATH, "w", encoding="utf-8") as checkpoint_file:
        json.dump(checkpoint, checkpoint_file, indent=2, sort_keys=True)
    logger.info("Saved verified workflow checkpoint | stage=%s | engagement_id=%s", stage, engagement_id)
    return checkpoint


def load_checkpoint() -> Optional[Dict[str, Any]]:
    """Return the latest checkpoint, or None when no workflow has been started."""
    if not os.path.exists(CHECKPOINT_PATH):
        logger.info("No workflow checkpoint found")
        return None
    try:
        with open(CHECKPOINT_PATH, encoding="utf-8") as checkpoint_file:
            checkpoint = json.load(checkpoint_file)
        if checkpoint.get("stage") not in STAGE_ORDER or not checkpoint.get("engagement_id"):
            raise ValueError("checkpoint must contain a known stage and engagement_id")
        logger.info("Loaded workflow checkpoint | stage=%s | engagement_id=%s", checkpoint["stage"], checkpoint["engagement_id"])
        return checkpoint
    except (OSError, json.JSONDecodeError, ValueError) as error:
        logger.error("Unable to load workflow checkpoint: %s", error)
        raise RuntimeError(f"Invalid workflow checkpoint at {CHECKPOINT_PATH}: {error}") from error


def next_stage(current_stage: str) -> Optional[str]:
    """Return the following confirmed stage, or None after final partner sign-off."""
    try:
        index = STAGE_ORDER.index(current_stage)
    except ValueError as error:
        raise ValueError(f"Unknown workflow stage: {current_stage}") from error
    return STAGE_ORDER[index + 1] if index + 1 < len(STAGE_ORDER) else None


def clear_checkpoint() -> None:
    """Remove resume state after a completed workflow or explicit reset."""
    if os.path.exists(CHECKPOINT_PATH):
        os.remove(CHECKPOINT_PATH)
        logger.info("Cleared workflow checkpoint")
    else:
        logger.info("No workflow checkpoint to clear")
