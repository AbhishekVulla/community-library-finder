# 📚 Community Library Book Finder

A modern web application built to help community library visitors discover books and suggest new titles for the collection.

## Project Overview
This mobile-friendly web app, built with Python and Streamlit, enables users to easily browse, search, and filter through a library's book collection. It also allows visitors to submit suggestions for new books to add to the library's catalog.

## Features

### 🔍 Book Discovery
- Filter books by genre and age group (Small Kids or Teens & Adults)
- Search books by title or author name
- View book details including cover image, description, and popularity rating
- Download search results as CSV for offline access

### 📊 Visual Analytics
- Interactive donut chart showing genre distribution
- Collection statistics overview
- Visual indication of book popularity with star ratings

### 💡 Book Suggestions
- Intuitive form for suggesting new titles
- Form validation for required fields
- Information about the suggestion process and guidelines
- Submission tracking in a separate database table

### 💻 Technical Features
- Mobile-responsive design
- Modern user interface with consistent styling
- SQLite database for persistent storage
- Error handling for broken image links
- Modular code architecture (app logic, database, and utilities)

## Technology Stack
- Python 3.11
- Streamlit (web framework)
- SQLite (database)
- Pandas (data manipulation)
- Plotly (data visualization)

## Project Structure
- `app.py`: Main application with UI components and routing
- `database.py`: Database connection and query functionality
- `utils.py`: Helper functions for UI rendering
- `sample_data.py`: Initial sample book data
- `.streamlit/config.toml`: Streamlit configuration

## Future Enhancements
- User accounts for librarians to review and approve suggestions
- Book checkout and reservation system
- Reading history and recommendation engine
- Integration with external book APIs for enhanced metadata

## Development 
This project was developed as a college application showcase demonstrating:
- Full-stack application design principles
- Database design and implementation
- User interface design and user experience considerations
- Data visualization and analytics
- Mobile-responsive web development techniques
