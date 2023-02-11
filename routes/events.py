from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status, Depends
from starlette.responses import JSONResponse

from auth.authenticate import authenticate
from database.connection import Database
from models.event import Event, EventUpdate

event_router = APIRouter(
    tags=["Events"]
)

event_database = Database(Event)


@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    events = await Event.find_all().to_list()
    return events


@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: PydanticObjectId) -> Event:
    event = await Event.find_one(Event.id == id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with the supplied ID does not exist"
        )
    return event


@event_router.post("/new")
async def create_event(body: Event, user: str = Depends(authenticate)) -> dict:
    body.creator = user
    await Event.save(body)
    return {
        "message": "Event created successfully"
    }


@event_router.put("/attend_event{id}")
async def attend_event(id: PydanticObjectId, user: str = Depends(authenticate)) -> dict:
    event = await Event.find_one(Event.id == id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    if user in event.attendees:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already an attendee"
        )
    event.attendees.append(user)
    await Event.save(event)

    return {
        "message":"Successfully added as an attendee"
    }


@event_router.put("/{id}")
async def update_event(id: PydanticObjectId, body: EventUpdate,
                       user: str = Depends(authenticate)) -> dict:
    event = await Event.find_one(Event.id == id)
    if event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Operation not allowed"
        )

    updated_event = await event_database.update(id, body)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return updated_event


@event_router.delete("/{id}")
async def delete_event(id: PydanticObjectId, user: str = Depends(authenticate)) -> dict:
    event = await Event.find_one(Event.id == id)
    if event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't perform this action! You can only delete event created by you"
        )

    is_event = await Event.delete(event)
    if not is_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with the supplied ID does not exist"
        )
    return {
        "message": "Event deleted successfully."
    }


# @event_router.post("/logout")
# async def logout(user: str = Depends(authenticate)):
#     # Invalidate the current authentication token
#     # For example, you could use a token blacklisting system
#     # to prevent the token from being used again
#
#     # Clear the authentication token from the client-side storage
#     response = JSONResponse(content={"message": "Successfully logged out"})
#     response.delete_cookie(key="Authorization")
#     return response
