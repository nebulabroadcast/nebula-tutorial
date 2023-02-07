"""
Validator plugin is executed every time an asset is created or updated
via the API. You can put any site-specific logic here.
"""

import nebula

from nebula.enum import ContentType, MediaType, ObjectStatus
from nebula.exceptions import ValidationException

from typing import Any
from enum import IntEnum


class Folder(IntEnum):
    MOVIE = 1
    EPISODE = 2
    STORY = 3
    SONG = 4
    FILL = 5
    TRAILER = 6
    JINGLE = 7
    GRAPHIC = 8
    COMMERCIAL = 9
    TELESHOPPING = 10
    DATASET = 11
    INCOMING = 12
    SERIE = 13


async def validate(
    asset: nebula.Asset, # Original or empty asset to be created/updated
    meta: dict[str, Any], # Metadata from the request
    connection: nebula.DB, # Database connection
    user: nebula.User, # User who made the request
) -> None:
    """Validate the asset.

    The validator runs in a transaction, so at any point you can raise
    an exception to abort the transaction.
    """

    asset.update(meta)

    # Do a simple check to see if all required fields are present.

    if not asset["title"]:
        raise ValidationException("Title is required")

    # We need an asset id to continue, so if it's a new asset,
    # we need to save it first. This will generate an id.
    # Remember that we're in a transaction, so if we raise an exception
    # later, the asset will be rolled back.

    if not asset.id:
        await asset.save()

    # Fill additional fields based on the folder.

    if asset["id_folder"] == Folder.DATASET:
        asset["media_type"] = MediaType.VIRTUAL
        asset["content_type"] = ContentType.TEXT
        asset["status"] = ObjectStatus.ONLINE

    elif asset["id_folder"] == Folder.SERIE:
        asset["media_type"] = MediaType.VIRTUAL
        asset["content_type"] = ContentType.PACKAGE
        asset["status"] = ObjectStatus.ONLINE

        await connection.execute(
            """
            INSERT INTO cs (cs, value, settings)
            VALUES ($1, $2, $3)
            ON CONFLICT (cs, value) DO UPDATE SET settings = $3
            """,
            "urn:site:series",
            str(asset.id),
            {
                "aliases": {"en": asset["title"]},
            },
        )

    else:
        # Primary identifier is the asset id in this case
        asset["id/main"] = f"{asset.id:06x}"
        asset["media_type"] = MediaType.FILE
        asset["content_type"] = ContentType.VIDEO

        # New asset doesn't have a file yet, so we fill the
        # path, where the file will be expected.
        # But since the asset may be created using watch folder,
        # we cannot update the path if it's already set.
        if not asset["path"]:
            subdir = Folder(asset["id_folder"]).name.lower() + "s"
            asset["id_storage"] = 1
            asset["path"] = f"media.dir/{subdir}/{asset['id/main']}.mxf"
            asset["status"] = ObjectStatus.OFFLINE

    # We're done, all changes made to the asset will be saved
    # outside of this function, so we don't need to call save()
    # or return anything.
