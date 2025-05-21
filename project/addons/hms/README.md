# Hospital Management System (HMS)

A comprehensive Odoo module for managing hospital operations, patient records, and medical staff.

## 🏥 Features

### Patient Management
- Complete patient registration and profiling
- Medical history tracking
- Blood type and PCR test results management
- Department assignment and transfer capabilities
- Doctor assignment with many-to-many relationship
- Patient log history with automatic tracking
- Custom email validation and age calculation

### Security & Access Rights
- Multi-level user access (User/Manager)
- Record-based security rules
- Department-specific access controls
- Custom view permissions

### Medical Staff Management
- Doctor profiles with image support
- Department management with capacity tracking
- Staff-patient relationship tracking

### Reports & Analytics
- Custom PDF patient reports with QWeb
- Excel report generation via API endpoints
- Patient statistics and analytics
- Department capacity monitoring

### Technical Features
- REST API integration with authentication
- Custom field validations and constraints
- Automated workflow actions
- State management with statusbar
- Smart buttons for related records
- Custom wizards for patient transfer
- Image handling and storage
- Mail thread integration
- Custom sequence generation

## 🛠️ Technical Details

### Models
- `hms.patient`: Main patient management
- `hms.doctors`: Doctor profiles
- `hms.department`: Department management
- `hms.patient.log`: Patient history logging

### API Endpoints
- `GET /api/hms/patient/report`: Generate Excel reports
- `POST /api/hms/auth/token`: Authentication endpoint
- Various CRUD operations for patient management

### Dependencies
- base
- crm
- mail

## 📦 Installation

1. Clone this repository:
```bash
git clone <repository-url>
```

2. Copy the `hms` folder to your Odoo addons directory

3. Update your Odoo apps list and install the HMS module

## 👥 Access Rights

- **Manager**: Full access to all features
- **User**: Limited access to patient records
- **System Admin**: Administrative access

## 🔧 Configuration

1. Go to Settings > Users & Companies > Groups
2. Configure user access rights
3. Set up departments and doctors
4. Configure email templates and sequences

## 💻 Development Notes

- Python 3.8+ compatible
- Following Odoo 17.0 guidelines
- PEP 8 compliant code
- Modular and extensible architecture

## 🤝 Contributing

Pull requests are welcome. Please ensure:
- Code follows Odoo standards
- Tests are included
- Documentation is updated

## 📝 License

LGPL-3
