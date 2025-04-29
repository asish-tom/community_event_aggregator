# Community Event Aggregator

[![Tests](../../actions/workflows/test.yml/badge.svg)](../../actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/USERNAME/community_event_aggregator/branch/main/graph/badge.svg?token=YOUR_TOKEN)](https://codecov.io/gh/USERNAME/community_event_aggregator)

A Python-based system that aggregates local community events from various online sources, filters them based on user preferences, and provides personalized notifications.

## Features

- Web scraping/API integration for event collection
- User preference management
- Event filtering and matching
- Email notification system
- High test coverage (98%)

## Installation

```bash
# Clone the repository
git clone https://github.com/USERNAME/community_event_aggregator.git
cd community_event_aggregator

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` with your settings:
- SMTP configuration for email notifications
- Event source URLs
- API keys (if needed)

## Usage

```bash
python main.py
```

The system will:
1. Fetch events from configured sources
2. Filter them based on user preferences
3. Send notifications for matching events
4. Repeat the process hourly

## Testing

The project uses pytest for testing and includes comprehensive test coverage. Tests run automatically on GitHub Actions for Python 3.10, 3.11, and 3.12.

### Running Tests Locally

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests with coverage report
python -m pytest --cov=src --cov-report=term-missing

# Run tests with verbose output
python -m pytest -v
```

### Continuous Integration

Tests run automatically on:
- Every push to main branch
- Every pull request to main branch

The workflow:
1. Sets up Python environment
2. Installs dependencies
3. Runs tests with coverage
4. Uploads coverage report to Codecov

### Setting up Codecov

1. Sign up for [Codecov](https://codecov.io) and add your repository
2. Get your Codecov token from repository settings
3. Add the token to your GitHub repository:
   - Go to Settings > Secrets and variables > Actions
   - Add new secret named `CODECOV_TOKEN`
   - Paste your Codecov token as the value

4. Update the Codecov badge in this README:
   - Replace `USERNAME` with your GitHub username
   - Replace `YOUR_TOKEN` with your Codecov repository upload token

## Project Structure

```
├── .github/
│   └── workflows/
│       └── test.yml      # GitHub Actions workflow
├── src/
│   ├── models/
│   │   ├── event.py
│   │   └── user_preferences.py
│   ├── services/
│   │   └── event_processor.py
│   └── sources/
│       ├── base.py
│       └── web_scraper.py
├── tests/
│   ├── test_models.py
│   ├── test_services.py
│   └── test_sources.py
├── .env.example
├── main.py
├── requirements.txt
└── pytest.ini
```

## Coverage Report

```
Name                              Stmts   Miss  Cover
-------------------------------------------------------
src/models/event.py                  20      0   100%
src/models/user_preferences.py       21      1    95%
src/services/event_processor.py      50      0   100%
src/sources/base.py                  20      1    95%
src/sources/web_scraper.py           54      1    98%
-------------------------------------------------------
TOTAL                               165      3    98%