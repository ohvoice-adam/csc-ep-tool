# 8-Hour Prototype Plan (3 Developers = 24 person-hours)

## Prototype Scope

**Goal**: Demonstrate core concept with minimal viable features using mock data.

**What's IN the prototype**:
- ✅ Flask web app with basic routing
- ✅ Mock authentication (simple login form, no real OAuth)
- ✅ Sample polling place data (1000 locations across Virginia)
- ✅ Simple risk score calculation (formula-based, no ML)
- ✅ Polling place list view (filterable, sortable)
- ✅ Polling place detail page
- ✅ Basic map view with markers
- ✅ User report submission form
- ✅ Mobile-responsive UI (Bootstrap)
- ✅ Basic accessibility features

**What's OUT of the prototype**:
- ❌ Real Google OAuth
- ❌ BigQuery integration
- ❌ Machine learning model
- ❌ Real data sources
- ❌ VIP API format
- ❌ Advanced filtering
- ❌ Photo uploads
- ❌ Database (use JSON files)

## Time Allocation (Per Developer)

| Developer | Hours | Focus Area |
|-----------|-------|------------|
| Dev 1 | 8h | Backend: Flask routes, data layer, risk calculation |
| Dev 2 | 8h | Frontend: Templates, list view, detail view, forms |
| Dev 3 | 8h | Frontend: Map integration, styling, mobile responsive |

## Work Breakdown

### Dev 1: Backend (8 hours)
**Hours 1-2**: Setup & Data Layer
- Set up Flask app structure
- Create mock data JSON files
- Create data loading utilities
- Simple in-memory data store

**Hours 3-4**: Core Routes & Logic
- Authentication (mock login/logout)
- Polling place list endpoint
- Polling place detail endpoint
- Risk score calculation function

**Hours 5-6**: Reports & Filtering
- Report submission endpoint
- List filtering logic
- Sorting logic
- JSON API endpoints for frontend

**Hours 7-8**: Integration & Testing
- Test all routes
- Help integrate with frontend
- Bug fixes

### Dev 2: Frontend Templates (8 hours)
**Hours 1-2**: Base Templates
- Base layout with navigation
- Login page
- Bootstrap integration
- Basic styling

**Hours 3-4**: List View
- Polling place list template
- Filter UI (county, risk score)
- Sort controls
- Table/card layout

**Hours 5-6**: Detail View
- Polling place detail template
- Statistics display
- Report list display
- Submit report form

**Hours 7-8**: Forms & Polish
- Report submission form
- Form validation
- Error messages
- Responsive tweaks

### Dev 3: Map & Styling (8 hours)
**Hours 1-2**: Map Setup
- Choose map library (Leaflet.js - free)
- Set up map container
- Load polling places as markers
- Basic marker styling

**Hours 3-4**: Map Interactivity
- Color-code markers by risk
- Marker popups with data
- Link to detail page
- Map filters

**Hours 5-6**: Mobile Responsive
- Test on mobile viewports
- Adjust layouts
- Touch-friendly controls
- Navigation improvements

**Hours 7-8**: Styling & Accessibility
- Color scheme
- WCAG contrast compliance
- ARIA labels
- Keyboard navigation
- Final polish

## Technical Stack (Simplified)

- **Backend**: Flask (no database, JSON files)
- **Frontend**: Jinja2 templates, Bootstrap 5
- **Maps**: Leaflet.js (open source, no API key needed)
- **Data Storage**: JSON files in `/data` directory
- **No Build Process**: Plain CSS/JS (no webpack/npm)

## Mock Data Structure

### polling_places.json
```json
[
  {
    "id": "pp-001",
    "name": "Lincoln Elementary School",
    "address": "123 Main St",
    "city": "Richmond",
    "county": "Richmond City",
    "state": "VA",
    "zip": "23219",
    "latitude": 37.5407,
    "longitude": -77.4360,
    "total_voters": 1200,
    "multi_state_registrations": 45,
    "recent_registrations": 89,
    "purged_voters": 12,
    "risk_score": 72
  }
]
```

### reports.json
```json
[
  {
    "id": "rpt-001",
    "polling_place_id": "pp-001",
    "reporter_name": "John Doe",
    "reporter_email": "john@example.com",
    "issue_type": "Long lines",
    "description": "Wait time over 2 hours",
    "timestamp": "2024-11-05T08:30:00Z",
    "status": "reported"
  }
]
```

## Risk Score Formula (Simple)

```python
def calculate_risk_score(polling_place):
    score = 0

    # High voter count = higher risk
    if polling_place['total_voters'] > 1500:
        score += 30
    elif polling_place['total_voters'] > 1000:
        score += 20
    elif polling_place['total_voters'] > 500:
        score += 10

    # Multi-state registrations
    multi_state_rate = polling_place['multi_state_registrations'] / polling_place['total_voters']
    score += min(multi_state_rate * 100, 30)

    # Recent registrations
    recent_rate = polling_place['recent_registrations'] / polling_place['total_voters']
    score += min(recent_rate * 50, 20)

    # Purged voters
    purge_rate = polling_place['purged_voters'] / polling_place['total_voters']
    score += min(purge_rate * 100, 20)

    return min(score, 100)
```

## Key Features by Priority

### P0 (Must Have)
1. Login page (mock)
2. Polling place list
3. Basic filtering (county, risk level)
4. Sorting (by risk, name, county)
5. Polling place detail page
6. Report submission form
7. Map with markers

### P1 (Should Have)
8. Color-coded risk levels
9. Mobile responsive
10. Basic accessibility (contrast, labels)

### P2 (Nice to Have)
11. Map popups
12. Report status display
13. Summary statistics

## Routes

```
GET  /                          -> Redirect to /login or /polling-places
GET  /login                     -> Login page
POST /login                     -> Process login
GET  /logout                    -> Logout
GET  /polling-places            -> List view
GET  /polling-places/<id>       -> Detail view
GET  /map                       -> Map view
GET  /report                    -> Report form (standalone)
POST /report                    -> Submit report
GET  /api/polling-places        -> JSON API (for map)
```

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
python app.py
```

3. Access at: http://localhost:8080

4. Login credentials (mock):
   - Username: `admin`
   - Password: `demo`

## Deliverables

1. ✅ Working Flask application
2. ✅ 1000 mock polling places across Virginia
3. ✅ 75 mock reports
4. ✅ List view with filters/sort
5. ✅ Detail page with reports
6. ✅ Interactive map
7. ✅ Report submission form
8. ✅ Mobile-responsive UI
9. ✅ Basic documentation

## Success Criteria

- App runs without errors
- All main pages render correctly
- Filters and sorting work
- Map displays all locations
- Forms can be submitted
- Mobile usable (tested on phone)
- Demonstrates core concept clearly
