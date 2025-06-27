from pathlib import Path
from typing import Dict, Set

from mcp.server import Server
from mcp.server.session import ServerSession
from mcp.types import (
    ResourceListChangedNotification,
    ServerNotification
)

# Global state: mapping watched paths -> subcribed ServerSession objects
watched: Dict[Path, Set[ServerSession]]


async def send_resources_list_changed_notification():
    # Get all sessions that might be interested in resource list changes
    all_sessions = set()
    for sessions in watched.values():
        all_sessions.update(sessions)

    if not all_sessions:
        return
    
    # Create notification
    notification = ResourceListChangedNotification(
        method="notifications/resources/list_changed"
    )

    # Send to all sessions
    for session in all_sessions:
        try:
            await session.send_notification(ServerNotification(root=ResourceListChangedNotification))
        except Exception:
            pass


server = Server(
    name="Filesystem Monitor MCP",
    instructions="Subcribe/Unsubcribe to filesystem event"
)
