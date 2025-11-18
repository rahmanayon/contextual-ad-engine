"""
Web scraping service for extracting content from URLs.
"""
import requests
from bs4 import BeautifulSoup
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class ScraperService:
    """Service for scraping web content."""
    
    @staticmethod
    async def scrape_url(url: str, timeout: int = 10) -> Optional[str]:
        """
        Scrape content from a URL.
        
        Args:
            url: The URL to scrape
            timeout: Request timeout in seconds
            
        Returns:
            Extracted text content or None if scraping fails
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer"]):
                script.decompose()
            
            # Get text
            text = soup.get_text(separator=' ', strip=True)
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Limit to first 2000 characters to avoid token limits
            return text[:2000] if text else None
            
        except requests.RequestException as e:
            logger.error(f"Scraping failed for {url}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error scraping {url}: {str(e)}")
            return None
