# Kaffipunktar Project AI Agent Instructions

## Project Overview
Kaffipunktar is a Flask-based golf scoring and game management system with SQLite backend. The application manages users, games, scorecards, and team competitions.

## Architecture & Data Flow

### Core Components
- **Database Layer** (`db.py`): SQLite connection management and initialization
- **User Management** (`user.py`): User CRUD operations with handicap tracking
- **Game System** (`game.py`): Manages game sessions, teams, and game types
- **Scoring System** (`score_card.py`): Handles golf scorecards and scoring logic

### Database Schema
Key tables (`schema.sql`):
- `user`: Player profiles with handicaps
- `game`: Match records linked to teams
- `scorecard`: Individual hole scores
- `team`: Two-player team combinations
- `game_type`: Different game format configurations
- `course`: Golf course information

## Development Workflow

### Environment Setup
1. Initialize database:
```bash
flask init-db
```

2. Run development server:
```bash
export FLASK_APP=kaffipunktar
export FLASK_ENV=development
flask run
```

### API Patterns
- All routes return JSON responses
- Error responses use `{"error": "message"}` format with appropriate HTTP status codes
- Success responses use `{"message": "success message"}` with 201 for creation
- Routes follow RESTful conventions (GET for retrieval, POST for creation)

## Key Conventions

### Team Construction
Teams are constructed using the `team_constructor` function in `game.py`:
```python
{
    "name_one": str,
    "handicap_one": float,
    "name_two": str,
    "handicap_two": float,
    "regulation_point": int,
    "handicap_sum": float,
    "green_regulation": bool
}
```

### Score Card Format
Score cards use an 18-hole array format with integers representing strokes per hole. Unused holes are marked as 0.

## Integration Points
1. User Authentication: Currently uses basic password hashing (Werkzeug security)
2. Database Sessions: Uses Flask's `g` object for connection management
3. Team Handicap Calculation: Automated in team construction

## Common Workflows
1. Creating a new game:
   - Create users if not exists
   - Form teams
   - Initialize score cards
   - Create game record

2. Score Updates:
   - Validate hole scores
   - Update scorecard
   - Recalculate team standings