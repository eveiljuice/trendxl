#!/usr/bin/env python3
"""
SeaTable Database Setup Script
Creates the required tables and columns for TrendXL application
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class SeaTableSetup:
    def __init__(self):
        self.base_url = os.getenv(
            "SEATABLE_BASE_URL", "https://cloud.seatable.io")
        self.api_token = os.getenv("SEATABLE_API_TOKEN")
        self.base_uuid = os.getenv(
            "SEATABLE_BASE_UUID") or os.getenv("SEATABLE_ID")

        if not self.api_token:
            raise ValueError(
                "SEATABLE_API_TOKEN not found in environment variables")

        self.headers = {
            "Authorization": f"Token {self.api_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def create_table(self, table_name: str, columns: list):
        """Create a table with specified columns"""
        try:
            # First, check if table already exists
            existing_tables = self.get_tables()
            if table_name in [table['name'] for table in existing_tables]:
                print(f"⚠️  Table '{table_name}' already exists")
                return True

            # Create table
            url = f"{self.base_url}/api/v2.1/dtables/{self.base_uuid}/tables/"
            data = {
                "table_name": table_name,
                "columns": columns
            }

            response = requests.post(
                url, json=data, headers=self.headers, timeout=30)
            response.raise_for_status()

            print(f"✅ Table '{table_name}' created successfully")
            return True

        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to create table '{table_name}': {str(e)}")
            return False

    def get_tables(self):
        """Get list of existing tables"""
        try:
            url = f"{self.base_url}/api/v2.1/dtables/{self.base_uuid}/tables/"
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()

            result = response.json()
            return result.get('tables', [])

        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to get tables: {str(e)}")
            # Added for detailed debugging
            if hasattr(e, 'response') and e.response is not None:
                print(f"📄 Server response: {e.response.text}")
            return []

    def setup_users_table(self):
        """Create Users table with all required columns"""
        columns = [
            {"column_name": "Username", "column_type": "text"},
            {"column_name": "Display_Name", "column_type": "text"},
            {"column_name": "Follower_Count", "column_type": "number"},
            {"column_name": "Following_Count", "column_type": "number"},
            {"column_name": "Video_Count", "column_type": "number"},
            {"column_name": "Likes_Count", "column_type": "number"},
            {"column_name": "Bio", "column_type": "long_text"},
            {"column_name": "Avatar_URL", "column_type": "url"},
            {"column_name": "Verified", "column_type": "checkbox"},
            {"column_name": "Region", "column_type": "text"},
            {"column_name": "Language", "column_type": "text"},
            {"column_name": "Niche", "column_type": "single_select", "options": [
                {"name": "Beauty", "color": "#FF69B4"},
                {"name": "Tech", "color": "#00BFFF"},
                {"name": "Comedy", "color": "#FFD700"},
                {"name": "Food", "color": "#FF6347"},
                {"name": "Fitness", "color": "#32CD32"},
                {"name": "Lifestyle", "color": "#DDA0DD"},
                {"name": "Fashion", "color": "#FF1493"},
                {"name": "Music", "color": "#9370DB"},
                {"name": "Gaming", "color": "#FF4500"},
                {"name": "Education", "color": "#4169E1"},
                {"name": "Other", "color": "#808080"}
            ]},
            {"column_name": "Interests", "column_type": "long_text"},
            {"column_name": "Keywords", "column_type": "long_text"},
            {"column_name": "Hashtags", "column_type": "long_text"},
            {"column_name": "Target_Audience", "column_type": "long_text"},
            {"column_name": "Content_Style", "column_type": "text"},
            {"column_name": "Region_Focus", "column_type": "text"},
            {"column_name": "Created_At", "column_type": "date"},
            {"column_name": "Last_Updated", "column_type": "date"}
        ]

        return self.create_table("Users", columns)

    def setup_trends_table(self):
        """Create Trends table with all required columns"""
        columns = [
            {"column_name": "Username", "column_type": "text"},
            {"column_name": "Aweme_ID", "column_type": "text"},
            {"column_name": "Description", "column_type": "long_text"},
            {"column_name": "Author_Username", "column_type": "text"},
            {"column_name": "Author_Nickname", "column_type": "text"},
            {"column_name": "Author_Followers", "column_type": "number"},
            {"column_name": "Views", "column_type": "number"},
            {"column_name": "Likes", "column_type": "number"},
            {"column_name": "Comments", "column_type": "number"},
            {"column_name": "Shares", "column_type": "number"},
            {"column_name": "Downloads", "column_type": "number"},
            {"column_name": "Favourited", "column_type": "number"},
            {"column_name": "Whatsapp_Shares", "column_type": "number"},
            {"column_name": "Engagement_Rate",
                "column_type": "number", "format": "percent"},
            {"column_name": "Duration", "column_type": "number"},
            {"column_name": "Video_Cover", "column_type": "url"},
            {"column_name": "Video_URL", "column_type": "url"},
            {"column_name": "Music_Title", "column_type": "text"},
            {"column_name": "Music_Author", "column_type": "text"},
            {"column_name": "Music_ID", "column_type": "text"},
            {"column_name": "Hashtags", "column_type": "long_text"},
            {"column_name": "Region", "column_type": "text"},
            {"column_name": "Video_Type", "column_type": "single_select", "options": [
                {"name": "Original", "color": "#32CD32"},
                {"name": "Repost", "color": "#FFA500"},
                {"name": "Duet", "color": "#FF69B4"},
                {"name": "Stitch", "color": "#00BFFF"}
            ]},
            {"column_name": "Sound_Type", "column_type": "single_select", "options": [
                {"name": "Original", "color": "#32CD32"},
                {"name": "Background", "color": "#9370DB"},
                {"name": "Trending", "color": "#FF6347"}
            ]},
            {"column_name": "Relevance_Score", "column_type": "number"},
            {"column_name": "Relevance_Reason", "column_type": "long_text"},
            {"column_name": "Trend_Category", "column_type": "text"},
            {"column_name": "Audience_Match", "column_type": "checkbox"},
            {"column_name": "Trend_Potential", "column_type": "single_select", "options": [
                {"name": "Growing", "color": "#32CD32"},
                {"name": "Stable", "color": "#00BFFF"},
                {"name": "Declining", "color": "#FFA500"}
            ]},
            {"column_name": "Keyword", "column_type": "text"},
            {"column_name": "Hashtag", "column_type": "text"},
            {"column_name": "TikTok_URL", "column_type": "url"},
            {"column_name": "Sentiment", "column_type": "single_select", "options": [
                {"name": "Positive", "color": "#32CD32"},
                {"name": "Neutral", "color": "#808080"},
                {"name": "Negative", "color": "#FF6347"}
            ]},
            {"column_name": "Audience", "column_type": "single_select", "options": [
                {"name": "Niche", "color": "#9370DB"},
                {"name": "Growing", "color": "#00BFFF"},
                {"name": "Mainstream", "color": "#FFD700"},
                {"name": "Viral", "color": "#FF1493"}
            ]},
            {"column_name": "Created_At", "column_type": "date"},
            {"column_name": "Saved_At", "column_type": "date"}
        ]

        return self.create_table("Trends", columns)

    def setup_database(self):
        """Setup complete database with all required tables"""
        print("🔧 Setting up SeaTable database for TrendXL...")
        print(f"Base URL: {self.base_url}")
        print(f"Base UUID: {self.base_uuid}")
        print("-" * 50)

        # Check connection
        try:
            tables = self.get_tables()
            print(f"✅ Successfully connected to SeaTable")
            print(f"📊 Found {len(tables)} existing tables")
        except Exception as e:
            print(f"❌ Failed to connect to SeaTable: {str(e)}")
            return False

        # Setup tables
        success_count = 0

        print("\n🏗️  Creating Users table...")
        if self.setup_users_table():
            success_count += 1

        print("\n🏗️  Creating Trends table...")
        if self.setup_trends_table():
            success_count += 1

        print("\n" + "=" * 50)
        if success_count == 2:
            print("✅ Database setup completed successfully!")
            print("🎉 TrendXL is ready to use!")
        else:
            print(
                f"⚠️  Database setup partially completed ({success_count}/2 tables)")
            print("Please check the errors above and try again")

        return success_count == 2


def main():
    """Main setup function"""
    print("🌟 TrendXL SeaTable Database Setup")
    print("=" * 50)

    try:
        setup = SeaTableSetup()
        setup.setup_database()
    except ValueError as e:
        print(f"❌ Configuration error: {str(e)}")
        print("\nPlease ensure your .env file contains:")
        print("- SEATABLE_API_TOKEN")
        print("- SEATABLE_BASE_URL (optional, defaults to cloud.seatable.io)")
        print("- SEATABLE_BASE_UUID or SEATABLE_ID (required)")
        print("\n📋 To get access to TrendXL SeaTable database:")
        print("🔗 Join here: https://cloud.seatable.io/dtable/links/bc4b5e5624bf47b49d82")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()
