from flask import Blueprint, jsonify, request
import os
import logging

logger = logging.getLogger(__name__)
config_bp = Blueprint('config', __name__)

@config_bp.route('/api-keys', methods=['GET'])
def get_api_keys():
    """Get current API key configuration status (masked)"""
    try:
        # Check if API keys are configured
        cryptocompare_configured = bool(os.getenv('CRYPTOCOMPARE_API_KEY'))
        oanda_configured = bool(os.getenv('OANDA_API_KEY'))
        oanda_account_id = os.getenv('OANDA_ACCOUNT_ID', '')
        oanda_environment = os.getenv('OANDA_ENVIRONMENT', 'practice')

        return jsonify({
            'cryptocompare_configured': cryptocompare_configured,
            'oanda_configured': oanda_configured,
            'oanda_account_id': oanda_account_id if oanda_configured else '',
            'oanda_environment': oanda_environment
        })
    except Exception as e:
        logger.error(f'Error getting API keys: {e}')
        return jsonify({'error': str(e)}), 500

@config_bp.route('/api-keys', methods=['POST'])
def save_api_keys():
    """Save API keys to .env file"""
    try:
        data = request.json
        cryptocompare_key = data.get('cryptocompare_api_key', '').strip()
        oanda_key = data.get('oanda_api_key', '').strip()
        oanda_account_id = data.get('oanda_account_id', '').strip()
        oanda_environment = data.get('oanda_environment', 'practice')

        # Don't save if it's the masked placeholder
        if cryptocompare_key == '••••••••':
            cryptocompare_key = ''
        if oanda_key == '••••••••':
            oanda_key = ''

        # Read current .env file
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
        env_lines = []

        # Read existing file if it exists
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                env_lines = f.readlines()
        else:
            # Create from .env.example
            example_path = env_path + '.example'
            if os.path.exists(example_path):
                with open(example_path, 'r') as f:
                    env_lines = f.readlines()

        # Update or add API keys
        updated_lines = []
        keys_to_update = {
            'CRYPTOCOMPARE_API_KEY': cryptocompare_key,
            'OANDA_API_KEY': oanda_key,
            'OANDA_ACCOUNT_ID': oanda_account_id,
            'OANDA_ENVIRONMENT': oanda_environment
        }

        keys_found = set()

        for line in env_lines:
            updated = False
            for key, value in keys_to_update.items():
                if line.startswith(f'{key}=') or line.startswith(f'# {key}='):
                    if value:  # Only write if there's a value
                        updated_lines.append(f'{key}={value}\n')
                        keys_found.add(key)
                    else:
                        # Comment out if empty
                        updated_lines.append(f'# {key}=\n')
                        keys_found.add(key)
                    updated = True
                    break
            if not updated:
                updated_lines.append(line)

        # Add any missing keys at the end
        for key, value in keys_to_update.items():
            if key not in keys_found and value:
                updated_lines.append(f'\n{key}={value}\n')

        # Write back to .env file
        with open(env_path, 'w') as f:
            f.writelines(updated_lines)

        logger.info('API keys saved successfully')
        return jsonify({
            'success': True,
            'message': 'API keys saved successfully. Restart the backend to apply changes.'
        })

    except Exception as e:
        logger.error(f'Error saving API keys: {e}')
        return jsonify({'error': str(e)}), 500

@config_bp.route('/test-api-keys', methods=['POST'])
def test_api_keys():
    """Test API key connections"""
    try:
        data = request.json
        cryptocompare_key = data.get('cryptocompare_api_key', '').strip()
        oanda_key = data.get('oanda_api_key', '').strip()
        oanda_account_id = data.get('oanda_account_id', '').strip()
        oanda_environment = data.get('oanda_environment', 'practice')

        # Skip masked placeholders
        if cryptocompare_key == '••••••••':
            cryptocompare_key = os.getenv('CRYPTOCOMPARE_API_KEY', '')
        if oanda_key == '••••••••':
            oanda_key = os.getenv('OANDA_API_KEY', '')
        if not oanda_account_id:
            oanda_account_id = os.getenv('OANDA_ACCOUNT_ID', '')

        results = {
            'oanda_status': False,
            'cryptocompare_status': False,
            'oanda_message': '',
            'cryptocompare_message': ''
        }

        # Test OANDA
        if oanda_key and oanda_account_id:
            try:
                from oandapyV20 import API
                from oandapyV20.exceptions import V20Error
                import oandapyV20.endpoints.accounts as accounts

                client = API(access_token=oanda_key, environment=oanda_environment)
                r = accounts.AccountSummary(accountID=oanda_account_id)
                response = client.request(r)

                if response and 'account' in response:
                    results['oanda_status'] = True
                    results['oanda_message'] = 'Connected successfully'
                else:
                    results['oanda_message'] = 'Invalid response from OANDA'
            except V20Error as e:
                results['oanda_message'] = f'OANDA API error: {str(e)}'
            except Exception as e:
                results['oanda_message'] = f'Error: {str(e)}'
        else:
            results['oanda_message'] = 'API key or Account ID missing'

        # Test CryptoCompare
        if cryptocompare_key:
            try:
                import requests
                url = 'https://min-api.cryptocompare.com/data/price'
                params = {'fsym': 'BTC', 'tsyms': 'USD'}
                headers = {'authorization': f'Apikey {cryptocompare_key}'}

                response = requests.get(url, params=params, headers=headers, timeout=10)
                if response.status_code == 200 and 'USD' in response.json():
                    results['cryptocompare_status'] = True
                    results['cryptocompare_message'] = 'Connected successfully'
                else:
                    results['cryptocompare_message'] = f'API returned status {response.status_code}'
            except Exception as e:
                results['cryptocompare_message'] = f'Error: {str(e)}'
        else:
            results['cryptocompare_message'] = 'API key missing'

        return jsonify(results)

    except Exception as e:
        logger.error(f'Error testing API keys: {e}')
        return jsonify({'error': str(e)}), 500
