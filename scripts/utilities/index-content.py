#!/usr/bin/env python3
"""
Utility script to index book content into the vector database
This script reads markdown files from the docs directory and indexes them
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import List, Dict
import frontmatter  # This would need to be installed: pip install python-frontmatter

# Add the backend src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend', 'src'))

from services.content_index_service import ContentIndexService
from models.book_content import BookContent
from config.settings import settings


async def read_markdown_files(docs_dir: str) -> List[Dict]:
    """
    Read all markdown files from the docs directory
    """
    content_list = []

    docs_path = Path(docs_dir)

    for md_file in docs_path.rglob("*.md"):
        with open(md_file, 'r', encoding='utf-8') as f:
            # Use frontmatter to parse the file (handles both regular markdown and markdown with frontmatter)
            post = frontmatter.load(f)

            # Extract content and metadata
            content_text = post.content
            metadata = post.metadata

            # Create content entry
            content_entry = {
                'title': metadata.get('title', md_file.stem),
                'content': content_text,
                'section': metadata.get('section', ''),
                'page_path': str(md_file.relative_to(docs_path.parent)).replace('\\', '/').replace('.md', ''),
                'file_path': str(md_file)
            }

            content_list.append(content_entry)

    return content_list


async def index_book_content():
    """
    Main function to index all book content
    """
    print("Starting content indexing process...")

    # Initialize the content index service
    index_service = ContentIndexService()

    # Get the docs directory (relative to frontend)
    docs_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'docs')

    if not os.path.exists(docs_dir):
        print(f"Error: Docs directory not found at {docs_dir}")
        return

    # Read all markdown files
    print("Reading markdown files...")
    content_list = await read_markdown_files(docs_dir)

    print(f"Found {len(content_list)} content files to index")

    # Index each piece of content
    indexed_count = 0
    failed_count = 0

    for content_data in content_list:
        try:
            # Create a BookContent object
            book_content = BookContent(
                title=content_data['title'],
                content=content_data['content'],
                section=content_data['section'],
                page_path=content_data['page_path']
            )

            # Index the content
            success = await index_service.index_content(book_content)

            if success:
                print(f"Successfully indexed: {content_data['title']} ({content_data['page_path']})")
                indexed_count += 1
            else:
                print(f"Failed to index: {content_data['title']}")
                failed_count += 1

        except Exception as e:
            print(f"Error indexing {content_data['title']}: {str(e)}")
            failed_count += 1

    print(f"\nIndexing complete!")
    print(f"Successfully indexed: {indexed_count} files")
    print(f"Failed to index: {failed_count} files")


if __name__ == "__main__":
    # Check if required environment variables are set
    required_vars = ['OPENAI_API_KEY', 'QDRANT_URL', 'DATABASE_URL']
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these variables in your environment or .env file")
        sys.exit(1)

    # Run the indexing process
    asyncio.run(index_book_content())