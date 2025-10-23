from flask import Blueprint, send_file, jsonify
import os
import zipfile
import tempfile
import shutil
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)
export_bp = Blueprint('export', __name__)


def create_zip_archive(files_dict, zip_name):
    """
    Create a zip archive from a dictionary of files

    Args:
        files_dict: Dictionary with {archive_path: file_path}
        zip_name: Name of the zip file

    Returns:
        Path to created zip file
    """
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, zip_name)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for archive_path, file_path in files_dict.items():
            if os.path.exists(file_path):
                if os.path.isdir(file_path):
                    for root, dirs, files in os.walk(file_path):
                        for file in files:
                            file_full_path = os.path.join(root, file)
                            arcname = os.path.join(archive_path, os.path.relpath(file_full_path, file_path))
                            zipf.write(file_full_path, arcname)
                else:
                    zipf.write(file_path, archive_path)

    return zip_path


@export_bp.route('/models', methods=['GET'])
def download_models():
    """Download all trained models as a zip file"""
    try:
        models_dir = os.path.join(os.path.dirname(__file__), '../../models')

        if not os.path.exists(models_dir) or not os.listdir(models_dir):
            return jsonify({'error': 'No trained models found'}), 404

        files_dict = {}
        for filename in os.listdir(models_dir):
            file_path = os.path.join(models_dir, filename)
            files_dict[f'models/{filename}'] = file_path

        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        zip_path = create_zip_archive(files_dict, f'horus_models_{timestamp}.zip')

        return send_file(
            zip_path,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'horus_models_{timestamp}.zip'
        )

    except Exception as e:
        logger.error(f'Error creating models archive: {e}')
        return jsonify({'error': str(e)}), 500


@export_bp.route('/backend-full', methods=['GET'])
def download_backend_full():
    """Download complete backend package including code, models, and configs"""
    try:
        backend_dir = os.path.join(os.path.dirname(__file__), '../..')

        files_dict = {}

        # Include Python source files
        for root, dirs, files in os.walk(backend_dir):
            # Skip __pycache__ and .git directories
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'venv', 'node_modules', '.pytest_cache']]

            for file in files:
                if file.endswith(('.py', '.txt', '.md', '.json', '.env.example', '.sh', '.bat')):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, backend_dir)
                    files_dict[f'backend/{relative_path}'] = file_path

        # Include models if they exist
        models_dir = os.path.join(backend_dir, 'models')
        if os.path.exists(models_dir):
            files_dict['backend/models'] = models_dir

        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        zip_path = create_zip_archive(files_dict, f'horus_backend_full_{timestamp}.zip')

        return send_file(
            zip_path,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'horus_backend_full_{timestamp}.zip'
        )

    except Exception as e:
        logger.error(f'Error creating full backend archive: {e}')
        return jsonify({'error': str(e)}), 500


