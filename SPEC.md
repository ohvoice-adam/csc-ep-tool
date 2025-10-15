# Product Specification: Election Protection Polling Place Monitoring Tool

## Overview

A Flask-based web application for monitoring and predicting potential issues at polling places during elections. The system collects voter and polling place data, applies machine learning to identify high-risk locations, and provides real-time monitoring capabilities with multiple data visualization options.

## System Architecture

### Technology Stack
- **Backend**: Python/Flask
- **Database**: Google BigQuery (primary data source)
- **ML Framework**: scikit-learn / TensorFlow
- **Frontend**: HTML5, CSS3, JavaScript (mobile-first)
- **Authentication**: Google OAuth 2.0 (SSO)
- **Maps**: Google Maps API or Mapbox
- **Deployment**: Google Cloud Run

### Architecture Components
1. Data Collection Layer
2. Data Processing & ML Layer
3. API Layer (VIP format)
4. Web Application Layer (Frontend)
5. Authentication Layer

---

## 1. Data Collection (Backend)

### 1.1 Polling Place Locations
**Objective**: Maintain up-to-date database of polling places with precinct assignments

**Data Points**:
- Polling place name
- Physical address
- Geographic coordinates (lat/long)
- Precinct(s) assigned
- County
- Operating hours
- Accessibility information

**Data Sources**:
- Secretary of State API/data feeds
- County boards of elections
- Manual updates/corrections

**Update Frequency**: Daily during election periods, weekly otherwise

### 1.2 Voter Assignment Data
**Objective**: Track voters assigned to each polling location

**Data Points**:
- Total registered voters per polling place
- Voters by precinct
- Demographic breakdowns (age, party affiliation if available)

**Data Source**: Catalist voter file (CTA PAD BigQuery)

### 1.3 Multi-State Registration Detection
**Objective**: Identify voters registered in multiple states

**Data Points**:
- Count of multi-state registered voters per polling place
- Individual voter flags (for internal use only)
- State combinations

**Data Source**: Catalist voter file (CTA PAD BigQuery)

**Privacy Note**: Aggregate counts only for display; individual data protected

### 1.4 Recent Registration Activity
**Objective**: Track new registrations and updates

**Data Points**:
- Count of new registrations (last 30/60/90 days)
- Count of registration updates (address changes, etc.)
- Date ranges for filtering

**Data Source**: Catalist voter file (CTA PAD BigQuery)

### 1.5 Voter Roll Purges
**Objective**: Track voters removed from rolls

**Data Points**:
- Count of voters removed (by time period)
- Reason codes (if available)
- Demographic patterns in removals

**Data Sources**:
- Catalist voter file (CTA PAD BigQuery)
- Secretary of State
- County boards of elections

### 1.6 Real-Time User Reports
**Objective**: Collect in-the-moment problem reports

**Data Points**:
- Reporter name and contact
- Polling place
- Issue type (long lines, equipment failure, accessibility, staffing, etc.)
- Timestamp
- Description
- Photos (optional)
- Status (reported, investigating, resolved)

**Collection Method**: Web form submission

---

## 2. Data Modeling (Backend)

### 2.1 Machine Learning Model
**Objective**: Predict likelihood of issues at each polling place

**Model Type**: Binary classification or regression (risk score 0-100)

**Features**:
- Voter count assigned to location
- Multi-state registration rate
- Recent registration activity rate
- Voter roll purge rate
- Historical issue data (from past elections)
- Accessibility scores
- Equipment age/type (if available)
- Geographic factors
- Demographic factors

**Training Data**: Historical incident reports from previous elections

**Output**: Risk score (0-100) per polling place

**Model Refresh**: Retrained after each election; updated with real-time data during election day

### 2.2 Anomaly Detection
**Objective**: Flag unusual patterns in real-time

**Approach**: Statistical anomaly detection for:
- Sudden spikes in user reports
- Unusual voting patterns
- Equipment failures

---

## 3. Internal API

### 3.1 VIP Format Compliance
**Standard**: Voting Information Project Specification v6.0
**Reference**: https://github.com/votinginfoproject/vip-specification/tree/v6.0-release

**Core Objects to Implement**:
- Election
- PollingLocation
- Precinct
- LocalityReport

