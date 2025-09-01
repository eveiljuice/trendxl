-- TrendXL Database Schema for SQLite
-- SQL script for creating the TrendXL SQLite database with all required tables

-- ========================================
-- Table: Users (SeaTable-compatible)
-- ========================================
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- SeaTable-compatible fields
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
    -- AI Analysis fields
    Niche TEXT,
    Interests TEXT, -- JSON string
    Keywords TEXT, -- JSON string
    Hashtags TEXT, -- JSON string
    Target_Audience TEXT,
    Content_Style TEXT,
    Region_Focus TEXT,
    -- Timestamps
    Created_At TEXT DEFAULT CURRENT_TIMESTAMP,
    Last_Updated TEXT DEFAULT CURRENT_TIMESTAMP
);

-- ========================================
-- Table: Trends (SeaTable-compatible)
-- ========================================
CREATE TABLE IF NOT EXISTS Trends (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- SeaTable-compatible fields
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
    Hashtags TEXT, -- JSON string
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

    -- Foreign key to Users table (by username)
    FOREIGN KEY (Username) REFERENCES Users(Username) ON DELETE CASCADE
);

-- ========================================
-- Table: InteractionLog
-- ========================================
CREATE TABLE IF NOT EXISTS InteractionLog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL, -- Reference to Users(id)
    trend_id INTEGER NOT NULL, -- Reference to Trends(id)
    action_type TEXT NOT NULL CHECK(action_type IN ('watched', 'clicked', 'ignored', 'shared', 'saved')),
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (trend_id) REFERENCES Trends(id) ON DELETE CASCADE,
    UNIQUE(user_id, trend_id, action_type)
);

-- ========================================
-- Table: NicheAdapters
-- ========================================
CREATE TABLE IF NOT EXISTS NicheAdapters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain TEXT NOT NULL UNIQUE,
    parsed_by_gpt_summary TEXT,
    topic_tags TEXT, -- JSON string
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- ========================================
-- Views for Analytics
-- ========================================

-- View: User Engagement Summary
CREATE VIEW IF NOT EXISTS user_engagement_summary AS
SELECT
    u.id,
    u.Username,
    u.Niche as parsed_niche,
    u.Follower_Count as followers,
    0.0 as engagement_rate, -- Calculate from trends
    COUNT(DISTINCT t.id) as total_trends,
    COUNT(DISTINCT il.id) as total_interactions,
    AVG(t.Relevance_Score) as avg_trend_relevance,
    MAX(t.Created_At) as last_trend_date,
    u.Created_At as user_created_at
FROM Users u
LEFT JOIN Trends t ON u.Username = t.Username
LEFT JOIN InteractionLog il ON u.id = il.user_id
GROUP BY u.id, u.Username, u.Niche, u.Follower_Count, u.Created_At;

-- View: Trend Performance
CREATE VIEW IF NOT EXISTS trend_performance AS
SELECT
    t.id,
    t.Description as trend_title,
    'tiktok' as platform,
    u.Username as user_link,
    u.Niche as parsed_niche,
    t.Views as views,
    t.Engagement_Rate as engagement_rate,
    t.Likes as likes,
    t.Comments as comments,
    t.Relevance_Score,
    COUNT(il.id) as interaction_count,
    t.Created_At as trend_date,
    t.Created_At as created_at
FROM Trends t
JOIN Users u ON t.Username = u.Username
LEFT JOIN InteractionLog il ON t.id = il.trend_id
GROUP BY t.id, t.Description, u.Username, u.Niche, t.Views,
         t.Engagement_Rate, t.Likes, t.Comments, t.Relevance_Score,
         t.Created_At;

-- ========================================
-- Indexes for Performance
-- ========================================

-- Users table indexes
CREATE INDEX IF NOT EXISTS idx_users_username ON Users(Username);
CREATE INDEX IF NOT EXISTS idx_users_niche ON Users(Niche);
CREATE INDEX IF NOT EXISTS idx_users_followers ON Users(Follower_Count);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON Users(Created_At);

-- Trends table indexes
CREATE INDEX IF NOT EXISTS idx_trends_username ON Trends(Username);
CREATE INDEX IF NOT EXISTS idx_trends_aweme_id ON Trends(Aweme_ID);
CREATE INDEX IF NOT EXISTS idx_trends_relevance_score ON Trends(Relevance_Score);
CREATE INDEX IF NOT EXISTS idx_trends_created_at ON Trends(Created_At);
CREATE INDEX IF NOT EXISTS idx_trends_saved_at ON Trends(Saved_At);

