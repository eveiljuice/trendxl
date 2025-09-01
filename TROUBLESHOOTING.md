# TrendXL Troubleshooting Guide

## 🚨 Common Error: "502: Incomplete user data from TikTok API (missing username)"

This error occurs when the Ensemble Data API cannot return valid user profile data. Here's how to diagnose and fix it:

### 🔍 Step 1: Check API Keys

Visit: `http://localhost:8000/api/debug/api-keys`

Make sure you have:

- ✅ `ENSEMBLE_DATA_API_KEY` configured in `.env`
- ✅ `OPENAI_API_KEY` configured in `.env`
- ✅ `SEATABLE_API_TOKEN` configured in `.env` (optional)

### 🧪 Step 2: Test Ensemble Data API

Visit: `http://localhost:8000/api/debug/test-ensemble`

This will test the API with a known working profile. Expected response:

```json
{
  "success": true,
  "test_username": "daviddobrik",
  "api_responded": true,
  "has_username": true,
  "follower_count": 123456
}
```

### 🎯 Step 3: Test Specific Profile

Visit: `http://localhost:8000/api/debug/test-profile/{username}`

Replace `{username}` with the username you're trying to analyze (without @).

Example: `http://localhost:8000/api/debug/test-profile/daviddobrik`

### 📋 Common Issues & Solutions

#### Issue: API Key Invalid

```json
{
  "success": false,
  "error": "Authentication failed"
}
```

**Solution**: Check your Ensemble Data API key at https://dashboard.ensembledata.com/

#### Issue: Profile Not Found

```json
{
  "success": false,
  "error": "User @username not found via Ensemble API"
}
```

**Solution**:

- Verify the TikTok profile exists and is public
- Check the username spelling
- Try a different profile to test

#### Issue: API Rate Limit

```json
{
  "success": false,
  "error": "Rate limit exceeded"
}
```

**Solution**: Wait and try again, or upgrade your Ensemble Data plan

#### Issue: No Username in Response

```json
{
  "has_username": false,
  "unique_id": "",
  "nickname": "User Name"
}
```

**Solution**: This is now handled automatically - the system will use fallback logic

### 🔧 Debug Mode

The enhanced error handling now provides:

- ✅ Detailed logging of API responses
- ✅ Fallback username extraction
- ✅ Better error messages
- ✅ Debug endpoints for testing

### 📞 Getting Help

If you're still having issues:

1. **Check the server logs** for detailed error messages
2. **Test with a known working profile** like `daviddobrik` or `zachking`
3. **Verify your API key** has sufficient credits
4. **Check if the profile is public** - private profiles may not be accessible

### 🌟 Debug Endpoints

- `GET /api/debug/api-keys` - Check API key configuration
- `GET /api/debug/test-ensemble` - Test Ensemble Data API
- `GET /api/debug/test-gpt` - Test OpenAI GPT API
- `GET /api/debug/test-profile/{username}` - Test specific profile
- `GET /api/health` - Overall system health

### ⚡ Quick Fix Checklist

1. ✅ Valid ENSEMBLE_DATA_API_KEY in `.env`
2. ✅ Profile exists and is public on TikTok
3. ✅ Username format: use `daviddobrik` not `@daviddobrik`
4. ✅ API key has sufficient credits
5. ✅ Server is running and accessible

With these improvements, the "502: Incomplete user data" error should be much more rare and easier to diagnose when it does occur!
