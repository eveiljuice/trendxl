#!/usr/bin/env python3
"""
Migration script to update TrendXL database from old schema to new SeaTable-compatible schema
"""

import sqlite3
import os
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SQLiteMigrator:
    """Handles database migration to new schema"""

    def __init__(self, db_path='trendxl_local.db'):
        self.db_path = Path(db_path)
        self.new_db_path = Path('trendxl.db')

    def migrate_database(self):
        """Main migration method"""
        if not self.db_path.exists():
            logger.error(f"Source database {self.db_path} not found")
            return False

        logger.info("Starting database migration...")

        try:
            # Connect to existing database
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Check current schema
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            logger.info(f"Found tables: {tables}")

            # Create new database with new schema
            self._create_new_schema()

            # Migrate data
            self._migrate_users(cursor)
            self._migrate_trends(cursor)

            conn.close()

            # Backup old database
            backup_path = self.db_path.with_suffix('.backup')
            self.db_path.rename(backup_path)
            logger.info(f"Old database backed up as: {backup_path}")

            # Rename new database
            self.new_db_path.rename(self.db_path)
            logger.info(f"New database created: {self.db_path}")

            return True

        except Exception as e:
            logger.error(f"Migration failed: {e}")
            return False

    def _create_new_schema(self):
        """Create new database with updated schema"""
        try:
            conn = sqlite3.connect(self.new_db_path)
            cursor = conn.cursor()

            # Read and execute the new schema
            schema_path = Path(__file__).parent / "trendxl.sql"
            if schema_path.exists():
                with open(schema_path, 'r', encoding='utf-8') as f:
                    sql_content = f.read()

                cursor.executescript(sql_content)
                conn.commit()
                logger.info("New schema created successfully")
            else:
                logger.error(f"Schema file not found: {schema_path}")

            conn.close()

        except Exception as e:
            logger.error(f"Failed to create new schema: {e}")
            raise

    def _migrate_users(self, cursor):
        """Migrate users from old to new schema"""
        try:
            # Check if old Users table exists and has data
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='Users'")
            if not cursor.fetchone():
                logger.info(
                    "No old Users table found, skipping user migration")
                return

            cursor.execute("SELECT COUNT(*) FROM Users")
            user_count = cursor.fetchone()[0]
            logger.info(f"Migrating {user_count} users...")

            # Get users from old table
            cursor.execute("SELECT * FROM Users")
            old_users = cursor.fetchall()

            # Connect to new database
            new_conn = sqlite3.connect(self.new_db_path)
            new_cursor = new_conn.cursor()

            for user in old_users:
                # Convert old format to new SeaTable-compatible format
                user_dict = dict(user)

                new_user = {
                    "Username": user_dict.get("link", "").replace("https://tiktok.com/@", ""),
                    "Display_Name": user_dict.get("parsed_niche", ""),
                    "Follower_Count": user_dict.get("followers", 0),
                    "Following_Count": 0,
                    "Video_Count": 0,
                    "Likes_Count": 0,
                    "Bio": "",
                    "Avatar_URL": "",
                    "Verified": False,
                    "Sec_UID": "",
                    "UID": "",
                    "Region": user_dict.get("location", ""),
                    "Language": "",
                    "Niche": user_dict.get("parsed_niche", ""),
                    "Interests": user_dict.get("top_posts", "[]"),
                    "Keywords": "[]",
                    "Hashtags": user_dict.get("top_posts", "[]"),
                    "Target_Audience": "",
                    "Content_Style": "",
                    "Region_Focus": "",
                    "Created_At": user_dict.get("created_at", datetime.now().isoformat()),
                    "Last_Updated": user_dict.get("updated_at", datetime.now().isoformat())
                }

                # Insert into new table
                columns = ', '.join(new_user.keys())
                placeholders = ', '.join(['?' for _ in new_user])
                values = list(new_user.values())

                sql = f"INSERT OR REPLACE INTO Users ({columns}) VALUES ({placeholders})"
                new_cursor.execute(sql, values)

            new_conn.commit()
            new_conn.close()
            logger.info("Users migration completed")

        except Exception as e:
            logger.error(f"User migration failed: {e}")

    def _migrate_trends(self, cursor):
        """Migrate trends from old to new schema"""
        try:
            # Check if old TrendFeed table exists and has data
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='TrendFeed'")
            if not cursor.fetchone():
                logger.info(
                    "No old TrendFeed table found, skipping trend migration")
                return

            cursor.execute("SELECT COUNT(*) FROM TrendFeed")
            trend_count = cursor.fetchone()[0]
            logger.info(f"Migrating {trend_count} trends...")

            # Get trends from old table
            cursor.execute("SELECT * FROM TrendFeed")
            old_trends = cursor.fetchall()

            # Connect to new database
            new_conn = sqlite3.connect(self.new_db_path)
            new_cursor = new_conn.cursor()

            for trend in old_trends:
                # Convert old format to new SeaTable-compatible format
                trend_dict = dict(trend)

                # Parse stat_metrics JSON
                import json
                stat_metrics = json.loads(trend_dict.get("stat_metrics", "{}"))

                new_trend = {
                    "Username": "",  # Will be set based on user_id lookup
                    "Aweme_ID": f"old_{trend_dict['id']}",  # Generate fake ID
                    "Description": trend_dict.get("trend_title", ""),
                    "Author_Username": "",
                    "Author_Nickname": "",
                    "Author_Followers": 0,
                    "Views": stat_metrics.get("views", 0),
                    "Likes": stat_metrics.get("likes", 0),
                    "Comments": stat_metrics.get("comments", 0),
                    "Shares": 0,
                    "Downloads": 0,
                    "Favourited": 0,
                    "Whatsapp_Shares": 0,
                    "Engagement_Rate": stat_metrics.get("ER", 0.0),
                    "Duration": 0,
                    "Video_Cover": "",
                    "Video_URL": trend_dict.get("video_url", ""),
                    "Music_Title": "",
                    "Music_Author": "",
                    "Music_ID": "",
                    "Hashtags": "[]",
                    "Region": "",
                    "Video_Type": "",
                    "Sound_Type": "",
                    "Relevance_Score": trend_dict.get("relevance_score", 0.0),
                    "Relevance_Reason": "",
                    "Trend_Category": "",
                    "Audience_Match": False,
                    "Trend_Potential": "",
                    "Keyword": "",
                    "Hashtag": "",
                    "TikTok_URL": trend_dict.get("video_url", ""),
                    "Sentiment": "Neutral",
                    "Audience": "General",
                    "Created_At": trend_dict.get("created_at", datetime.now().isoformat()),
                    "Saved_At": trend_dict.get("created_at", datetime.now().isoformat())
                }

                # Insert into new table
                columns = ', '.join(new_trend.keys())
                placeholders = ', '.join(['?' for _ in new_trend])
                values = list(new_trend.values())

                sql = f"INSERT OR REPLACE INTO Trends ({columns}) VALUES ({placeholders})"
                new_cursor.execute(sql, values)

            new_conn.commit()
            new_conn.close()
            logger.info("Trends migration completed")

        except Exception as e:
            logger.error(f"Trend migration failed: {e}")


def main():
    """Main migration function"""
    print("🔄 TrendXL Database Migration Tool")
    print("=" * 50)

    # Use default path or get from environment
    db_path = os.getenv('SQLITE_DB_PATH', 'trendxl_local.db')

    migrator = SQLiteMigrator(db_path)

    if migrator.migrate_database():
        print("✅ Migration completed successfully!")
        print(
            f"📁 Old database backed up as: {migrator.db_path.with_suffix('.backup')}")
        print(f"🗄️  New database created: {migrator.db_path}")
        print("\n📝 Next steps:")
        print("1. Test your application with USE_SQLITE=true")
        print("2. Verify data integrity")
        print("3. Remove backup file if everything works correctly")
    else:
        print("❌ Migration failed!")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
