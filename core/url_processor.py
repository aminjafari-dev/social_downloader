"""
URL Processor Module

This module handles URL validation, processing, and batch operations.
It provides functionality to validate URLs, process batch URLs, and manage URL collections.

Usage:
    from core.url_processor import URLProcessor
    
    processor = URLProcessor()
    valid_urls = processor.validate_urls(url_list)
    batch_urls = processor.process_batch_text(batch_text)
"""

import logging
import re
from typing import List, Tuple, Optional
from urllib.parse import urlparse

# Configure logging
logger = logging.getLogger(__name__)


class URLProcessor:
    """
    Handles URL processing, validation, and batch operations.
    
    This class provides:
    - URL validation for different platforms
    - Batch URL processing from text
    - Duplicate URL detection and removal
    - URL normalization and cleaning
    
    Attributes:
        supported_domains (dict): Dictionary mapping platform names to domain lists
        url_patterns (dict): Dictionary mapping platform names to URL regex patterns
    """
    
    def __init__(self):
        """Initialize the URL processor with supported platforms."""
        # Define supported domains for different platforms
        self.supported_domains = {
            'tiktok': [
                'tiktok.com',
                'vm.tiktok.com',
                'vt.tiktok.com',
                'www.tiktok.com'
            ],
            'youtube': [
                'youtube.com',
                'www.youtube.com',
                'youtu.be',
                'm.youtube.com'
            ],
            'instagram': [
                'instagram.com',
                'www.instagram.com',
                'instagr.am'
            ],
            'twitter': [
                'twitter.com',
                'www.twitter.com',
                'x.com',
                'www.x.com'
            ]
        }
        
        # Define URL patterns for validation
        self.url_patterns = {
            'tiktok': r'https?://(?:www\.)?(?:tiktok\.com|vm\.tiktok\.com|vt\.tiktok\.com)/[^\s]+',
            'youtube': r'https?://(?:www\.)?(?:youtube\.com|youtu\.be)/[^\s]+',
            'instagram': r'https?://(?:www\.)?instagram\.com/[^\s]+',
            'twitter': r'https?://(?:www\.)?(?:twitter\.com|x\.com)/[^\s]+'
        }
        
        logger.info("URLProcessor initialized with support for multiple platforms")
    
    def validate_url(self, url: str, platform: str = None) -> bool:
        """
        Validate if the provided URL is a valid URL for the specified platform.
        
        Args:
            url (str): The URL to validate
            platform (str): Platform to validate against (optional, auto-detect if None)
            
        Returns:
            bool: True if URL is valid, False otherwise
        """
        if not url or not url.strip():
            return False
        
        url = url.strip()
        
        # Basic URL validation
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False
        except Exception:
            return False
        
        # If platform is specified, validate against that platform
        if platform and platform.lower() in self.supported_domains:
            return any(domain in parsed.netloc.lower() 
                      for domain in self.supported_domains[platform.lower()])
        
        # Auto-detect platform and validate
        detected_platform = self.detect_platform(url)
        if detected_platform:
            return True
        
        # If no platform detected, check if it's a valid HTTP/HTTPS URL
        return url.startswith(('http://', 'https://'))
    
    def detect_platform(self, url: str) -> Optional[str]:
        """
        Detect the platform of a given URL.
        
        Args:
            url (str): The URL to analyze
            
        Returns:
            Optional[str]: Platform name if detected, None otherwise
        """
        try:
            parsed = urlparse(url.lower())
            netloc = parsed.netloc.lower()
            
            for platform, domains in self.supported_domains.items():
                if any(domain in netloc for domain in domains):
                    return platform
            
            return None
            
        except Exception:
            return None
    
    def validate_urls(self, urls: List[str], platform: str = None) -> Tuple[List[str], List[str]]:
        """
        Validate a list of URLs and return valid and invalid URLs.
        
        Args:
            urls (List[str]): List of URLs to validate
            platform (str): Platform to validate against (optional)
            
        Returns:
            Tuple[List[str], List[str]]: (valid_urls, invalid_urls)
        """
        try:
            if not urls:
                logger.info("Empty URL list provided to validate_urls, returning empty lists")
                return [], []
            
            valid_urls = []
            invalid_urls = []
            
            for url in urls:
                try:
                    if self.validate_url(url, platform):
                        valid_urls.append(url.strip())
                    else:
                        invalid_urls.append(url.strip())
                except Exception as e:
                    logger.warning(f"Error validating URL '{url}': {str(e)}")
                    invalid_urls.append(url.strip())
            
            logger.info(f"URL validation completed: {len(valid_urls)} valid, {len(invalid_urls)} invalid")
            
            # Ensure we return a proper tuple
            result = (valid_urls, invalid_urls)
            logger.debug(f"Returning validation result: {type(result)}, length: {len(result)}")
            return result
            
        except Exception as e:
            logger.error(f"Error in validate_urls: {str(e)}")
            logger.error(f"Error type: {type(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            # Return empty lists on error
            return [], []
    
    def process_batch_text(self, text: str, platform: str = None) -> Tuple[List[str], List[str]]:
        """
        Process batch text containing URLs and extract valid URLs.
        
        Args:
            text (str): Text containing URLs (one per line or separated by spaces)
            platform (str): Platform to validate against (optional)
            
        Returns:
            Tuple[List[str], List[str]]: (valid_urls, invalid_urls)
        """
        try:
            if not text:
                logger.info("Empty text provided to process_batch_text, returning empty lists")
                return [], []
            
            # Split text into lines and then by spaces to handle different formats
            lines = text.strip().split('\n')
            urls = []
            
            for line in lines:
                line_urls = line.strip().split()
                urls.extend(line_urls)
            
            # Remove empty strings and duplicates
            urls = [url.strip() for url in urls if url.strip()]
            unique_urls = list(dict.fromkeys(urls))  # Preserve order while removing duplicates
            
            logger.info(f"Processed batch text: found {len(unique_urls)} unique URLs")
            
            # Call validate_urls and ensure it returns a tuple
            validation_result = self.validate_urls(unique_urls, platform)
            
            # Ensure we always return a tuple
            if isinstance(validation_result, tuple) and len(validation_result) == 2:
                logger.info(f"Validation result: {len(validation_result[0])} valid, {len(validation_result[1])} invalid")
                return validation_result
            else:
                logger.error(f"validate_urls returned unexpected result: {type(validation_result)}, value: {validation_result}")
                # Fallback: return empty lists
                return [], []
                
        except Exception as e:
            logger.error(f"Error in process_batch_text: {str(e)}")
            logger.error(f"Error type: {type(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            # Return empty lists on error
            return [], []
    
    def remove_duplicates(self, urls: List[str]) -> List[str]:
        """
        Remove duplicate URLs while preserving order.
        
        Args:
            urls (List[str]): List of URLs to deduplicate
            
        Returns:
            List[str]: List of unique URLs
        """
        if not urls:
            return []
        
        # Normalize URLs for better duplicate detection
        normalized_urls = []
        seen_urls = set()
        unique_urls = []
        
        for url in urls:
            normalized = self.normalize_url(url)
            if normalized not in seen_urls:
                seen_urls.add(normalized)
                unique_urls.append(url)
        
        removed_count = len(urls) - len(unique_urls)
        if removed_count > 0:
            logger.info(f"Removed {removed_count} duplicate URLs")
        
        return unique_urls
    
    def normalize_url(self, url: str) -> str:
        """
        Normalize a URL for duplicate detection.
        
        Args:
            url (str): URL to normalize
            
        Returns:
            str: Normalized URL
        """
        if not url:
            return ""
        
        url = url.strip().lower()
        
        # Remove common tracking parameters
        tracking_params = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content']
        for param in tracking_params:
            url = re.sub(rf'[?&]{param}=[^&]*', '', url)
        
        # Remove trailing slashes
        url = url.rstrip('/')
        
        # Remove www. prefix for comparison
        url = re.sub(r'^https?://www\.', 'https://', url)
        
        return url
    
    def extract_urls_from_text(self, text: str, platform: str = None) -> List[str]:
        """
        Extract URLs from text using regex patterns.
        
        Args:
            text (str): Text to extract URLs from
            platform (str): Platform to extract URLs for (optional)
            
        Returns:
            List[str]: List of extracted URLs
        """
        if not text:
            return []
        
        urls = []
        
        if platform and platform.lower() in self.url_patterns:
            # Extract URLs for specific platform
            pattern = self.url_patterns[platform.lower()]
            matches = re.findall(pattern, text, re.IGNORECASE)
            urls.extend(matches)
        else:
            # Extract all URLs
            general_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
            matches = re.findall(general_pattern, text, re.IGNORECASE)
            urls.extend(matches)
        
        # Remove duplicates and validate
        unique_urls = list(dict.fromkeys(urls))
        valid_urls, _ = self.validate_urls(unique_urls, platform)
        
        logger.info(f"Extracted {len(valid_urls)} valid URLs from text")
        return valid_urls
    
    def get_platform_stats(self, urls: List[str]) -> dict:
        """
        Get statistics about URLs by platform.
        
        Args:
            urls (List[str]): List of URLs to analyze
            
        Returns:
            dict: Dictionary with platform statistics
        """
        stats = {}
        total_urls = len(urls)
        
        for url in urls:
            platform = self.detect_platform(url)
            if platform:
                stats[platform] = stats.get(platform, 0) + 1
            else:
                stats['unknown'] = stats.get('unknown', 0) + 1
        
        # Add percentages
        for platform, count in stats.items():
            percentage = (count / total_urls * 100) if total_urls > 0 else 0
            stats[f"{platform}_percentage"] = round(percentage, 2)
        
        stats['total'] = total_urls
        
        logger.info(f"Platform statistics: {stats}")
        return stats
    
    def clean_url(self, url: str) -> str:
        """
        Clean and normalize a URL.
        
        Args:
            url (str): URL to clean
            
        Returns:
            str: Cleaned URL
        """
        if not url:
            return ""
        
        # Remove whitespace
        url = url.strip()
        
        # Ensure protocol
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Remove trailing slashes
        url = url.rstrip('/')
        
        return url
    
    def batch_validate_and_clean(self, urls: List[str], platform: str = None) -> List[str]:
        """
        Validate, clean, and deduplicate a list of URLs.
        
        Args:
            urls (List[str]): List of URLs to process
            platform (str): Platform to validate against (optional)
            
        Returns:
            List[str]: List of clean, valid, unique URLs
        """
        if not urls:
            return []
        
        # Clean URLs
        cleaned_urls = [self.clean_url(url) for url in urls if url.strip()]
        
        # Remove duplicates
        unique_urls = self.remove_duplicates(cleaned_urls)
        
        # Validate URLs
        valid_urls, invalid_urls = self.validate_urls(unique_urls, platform)
        
        if invalid_urls:
            logger.warning(f"Found {len(invalid_urls)} invalid URLs: {invalid_urls[:5]}...")
        
        logger.info(f"Batch processing completed: {len(valid_urls)} valid URLs")
        return valid_urls
