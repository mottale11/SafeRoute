# SafeRoute – Women's Safety Heatmap & Trusted Travel Community

SafeRoute is a Women's Safety Web App that provides a real-time heatmap of safe and unsafe areas based on crowdsourced reports. The platform displays user-submitted photos of suspects/offenders and photos of locations where incidents or risks have occurred, community safety tips, and emergency tools.

## Features

- **Real-time Safety Heatmap**: Interactive map showing risk zones based on community reports
- **Incident Reporting**: Submit detailed reports with photos, location, and severity levels
- **Image Gallery**: View suspect/offender photos and location photos (blurred by default)
- **Safety Tips**: Comprehensive guides for road safety, gender-based violence protection, digital scams, and night travel
- **User Dashboard**: Track your reports, saved zones, and area incidents
- **Community Features**: Mark reports as helpful, share incidents, and save risk zones

## Tech Stack

- **Backend**: Django, Python
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, Bootstrap 5
- **Maps**: Leaflet.js with Heatmap plugin
- **Styling**: Custom CSS with Belleza and Alegreya fonts

## Color Scheme

- **Primary Color**: Deep rose (#C72375)
- **Background Color**: Soft blush (#F4DDE8)
- **Accent Color**: Coral (#FF7F50)






## Project Structure

```
SR2/
├── saferoute/          # Main Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/           # User authentication app
│   ├── models.py      # CustomUser model
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── reports/            # Main reports app
│   ├── models.py      # IncidentReport, IncidentImage, etc.
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── templates/         # HTML templates
│   ├── base.html
│   ├── accounts/
│   └── reports/
├── static/            # Static files
│   └── css/
│       └── style.css
└── media/            # User-uploaded files
```

## Key Pages

1. **Landing Page** (`/`): Hero section, live safety snapshot, recent incidents, how it works
2. **Registration** (`/accounts/register/`): User signup with optional ID verification
3. **Login** (`/accounts/login/`): User authentication
4. **Dashboard** (`/dashboard/`): User home with quick actions and activity feed
5. **Submit Report** (`/submit/`): Incident reporting form with map and image uploads
6. **Heatmap** (`/heatmap/`): Interactive safety heatmap with filters
7. **Report Detail** (`/reports/<id>/`): Full incident details with image carousel
8. **Gallery** (`/gallery/`): Suspects and risk locations gallery
9. **Safety Tips** (`/safety-tips/`): Comprehensive safety guides
10. **Profile** (`/accounts/profile/`): User profile and settings

## Models

- **CustomUser**: Extended user model with verification status
- **IncidentReport**: Main incident report with location, category, severity
- **IncidentImage**: Images associated with reports (suspect, location, evidence)
- **IncidentVideo/Audio**: Additional evidence files
- **SavedZone**: User-saved risk zones
- **HelpfulReport**: Users marking reports as helpful

## Security Features

- User authentication and authorization
- Image blurring for privacy protection
- Content moderation and verification system
- Abuse reporting mechanism
- False reporting warnings

## Future Enhancements

- Panic button functionality
- Share trip tracking
- Community discussion forums
- Mobile app version
- Real-time notifications
- Integration with emergency services


