import json
import requests
import os
import logging
from time import sleep
from typing import List, Dict, Any


logging.basicConfig(
    filename='json_rpc_pusher.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class OdooAPI:
    def __init__(self, url: str, db: str, username: str, password: str):
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        self.uid = None
        self.headers = {"Content-Type": "application/json"}
        self.authenticate()

    def authenticate(self, max_retries: int = 3) -> None:
        for attempt in range(max_retries):
            try:
                payload = {
                    "jsonrpc": "2.0",
                    "method": "call",
                    "params": {
                        "service": "common",
                        "method": "authenticate",
                        "args": [self.db, self.username, self.password, {}],
                    },
                    "id": 1,
                }
                response = requests.post(
                    self.url,
                    headers=self.headers,
                    data=json.dumps(payload)
                )
                self.uid = response.json().get("result")
                if self.uid:
                    logging.info(f"Authentication successful. UID: {self.uid}")
                    return
            except Exception as e:
                logging.error(f"Authentication attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    sleep(2 ** attempt)
                continue
        raise Exception("Failed to authenticate after multiple attempts")

    def search_records(self, model: str, domain: List) -> List:
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    self.db,
                    self.uid,
                    self.password,
                    model,
                    "search_read",
                    [domain],
                    {"fields": ["source_url"]}
                ],
            },
        }
        response = requests.post(self.url, headers=self.headers, data=json.dumps(payload))
        return response.json().get("result", [])

    def create_record(self, model: str, records: List[Dict], max_retries: int = 3) -> None:
        if not self._validate_records(model, records):
            return

        existing_records = self.search_records(model, [
            ("source_url", "in", [r.get("source_url") for r in records])
        ])
        existing_urls = set(r["source_url"] for r in existing_records)

        new_records = [r for r in records if r["source_url"] not in existing_urls]

        if not new_records:
            logging.info(f"No new records to create for model {model}")
            return

        for attempt in range(max_retries):
            try:
                payload = {
                    "jsonrpc": "2.0",
                    "method": "call",
                    "params": {
                        "service": "object",
                        "method": "execute_kw",
                        "args": [
                            self.db,
                            self.uid,
                            self.password,
                            model,
                            "create",
                            [new_records],
                        ],
                    },
                }
                response = requests.post(
                    self.url,
                    headers=self.headers,
                    data=json.dumps(payload)
                )
                result = response.json()
                if "error" in result:
                    raise Exception(result["error"])
                logging.info(
                    f"Successfully created {len(new_records)} records for {model}"
                )
                return
            except Exception as e:
                logging.error(f"Create attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    sleep(2 ** attempt)
                continue
        raise Exception(f"Failed to create records for {model} after multiple attempts")

    def _validate_records(self, model: str, records: List[Dict]) -> bool:
        required_fields = {
            "scraped.page": ["title", "content", "source_url"],
            "scraped.job": ["name", "company_name", "location", "source_url"],
            "scraped.blog": ["title", "content", "source_url"]
        }

        if model not in required_fields:
            logging.error(f"Unknown model: {model}")
            return False

        for record in records:
            missing_fields = [
                field for field in required_fields[model]
                if not record.get(field)
            ]
            if missing_fields:
                logging.error(
                    f"Missing required fields {missing_fields} in record: {record}"
                )
                return False
        return True

def main():
    try:
        api = OdooAPI(
            url="http://localhost:8017/jsonrpc",
            db="odoo_db",
            username="admin",
            password="password"
        )

        base_path = os.path.dirname(os.path.abspath(__file__))

        # VentureBeat pages
        with open(os.path.join(base_path, "venturebeat_about.json"), "r", encoding="utf-8") as f:
            page_data = json.load(f)

        api.create_record(
            "scraped.page",
            [{
                "title": page_data["title"],
                "content": page_data["content"],
                "source_url": page_data["url"],
            }]
        )

        # LinkedIn jobs
        with open(os.path.join(base_path, "linkedin_jobs.json"), "r", encoding="utf-8") as f:
            jobs_data = json.load(f)

        job_records = [
            {
                "name": job["title"],
                "company_name": job["company"],
                "location": job["location"],
                "date_posted": job["posted_date"],
                "source_url": job["link"],
                "company_logo_url": job.get("company_logo", ""),
            }
            for job in jobs_data["jobs"]
        ]
        api.create_record("scraped.job", job_records)

        # TechCrunch blogs
        with open(
            os.path.join(base_path, "techcrunch_articles_20250518_113258.json"),
            "r",
            encoding="utf-8"
        ) as f:
            blogs_data = json.load(f)

        blog_records = [
            {
                "title": article["title"],
                "content": article.get("full_content", "") or "",
                "published_date": article.get("published_date", ""),
                "source_url": article["source_url"],
            }
            for article in blogs_data
        ]
        api.create_record("scraped.blog", blog_records)

    except Exception as e:
        logging.error(f"Main execution failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
