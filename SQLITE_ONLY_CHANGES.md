# SQLite-Only Mode Changes

## Overview
This document outlines the changes made to support SQLite-only mode in TrendXL, removing dependencies on SeaTable for simpler deployment.

## Key Changes

### 1. Database Configuration
- **Removed**: SeaTable API integration
- **Added**: SQLite database with automatic schema management
- **Benefits**: No external dependencies, faster setup, local data storage

### 2. Environment Variables
```diff
# .env file changes
# API Keys for TrendXL
ENSEMBLE_DATA_API_KEY=your_ensemble_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
- SEATABLE_API_TOKEN=your_seatable_token_here

# Database Configuration (SQLite-only)
USE_SQLITE=true
SQLITE_DB_PATH=trendxl.db
```

### 3. Database Schema
```sql
-- SQLite Schema
CREATE TABLE IF NOT EXISTS trends (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hashtag TEXT NOT NULL,
    content TEXT,
    engagement_score REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trend_id INTEGER,
    metric_type TEXT,
    value REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (trend_id) REFERENCES trends(id)
);
```

### 4. Service Layer Changes

#### Database Adapter
- **File**: `backend/services/database_adapter.py`
- **Function**: Automatic SQLite database creation
- **Migration**: Schema updates on startup

#### Removed Dependencies
- `seatable-api` package
- SeaTable authentication
- External API calls for data storage

### 5. API Endpoints
All endpoints remain compatible:
- `GET /api/v1/trends` - Fetch trends
- `POST /api/v1/analytics` - Store analytics
- `GET /api/health` - Health check

### 6. Performance Improvements
- **Faster**: Local database queries
- **Reliable**: No network dependencies
- **Backup**: Simple file-based backup
- **Concurrent**: SQLite supports multiple readers

## Migration Guide

### From SeaTable to SQLite

1. **Backup Data** (if needed)
```bash
# Export SeaTable data to CSV
# (Manual process through SeaTable UI)
```

2. **Update Configuration**
```bash
# Edit .env
USE_SQLITE=true
# Remove SEATABLE_API_TOKEN
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
# Note: seatable-api no longer required
```

4. **Run Migration**
```python
# Database schema created automatically
python backend/main.py
```

## Benefits of SQLite Mode

### ✅ Advantages
- **Simple Setup**: No external accounts needed
- **Fast Development**: Quick iteration cycles
- **Local Storage**: Data stays on your machine
- **Backup Easy**: Single file backup
- **No Costs**: Free database solution
- **Concurrent Access**: Multiple readers supported

### ⚠️ Limitations
- **Single Writer**: Only one write operation at a time
- **File-based**: Database is a single file
- **No Replication**: Not suitable for high-availability
- **Size Limits**: Practical limit ~1TB per database

## Production Considerations

### For Production Use
```bash
# Use WAL mode for better concurrency
PRAGMA journal_mode=WAL;

# Regular backups
sqlite3 trendxl.db .backup backup.db

# Optimize database
sqlite3 trendxl.db VACUUM;
```

### Monitoring
- **Database Size**: Monitor `trendxl.db` file size
- **Performance**: Use `EXPLAIN QUERY PLAN` for optimization
- **Backups**: Regular automated backups

## Troubleshooting

### Common SQLite Issues

1. **Database Locked Error**
   - Close all connections
   - Check for long-running transactions
   - Use WAL mode: `PRAGMA journal_mode=WAL;`

2. **Corruption**
   - Restore from backup
   - Run integrity check: `PRAGMA integrity_check;`

3. **Performance**
   - Add indexes on frequently queried columns
   - Use connection pooling for high traffic

### Migration Issues
- **Data Loss**: Always backup before migration
- **Schema Changes**: Update schema version in code
- **Dependencies**: Remove SeaTable imports from code

## Future Enhancements

### Potential Improvements
- **Connection Pooling**: For high-concurrency scenarios
- **Read Replicas**: Multiple read-only database files
- **Encryption**: Database file encryption at rest
- **Migration Tools**: Automated schema migrations

### Alternative Databases
- **PostgreSQL**: For production workloads
- **MySQL**: Enterprise environments
- **MongoDB**: Document-based storage

## Support

For issues with SQLite mode:
1. Check logs in `logs/trendxl.log`
2. Verify database file permissions
3. Test with a fresh database file
4. Review SQLite documentation for specific errors