-- InteractionLog table indexes
CREATE INDEX IF NOT EXISTS idx_interaction_user ON InteractionLog(user_id);
CREATE INDEX IF NOT EXISTS idx_interaction_trend ON InteractionLog(trend_id);
CREATE INDEX IF NOT EXISTS idx_interaction_action ON InteractionLog(action_type);
CREATE INDEX IF NOT EXISTS idx_interaction_timestamp ON InteractionLog(timestamp);

-- NicheAdapters table indexes
CREATE INDEX IF NOT EXISTS idx_niche_domain ON NicheAdapters(domain);
CREATE INDEX IF NOT EXISTS idx_niche_created_at ON NicheAdapters(created_at);

-- ========================================
-- Sample Data Inserts (Optional)
-- ========================================

-- Sample Users
INSERT OR IGNORE INTO Users (
    Username, Display_Name, Follower_Count, Following_Count, Video_Count,
    Bio, Avatar_URL, Region, Niche, Interests, Keywords, Hashtags,
    Target_Audience, Content_Style, Region_Focus
) VALUES
('fashionista', 'Fashion Guru', 125000, 500, 1200,
 'Fashion and lifestyle content creator', 'https://avatar1.jpg', 'New York',
 'Fashion', '["clothing", "style", "beauty"]', '["fashion", "outfit", "style"]', '["#fashion", "#style", "#ootd"]',
 'Young adults 18-35', 'Educational & Inspirational', 'North America'),

('techguru', 'Tech Expert', 89000, 300, 800,
 'Technology and programming tutorials', 'https://avatar2.jpg', 'San Francisco',
 'Technology', '["programming", "gadgets", "software"]', '["tech", "coding", "programming"]', '["#tech", "#programming", "#coding"]',
 'Developers and tech enthusiasts', 'Educational', 'Global'),

('foodiechef', 'Culinary Artist', 234000, 800, 1500,
 'Cooking recipes and food reviews', 'https://avatar3.jpg', 'Los Angeles',
 'Food', '["cooking", "recipes", "food"]', '["cooking", "recipes", "foodie"]', '["#cooking", "#food", "#recipe"]',
 'Home cooks and food lovers', 'Educational & Entertaining', 'North America');

-- Sample Niche Adapters
INSERT OR IGNORE INTO NicheAdapters (domain, parsed_by_gpt_summary, topic_tags) VALUES
('fashion', 'Fashion and lifestyle content focusing on clothing, style, and beauty trends', '["clothing", "style", "beauty", "fashion", "outfit"]'),
('technology', 'Tech content covering gadgets, software, programming, and digital innovation', '["tech", "gadgets", "programming", "software", "innovation"]'),
('food', 'Culinary content featuring recipes, cooking tips, and food reviews', '["cooking", "recipes", "food", "culinary", "kitchen"]');

-- ========================================
-- Useful Queries Examples
-- ========================================

-- Top performing users by followers
/*
SELECT Username, Follower_Count, Niche
FROM Users
ORDER BY Follower_Count DESC
LIMIT 10;
*/

-- Recent trends with high relevance
/*
SELECT t.Description, t.Relevance_Score, u.Username
FROM Trends t
JOIN Users u ON t.Username = u.Username
WHERE t.Relevance_Score > 0.7
ORDER BY t.Relevance_Score DESC
LIMIT 20;
*/

-- User interaction patterns
/*
SELECT u.Username, il.action_type, COUNT(*) as action_count
FROM Users u
JOIN InteractionLog il ON u.id = il.user_id
GROUP BY u.Username, il.action_type
ORDER BY u.Username, action_count DESC;
*/

-- Niche analysis
/*
SELECT na.domain, COUNT(DISTINCT u.id) as user_count, AVG(u.Follower_Count) as avg_followers
FROM NicheAdapters na
LEFT JOIN Users u ON na.domain = u.Niche
GROUP BY na.domain
ORDER BY user_count DESC;
*/

-- ========================================
-- Database Maintenance
-- ========================================

-- Clean up old interaction logs (older than 1 year)
/*
DELETE FROM InteractionLog
WHERE timestamp < datetime('now', '-1 year');
*/

-- Update user statistics (engagement rate calculation)
/*
UPDATE Users
SET Last_Updated = datetime('now')
WHERE id IN (
    SELECT DISTINCT u.id
    FROM Users u
    JOIN Trends t ON u.Username = t.Username
    WHERE t.Created_At >= datetime('now', '-30 days')
);
*/
