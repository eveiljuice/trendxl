-- TrendXL Sample Data
-- SQL inserts for populating the database with sample data

USE trendxl_db;

-- ========================================
-- Sample Users Data
-- ========================================
INSERT INTO Users (link, parsed_niche, location, followers, engagement_rate, top_posts) VALUES
('https://tiktok.com/@fashionista', 'Fashion', 'New York', 125000, 4.25, '["https://tiktok.com/@fashionista/video/123456789", "https://tiktok.com/@fashionista/video/987654321"]'),
('https://tiktok.com/@techguru', 'Technology', 'San Francisco', 89000, 6.12, '["https://tiktok.com/@techguru/video/111222333", "https://tiktok.com/@techguru/video/444555666"]'),
('https://tiktok.com/@foodiechef', 'Food', 'Los Angeles', 234000, 3.89, '["https://tiktok.com/@foodiechef/video/777888999", "https://tiktok.com/@foodiechef/video/000111222"]'),
('https://instagram.com/beautyqueen', 'Beauty', 'Miami', 456000, 5.67, '["https://instagram.com/p/AAA111", "https://instagram.com/p/BBB222"]'),
('https://tiktok.com/@fitnesscoach', 'Fitness', 'Chicago', 167000, 4.98, '["https://tiktok.com/@fitnesscoach/video/333444555", "https://tiktok.com/@fitnesscoach/video/666777888"]'),
('https://youtube.com/@lifestylevlogger', 'Lifestyle', 'Austin', 789000, 3.45, '["https://youtube.com/watch?v=CCC333", "https://youtube.com/watch?v=DDD444"]'),
('https://tiktok.com/@comedian', 'Comedy', 'Seattle', 321000, 7.23, '["https://tiktok.com/@comedian/video/555666777", "https://tiktok.com/@comedian/video/888999000"]'),
('https://instagram.com/travelblogger', 'Travel', 'Denver', 234000, 4.56, '["https://instagram.com/p/EEE555", "https://instagram.com/p/FFF666"]');

-- ========================================
-- Sample TrendFeed Data
-- ========================================
INSERT INTO TrendFeed (user_id, trend_title, platform, video_url, stat_metrics, relevance_score, trend_date) VALUES
(1, 'Spring Fashion Haul 2024 - Affordable Outfits Under $50', 'tiktok', 'https://tiktok.com/@fashionista/video/123456789', '{"views": 2500000, "ER": 4.25, "likes": 185000, "comments": 12500}', 0.85, '2024-03-15'),
(1, 'Minimalist Wardrobe Essentials Every Girl Needs', 'tiktok', 'https://tiktok.com/@fashionista/video/987654321', '{"views": 1800000, "ER": 3.98, "likes": 142000, "comments": 8900}', 0.78, '2024-03-10'),
(2, 'AI Tools That Will Change Your Life in 2024', 'tiktok', 'https://tiktok.com/@techguru/video/111222333', '{"views": 950000, "ER": 6.12, "likes": 78000, "comments": 5600}', 0.92, '2024-03-14'),
(2, 'Programming Languages You Should Learn This Year', 'tiktok', 'https://tiktok.com/@techguru/video/444555666', '{"views": 1200000, "ER": 5.45, "likes": 65000, "comments": 4200}', 0.88, '2024-03-12'),
(3, 'Easy 5-Minute Healthy Breakfast Recipes', 'tiktok', 'https://tiktok.com/@foodiechef/video/777888999', '{"views": 3200000, "ER": 3.89, "likes": 245000, "comments": 18700}', 0.76, '2024-03-16'),
(3, 'Restaurant Vs Homemade: Taste Test Challenge', 'tiktok', 'https://tiktok.com/@foodiechef/video/000111222', '{"views": 4100000, "ER": 4.12, "likes": 298000, "comments": 22300}', 0.81, '2024-03-13'),
(4, 'Skincare Routine That Actually Works - Before & After', 'instagram', 'https://instagram.com/p/AAA111', '{"views": 890000, "ER": 5.67, "likes": 67000, "comments": 3400}', 0.89, '2024-03-11'),
(4, 'Top 10 Drugstore Makeup Products You Need', 'instagram', 'https://instagram.com/p/BBB222', '{"views": 1200000, "ER": 4.98, "likes": 89000, "comments": 5600}', 0.83, '2024-03-09'),
(5, 'Home Workout No Equipment Needed - 15 Minute Routine', 'tiktok', 'https://tiktok.com/@fitnesscoach/video/333444555', '{"views": 2800000, "ER": 4.98, "likes": 210000, "comments": 15600}', 0.87, '2024-03-15'),
(5, 'Healthy Meal Prep for the Week - Step by Step', 'tiktok', 'https://tiktok.com/@fitnesscoach/video/666777888', '{"views": 1950000, "ER": 4.56, "likes": 165000, "comments": 12300}', 0.79, '2024-03-12'),
(6, 'A Day in My Life as a Digital Nomad', 'youtube', 'https://youtube.com/watch?v=CCC333', '{"views": 45000, "ER": 3.45, "likes": 3200, "comments": 450}', 0.73, '2024-03-14'),
(6, 'Top 5 Apps That Boost My Productivity', 'youtube', 'https://youtube.com/watch?v=DDD444', '{"views": 67000, "ER": 3.78, "likes": 4800, "comments": 620}', 0.76, '2024-03-11'),
(7, 'When Life Gives You Lemons... Comedy Skit', 'tiktok', 'https://tiktok.com/@comedian/video/555666777', '{"views": 5600000, "ER": 7.23, "likes": 456000, "comments": 34500}', 0.91, '2024-03-16'),
(7, 'My Most Embarrassing Moment Ever - Story Time', 'tiktok', 'https://tiktok.com/@comedian/video/888999000', '{"views": 4200000, "ER": 6.89, "likes": 378000, "comments": 28900}', 0.85, '2024-03-13'),
(8, 'Hidden Gems in Colorado You Need to Visit', 'instagram', 'https://instagram.com/p/EEE555', '{"views": 780000, "ER": 4.56, "likes": 56000, "comments": 2900}', 0.82, '2024-03-10'),
(8, 'Solo Backpacking Through Europe - Tips & Tricks', 'instagram', 'https://instagram.com/p/FFF666', '{"views": 950000, "ER": 4.23, "likes": 67000, "comments": 3400}', 0.78, '2024-03-08');

