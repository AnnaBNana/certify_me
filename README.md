#Certify Me

Certify Me is a tool for certificate generation.  The app stores data about businesses, their certificate requirements, their seminars, attendees, instructors, etc, and allows the user to generate certificates based on this data.

The user inputs a template PDF file and a CSV containing attendee data, and returns a PDF for each row in the CSV file.  These files are then stored in dropbox, and each user is sent an email with the pdf attached.

dependencies:
- Flask
- SQLAlchemy
- Dropbox
- SendGrid
- ReportLab
- PyPDF2
- PDFMiner
