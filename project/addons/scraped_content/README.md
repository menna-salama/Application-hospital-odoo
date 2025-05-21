# Web Content Scraper for Odoo (scraped_content)

A comprehensive Odoo module for scraping and managing web content with enhanced data validation and idempotency support.

## 📋 Setup Instructions

### Prerequisites
- Python 3.8+
- Odoo 17.0
- Docker and Docker Compose

### Required Python Packages
```bash
pip install requests beautifulsoup4 selenium xlsxwriter typing
```

### Environment Setup
1. Clone the repository:
```bash
git clone <repository-url>
cd odoo_projects
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

## 🤖 Running the Scrapers

### 1. Configure Scraping Settings
Edit `external_scripts/config.py`:
```python
SCRAPING_CONFIG = {
    "linkedin": {
        "search_terms": ["python developer", "odoo developer"],
        "location": "United States"
    },
    "techcrunch": {
        "categories": ["startups", "technology"],
        "max_articles": 50
    },
    "venturebeat": {
        "sections": ["ai", "cloud"]
    }
}
```

### 2. Run Individual Scrapers
```bash
cd external_scripts

# VentureBeat Pages
python static_page_scraping.py

# LinkedIn Jobs
python linkedin_scraping.py

# TechCrunch Articles
python blog_scraping.py
```

## 📤 Running the Data Pusher

### 1. Configure API Settings
Edit `external_scripts/json_rpc_pusher.py`:
```python
api = OdooAPI(
    url="http://localhost:8017/jsonrpc",
    db="odoo_db",
    username="admin",
    password="password"
)
```

### 2. Execute Pusher Script
```bash
python json_rpc_pusher.py
```

### 3. Monitor Logs
```bash
tail -f json_rpc_pusher.log
```

## 🔧 Installing Odoo Module

1. Copy module to Odoo addons:
```bash
cp -r addons/scraped_content /path/to/odoo/addons/
```

2. Set proper permissions:
```bash
sudo chown -R odoo:odoo /path/to/odoo/addons/scraped_content
```

3. Update module list in Odoo:
```bash
docker exec -it odoo_projects-odoo-1 odoo -u scraped_content -d odoo_db
```

4. Install via Odoo interface:
- Go to Apps
- Remove "Apps" filter
- Search for "Scraped Content"
- Click Install

## 🌐 Viewing Data on Odoo Website

### 1. Access Scraped Content
- Navigate to: `http://localhost:8017/web`
- Login with admin credentials
- Go to Scraped Content menu

### 2. View Different Content Types
- **Jobs**: `http://localhost:8017/jobs`
  - Browse LinkedIn job listings
  - Filter by company, location
  - Track application status

- **Blogs**: `http://localhost:8017/blogs`
  - Read TechCrunch articles
  - Filter by publication date
  - Mark as read/unread

- **Pages**: `http://localhost:8017/pages`
  - View VentureBeat content
  - Track visit status
  - Search by title/content

### 3. Content Management
- Use status filters to track content
- Enable/disable website publication
- Manage content visibility

## 🔍 Key Features

### Enhanced Data Validation
- Automatic field validation
- Required field checking
- Data type verification

### Idempotency Support
- Duplicate prevention
- Source URL tracking
- Update existing records

### Error Handling
- Comprehensive logging
- Retry mechanism
- Detailed error messages

### Security
- Role-based access control
- API authentication
- Data validation

## 📝 License

LGPL-3
