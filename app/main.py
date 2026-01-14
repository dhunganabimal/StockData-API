from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler

from app.database import engine, Base, get_db
from app.models import StockData
from app.scraper import scrape_and_save_task
Base.metadata.create_all(bind=engine)

# Initialize scheduler (global, single instance)
scheduler = BackgroundScheduler(daemon=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not scheduler.running:
        print(" Starting Scheduler...")

        scheduler.add_job(
            scrape_and_save_task,
            trigger="interval",
            hours=24,
            id="daily_scrape",
            replace_existing=True
        )

        # Optional: run once on startup
        scheduler.add_job(
            scrape_and_save_task,
            trigger="date",
            id="startup_scrape",
            replace_existing=True
        )

        scheduler.start()

    yield

    print(" Stopping Scheduler...")
    scheduler.shutdown(wait=False)
app = FastAPI(lifespan=lifespan)
@app.get("/")
def home():
    return {"message": "Scraper API is running"}


@app.get("/data")
def get_scraped_data(db: Session = Depends(get_db)):
    return db.query(StockData).order_by(StockData.created_at.desc()).all()


@app.post("/trigger-scrape")
def trigger_scrape_manually():
    scrape_and_save_task()
    return {"message": "Scraper executed successfully"}