**Endpoints**:
- `GET /api/v1/vip/election/{election_id}` - Election data
- `GET /api/v1/vip/polling-locations` - All polling locations
- `GET /api/v1/vip/polling-location/{id}` - Single location detail
- `GET /api/v1/vip/precincts` - Precinct data

### 3.2 Custom API Endpoints
**Base URL**: `/api/v1/`

**Endpoints**:
- `GET /polling-places` - List all with filters
  - Query params: county, risk_score_min, risk_score_max, sort_by
- `GET /polling-places/{id}` - Single polling place detail
- `GET /polling-places/{id}/reports` - User reports for location
- `POST /reports` - Submit new user report
- `GET /reports` - List all reports (with filters)
- `PATCH /reports/{id}` - Update report status
- `GET /analytics/summary` - Aggregate statistics
- `GET /analytics/high-risk` - Top N high-risk locations

**Authentication**: Bearer token (from Google OAuth)

**Response Format**: JSON

---

## 4. Frontend

### 4.1 General Requirements
- **Responsive Design**: Mobile-first approach
- **Accessibility**: WCAG 2.1 AA compliance minimum
  - Color contrast ratios (4.5:1 for text)
  - Screen reader compatible
  - Keyboard navigation
  - ARIA labels
  - Alt text for images
  - Focus indicators
- **Performance**: Page load < 3 seconds on 3G
- **Browser Support**: Modern browsers (Chrome, Firefox, Safari, Edge)

### 4.2 Authentication
- **Google SSO**: Required for all access
- **No Public Access**: All pages require authentication
- **Role Management** (future): Admin, Analyst, Read-only

### 4.3 Views

#### 4.3.1 Dashboard/Home View
**Purpose**: Overview of statewide or county-wide status

**Components**:
- Summary statistics cards
  - Total polling places
  - High-risk locations count
  - Active reports count
- Quick filters (county selector)
- Link to main views

#### 4.3.2 Polling Place List View
**Purpose**: Searchable, filterable, sortable list

**Features**:
- **Filters**:
  - County (multi-select)
  - Risk score range (slider)
  - Voter count range
  - Multi-state registration count
  - Recent registration count
  - Purge count
  - Active reports (yes/no)

- **Sort Options**:
  - Risk score (high to low)
  - Voter count
  - Multi-state registrations
  - Recent registrations
  - Purges
  - Alphabetical (name)
  - County

- **Display Columns**:
  - Polling place name
  - Address
  - County
  - Risk score (color-coded)
  - Assigned voters
  - Active report count
  - Actions (view details)

- **Export**: CSV download of filtered results

#### 4.3.3 High-Risk Locations View
**Purpose**: Focus on most likely problem areas

**Features**:
- Top 50 (or configurable N) highest-risk locations
- Same display as list view
- Expandable rows showing:
  - Voter counts by category
  - Contributing risk factors
  - Historical issues (if any)

#### 4.3.4 Map Views

##### Risk Map
**Purpose**: Geographic visualization of predicted issues

**Features**:
- Markers for each polling place, color-coded by risk:
  - Green (0-33): Low risk
  - Yellow (34-66): Medium risk
  - Red (67-100): High risk
- Marker size proportional to voter count
- Click marker for popup with:
  - Polling place name
  - Risk score
  - Key statistics
  - "View Details" link
- County boundaries overlay (toggle)
- Heat map option (toggle)
- Filters (same as list view)

##### Live Issues Map
**Purpose**: Real-time problem reporting

**Features**:
- Markers for polling places with active reports
- Color-coded by severity/issue type
- Pulsing animation for new reports (< 15 min old)
- Click marker for popup with:
  - Polling place name
  - Report count
  - Most recent report summary
  - "View All Reports" link
- Auto-refresh (30 seconds)

#### 4.3.5 Polling Place Detail Page
**Purpose**: Comprehensive view of single location

**URL**: `/polling-place/{id}`

**Sections**:

1. **Header**
   - Polling place name
   - Risk score (large, prominent, color-coded)
   - Address with map link
   - Operating hours

2. **Statistics Panel**
   - Total registered voters
   - Multi-state registrations
   - Recent registrations (30/60/90 day counts)
   - Recent purges
   - Historical issue count

3. **Risk Factors**
   - List of contributing factors to risk score
   - Visual indicators (progress bars or icons)

4. **User Reports Section**
   - List of all reports (most recent first)
   - Each report shows:
     - Timestamp
     - Reporter name
     - Issue type
     - Description
     - Status badge
     - Photos (if attached)
   - Admin actions: Update status

