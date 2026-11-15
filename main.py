# Backend Development I · Аяллын API (санах ойн өгөгдөлтэй)
# Ажиллуулах:  uvicorn main:app --reload
# Баримт бичиг: http://localhost:8000/docs

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Travel API")

# Түр өгөгдөл. Backend II-д PostgreSQL-ээр солино.
tours = [
    {"tour_id": 1, "name": "Хөвсгөлийн аялал", "destination": "Хөвсгөл",    "days": 5,  "price": 1250000},
    {"tour_id": 2, "name": "Говийн аялал",     "destination": "Өмнөговь",   "days": 7,  "price": 1800000},
    {"tour_id": 3, "name": "Тэрэлжийн амралт", "destination": "Төв",        "days": 2,  "price": 450000},
    {"tour_id": 4, "name": "Алтайн экспедиц",  "destination": "Баян-Өлгий", "days": 10, "price": 2900000},
    {"tour_id": 5, "name": "Хархорины түүх",   "destination": "Өвөрхангай", "days": 3,  "price": 650000},
    {"tour_id": 6, "name": "Мөсөн баяр",       "destination": "Хөвсгөл",    "days": 4,  "price": 1100000},
]
bookings = []


@app.get("/")
def health():
    return {"status": "ok"}


# GET /tours  ·  GET /tours?destination=Хөвсгөл&max_price=1200000
@app.get("/tours")
def list_tours(destination: str | None = None, max_price: int | None = None):
    result = tours
    if destination:
        result = [t for t in result if t["destination"] == destination]
    if max_price:
        result = [t for t in result if t["price"] <= max_price]
    return result


# GET /tours/4
@app.get("/tours/{tour_id}")
def get_tour(tour_id: int):
    for t in tours:
        if t["tour_id"] == tour_id:
            return t
    raise HTTPException(status_code=404, detail="Аялал олдсонгүй")


class BookingCreate(BaseModel):
    tour_id: int
    customer_name: str = Field(min_length=2)
    people: int = Field(gt=0, le=20)


# POST /bookings  (body: {"tour_id": 1, "customer_name": "Бат", "people": 2})
@app.post("/bookings", status_code=201)
def create_booking(data: BookingCreate):
    tour = get_tour(data.tour_id)            # байхгүй бол 404
    booking = {
        "booking_id": len(bookings) + 1,
        "tour_id": tour["tour_id"],
        "customer_name": data.customer_name,
        "people": data.people,
        "total": tour["price"] * data.people,
        "status": "pending",
    }
    bookings.append(booking)
    return booking


@app.get("/bookings")
def list_bookings():
    return bookings