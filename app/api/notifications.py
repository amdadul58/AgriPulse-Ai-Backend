from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.notification import Notification


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


# =========================================================
# GET ALL NOTIFICATIONS
# =========================================================
@router.get("")
async def get_notifications(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Notification)
        .where(Notification.user_id == current_user.id)
        .order_by(Notification.created_at.desc())
    )

    notifications = result.scalars().all()

    return {
        "success": True,
        "total": len(notifications),
        "unread": sum(
            1
            for notification in notifications
            if not notification.is_read
        ),
        "notifications": [
            {
                "id": notification.id,
                "title": notification.title,
                "message": notification.message,
                "type": notification.type,
                "is_read": notification.is_read,
                "created_at": notification.created_at,
            }
            for notification in notifications
        ]
    }


# =========================================================
# CREATE NOTIFICATION
# =========================================================
@router.post("")
async def create_notification(
    title: str,
    message: str,
    type: str = "info",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    notification = Notification(
        user_id=current_user.id,
        title=title,
        message=message,
        type=type,
        is_read=False
    )

    db.add(notification)

    await db.commit()
    await db.refresh(notification)

    return {
        "success": True,
        "message": "Notification created successfully",
        "notification": {
            "id": notification.id,
            "title": notification.title,
            "message": notification.message,
            "type": notification.type,
            "is_read": notification.is_read,
            "created_at": notification.created_at,
        }
    }


# =========================================================
# GET UNREAD COUNT
# =========================================================
@router.get("/unread-count")
async def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(func.count(Notification.id))
        .where(
            Notification.user_id == current_user.id,
            Notification.is_read.is_(False)
        )
    )

    unread_count = result.scalar() or 0

    return {
        "success": True,
        "unread": unread_count
    }


# =========================================================
# MARK ONE NOTIFICATION AS READ
# =========================================================
@router.patch("/{notification_id}/read")
async def mark_notification_as_read(
    notification_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Notification).where(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        )
    )

    notification = result.scalar_one_or_none()

    if notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    notification.is_read = True

    await db.commit()

    return {
        "success": True,
        "message": "Notification marked as read"
    }


# =========================================================
# MARK ALL NOTIFICATIONS AS READ
# =========================================================
@router.patch("/read-all")
async def mark_all_notifications_as_read(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Notification).where(
            Notification.user_id == current_user.id,
            Notification.is_read.is_(False)
        )
    )

    notifications = result.scalars().all()

    for notification in notifications:
        notification.is_read = True

    await db.commit()

    return {
        "success": True,
        "message": f"{len(notifications)} notification(s) marked as read"
    }


# =========================================================
# DELETE NOTIFICATION
# =========================================================
@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Notification).where(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        )
    )

    notification = result.scalar_one_or_none()

    if notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    await db.delete(notification)
    await db.commit()

    return {
        "success": True,
        "message": "Notification deleted successfully"
    }

