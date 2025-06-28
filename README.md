# YouTube Trending Tracker

An automated data pipeline that tracks YouTube trending videos daily, processes the data with pandas, and stores it in PostgreSQL using Apache Airflow for orchestration.

## 🛠️ Tech Stack

- **Python** + **pandas** for data processing
- **PostgreSQL** for data storage
- **Apache Airflow** for workflow scheduling
- **Docker** for containerization
- **YouTube Data API v3** for data collection

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/yourusername/youtube-trending-tracker.git
cd youtube-trending-tracker
```

### 2. Environment Configuration
Create `.env` file:
```env
YOUTUBE_API_KEY=your_youtube_api_key
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
DB_URI=
AIRFLOW_DB_USER=
AIRFLOW_DB_PASS=
AIRFLOW_DB_NAME=
```

### 3. Initialize Airflow
```bash
# Initialize Airflow database
docker-compose run --rm airflow-webserver airflow db init

# Create Airflow admin user
docker-compose run --rm airflow-webserver airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
```

### 4. Start Services
```bash
docker-compose up -d
```

### 5. Access Airflow
- URL: http://localhost:8080
- Default credentials: `admin` / `admin`

## ⚙️ How It Works

**Daily Airflow DAG (`youtube_trending_daily`):**
1. **Fetch**: Get trending videos from YouTube API
2. **Process**: Clean and transform data with pandas
3. **Store**: Save processed data to PostgreSQL
4. **Validate**: Run data quality checks

## 📊 Data Collected

- Video metadata (title, description, duration)
- Statistics (views, likes, comments)
- Channel information
- Trending timestamps and categories

## 🔧 Setup Requirements

- Docker & Docker Compose
- YouTube Data API key ([Get one here](https://console.cloud.google.com/))