5. **Submit Report Form**
   - Issue type dropdown
   - Description textarea
   - Photo upload
   - Submit button

6. **Map**
   - Location marker
   - Nearby polling places

#### 4.3.6 Report Submission Form (Standalone)
**Purpose**: Quick report submission (mobile optimized)

**URL**: `/report` or `/report?polling_place_id={id}`

**Fields**:
- Polling place selector (autocomplete) or pre-filled
- Your name (auto-filled from Google profile)
- Contact info (email/phone)
- Issue type (dropdown):
  - Long lines/wait times
  - Equipment failure (voting machines)
  - Equipment failure (check-in)
  - Accessibility issue
  - Staffing problem
  - Voter intimidation
  - ID requirements issue
  - Other
- Description (required)
- Photo upload (optional, multiple)
- Submit button

**Confirmation**: Success message with report ID

---

## 5. Data Privacy & Security

### 5.1 Privacy Considerations
- Individual voter data never displayed publicly
- Aggregate counts only in UI
- User reports contain only reporter info (who submitted), not voter info
- BigQuery access restricted to service accounts
- Audit logging for data access

### 5.2 Security Requirements
- HTTPS only
- OAuth 2.0 for authentication
- JWT for API authorization
- Rate limiting on API endpoints
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- CSRF tokens for forms

---

## 6. Database Schema

### 6.1 PostgreSQL Tables (Application Database)

#### polling_places
- id (PK)
- name
- address
- city
- county
- state
- zip_code
- latitude
- longitude
- precincts (array or JSON)
- operating_hours
- accessibility_notes
- created_at
- updated_at

#### polling_place_metrics
- id (PK)
- polling_place_id (FK)
- date
- total_voters
- multi_state_count
- recent_registration_count_30d
- recent_registration_count_60d
- recent_registration_count_90d
- purge_count_30d
- purge_count_60d
- purge_count_90d
- risk_score
- risk_factors (JSON)
- created_at

#### user_reports
- id (PK)
- polling_place_id (FK)
- reporter_name
- reporter_email
- reporter_phone
- issue_type
- description
- photos (array of URLs)
- status (reported, investigating, resolved)
- reported_at
- updated_at
- resolved_at

#### users (for session management)
- id (PK)
- google_id
- email
- name
- role (admin, analyst, viewer)
- last_login
- created_at

### 6.2 BigQuery Queries
- Queries to Catalist voter file for aggregations
- Scheduled queries to refresh polling_place_metrics daily

---

## 7. Implementation Phases

### Phase 1: Core Infrastructure (Weeks 1-2)
- Flask application structure
- Google OAuth integration
- Database setup
- BigQuery connection
- Basic API endpoints

### Phase 2: Data Collection (Weeks 3-4)
- Data ingestion pipelines
- Secretary of State connectors
- BigQuery query implementations
- Polling place data management

### Phase 3: ML Model (Weeks 5-6)
- Feature engineering
- Model training pipeline
- Risk score calculation
- Model deployment

### Phase 4: Frontend - Core Views (Weeks 7-9)
- Responsive UI framework
- Dashboard
- Polling place list view
- Detail pages
- Accessibility compliance

### Phase 5: Frontend - Maps & Reports (Weeks 10-11)
- Map integrations
- Risk map
- Live issues map
- Report submission forms

### Phase 6: VIP API (Week 12)
- VIP format implementation
- API documentation
- Testing

### Phase 7: Testing & Launch (Weeks 13-14)
- End-to-end testing
- Performance optimization
- Security audit
- Deployment to Cloud Run
- User acceptance testing

---

## 8. Success Metrics

- **System Uptime**: 99.9% during election day
- **API Response Time**: < 500ms for 95th percentile
- **Page Load Time**: < 3s on 3G
- **Accessibility Score**: 100 on Lighthouse
- **User Adoption**: Track daily active users
- **Report Response Time**: Median time from report to resolution
- **Prediction Accuracy**: % of high-risk locations with actual issues

---

## 9. Future Enhancements

- SMS/email alerts for high-priority issues
- Mobile native app (iOS/Android)
- Integration with voter protection hotlines
- Historical trending analysis
- Public-facing (anonymized) dashboard
- Multi-language support
- Volunteer coordination features
- Resource allocation recommendations
