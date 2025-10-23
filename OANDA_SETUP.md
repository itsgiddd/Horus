# OANDA API Setup Guide for HORUS

This guide will help you configure HORUS to display real historical candles from OANDA and CryptoCompare APIs instead of simulated data.

## Quick Setup

### Step 1: Get Your OANDA API Credentials

1. **Create an OANDA Account** (if you don't have one):
   - Go to https://www.oanda.com/
   - Sign up for a FREE practice account (no credit card needed!)
   - This gives you access to real forex data without risking any money

2. **Generate Your API Token**:
   - Log into your OANDA account
   - Go to **"Manage API Access"** in your account settings
   - Or visit: https://www.oanda.com/account/tpa/personal_token
   - Click **"Generate"** to create a new personal access token
   - **IMPORTANT**: Copy this token immediately - you won't see it again!

3. **Find Your Account ID**:
   - In your OANDA dashboard, look for "Account ID"
   - It's usually in the format: `XXX-XXX-XXXXXXXX-XXX`
   - Or check the account dropdown menu

### Step 2: Get CryptoCompare API Key (for BTC/ETH/SOL)

1. Visit https://min-api.cryptocompare.com/
2. Sign up for a FREE account
3. Go to your dashboard and generate an API key
4. Copy the API key

### Step 3: Configure HORUS Backend

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Copy the example environment file**:
   ```bash
   cp .env.example .env
   ```

3. **Edit the .env file**:
   Open `backend/.env` in your text editor and add your credentials:

   ```env
   # OANDA API Configuration
   OANDA_API_KEY=your_oanda_api_token_here
   OANDA_ACCOUNT_ID=your_account_id_here
   OANDA_ENVIRONMENT=practice

   # CryptoCompare API Configuration
   CRYPTOCOMPARE_API_KEY=your_cryptocompare_api_key_here
   ```

   **Example**:
   ```env
   OANDA_API_KEY=abc123def456ghi789jkl012mno345pqr678-stu901vwx234yz
   OANDA_ACCOUNT_ID=101-123-4567890-001
   OANDA_ENVIRONMENT=practice
   CRYPTOCOMPARE_API_KEY=xyz789abc123def456ghi
   ```

4. **Save the file**

### Step 4: Restart the Backend

If your backend is running, restart it to load the new environment variables:

```bash
# Stop the backend (Ctrl+C if running in terminal)
# Then restart:
python app.py
```

Or from the Electron app:
- The backend should auto-detect and use your API keys
- You can verify in the backend console logs

## Verification

Once configured, you should see:

### In the Backend Console:
```
[INFO] OANDA API configured successfully
[INFO] CryptoCompare API configured successfully
[INFO] Fetched 200 historical data points for EUR/USD from OANDA
[INFO] Fetched 200 historical data points for BTC from CryptoCompare
```

### In the HORUS App:
- Charts will show **real historical candle data** instead of simulated data
- Volume data will be accurate
- Price movements will match real market conditions
- All USD forex pairs and crypto pairs will have live data

## Troubleshooting

### Issue: Charts still showing simulated data

**Solution 1**: Check your .env file location
- The `.env` file MUST be in the `backend/` directory
- Not in the root directory
- File name is exactly `.env` (with the dot)

**Solution 2**: Check your credentials
- OANDA API token should be ~50-60 characters long
- Account ID should be in format: `XXX-XXX-XXXXXXXX-XXX`
- No extra spaces before or after the values

**Solution 3**: Check environment variable
- Make sure `OANDA_ENVIRONMENT=practice` (not `live` unless you're ready for real trading!)
- Practice account uses different API endpoint than live

**Solution 4**: Restart everything
```bash
# Stop the Electron app
# Stop the backend (Ctrl+C)
# Start backend again:
cd backend
python app.py

# Start Electron app again
```

### Issue: "OANDA API error" in console

**Possible causes**:
1. **Invalid API token** - Generate a new one from OANDA
2. **Wrong account ID** - Double-check the ID in your OANDA dashboard
3. **Rate limit exceeded** - Free accounts have limits, wait a few minutes
4. **Network issue** - Check your internet connection

### Issue: Crypto data not showing

**Solution**: Verify CryptoCompare API key
- Log into https://www.cryptocompare.com/
- Check API key is active and has sufficient credits (free tier is fine)
- CryptoCompare free tier includes 100,000 calls/month

### Issue: Some forex pairs not working

**Note**: OANDA practice accounts may not have access to all exotic pairs. The following pairs are guaranteed to work:
- EUR/USD, GBP/USD, USD/JPY, AUD/USD, USD/CAD, NZD/USD, USD/CHF

Exotic pairs (USD/CNY, USD/INR, etc.) require a live OANDA account or may fallback to free exchange rate APIs.

## Using Live Trading (Advanced)

⚠️ **WARNING**: Only change to live trading if you understand the risks!

1. Set up a live OANDA trading account (requires deposit)
2. Generate a live API token
3. In your `.env` file, change:
   ```env
   OANDA_ENVIRONMENT=live
   ```
4. **This connects to real money accounts - be careful!**

## Environment Variables Reference

```env
# Required for OANDA forex data
OANDA_API_KEY=<your_api_token>
OANDA_ACCOUNT_ID=<your_account_id>
OANDA_ENVIRONMENT=practice   # or 'live' for real trading

# Required for crypto data (BTC, ETH, SOL, etc.)
CRYPTOCOMPARE_API_KEY=<your_api_key>

# Server settings (don't change unless needed)
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
FLASK_DEBUG=True
```

## Supported Assets

### With OANDA API:
All USD forex pairs:
- Major: EUR/USD, GBP/USD, USD/JPY, AUD/USD, USD/CAD, NZD/USD, USD/CHF
- Exotic: USD/CNY, USD/HKD, USD/SGD, USD/SEK, USD/NOK, USD/DKK, USD/ZAR, USD/MXN, USD/TRY, USD/INR, USD/KRW, USD/BRL, USD/PLN, USD/THB, USD/IDR, USD/CZK, USD/HUF, USD/ILS, USD/CLP, USD/PHP, USD/AED, USD/SAR, USD/MYR, USD/RON

### With CryptoCompare API:
All major cryptocurrencies:
- BTC, ETH, SOL, ADA, XRP, DOT, LINK, MATIC, AVAX, UNI

## Need Help?

1. Check the backend console for error messages
2. Verify your API credentials are correct
3. Make sure the `.env` file is in the `backend/` directory
4. Restart both the backend and the Electron app
5. Check OANDA/CryptoCompare account status (not suspended, has credits, etc.)

## Success!

Once configured correctly, HORUS will display:
- ✅ Real historical price data from OANDA for forex
- ✅ Real historical price data from CryptoCompare for crypto
- ✅ Accurate volume information
- ✅ Live price updates
- ✅ All USD pairs available for trading analysis
- ✅ AI predictions based on real market data

Happy trading! 📈
