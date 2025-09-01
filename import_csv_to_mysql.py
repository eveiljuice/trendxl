#!/usr/bin/env python3
"""
Script to import CSV data into TrendXL MySQL database
"""

import mysql.connector
import csv
import json
from datetime import datetime
import os


class MySQLImporter:
    def __init__(self, host='localhost', user='root', password='', database='trendxl_db'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        """Connect to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print(f"✅ Connected to MySQL database: {self.database}")
            return True
        except mysql.connector.Error as e:
            print(f"❌ MySQL connection error: {e}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("🔌 Database connection closed")

    def import_users_csv(self, csv_file_path):
        """Import users data from CSV file"""
        print(f"\n📥 Importing users from: {csv_file_path}")

        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)

                for row in csv_reader:
                    # Parse JSON arrays
                    top_posts = json.loads(
                        row['top_posts']) if row['top_posts'] else []

                    # Insert user data
                    sql = """
                        INSERT INTO Users (id, link, parsed_niche, location, followers,
                                         engagement_rate, top_posts, created_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                        link=VALUES(link), parsed_niche=VALUES(parsed_niche),
                        location=VALUES(location), followers=VALUES(followers),
                        engagement_rate=VALUES(engagement_rate), top_posts=VALUES(top_posts)
                    """

                    values = (
                        int(row['id']),
                        row['link'],
                        row['parsed_niche'],
                        row['location'],
                        int(row['followers']),
                        float(row['engagement_rate']),
                        json.dumps(top_posts),
                        row['created_at']
                    )

                    self.cursor.execute(sql, values)

                self.connection.commit()
                print(f"✅ Users data imported successfully")

        except Exception as e:
            print(f"❌ Error importing users: {e}")
            self.connection.rollback()

    def import_trendfeed_csv(self, csv_file_path):
        """Import trend feed data from CSV file"""
        print(f"\n📥 Importing trend feed from: {csv_file_path}")

        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)

                for row in csv_reader:
                    # Parse JSON stat_metrics
                    stat_metrics = json.loads(
                        row['stat_metrics']) if row['stat_metrics'] else {}

                    # Insert trend data
                    sql = """
                        INSERT INTO TrendFeed (id, user_id, trend_title, platform, video_url,
                                             stat_metrics, relevance_score, trend_date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                        trend_title=VALUES(trend_title), platform=VALUES(platform),
                        video_url=VALUES(video_url), stat_metrics=VALUES(stat_metrics),
                        relevance_score=VALUES(relevance_score)
                    """

                    values = (
                        int(row['id']),
                        int(row['user_id']),
                        row['trend_title'],
                        row['platform'],
                        row['video_url'],
                        json.dumps(stat_metrics),
                        float(row['relevance_score']),
                        row['date']
                    )

                    self.cursor.execute(sql, values)

                self.connection.commit()
                print(f"✅ Trend feed data imported successfully")

        except Exception as e:
            print(f"❌ Error importing trend feed: {e}")
            self.connection.rollback()

    def import_interactionlog_csv(self, csv_file_path):
        """Import interaction log data from CSV file"""
        print(f"\n📥 Importing interaction log from: {csv_file_path}")

        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)

                for row in csv_reader:
                    # Insert interaction data
                    sql = """
                        INSERT INTO InteractionLog (user_id, trend_id, action_type, timestamp)
                        VALUES (%s, %s, %s, %s)
                    """

                    values = (
                        int(row['user_id']),
                        int(row['trend_id']),
                        row['action_type'],
                        row['timestamp']
                    )

                    self.cursor.execute(sql, values)

                self.connection.commit()
                print(f"✅ Interaction log data imported successfully")

        except Exception as e:
            print(f"❌ Error importing interaction log: {e}")
            self.connection.rollback()

    def import_nicheadapters_csv(self, csv_file_path):
        """Import niche adapters data from CSV file"""
        print(f"\n📥 Importing niche adapters from: {csv_file_path}")

        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)

                for row in csv_reader:
                    # Parse JSON topic_tags
                    topic_tags = json.loads(
                        row['topic_tags']) if row['topic_tags'] else []

                    # Insert niche adapter data
                    sql = """
                        INSERT INTO NicheAdapters (id, domain, parsed_by_gpt_summary,
                                                 topic_tags, created_at)
                        VALUES (%s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                        domain=VALUES(domain), parsed_by_gpt_summary=VALUES(parsed_by_gpt_summary),
                        topic_tags=VALUES(topic_tags)
                    """

                    values = (
                        int(row['id']),
                        row['domain'],
                        row['parsed_by_gpt_summary'],
                        json.dumps(topic_tags),
                        row['created_at']
                    )

                    self.cursor.execute(sql, values)

                self.connection.commit()
                print(f"✅ Niche adapters data imported successfully")

        except Exception as e:
            print(f"❌ Error importing niche adapters: {e}")
            self.connection.rollback()

    def get_table_counts(self):
        """Get row counts for all tables"""
        print("\n📊 TABLE ROW COUNTS:")

        tables = ['Users', 'TrendFeed', 'InteractionLog', 'NicheAdapters']

        for table in tables:
            try:
                self.cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                result = self.cursor.fetchone()
                print(f"   {table}: {result[0]} rows")
            except Exception as e:
                print(f"   {table}: Error - {e}")

    def run_import(self, csv_directory='.'):
        """Run complete import process"""
        print("🚀 TrendXL CSV Import Process")
        print("=" * 50)

        # Connect to database
        if not self.connect():
            return False

        try:
            # Import data from CSV files
            self.import_users_csv(os.path.join(csv_directory, 'users.csv'))
            self.import_trendfeed_csv(
                os.path.join(csv_directory, 'trendfeed.csv'))
            self.import_interactionlog_csv(
                os.path.join(csv_directory, 'interactionlog.csv'))
            self.import_nicheadapters_csv(
                os.path.join(csv_directory, 'nicheadapters.csv'))

            # Show final counts
            self.get_table_counts()

            print("\n🎉 Import completed successfully!")
            return True

        except Exception as e:
            print(f"\n❌ Import failed: {e}")
            return False
        finally:
            self.disconnect()


def main():
    """Main function"""
    print("📁 TrendXL MySQL CSV Importer")
    print("=" * 40)

    # Database configuration
    # You can modify these values or use environment variables
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'trendxl_db')
    }

    print(f"Database: {db_config['database']}")
    print(f"Host: {db_config['host']}")
    print(f"User: {db_config['user']}")
    print()

    # Create importer instance
    importer = MySQLImporter(**db_config)

    # Run import
    success = importer.run_import()

    if success:
        print("\n✅ All data imported successfully!")
        print("You can now query your TrendXL database.")
    else:
        print("\n❌ Import failed. Please check the errors above.")
        print("Make sure:")
        print("1. MySQL server is running")
        print("2. Database 'trendxl_db' exists (run trendxl.sql first)")
        print("3. CSV files are in the current directory")
        print("4. Database credentials are correct")


if __name__ == "__main__":
    main()
