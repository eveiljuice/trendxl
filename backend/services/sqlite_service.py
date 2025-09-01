"""
SQLite Service for TrendXL
Full-featured SQLite database service that mimics SeaTable API interface
"""

import sqlite3
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class SQLiteService:
    """
    SQLite implementation that fully mimics SeaTable service interface
    Compatible with existing SeaTable API calls for seamless migration
    """

    def __init__(self, db_path=None):
        """Initialize SQLite service"""
        # Get database path from environment or use default
        if db_path is None:
            db_path = os.getenv('SQLITE_DB_PATH', 'trendxl.db')

        self.db_path = Path(db_path)
        self.connection = None
        self.cursor = None

        # Mimic SeaTable configuration for compatibility
        self.base_url = "sqlite://local"  # Placeholder
        self.api_token = "local_token"    # Placeholder
        self.base_uuid = "local_uuid"     # Placeholder

        self.headers = {}  # Not needed for SQLite

        # Ensure database exists and is up to date
        if not self.db_path.exists():
            logger.info(
                f"SQLite database not found at {self.db_path}. Creating new database...")
            self._create_database()
        else:
            logger.info(f"Using existing SQLite database: {self.db_path}")
            self._ensure_schema_updated()

    def _create_database(self):
        """Create database with full schema"""
        try:
            # Connect to create the database
            self.connection = sqlite3.connect(self.db_path)
            self.connection.execute("PRAGMA foreign_keys = ON")
            self.cursor = self.connection.cursor()

            # Read and execute the SQL schema
            schema_path = Path(__file__).parent.parent.parent / "trendxl.sql"
            if schema_path.exists():
                with open(schema_path, 'r', encoding='utf-8') as f:
                    sql_content = f.read()

                # Execute the schema
                self.cursor.executescript(sql_content)
                self.connection.commit()
                logger.info("Database schema created successfully")
            else:
                logger.error(f"Schema file not found: {schema_path}")
                self._create_schema_manually()

            self.disconnect()

        except Exception as e:
            logger.error(f"Error creating database: {e}")
            raise

    def _create_schema_manually(self):
        """Create schema manually if SQL file not found"""
        # Users table (SeaTable-compatible)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL UNIQUE,
                Display_Name TEXT,
                Follower_Count INTEGER DEFAULT 0,
                Following_Count INTEGER DEFAULT 0,
                Video_Count INTEGER DEFAULT 0,
                Likes_Count INTEGER DEFAULT 0,
                Bio TEXT,
                Avatar_URL TEXT,
                Verified BOOLEAN DEFAULT 0,
                Sec_UID TEXT,
                UID TEXT,
                Region TEXT,
                Language TEXT,
                Niche TEXT,
                Interests TEXT,
                Keywords TEXT,
                Hashtags TEXT,
                Target_Audience TEXT,
                Content_Style TEXT,
                Region_Focus TEXT,
                Created_At TEXT DEFAULT CURRENT_TIMESTAMP,
                Last_Updated TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Trends table (SeaTable-compatible)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Trends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL,
                Aweme_ID TEXT NOT NULL UNIQUE,
                Description TEXT,
                Author_Username TEXT,
                Author_Nickname TEXT,
                Author_Followers INTEGER DEFAULT 0,
                Views INTEGER DEFAULT 0,
                Likes INTEGER DEFAULT 0,
                Comments INTEGER DEFAULT 0,
                Shares INTEGER DEFAULT 0,
                Downloads INTEGER DEFAULT 0,
                Favourited INTEGER DEFAULT 0,
                Whatsapp_Shares INTEGER DEFAULT 0,
                Engagement_Rate REAL DEFAULT 0.0,
                Duration INTEGER DEFAULT 0,
                Video_Cover TEXT,
                Video_URL TEXT,
                Music_Title TEXT,
                Music_Author TEXT,
                Music_ID TEXT,
                Hashtags TEXT,
                Region TEXT,
                Video_Type TEXT,
                Sound_Type TEXT,
                Relevance_Score REAL DEFAULT 0.0,
                Relevance_Reason TEXT,
                Trend_Category TEXT,
                Audience_Match BOOLEAN DEFAULT 0,
                Trend_Potential TEXT,
                Keyword TEXT,
                Hashtag TEXT,
                TikTok_URL TEXT,
                Sentiment TEXT,
                Audience TEXT,
                Created_At TEXT DEFAULT CURRENT_TIMESTAMP,
                Saved_At TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (Username) REFERENCES Users(Username) ON DELETE CASCADE
            )
        """)

        # InteractionLog table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS InteractionLog (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                trend_id INTEGER NOT NULL,
                action_type TEXT NOT NULL CHECK(action_type IN ('watched', 'clicked', 'ignored', 'shared', 'saved')),
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
                FOREIGN KEY (trend_id) REFERENCES Trends(id) ON DELETE CASCADE,
                UNIQUE(user_id, trend_id, action_type)
            )
        """)

        # NicheAdapters table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS NicheAdapters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT NOT NULL UNIQUE,
                parsed_by_gpt_summary TEXT,
                topic_tags TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.connection.commit()
        logger.info("Database schema created manually")

    def _ensure_schema_updated(self):
        """Ensure database schema is up to date"""
        try:
            if not self.connect():
                return

            # Check if tables exist and create missing ones
            self.cursor.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name IN ('Users', 'Trends', 'InteractionLog', 'NicheAdapters')
            """)

            existing_tables = [row[0] for row in self.cursor.fetchall()]
            required_tables = ['Users', 'Trends',
                               'InteractionLog', 'NicheAdapters']

            missing_tables = [
                table for table in required_tables if table not in existing_tables]

            if missing_tables:
                logger.info(f"Creating missing tables: {missing_tables}")
                self._create_schema_manually()

            self.disconnect()

        except Exception as e:
            logger.error(f"Error ensuring schema update: {e}")

    def connect(self):
        """Connect to SQLite database"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.execute("PRAGMA foreign_keys = ON")
            self.connection.row_factory = sqlite3.Row  # Enable column access by name
            self.cursor = self.connection.cursor()
            return True
        except sqlite3.Error as e:
            logger.error(f"SQLite connection error: {e}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()

    def is_healthy(self) -> bool:
        """Check if the service is healthy (mimics SeaTable health check)"""
        try:
            if not self.connect():
                return False

            # Test basic connectivity and tables
            self.cursor.execute("SELECT COUNT(*) FROM Users")
            user_count = self.cursor.fetchone()[0]

            self.cursor.execute("SELECT COUNT(*) FROM Trends")
            trend_count = self.cursor.fetchone()[0]

            self.disconnect()
            logger.info(
                f"SQLite health check passed - {user_count} users, {trend_count} trends")
            return True

        except Exception as e:
            logger.error(f"SQLite health check failed: {e}")
            return False

    def _validate_configuration(self) -> bool:
        """Validate configuration (always true for SQLite)"""
        return True

    def _construct_api_url(self, endpoint: str) -> str:
        """Mock API URL construction for compatibility"""
        return f"sqlite://local/{endpoint}"

    async def ensure_tables_exist(self) -> bool:
        """Ensure required tables exist (mimics SeaTable table check)"""
        try:
            if not self.connect():
                return False

            # Check if required tables exist
            self.cursor.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name IN ('Users', 'Trends', 'InteractionLog', 'NicheAdapters')
            """)

            existing_tables = [row[0] for row in self.cursor.fetchall()]
            required_tables = ['Users', 'Trends']

            missing_tables = [
                table for table in required_tables if table not in existing_tables]

            if missing_tables:
                logger.warning(f"Missing tables: {missing_tables}")
                logger.info("Creating missing tables...")
                self._create_schema_manually()
                return True
            else:
                logger.info("All required tables exist")
                self.disconnect()
                return True

        except Exception as e:
            logger.error(f"Error checking tables: {e}")
            return False

    async def create_user_profile(self, profile_data: Dict[str, Any], analysis_data: Dict[str, Any]) -> str:
        """Create or update user profile in SQLite (SeaTable-compatible)"""
        if not self.connect():
            raise ValueError("Cannot connect to database")

        try:
            # Prepare user data in SeaTable format
            user_record = {
                "Username": profile_data.get("username", ""),
                "Display_Name": profile_data.get("display_name", ""),
                "Follower_Count": profile_data.get("follower_count", 0),
                "Following_Count": profile_data.get("following_count", 0),
                "Video_Count": profile_data.get("video_count", 0),
                "Likes_Count": profile_data.get("likes_count", 0),
                "Bio": profile_data.get("bio", ""),
                "Avatar_URL": profile_data.get("avatar_url", ""),
                "Verified": profile_data.get("verified", False),
                "Sec_UID": profile_data.get("sec_uid", ""),
                "UID": profile_data.get("uid", ""),
                "Region": profile_data.get("region", ""),
                "Language": profile_data.get("language", ""),
                "Niche": analysis_data.get("niche", ""),
                "Interests": json.dumps(analysis_data.get("interests", [])),
                "Keywords": json.dumps(analysis_data.get("keywords", [])),
                "Hashtags": json.dumps(analysis_data.get("hashtags", [])),
                "Target_Audience": analysis_data.get("target_audience", ""),
                "Content_Style": analysis_data.get("content_style", ""),
                "Region_Focus": analysis_data.get("region_focus", ""),
                "Created_At": datetime.now().isoformat(),
                "Last_Updated": datetime.now().isoformat()
            }

            # Check if user already exists (direct query to avoid recursion)
            self.cursor.execute(
                "SELECT id FROM Users WHERE Username = ?", (profile_data.get("username", ""),))
            existing = self.cursor.fetchone()

            if existing:
                # Update existing user
                user_id = existing[0]
                await self._update_table_row("Users", user_id, user_record)
                return str(user_id)
            else:
                # Create new user
                return await self._create_table_row("Users", user_record)

        except Exception as e:
            logger.error(f"Error creating/updating user profile: {e}")
            raise ValueError(f"Failed to save user profile: {str(e)}")
        finally:
            self.disconnect()

    async def get_user_profile(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user profile from SQLite (SeaTable-compatible)"""
        if not self.connect():
            return None

        try:
            # Query users table directly
            self.cursor.execute(
                "SELECT * FROM Users WHERE Username = ?", (username,))
            row = self.cursor.fetchone()

            if row:
                # Convert row to dict
                columns = [desc[0] for desc in self.cursor.description]
                user_data = {}
                for i, col in enumerate(columns):
                    user_data[col] = row[i]

                # Parse JSON fields
                user_data["Interests"] = json.loads(
                    user_data.get("Interests", "[]"))
                user_data["Keywords"] = json.loads(
                    user_data.get("Keywords", "[]"))
                user_data["Hashtags"] = json.loads(
                    user_data.get("Hashtags", "[]"))
                # Add _id for SeaTable compatibility
                user_data["_id"] = user_data["id"]
                return user_data

            return None

        except Exception as e:
            logger.error(f"Error getting user profile for {username}: {e}")
            return None
        finally:
            self.disconnect()

    def get_user_profile_sync(self, username: str) -> Optional[Dict[str, Any]]:
        """Synchronous version of get_user_profile for internal use."""
        if not self.connect():
            return None

        try:
            self.cursor.execute(
                "SELECT * FROM Users WHERE Username = ?", (username,)
            )
            row = self.cursor.fetchone()

            if row:
                columns = [desc[0] for desc in self.cursor.description]
                user_data = dict(zip(columns, row))

                # Parse JSON fields
                user_data["Interests"] = json.loads(
                    user_data.get("Interests", "[]"))
                user_data["Keywords"] = json.loads(
                    user_data.get("Keywords", "[]"))
                user_data["Hashtags"] = json.loads(
                    user_data.get("Hashtags", "[]"))
                user_data["_id"] = user_data["id"]
                return user_data

            return None
        except Exception as e:
            logger.error(
                f"Error getting user profile sync for {username}: {e}")
            return None
        finally:
            self.disconnect()

    async def save_trends(self, trends: List[Dict[str, Any]], username: str) -> bool:
        """Save filtered trends to SQLite (SeaTable-compatible)"""
        if not self.connect():
            return False

        try:
            saved_count = 0

            for trend in trends:
                trend_record = {
                    "Username": username,
                    "Aweme_ID": trend.get("aweme_id", ""),
                    # Limit description length
                    "Description": trend.get("desc", "")[:1000],
                    "Author_Username": trend.get("author", {}).get("unique_id", ""),
                    "Author_Nickname": trend.get("author", {}).get("nickname", ""),
                    "Author_Followers": trend.get("author", {}).get("follower_count", 0),
                    "Views": trend.get("statistics", {}).get("play_count", 0),
                    "Likes": trend.get("statistics", {}).get("digg_count", 0),
                    "Comments": trend.get("statistics", {}).get("comment_count", 0),
                    "Shares": trend.get("statistics", {}).get("share_count", 0),
                    "Downloads": trend.get("statistics", {}).get("download_count", 0),
                    "Favourited": trend.get("statistics", {}).get("collect_count", 0),
                    "Whatsapp_Shares": trend.get("statistics", {}).get("whatsapp_share_count", 0),
                    "Engagement_Rate": trend.get("engagement_rate", 0.0),
                    "Duration": trend.get("video", {}).get("duration", 0),
                    "Video_Cover": trend.get("video", {}).get("cover", ""),
                    "Video_URL": trend.get("video", {}).get("download_addr", ""),
                    "Music_Title": trend.get("music", {}).get("title", ""),
                    "Music_Author": trend.get("music", {}).get("author", ""),
                    "Music_ID": trend.get("music", {}).get("mid", ""),
                    "Hashtags": json.dumps([tag.get("hashtag_name", "") for tag in trend.get("text_extra", []) if tag.get("hashtag_name")]),
                    "Region": trend.get("region", ""),
                    "Video_Type": str(trend.get("aweme_type", 0)),
                    "Sound_Type": "Original" if trend.get("music", {}).get("mid") else "Background",
                    "Relevance_Score": trend.get("relevance_score", 0),
                    "Relevance_Reason": trend.get("relevance_reason", ""),
                    "Trend_Category": trend.get("trend_category", ""),
                    "Audience_Match": trend.get("audience_match", False),
                    "Trend_Potential": trend.get("trend_potential", ""),
                    "Keyword": trend.get("keyword", ""),
                    "Hashtag": trend.get("hashtag", ""),
                    "TikTok_URL": f"https://www.tiktok.com/@{trend.get('author', {}).get('unique_id', '')}/video/{trend.get('aweme_id', '')}",
                    "Sentiment": trend.get("sentiment", "Neutral"),
                    "Audience": trend.get("audience", "General"),
                    "Created_At": datetime.fromtimestamp(trend.get("create_time", 0)).isoformat() if trend.get("create_time") else datetime.now().isoformat(),
                    "Saved_At": datetime.now().isoformat()
                }

                # Check if trend already exists (direct query)
                self.cursor.execute(
                    "SELECT id FROM Trends WHERE Aweme_ID = ?", (trend.get("aweme_id", ""),))
                existing = self.cursor.fetchone()

                if not existing:
                    await self._create_table_row("Trends", trend_record)
                    saved_count += 1
                else:
                    # Update existing trend
                    trend_id = existing[0]
                    await self._update_table_row("Trends", trend_id, trend_record)
                    saved_count += 1

            self.connection.commit()
            logger.info(f"Saved {saved_count} trends for user {username}")
            return True

        except Exception as e:
            logger.error(f"Error saving trends: {e}")
            return False
        finally:
            self.disconnect()

    async def get_user_trends(self, username: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get saved trends for a user (SeaTable-compatible)"""
        if not self.connect():
            return []

        try:
            # Query trends table directly
            self.cursor.execute("""
                SELECT * FROM Trends
                WHERE Username = ?
                ORDER BY Saved_At DESC
                LIMIT ?
            """, (username, limit))

            # Convert rows to dicts
            columns = [desc[0] for desc in self.cursor.description]
            trends = []

            for row in self.cursor.fetchall():
                trend = {}
                for i, col in enumerate(columns):
                    trend[col] = row[i]

                # Parse JSON fields and format data
                trend["Hashtags"] = json.loads(trend.get("Hashtags", "[]"))
                trend["Sentiment"] = trend.get("Sentiment", "Neutral")
                trend["Audience"] = trend.get("Audience", "General")
                trend["_id"] = trend["id"]
                trends.append(trend)

            return trends

        except Exception as e:
            logger.error(f"Error getting trends for {username}: {e}")
            return []
        finally:
            self.disconnect()

    async def get_all_trends(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all recent trends (SeaTable-compatible)"""
        if not self.connect():
            return []

        try:
            # Query trends table directly
            self.cursor.execute("""
                SELECT * FROM Trends
                ORDER BY Saved_At DESC
                LIMIT ?
            """, (limit,))

            # Convert rows to dicts
            columns = [desc[0] for desc in self.cursor.description]
            trends = []

            for row in self.cursor.fetchall():
                trend = {}
                for i, col in enumerate(columns):
                    trend[col] = row[i]

                # Parse JSON fields and format data
                trend["Hashtags"] = json.loads(trend.get("Hashtags", "[]"))
                trend["Sentiment"] = trend.get("Sentiment", "Neutral")
                trend["Audience"] = trend.get("Audience", "General")
                trend["_id"] = trend["id"]
                trends.append(trend)

            return trends

        except Exception as e:
            logger.error(f"Error getting all trends: {e}")
            return []
        finally:
            self.disconnect()

    async def _create_table_row(self, table_name: str, data: Dict[str, Any]) -> str:
        """Create a new row in SQLite table (mimics SeaTable API)"""
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            values = list(data.values())

            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

            self.cursor.execute(sql, values)
            self.connection.commit()

            row_id = self.cursor.lastrowid
            logger.info(f"Successfully created row with ID: {row_id}")
            return str(row_id)

        except Exception as e:
            logger.error(f"Error creating row in {table_name}: {e}")
            raise

    async def _update_table_row(self, table_name: str, row_id: str, data: Dict[str, Any]) -> str:
        """Update a row in SQLite table (mimics SeaTable API)"""
        try:
            set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
            values = list(data.values()) + [row_id]

            sql = f"UPDATE {table_name} SET {set_clause} WHERE id = ?"

            self.cursor.execute(sql, values)
            self.connection.commit()

            return row_id

        except Exception as e:
            logger.error(f"Error updating row {row_id} in {table_name}: {e}")
            raise

    async def _query_table(self, table_name: str, filters: str = "", limit: int = 100, order_by: str = "") -> List[Dict[str, Any]]:
        """Query table with filters (mimics SeaTable API)"""
        try:
            sql = f"SELECT * FROM {table_name}"

            conditions = []
            params = []

            if filters:
                # Simple filter parsing (supports basic equality filters like "Username='test'")
                if " AND " in filters or " OR " in filters:
                    # Complex filters - for now just add as is
                    conditions.append(filters)
                else:
                    # Simple equality filter
                    conditions.append(filters)

            if conditions:
                sql += " WHERE " + " AND ".join(conditions)

            if order_by:
                sql += f" ORDER BY {order_by}"

            if limit:
                sql += f" LIMIT {limit}"

            self.cursor.execute(sql, params)

            # Convert rows to dictionaries
            columns = [desc[0] for desc in self.cursor.description]
            results = []

            for row in self.cursor.fetchall():
                row_dict = {}
                for i, col in enumerate(columns):
                    row_dict[col] = row[i]
                # Add _id for SeaTable compatibility
                row_dict["_id"] = row_dict["id"]
                results.append(row_dict)

            return results

        except Exception as e:
            logger.error(f"Error querying {table_name}: {e}")
            return []

    def _analyze_sentiment(self, text: str) -> str:
        """Basic sentiment analysis (placeholder)"""
        positive_words = ['love', 'amazing', 'awesome',
                          'great', 'fantastic', 'beautiful', 'perfect']
        negative_words = ['hate', 'terrible', 'awful',
                          'bad', 'worst', 'horrible', 'disgusting']

        text_lower = text.lower()
        positive_count = sum(
            1 for word in positive_words if word in text_lower)
        negative_count = sum(
            1 for word in negative_words if word in text_lower)

        if positive_count > negative_count:
            return "Positive"
        elif negative_count > positive_count:
            return "Negative"
        else:
            return "Neutral"

    def _get_audience_info(self, stats: Dict[str, int]) -> str:
        """Determine audience type based on engagement patterns (placeholder)"""
        views = stats.get("views", 0)
        likes = stats.get("likes", 0)
        comments = stats.get("comments", 0)

        if views < 10000:
            return "Niche"
        elif views < 100000:
            return "Growing"
        elif views < 1000000:
            return "Mainstream"
        else:
            return "Viral"
