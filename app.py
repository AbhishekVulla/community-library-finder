import streamlit as st
import pandas as pd
import plotly.express as px
from database import (
    initialize_database,
    get_all_books,
    get_books_by_filter,
    add_book_suggestion,
    get_all_genres
)
from utils import format_book_card, DEFAULT_COVER_IMAGE_URL

# Set page config
st.set_page_config(
    page_title="Al Khor Community Library Book Finder",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
initialize_database()

# App states in session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'  # Default to home page
if 'selected_genre' not in st.session_state:
    st.session_state.selected_genre = 'All'
if 'selected_age_group' not in st.session_state:
    st.session_state.selected_age_group = 'All'
if 'search_query' not in st.session_state:
    st.session_state.search_query = ''

# Function to set page state
def set_page(page_name):
    st.session_state.page = page_name
    
# Function to reset filters
def reset_all_filters():
    st.session_state.selected_genre = 'All'
    st.session_state.selected_age_group = 'All'
    st.session_state.search_query = ''
    st.session_state.page = 'home'

# Al Khor Community Library Branding - Improved header with modern design
st.markdown("""
<div style="
    background: linear-gradient(135deg, #873600 0%, #D35400 100%);
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    overflow: hidden;
    position: relative;
">
    <div style="
        background-color: rgba(255,255,255,0.9);
        border-radius: 50%;
        width: 80px;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    ">
        <span style="font-size: 40px;">📚</span>
    </div>
    <div>
        <h1 style="color: white; margin-bottom: 5px; font-weight: 700; text-shadow: 1px 1px 3px rgba(0,0,0,0.3);">Al Khor Community Library</h1>
        <p style="color: #f8f8f8; font-size: 1.2em; margin: 0; font-style: italic;">Exploring Knowledge Together in Qatar</p>
    </div>
    <div style="
        position: absolute;
        right: -20px;
        top: -20px;
        width: 150px;
        height: 150px;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
        border-radius: 50%;
    "></div>
</div>
""", unsafe_allow_html=True)

# Navigation/Home button when not on home page
if st.session_state.page != 'home':
    if st.button("🏠 Back to Home", key="back_home"):
        set_page('home')
    st.markdown("<hr>", unsafe_allow_html=True)

# Enhanced App description with diversity focus
st.markdown("""
    <div style="background: linear-gradient(to right, #f0f8ff, #fff); padding: 20px; border-radius: 10px; 
            border-left: 5px solid #873600; margin-bottom: 25px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
        <h2 style="color: #873600; margin-top: 0; margin-bottom: 10px; font-size: 1.3rem;">Welcome to Al Khor Community's Digital Library</h2>
        <p style="margin-bottom: 12px; line-height: 1.5;">Discover books from our diverse collection representing Qatar's multicultural community. 
        Our catalog features works from Qatari authors, global literature, and resources that celebrate inclusivity.</p>
        <p style="margin: 0; line-height: 1.5;">Use our intuitive filters to find your next great read or suggest new titles that promote 
        understanding across cultures. Our mission is to provide equal access to knowledge for all Al Khor Community members.</p>
    </div>
""", unsafe_allow_html=True)

# Create tabs for Book Catalog, Suggestion Form, and Library Visit Scheduler
tab1, tab2, tab3 = st.tabs(["📖 Book Catalog", "✏️ Suggest a Book", "🗓️ Visit Scheduler"])

with tab1:
    # Sidebar for filters with enhanced styling
    with st.sidebar:
        st.markdown("""
        <div style="padding: 15px; background: linear-gradient(135deg, #873600 0%, #D35400 100%); border-radius: 12px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h3 style="color: white; margin-top: 0; font-weight: 600; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">📚 Filter Books</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Get all available genres for dropdown
        genres = get_all_genres()
        
        # Create a more modern filter interface
        with st.expander("Genre & Age Filters", expanded=True):
            selected_genre = st.selectbox(
                "Select Genre", 
                ["All"] + genres,
                help="Filter books by their genre"
            )
            
            # Age group filter with better visual cues
            st.markdown("##### Age Group")
            age_group = st.radio(
                "Select Age Group",
                options=["All", "Small Kids", "Teens & Adults"],
                horizontal=True,
                label_visibility="collapsed",
                help="Filter books by target age group"
            )
        
        # Search box with clear instructions
        st.markdown("##### Search")
        search_query = st.text_input(
            "Search by title or author name",
            placeholder="Enter title or author...",
            help="Search across both book titles and author names"
        )
        
        # Apply filters button
        col1, col2 = st.columns(2)
        with col1:
            filter_pressed = st.button("Apply Filters", use_container_width=True)
        with col2:
            reset_filters = st.button("Reset All", use_container_width=True)
        
        # Add genre distribution chart in sidebar
        st.markdown("""
        <div style="margin-top: 25px; margin-bottom: 10px;">
            <h4 style="color: #555;">📊 Collection Overview</h4>
        </div>
        """, unsafe_allow_html=True)
        
        books_df = pd.DataFrame(get_all_books())
        if not books_df.empty:
            # Show total book count
            total_books = len(books_df)
            st.metric("Total Books in Collection", total_books)
            
            # Get count of unique genres and authors
            unique_genres = len(books_df['genre'].unique())
            unique_authors = len(books_df['author'].unique())
            
            # Display in two columns
            stat_col1, stat_col2 = st.columns(2)
            with stat_col1:
                st.metric("Genres", unique_genres)
            with stat_col2:
                st.metric("Authors", unique_authors)
            
            # Genre distribution chart
            genre_counts = books_df['genre'].value_counts().reset_index()
            genre_counts.columns = ['Genre', 'Count']
            
            fig = px.pie(
                genre_counts, 
                values='Count', 
                names='Genre',
                title='Books by Genre',
                color_discrete_sequence=px.colors.qualitative.Pastel,
                hole=0.4  # Make it a donut chart for modern look
            )
            fig.update_layout(
                margin=dict(t=40, b=0, l=0, r=0),
                legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Main content area for books
    # Get books based on filters or reset if requested
    if reset_filters:
        books = get_all_books()
        st.rerun()  # Rerun the app to reset all filters (using the newer st.rerun instead of experimental_rerun)
    elif filter_pressed or search_query or selected_genre != "All" or age_group != "All":
        books = get_books_by_filter(
            genre=None if selected_genre == "All" else selected_genre,
            age_group=None if age_group == "All" else age_group,
            search_query=search_query
        )
    else:
        books = get_all_books()
    
    # Results section with better styling
    if not books:
        st.info("No books found matching your criteria. Try adjusting your filters.")
    else:
        # Create a header with results count and download button
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"""
            <h3 style="margin-bottom: 0px; color: #333;">
                Found {len(books)} books
            </h3>
            """, unsafe_allow_html=True)
            
            # Add active filter indicators
            active_filters = []
            if selected_genre != "All":
                active_filters.append(f"Genre: {selected_genre}")
            if age_group != "All":
                active_filters.append(f"Age: {age_group}")
            if search_query:
                active_filters.append(f"Search: '{search_query}'")
                
            if active_filters:
                st.markdown(f"""
                <div style="margin-bottom: 15px; font-size: 0.9em; color: #666;">
                    Filters: {' • '.join(active_filters)}
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            # Add download button for current results
            books_df = pd.DataFrame(books)
            csv = books_df.to_csv(index=False)
            st.download_button(
                "📥 Download Results",
                csv,
                "library_books.csv",
                "text/csv",
                key='download-csv',
                help="Download the current book list as a CSV file",
                use_container_width=True
            )
        
        # Display books in a responsive grid (3 columns on desktop, adjust for mobile)
        # For better mobile responsiveness
        if len(books) > 0:
            st.write("---")
            
            # Create a better grid layout for books
            for i in range(0, len(books), 3):
                row_books = books[i:min(i+3, len(books))]
                cols = st.columns(3)
                
                # Fill each column with a book
                for j, book in enumerate(row_books):
                    with cols[j]:
                        format_book_card(book)
                
                # Add a divider between rows for better visual separation
                st.write("---")

with tab2:
    st.header("📝 Suggest a Book for the Library")
    st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(135, 54, 0, 0.1) 0%, rgba(211, 84, 0, 0.05) 100%); 
                padding: 20px; border-radius: 12px; margin-bottom: 25px; border: 1px solid rgba(135, 54, 0, 0.2);">
            <h3 style="color: #873600; margin-top: 0; margin-bottom: 10px;">Contribute to Our Diverse Collection</h3>
            <p style="margin-bottom: 0;">Help us build a more inclusive library by suggesting books that represent 
            different cultures, perspectives, and experiences. We especially welcome recommendations for:
            <ul style="margin-top: 8px;">
                <li>Books by Qatari and Middle Eastern authors</li>
                <li>Literature featuring diverse characters and viewpoints</li>
                <li>Books that promote cultural understanding and global awareness</li>
                <li>Works in multiple languages that reflect our multinational community</li>
            </ul>
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for a more balanced layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Book suggestion form with enhanced styling
        with st.form("book_suggestion_form"):
            st.markdown("### Book Details")
            suggested_title = st.text_input("Book Title", max_chars=100, 
                                          help="Enter the full title of the book")
            suggested_author = st.text_input("Author", max_chars=100,
                                           help="Enter the author's full name")
            
            # Create two columns for genre and age group
            form_col1, form_col2 = st.columns(2)
            with form_col1:
                suggested_genre = st.selectbox("Genre", genres, 
                                             help="Select the most appropriate genre")
            with form_col2:
                suggested_age_group = st.radio("Age Group", ["Small Kids", "Teens & Adults"],
                                             help="Select the appropriate age group")
            
            suggested_description = st.text_area("Description", max_chars=500, 
                                               height=150,
                                               help="Brief description of the book (max 500 characters)")
            suggested_cover_url = st.text_input("Cover Image URL (optional)",
                                              help="Paste a URL to the book's cover image if available")
            
            # Form submission button with custom styling
            submitted = st.form_submit_button("Submit Suggestion", 
                                            use_container_width=True,
                                            help="Click to submit your book suggestion")
            
            if submitted:
                if suggested_title and suggested_author:
                    # Add suggestion to database
                    add_book_suggestion(
                        title=suggested_title,
                        author=suggested_author,
                        genre=suggested_genre,
                        age_group=suggested_age_group,
                        description=suggested_description,
                        cover_url=suggested_cover_url
                    )
                    st.success("Thank you for your suggestion! The library staff will review it.")
                else:
                    st.error("Please provide at least the book title and author.")
    
    with col2:
        # Information sidebar about the suggestion process
        st.markdown("""
        <div style="background-color: #e8f4f8; padding: 15px; border-radius: 8px; 
                   border-left: 4px solid #7E57C2;">
            <h4>📚 Why Suggest Books?</h4>
            <p>Your suggestions help us:</p>
            <ul>
                <li>Build a diverse collection</li>
                <li>Meet community interests</li>
                <li>Discover new authors and titles</li>
            </ul>
            <p>All suggestions are reviewed by our library staff before being added to our collection.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show a sample of recently suggested books or guidelines
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background-color: #f0f0f0; padding: 15px; border-radius: 8px;">
            <h4>📋 Suggestion Guidelines</h4>
            <ul>
                <li>Include accurate title and author</li>
                <li>Select appropriate genre and age group</li>
                <li>Add a brief description to help us understand why this book would be valuable</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.header("🗓️ Al Khor Community Library Visit Scheduler")
    st.markdown("""
        <div style="background-color: #f0f7ff; padding: 20px; border-radius: 10px; margin-bottom: 25px; border-left: 5px solid #873600;">
            <h4 style="margin-top: 0; color: #873600;">Plan Your Library Visit</h4>
            <p>Use this scheduler to plan your visit to Al Khor Community Library. Scheduling helps us ensure 
            we can provide the best assistance during your visit, especially for research projects, 
            study groups, or book consultations.</p>
            <p><strong>Library Location:</strong> Al Khor Community Center, Qatar</p>
            <p><strong>Regular Hours:</strong> Sunday-Thursday: 9:00 AM - 8:00 PM, Friday: 2:00 PM - 7:00 PM, Saturday: 10:00 AM - 6:00 PM</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for scheduler layout
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Visitor information section
        st.subheader("Visitor Information")
        
        with st.form("visit_scheduler_form"):
            visitor_name = st.text_input("Full Name", help="Please enter your full name")
            visitor_email = st.text_input("Email Address", help="We'll send a confirmation to this email")
            visitor_phone = st.text_input("Phone Number (optional)", help="For urgent communications")
            
            # Purpose of visit
            st.subheader("Visit Details")
            visit_purpose = st.selectbox(
                "Purpose of Visit",
                [
                    "General browsing",
                    "Book borrowing",
                    "Research assistance",
                    "Study group",
                    "Children's storytelling session",
                    "Library orientation",
                    "Other (please specify)"
                ],
                help="Select the main reason for your visit"
            )
            
            if visit_purpose == "Other (please specify)":
                other_purpose = st.text_input("Please specify purpose")
            
            # Number of visitors
            num_visitors = st.number_input(
                "Number of Visitors", 
                min_value=1, 
                max_value=20, 
                value=1,
                help="Please let us know if you're coming with a group"
            )
            
            # Date and time selection
            col1a, col1b = st.columns(2)
            with col1a:
                visit_date = st.date_input(
                    "Preferred Date",
                    min_value=pd.Timestamp.now().date(),
                    help="Select your preferred visit date"
                )
            with col1b:
                visit_time = st.selectbox(
                    "Preferred Time",
                    [
                        "9:00 AM - 11:00 AM",
                        "11:00 AM - 1:00 PM",
                        "1:00 PM - 3:00 PM",
                        "3:00 PM - 5:00 PM",
                        "5:00 PM - 7:00 PM"
                    ],
                    help="Select your preferred visit time"
                )
            
            # Additional notes
            additional_notes = st.text_area(
                "Additional Information or Special Requests",
                max_chars=500,
                height=100,
                help="Please include any specific requirements or questions"
            )
            
            # Submit button
            submit_visit = st.form_submit_button("Schedule Visit", use_container_width=True)
            
            if submit_visit:
                if visitor_name and visitor_email and visit_date:
                    st.success(f"Thank you, {visitor_name}! Your visit has been scheduled for {visit_date.strftime('%A, %B %d, %Y')} at {visit_time}. A confirmation email has been sent to {visitor_email}.")
                    
                    # Display a QR code (for demo purposes)
                    st.markdown("""
                        <div style="background-color: #f8f8f8; padding: 15px; border-radius: 5px; text-align: center; margin-top: 20px;">
                            <h4>📱 Save to Calendar</h4>
                            <p>Scan this QR code to add this visit to your calendar</p>
                            <img src="https://cdn.pixabay.com/photo/2020/08/04/08/21/qr-code-5462633_960_720.png" width="150px">
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("Please fill in all required fields (name, email, and visit date).")
    
    with col2:
        # Right sidebar with helpful information - with proper card styling
        st.markdown("""
        <div style="border-radius: 10px; overflow: hidden; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom: 20px;">
        """, unsafe_allow_html=True)
        st.image("https://cdn.pixabay.com/photo/2021/09/05/16/57/library-6599540_960_720.jpg", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 15px;">
            <h4>📚 Library Services</h4>
            <ul>
                <li><strong>Book Borrowing</strong> - AKC residents can borrow up to 5 books</li>
                <li><strong>Research Assistance</strong> - Librarians available for research help</li>
                <li><strong>Study Spaces</strong> - Quiet areas with Wi-Fi for individual study</li>
                <li><strong>Children's Corner</strong> - Interactive reading area for kids</li>
                <li><strong>Digital Resources</strong> - Access to online databases and e-books</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(135, 54, 0, 0.05) 0%, rgba(211, 84, 0, 0.1) 100%); 
                padding: 18px; border-radius: 10px; margin-top: 20px; border: 1px solid rgba(135, 54, 0, 0.1);">
            <h4 style="color: #873600; margin-top: 0;">🌟 Cultural Diversity Events</h4>
            <ul style="padding-left: 20px;">
                <li style="margin-bottom: 8px;"><strong>May 5, 2025</strong> - <span style="color: #873600;">Author Meet & Greet:</span> 
                Celebrated Qatari author Abdulaziz Al-Mahmoud discusses "The Corsair"</li>
                
                <li style="margin-bottom: 8px;"><strong>May 12, 2025</strong> - <span style="color: #873600;">Multilingual Children's Hour:</span> 
                Stories in Arabic, English, and Hindi for ages 4-8</li>
                
                <li style="margin-bottom: 8px;"><strong>May 18, 2025</strong> - <span style="color: #873600;">Book Club:</span> 
                Discussing "Girls of Riyadh" by Rajaa Alsanea - examining social change</li>
                
                <li style="margin-bottom: 8px;"><strong>May 25, 2025</strong> - <span style="color: #873600;">Cultural Exchange Workshop:</span> 
                "Literature Across Borders" featuring expat and local writers</li>
                
                <li style="margin-bottom: 8px;"><strong>June 3, 2025</strong> - <span style="color: #873600;">Inclusive Reading Series:</span> 
                Books featuring characters with diverse abilities and backgrounds</li>
            </ul>
            <p style="font-style: italic; margin-top: 15px; margin-bottom: 0; color: #555;">
                Join us for these events celebrating Qatar's diverse community! 
                <a href="#" style="color: #873600; text-decoration: none; font-weight: bold;">View full calendar</a>
            </p>
        </div>
        """, unsafe_allow_html=True)
