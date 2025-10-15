# Work Division for 8-Hour Prototype

This guide divides the prototype work among 3 developers for efficient parallel development.

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
python app.py
```

3. Access at: http://localhost:8080
   - Login: admin / demo

## Developer 1: Backend & Data (8 hours)

### ✅ Already Complete (Framework provided)
- Flask app structure (`app.py`)
- Mock data files (`data/polling_places.json`, `data/reports.json`)
- All routes and API endpoints
- Authentication (mock)
- Data loading functions

### Your Tasks

#### Hours 1-2: Setup & Testing
- [ ] Review `app.py` and understand all routes
- [ ] Test all routes work correctly:
  - `/login` - Login page
  - `/polling-places` - List view
  - `/polling-places/<id>` - Detail view
  - `/map` - Map view
  - `/report` - Report form
  - `/api/polling-places` - JSON API
- [ ] Add any missing error handling

#### Hours 3-4: Data Enhancements
- [ ] Add risk score calculation function (see PROTOTYPE_PLAN.md)
- [ ] Implement it to recalculate risk scores on data load
- [ ] Add more mock data if needed (currently 20 polling places, 8 reports)
- [ ] Add data validation for form submissions

#### Hours 5-6: Filtering & Sorting
- [ ] Test all filter combinations work correctly
- [ ] Optimize sorting performance if needed
- [ ] Add additional filter options if time permits:
  - Filter by "has reports"
  - Filter by voters count range
- [ ] Add pagination if list gets long

#### Hours 7-8: Integration & Testing
- [ ] Work with Dev 2 & 3 to integrate frontend components
- [ ] Fix any backend bugs discovered during testing
- [ ] Add any missing API endpoints for map features
- [ ] Write basic documentation for API endpoints
- [ ] Test mobile experience

### Files You'll Work With
- `app.py` - Main application
- `data/*.json` - Mock data
- `requirements.txt` - Dependencies (if needed)

---

## Developer 2: Frontend Templates (8 hours)

### ✅ Already Complete (Framework provided)
- Base template with Bootstrap 5 (`templates/base.html`)
- Login page (`templates/login.html`)
- Polling places list (`templates/polling_places_list.html`)
- Detail page (`templates/polling_place_detail.html`)
- Map page (`templates/map.html`)
- Report form (`templates/report_form.html`)

### Your Tasks

#### Hours 1-2: Review & Enhance Templates
- [ ] Review all templates and understand structure
- [ ] Test all pages render correctly
- [ ] Improve form UX:
  - Add client-side validation
  - Add loading states for form submissions
  - Improve error messages display
- [ ] Add helpful hints/tooltips where needed

#### Hours 3-4: List View Enhancements
- [ ] Improve the filters UI:
  - Make filters collapsible on mobile
  - Add "Apply" button loading state
  - Show active filter count
- [ ] Enhance table display:
  - Add row highlighting on hover
  - Make table more mobile-friendly (card view option?)
  - Add quick action buttons
- [ ] Add export functionality (CSV button - coordinate with Dev 1)

#### Hours 5-6: Detail Page Improvements
- [ ] Improve statistics display:
  - Add visual progress bars or charts
  - Color-code values (high/medium/low)
  - Add tooltips explaining each metric
- [ ] Enhance reports section:
  - Add filter/sort for reports
  - Add status update buttons (if time)
  - Improve timestamp display (relative time)
- [ ] Polish the mini map display

#### Hours 7-8: Forms & Polish
- [ ] Enhance report submission form:
  - Add auto-complete for polling place search
  - Add field validation with helpful messages
  - Add confirmation dialog before submit
  - Style success/error states
- [ ] Add breadcrumbs to all pages
- [ ] Improve flash messages styling
- [ ] Test all forms on mobile
- [ ] Add keyboard navigation improvements
- [ ] Final polish and bug fixes

### Files You'll Work With
- `templates/*.html` - All templates
- `static/css/style.css` - Styling (coordinate with Dev 3)

---

## Developer 3: Maps, Styling & Mobile (8 hours)

### ✅ Already Complete (Framework provided)
- Map page template with Leaflet.js integration
- Basic CSS styling (`static/css/style.css`)
- Risk color coding
- Responsive breakpoints

### Your Tasks

#### Hours 1-2: Map Setup & Testing
- [ ] Review map implementation in `templates/map.html`
- [ ] Test map loads correctly with all markers
- [ ] Verify marker colors match risk levels
- [ ] Test marker popups work correctly
- [ ] Ensure map is responsive on mobile

#### Hours 3-4: Map Enhancements
- [ ] Improve marker clustering for dense areas (use Leaflet.markercluster plugin)
- [ ] Add map controls:
  - Risk level filter toggles
  - County filter (show/hide by county)
  - "Show only locations with reports" toggle
- [ ] Enhance popup design:
  - Better styling
  - Show more information
  - Improve button visibility
- [ ] Add loading state while fetching data
- [ ] Test on mobile (touch interactions)

#### Hours 5-6: Styling & Mobile Optimization
- [ ] Enhance overall color scheme and branding
- [ ] Improve mobile navigation:
  - Hamburger menu works smoothly
  - Touch targets are large enough (min 44x44px)
  - Navigation is thumb-friendly
- [ ] Optimize table display on mobile:
  - Consider card layout as alternative
  - Horizontal scrolling if needed
- [ ] Test all pages on various screen sizes:
  - Mobile (320px, 375px, 414px)
  - Tablet (768px, 1024px)
  - Desktop (1280px+)
- [ ] Add touch-friendly interactions

#### Hours 7-8: Accessibility & Final Polish
- [ ] Accessibility audit:
  - Check color contrast ratios (use browser tools)
  - Ensure all interactive elements are keyboard accessible
  - Add proper ARIA labels where missing
  - Test with screen reader (if possible)
  - Add skip navigation link
- [ ] Add focus indicators that are visible
- [ ] Improve link and button styling for clarity
- [ ] Test with keyboard only (no mouse)
- [ ] Add CSS animations/transitions for better UX
- [ ] Final cross-browser testing
- [ ] Document any accessibility features

### Files You'll Work With
- `templates/map.html` - Map page
- `static/css/style.css` - Main stylesheet
- `static/js/` - Any JavaScript files you create
- All templates (for styling consistency)

---

## Coordination Points

### Dev 1 ↔ Dev 2
- **API Endpoints**: Dev 2 needs to know what data is available from Dev 1's API
- **Form Submissions**: Coordinate on validation (client vs server)
- **Error Handling**: Ensure error messages are user-friendly

### Dev 1 ↔ Dev 3
- **Map Data API**: Dev 3 fetches from `/api/polling-places` endpoint
- **Performance**: If map is slow with many markers, discuss optimization
- **Real-time Updates**: If adding live updates, coordinate on API

### Dev 2 ↔ Dev 3
- **Styling Consistency**: Use same CSS variables and classes
- **Responsive Design**: Coordinate on breakpoints and mobile layout
- **Accessibility**: Share ARIA labels and keyboard navigation patterns

## Testing Checklist (All Devs)

At the end of 8 hours, verify:

- [ ] Login works (admin/demo)
- [ ] Can view polling places list
- [ ] Can filter by county and risk score
- [ ] Can sort by different columns
- [ ] Can view polling place detail page
- [ ] Can see reports on detail page
- [ ] Map loads with all markers
- [ ] Markers are color-coded correctly
- [ ] Clicking marker shows popup
- [ ] Can submit a new report
- [ ] Report appears on detail page
- [ ] All pages work on mobile
- [ ] No console errors
- [ ] Acceptable color contrast
- [ ] Can navigate with keyboard

## Demo Preparation

**Practice demonstrating:**
1. Login flow
2. Browse polling places with filters
3. Click high-risk location
4. View details and existing reports
5. Submit a new report
6. View location on map
7. Use map to find locations by risk level
8. Show mobile responsiveness

## Common Issues & Solutions

### Map not loading
- Check console for errors
- Verify `/api/polling-places` returns data
- Check Leaflet.js loaded correctly

### Styles not applying
- Clear browser cache
- Check CSS file path in template
- Verify static files are being served

### Forms not submitting
- Check CSRF token if added
- Verify form action URL
- Check for JavaScript errors

### Mobile issues
- Test on real device if possible
- Use Chrome DevTools device emulation
- Check viewport meta tag is present

## Time-Saving Tips

1. **Don't reinvent**: Use Bootstrap components when possible
2. **Test frequently**: Don't wait until the end
3. **Ask for help**: Communicate with other devs
4. **Focus on core**: Polish is secondary to functionality
5. **Use examples**: Reference Bootstrap documentation
6. **Mobile first**: Test mobile early, not at the end

## Success Criteria

After 8 hours, the prototype should:
- ✅ Run without errors
- ✅ Demonstrate core concept clearly
- ✅ Show all key features working
- ✅ Be mobile-responsive
- ✅ Have basic accessibility features
- ✅ Look professional (not polished, but clean)
- ✅ Use real-looking mock data

Good luck! 🚀
