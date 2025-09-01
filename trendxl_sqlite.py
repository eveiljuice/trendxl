#!/usr/bin/env python3
"""
TrendXL SQLite Database Setup
Creates and initializes SQLite database for local development and testing
"""

import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path


class TrendXLSQLite:
    def __init__(self, db_path='trendxl_local.db'):
        """Initialize SQLite database connection"""
        self.db_path = Path(db_path)
        self.connection = None
        self.cursor = None

        print(f"🔧 TrendXL SQLite Database")
        print(f"📍 Database path: {self.db_path.absolute()}")
        print()

    def connect(self):
        """Connect to SQLite database"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.execute("PRAGMA foreign_keys = ON")
            self.cursor = self.connection.cursor()
            print("✅ Connected to SQLite database")
            return True
        except sqlite3.Error as e:
            print(f"❌ SQLite connection error: {e}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
        print("🔌 Database connection closed")

    def create_tables(self):
        """Create all required tables"""
        print("🏗️  Creating database tables...")

        # Enable foreign keys and JSON support
        self.cursor.execute("PRAGMA foreign_keys = ON")

        # Users table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                link TEXT NOT NULL UNIQUE,
                parsed_niche TEXT,
                location TEXT,
                followers INTEGER DEFAULT 0,
                engagement_rate REAL DEFAULT 0.0,
                top_posts TEXT,  -- JSON array
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # TrendFeed table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS TrendFeed (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                trend_title TEXT NOT NULL,
                platform TEXT CHECK(platform IN ('tiktok', 'instagram', 'youtube', 'twitter', 'other')),
                video_url TEXT,
                stat_metrics TEXT,  -- JSON object
                relevance_score REAL DEFAULT 0.0 CHECK(relevance_score >= 0.0 AND relevance_score <= 1.0),
                trend_date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
            )
        """)

        # InteractionLog table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS InteractionLog (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                trend_id INTEGER NOT NULL,
                action_type TEXT CHECK(action_type IN ('watched', 'clicked', 'ignored', 'shared', 'saved')),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
                FOREIGN KEY (trend_id) REFERENCES TrendFeed(id) ON DELETE CASCADE,
                UNIQUE(user_id, trend_id, action_type)
            )
        """)

        # NicheAdapters table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS NicheAdapters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT NOT NULL UNIQUE,
                parsed_by_gpt_summary TEXT,
                topic_tags TEXT,  -- JSON array
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create indexes for better performance
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_users_niche ON Users(parsed_niche)",
            "CREATE INDEX IF NOT EXISTS idx_users_location ON Users(location)",
            "CREATE INDEX IF NOT EXISTS idx_users_followers ON Users(followers)",
            "CREATE INDEX IF NOT EXISTS idx_users_created ON Users(created_at)",
            "CREATE INDEX IF NOT EXISTS idx_trends_user ON TrendFeed(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_trends_platform ON TrendFeed(platform)",
            "CREATE INDEX IF NOT EXISTS idx_trends_date ON TrendFeed(trend_date)",
            "CREATE INDEX IF NOT EXISTS idx_trends_relevance ON TrendFeed(relevance_score)",
            "CREATE INDEX IF NOT EXISTS idx_trends_created ON TrendFeed(created_at)",
            "CREATE INDEX IF NOT EXISTS idx_interactions_user ON InteractionLog(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_interactions_trend ON InteractionLog(trend_id)",
            "CREATE INDEX IF NOT EXISTS idx_interactions_action ON InteractionLog(action_type)",
            "CREATE INDEX IF NOT EXISTS idx_interactions_time ON InteractionLog(timestamp)",
            "CREATE INDEX IF NOT EXISTS idx_niches_domain ON NicheAdapters(domain)",
            "CREATE INDEX IF NOT EXISTS idx_niches_created ON NicheAdapters(created_at)"
        ]

        for index_sql in indexes:
            self.cursor.execute(index_sql)

        self.connection.commit()
        print("✅ All tables and indexes created successfully")

    def insert_sample_data(self):
        """Insert sample data for testing"""
        print("📥 Inserting sample data...")

        # Sample Users
        users_data = [
            ('https://tiktok.com/@fashionista', 'Fashion', 'New York', 125000, 4.25,
             json.dumps(['https://tiktok.com/@fashionista/video/123', 'https://tiktok.com/@fashionista/video/456'])),
            ('https://tiktok.com/@techguru', 'Technology', 'San Francisco', 89000, 6.12,
             json.dumps(['https://tiktok.com/@techguru/video/789', 'https://tiktok.com/@techguru/video/012'])),
            ('https://tiktok.com/@foodiechef', 'Food', 'Los Angeles', 234000, 3.89,
             json.dumps(['https://tiktok.com/@foodiechef/video/345', 'https://tiktok.com/@foodiechef/video/678'])),
            ('https://instagram.com/beautyqueen', 'Beauty', 'Miami', 456000, 5.67,
             json.dumps(['https://instagram.com/p/AAA111', 'https://instagram.com/p/BBB222'])),
            ('https://tiktok.com/@fitnesscoach', 'Fitness', 'Chicago', 167000, 4.98,
             json.dumps(['https://tiktok.com/@fitnesscoach/video/333', 'https://tiktok.com/@fitnesscoach/video/444']))
        ]

        self.cursor.executemany("""
            INSERT OR REPLACE INTO Users (link, parsed_niche, location, followers, engagement_rate, top_posts)
            VALUES (?, ?, ?, ?, ?, ?)
        """, users_data)

        # Sample Niche Adapters
        niches_data = [
            ('fashion', 'Fashion and lifestyle content focusing on clothing, style, and beauty trends',
             json.dumps(['clothing', 'style', 'beauty', 'fashion', 'outfit'])),
            ('technology', 'Tech content covering gadgets, software, programming, and digital innovation',
             json.dumps(['tech', 'gadgets', 'programming', 'software', 'innovation'])),
            ('food', 'Culinary content featuring recipes, cooking tips, and food reviews',
             json.dumps(['cooking', 'recipes', 'food', 'culinary', 'kitchen'])),
            ('beauty', 'Beauty and skincare content with makeup tutorials and product reviews',
             json.dumps(['beauty', 'skincare', 'makeup', 'cosmetics', 'routine'])),
            ('fitness', 'Fitness and health content including workouts, nutrition, and wellness',
             json.dumps(['fitness', 'workout', 'health', 'nutrition', 'exercise']))
        ]

        self.cursor.executemany("""
            INSERT OR REPLACE INTO NicheAdapters (domain, parsed_by_gpt_summary, topic_tags)
            VALUES (?, ?, ?)
        """, niches_data)

        # Sample Trends
        trends_data = [
            (1, 'Spring Fashion Haul 2024 - Affordable Outfits Under $50', 'tiktok',
             'https://tiktok.com/@fashionista/video/123456789',
             json.dumps({'views': 2500000, 'ER': 4.25,
                        'likes': 185000, 'comments': 12500}),
             0.85, '2024-03-15'),
            (2, 'AI Tools That Will Change Your Life in 2024', 'tiktok',
             'https://tiktok.com/@techguru/video/111222333',
             json.dumps({'views': 950000, 'ER': 6.12,
                        'likes': 78000, 'comments': 5600}),
             0.92, '2024-03-14'),
            (3, 'Easy 5-Minute Healthy Breakfast Recipes', 'tiktok',
             'https://tiktok.com/@foodiechef/video/777888999',
             json.dumps({'views': 3200000, 'ER': 3.89,
                        'likes': 245000, 'comments': 18700}),
             0.76, '2024-03-16')
        ]

        self.cursor.executemany("""
            INSERT OR REPLACE INTO TrendFeed (user_id, trend_title, platform, video_url, stat_metrics, relevance_score, trend_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, trends_data)

        # Sample Interactions
        interactions_data = [
            (1, 1, 'watched'),
            (1, 1, 'saved'),
            (2, 2, 'watched'),
            (2, 2, 'clicked'),
            (3, 3, 'watched'),
            (3, 3, 'shared')
        ]

        self.cursor.executemany("""
            INSERT OR IGNORE INTO InteractionLog (user_id, trend_id, action_type)
            VALUES (?, ?, ?)
        """, interactions_data)

        self.connection.commit()
        print("✅ Sample data inserted successfully")

    def get_table_counts(self):
        """Get row counts for all tables"""
        print("\n📊 TABLE ROW COUNTS:")

        tables = ['Users', 'TrendFeed', 'InteractionLog', 'NicheAdapters']

        for table in tables:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = self.cursor.fetchone()[0]
            print(f"   {table}: {count} rows")

    def run_sample_queries(self):
        """Run sample analytical queries"""
        print("\n🔍 SAMPLE ANALYTICAL QUERIES:")

        # Top users by engagement
        print("\n👥 Top users by engagement:")
        self.cursor.execute("""
            SELECT link, parsed_niche, followers, engagement_rate
            FROM Users
            ORDER BY engagement_rate DESC, followers DESC
            LIMIT 5
        """)
        for row in self.cursor.fetchall():
            print(
                f"   • {row[0]} ({row[1]}) - {row[2]} followers, {row[3]} ER")

        # Recent trends
        print("\n📈 Recent trends:")
        self.cursor.execute("""
            SELECT tf.trend_title, u.link, tf.platform, tf.relevance_score
            FROM TrendFeed tf
            JOIN Users u ON tf.user_id = u.id
            ORDER BY tf.trend_date DESC
            LIMIT 5
        """)
        for row in self.cursor.fetchall():
            print(f"   • {row[0]} by {row[1]} ({row[2]}) - Score: {row[3]}")

        # Niche distribution
        print("\n🏷️  Niche distribution:")
        self.cursor.execute("""
            SELECT parsed_niche, COUNT(*) as user_count, AVG(engagement_rate) as avg_er
            FROM Users
            GROUP BY parsed_niche
            ORDER BY user_count DESC
        """)
        for row in self.cursor.fetchall():
            print(f"   • {row[0]}: {row[1]} users, avg ER: {row[2]:.2f}")

    def create_views(self):
        """Create analytical views (SQLite version)"""
        print("📊 Creating analytical views...")

        # User engagement summary view
        self.cursor.execute("""
            CREATE VIEW IF NOT EXISTS user_engagement_summary AS
            SELECT
                u.id,
                u.link,
                u.parsed_niche,
                u.followers,
                u.engagement_rate,
                COUNT(DISTINCT tf.id) as total_trends,
                COUNT(DISTINCT il.id) as total_interactions,
                AVG(tf.relevance_score) as avg_trend_relevance,
                MAX(tf.created_at) as last_trend_date,
                u.created_at as user_created_at
            FROM Users u
            LEFT JOIN TrendFeed tf ON u.id = tf.user_id
            LEFT JOIN InteractionLog il ON u.id = il.user_id
            GROUP BY u.id, u.link, u.parsed_niche, u.followers, u.engagement_rate, u.created_at
        """)

        # Trend performance view
        self.cursor.execute("""
            CREATE VIEW IF NOT EXISTS trend_performance AS
            SELECT
                tf.id,
                tf.trend_title,
                tf.platform,
                u.link as user_link,
                u.parsed_niche,
                json_extract(tf.stat_metrics, '$.views') as views,
                json_extract(tf.stat_metrics, '$.ER') as engagement_rate,
                json_extract(tf.stat_metrics, '$.likes') as likes,
                json_extract(tf.stat_metrics, '$.comments') as comments,
                tf.relevance_score,
                COUNT(il.id) as interaction_count,
                tf.trend_date,
                tf.created_at
            FROM TrendFeed tf
            JOIN Users u ON tf.user_id = u.id
            LEFT JOIN InteractionLog il ON tf.id = il.trend_id
            GROUP BY tf.id, tf.trend_title, tf.platform, u.link, u.parsed_niche,
                     tf.stat_metrics, tf.relevance_score, tf.trend_date, tf.created_at
        """)

        self.connection.commit()
        print("✅ Analytical views created successfully")

    def setup_database(self):
        """Complete database setup process"""
        print("🚀 TrendXL SQLite Database Setup")
        print("=" * 50)

        if not self.connect():
            return False

        try:
            self.create_tables()
            self.create_views()
            self.insert_sample_data()
            self.get_table_counts()
            self.run_sample_queries()

            print("\n🎉 SQLite database setup completed successfully!")
            print(f"📍 Database file: {self.db_path.absolute()}")

            return True

        except Exception as e:
            print(f"\n❌ Setup failed: {e}")
            return False
        finally:
            self.disconnect()


def main():
    """Main function"""
    print("🗄️  TrendXL SQLite Database Creator")
    print("=" * 40)

    # Create database instance
    db = TrendXLSQLite()

    # Setup database
    success = db.setup_database()

    if success:
        print("\n✅ SQLite database is ready for use!")
        print("You can now connect your TrendXL application to this local database.")
        print(f"Database file location: {db.db_path.absolute()}")
    else:
        print("\n❌ Database setup failed. Please check the errors above.")

    print("\n💡 Next steps:")
    print("1. Update your application to use SQLite instead of SeaTable")
    print("2. Test your application with local data")
    print("3. Switch back to SeaTable once API issues are resolved")


if __name__ == "__main__":
    main()