-- ========================================
-- Sample InteractionLog Data
-- ========================================
INSERT INTO InteractionLog (user_id, trend_id, action_type, timestamp) VALUES
(1, 1, 'watched', '2024-03-15 10:30:00'),
(1, 1, 'saved', '2024-03-15 10:31:00'),
(2, 3, 'watched', '2024-03-14 14:20:00'),
(2, 3, 'clicked', '2024-03-14 14:21:00'),
(2, 4, 'watched', '2024-03-12 09:15:00'),
(3, 5, 'watched', '2024-03-16 16:45:00'),
(3, 6, 'shared', '2024-03-13 11:20:00'),
(4, 7, 'watched', '2024-03-11 13:30:00'),
(4, 8, 'saved', '2024-03-09 15:45:00'),
(5, 9, 'watched', '2024-03-15 08:20:00'),
(5, 10, 'clicked', '2024-03-12 12:10:00'),
(6, 11, 'watched', '2024-03-14 17:30:00'),
(6, 12, 'ignored', '2024-03-11 19:15:00'),
(7, 13, 'watched', '2024-03-16 20:45:00'),
(7, 14, 'shared', '2024-03-13 21:20:00'),
(8, 15, 'watched', '2024-03-10 14:30:00'),
(8, 16, 'saved', '2024-03-08 16:45:00');

-- ========================================
-- Sample NicheAdapters Data
-- ========================================
INSERT INTO NicheAdapters (domain, parsed_by_gpt_summary, topic_tags) VALUES
('fashion', 'Fashion and lifestyle content focusing on clothing, style, and beauty trends', '["clothing", "style", "beauty", "fashion", "outfit", "shopping", "haul"]'),
('technology', 'Tech content covering gadgets, software, programming, and digital innovation', '["tech", "gadgets", "programming", "software", "innovation", "coding", "ai"]'),
('food', 'Culinary content featuring recipes, cooking tips, and food reviews', '["cooking", "recipes", "food", "culinary", "kitchen", "restaurant", "taste"]'),
('beauty', 'Beauty and skincare content with makeup tutorials and product reviews', '["beauty", "skincare", "makeup", "cosmetics", "routine", "glow"]'),
('fitness', 'Fitness and health content including workouts, nutrition, and wellness', '["fitness", "workout", "health", "nutrition", "exercise", "wellness"]'),
('lifestyle', 'Lifestyle content covering daily life, productivity, and personal development', '["lifestyle", "productivity", "daily", "routine", "motivation", "success"]'),
('comedy', 'Comedy and entertainment content with humor, sketches, and funny stories', '["comedy", "humor", "funny", "entertainment", "laugh", "sketch"]'),
('travel', 'Travel content featuring destinations, tips, and adventure experiences', '["travel", "destination", "adventure", "vacation", "explore", "wanderlust"]');