@export_bp.route('/config', methods=['GET'])
def download_config():
    """Download configuration files as a zip"""
    try:
        backend_dir = os.path.join(os.path.dirname(__file__), '../..')

        files_dict = {}

        config_files = [
            '.env.example',
            'requirements.txt',
            'README.md',
            'start.sh',
            'start.bat'
        ]

        for filename in config_files:
            file_path = os.path.join(backend_dir, filename)
            if os.path.exists(file_path):
                files_dict[f'config/{filename}'] = file_path

        # Create a setup guide
        setup_guide = """# HORUS Backend Setup Guide

## Prerequisites
- Python 3.8+
- pip package manager

## Installation Steps

1. Extract this archive to your desired location
2. Navigate to the backend directory:
   ```
   cd backend
   ```

3. Create a virtual environment:
   ```
   python3 -m venv venv
   ```

4. Activate the virtual environment:
   - macOS/Linux: `source venv/bin/activate`
   - Windows: `venv\\Scripts\\activate`

5. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

6. Copy .env.example to .env:
   ```
   cp .env.example .env
   ```

7. Edit .env and add your API keys:
   - OANDA_API_KEY: Get from https://www.oanda.com
   - CRYPTOCOMPARE_API_KEY: Get from https://www.cryptocompare.com

8. Start the backend server:
   ```
   python app.py
   ```

The backend will be available at http://127.0.0.1:5000

## API Endpoints

### Market Data
- GET /api/market/history/<symbol> - Get historical OHLCV data
- GET /api/market/price/<symbol> - Get current price

### Signals & Predictions
- GET /api/signals/patterns/<symbol> - Detect chart patterns
- GET /api/signals/push-analysis/<symbol> - Trading Anarchy 4-push analysis
- POST /api/signals/advanced-prediction/<symbol> - AI diffusion predictions
- GET /api/signals/comprehensive-analysis/<symbol> - Full market analysis

### Training
- POST /api/training/start - Start automatic training
- POST /api/training/stop - Stop automatic training
- GET /api/training/status - Get training status
- POST /api/training/train/<symbol> - Train specific symbol

### Export
- GET /api/export/models - Download trained models
- GET /api/export/backend-full - Download complete backend
- GET /api/export/config - Download configuration files

## Features

- AI Diffusion Model for time series forecasting
- Virtual Economy Simulation with 100+ trader agents
- Pattern Recognition for 18+ trading patterns
- Trading Anarchy 4-push detection system
- Automatic model training with fresh market data
- OANDA and CryptoCompare API integration

## Support

For issues or questions, please refer to the main project README.
"""

        temp_guide_path = os.path.join(tempfile.gettempdir(), 'SETUP_GUIDE.md')
        with open(temp_guide_path, 'w') as f:
            f.write(setup_guide)

        files_dict['config/SETUP_GUIDE.md'] = temp_guide_path

        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        zip_path = create_zip_archive(files_dict, f'horus_config_{timestamp}.zip')

        os.remove(temp_guide_path)

        return send_file(
            zip_path,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'horus_config_{timestamp}.zip'
        )

    except Exception as e:
        logger.error(f'Error creating config archive: {e}')
        return jsonify({'error': str(e)}), 500


@export_bp.route('/data-backup', methods=['GET'])
def download_data_backup():
    """Download training data and metadata backup"""
    try:
        backend_dir = os.path.join(os.path.dirname(__file__), '../..')
        models_dir = os.path.join(backend_dir, 'models')

        files_dict = {}

        # Include all model metadata
        if os.path.exists(models_dir):
            for filename in os.listdir(models_dir):
                if filename.endswith('.json') or filename.endswith('.pt'):
                    file_path = os.path.join(models_dir, filename)
                    files_dict[f'backup/{filename}'] = file_path

        # Create backup manifest
        manifest = {
            'backup_date': datetime.utcnow().isoformat(),
            'backend_version': '1.0.0',
            'files': list(files_dict.keys()),
            'description': 'HORUS AI Trading Platform - Training Data Backup'
        }

        temp_manifest_path = os.path.join(tempfile.gettempdir(), 'backup_manifest.json')
        with open(temp_manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        files_dict['backup/manifest.json'] = temp_manifest_path

        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        zip_path = create_zip_archive(files_dict, f'horus_backup_{timestamp}.zip')

        os.remove(temp_manifest_path)

        return send_file(
            zip_path,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'horus_backup_{timestamp}.zip'
        )

    except Exception as e:
        logger.error(f'Error creating data backup: {e}')
        return jsonify({'error': str(e)}), 500


@export_bp.route('/package-info', methods=['GET'])
def get_package_info():
    """Get information about available export packages"""
    try:
        backend_dir = os.path.join(os.path.dirname(__file__), '../..')
        models_dir = os.path.join(backend_dir, 'models')

        info = {
            'models': {
                'available': os.path.exists(models_dir) and len(os.listdir(models_dir)) > 0,
                'count': len(os.listdir(models_dir)) if os.path.exists(models_dir) else 0,
                'size_mb': 0
            },
            'backend': {
                'available': True,
                'description': 'Complete backend package with all source code'
            },
            'config': {
                'available': True,
                'description': 'Configuration files and setup guide'
            },
            'backup': {
                'available': os.path.exists(models_dir) and len(os.listdir(models_dir)) > 0,
                'description': 'Training data and metadata backup'
            }
        }

        # Calculate models directory size
        if os.path.exists(models_dir):
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(models_dir):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    total_size += os.path.getsize(filepath)
            info['models']['size_mb'] = round(total_size / (1024 * 1024), 2)

        return jsonify(info)

    except Exception as e:
        logger.error(f'Error getting package info: {e}')
        return jsonify({'error': str(e)}), 500
