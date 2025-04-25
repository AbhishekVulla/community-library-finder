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
    page_title="Community Library Book Finder",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
initialize_database()

# App title and description
st.title("📚 Community Library Book Finder")
st.markdown("""
    Discover new books or suggest titles for our community library. 
    Use the filters and search to find your next great read!
""")

# Create tabs for Book Catalog and Suggestion Form
tab1, tab2 = st.tabs(["📖 Book Catalog", "✏️ Suggest a Book"])

with tab1:
    # Sidebar for filters with enhanced styling
    with st.sidebar:
        st.markdown("""
        <div style="padding: 10px; background-color: #f8f9fa; border-radius: 8px; margin-bottom: 15px;">
            <h3 style="color: #7E57C2; margin-top: 0;">📚 Filter Books</h3>
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
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            Do you have a book recommendation for our library? Fill out this form to suggest 
            a title you'd like to see in our collection! Your suggestions help us grow our library
            to better serve the community.
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
