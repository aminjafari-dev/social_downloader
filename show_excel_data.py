#!/usr/bin/env python3
"""
Script to display the Excel data in a readable format.

This script now uses the utils.excel_reader module for better code organization.
"""

from utils.excel_reader import show_excel_data

def main():
    """Main function to display Excel data."""
    print(show_excel_data())

if __name__ == "__main__":
    main()

