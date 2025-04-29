# Community Event Aggregator

[![Tests](https://github.com/USERNAME/community_event_aggregator/actions/workflows/test.yml/badge.svg)](https://github.com/USERNAME/community_event_aggregator/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/USERNAME/community_event_aggregator/branch/main/graph/badge.svg)](https://codecov.io/gh/USERNAME/community_event_aggregator)

A Python-based system that aggregates local community events from various online sources, filters them based on user preferences, and provides personalized notifications.

## Features

- Web scraping/API integration for event collection
- User preference management
- Event filtering and matching
- Email notification system
- High test coverage (97%)

## Event Sources

Currently supports:
1. Meetup.com API
2. Eventbrite API
3. Generic web scraping for community sites

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
```bash
# Event Source APIs
MEETUP_API_KEY=your_meetup_api_key_here
EVENTBRITE_API_KEY=your_eventbrite_api_key_here

# SMTP Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password
```

## Usage

```bash
python main.py
```

The system will:
1. Fetch events from configured sources
2. Filter them based on user preferences
3. Send notifications for matching events
4. Repeat the process hourly

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov coverage

# Run tests with coverage report
python -m pytest --cov=src --cov-report=term-missing

# Run tests with verbose output
python -m pytest -v
```

### Coverage Requirements

The project maintains high code quality standards:
- Overall coverage target: 90%
- New code coverage target: 95%
- Current coverage: 97%

### CI/CD Pipeline

The project uses GitHub Actions for continuous integration:
- Automated testing on Python 3.10, 3.11, and 3.12
- Code coverage reporting to Codecov
- Dependency caching for faster builds

To enable CI/CD:
1. Fork the repository
2. Go to repository Settings > Secrets and variables > Actions
3. Add the following secrets:
   - `CODECOV_TOKEN`: Your Codecov repository upload token
   - `MEETUP_API_KEY`: (Optional) Your Meetup API key
   - `EVENTBRITE_API_KEY`: (Optional) Your Eventbrite API key

## Project Structure

```
├── .github/
│   └── workflows/
│       └── test.yml      # CI/CD workflow
├── src/
│   ├── models/
│   │   ├── event.py
│   │   └── user_preferences.py
│   ├── services/
│   │   └── event_processor.py
│   └── sources/
│       ├── base.py
│       ├── web_scraper.py
│       ├── meetup.py
│       └── eventbrite.py
├── tests/
│   ├── test_models.py
│   ├── test_services.py
│   ├── test_sources.py
│   └── test_api_sources.py
├── .env.example
├── codecov.yml
├── main.py
├── requirements.txt
└── pytest.ini
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Ensure tests pass with coverage requirements (`pytest --cov=src`)
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.