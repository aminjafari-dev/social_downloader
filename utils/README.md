# Utils Module

This module contains utility functions and classes for the TikTok downloader project, specifically focused on Excel file handling and data processing.

## Structure

```
utils/
├── __init__.py          # Package initialization and exports
├── excel_loader.py      # Excel file loading and data extraction
├── excel_reader.py      # Excel file reading and display
└── README.md           # This documentation file
```

## Excel Loader (`excel_loader.py`)

The `ExcelLoader` class provides functionality for loading and reading Excel files, extracting data from specific columns, and validating Excel file formats.

### Key Features

- **File Validation**: Validate Excel files before processing
- **Column Extraction**: Extract column names and data from specific columns
- **URL Processing**: Extract and validate URLs from Excel columns
- **Data Preview**: Generate previews of Excel data
- **File Information**: Get comprehensive information about Excel files

### Usage Examples

```python
from utils.excel_loader import ExcelLoader

# Initialize the loader
loader = ExcelLoader()

# Validate an Excel file
is_valid, error_message = loader.validate_excel_file("path/to/file.xlsx")

# Get column names
columns = loader.get_column_names("path/to/file.xlsx")

# Extract URLs from a specific column
urls = loader.extract_urls_from_column("path/to/file.xlsx", "URL Column", url_validator)

# Get a preview of data
preview = loader.get_excel_preview("path/to/file.xlsx", "Column Name", max_preview=5)

# Get file information
info = loader.get_excel_info("path/to/file.xlsx")
```

### Convenience Functions

```python
from utils.excel_loader import load_excel_columns, extract_urls_from_excel, validate_excel_file

# Quick column loading
columns = load_excel_columns("path/to/file.xlsx")

# Quick URL extraction
urls = extract_urls_from_excel("path/to/file.xlsx", "URL Column")

# Quick file validation
is_valid, message = validate_excel_file("path/to/file.xlsx")
```

## Excel Reader (`excel_reader.py`)

The `ExcelReader` class provides functionality for reading, displaying, and analyzing Excel files.

### Key Features

- **File Discovery**: Find the most recent Excel files in directories
- **Data Display**: Format Excel data for readable display
- **Statistics**: Generate statistics from Excel data
- **Data Extraction**: Extract specific data from columns
- **Workbook Management**: Load and manage Excel workbooks

### Usage Examples

```python
from utils.excel_reader import ExcelReader

# Initialize the reader
reader = ExcelReader()

# Find the latest Excel file
latest_file = reader.find_latest_excel_file("downloads", "*.xlsx")

# Load a workbook
workbook = reader.load_excel_workbook("path/to/file.xlsx")

# Get headers
headers = reader.get_excel_headers(workbook)

# Get data summary
summary = reader.get_excel_data_summary(workbook)

# Format data for display
display_text = reader.format_excel_data_display(workbook, max_videos=10)

# Show Excel data
result = reader.show_excel_data("path/to/file.xlsx")

# Extract specific data
data = reader.extract_specific_data(workbook, "Column Name")

# Get statistics
stats = reader.get_excel_statistics(workbook)
```

### Convenience Functions

```python
from utils.excel_reader import show_excel_data, find_latest_excel_file

# Quick data display
display = show_excel_data("path/to/file.xlsx")

# Quick file finding
latest = find_latest_excel_file("downloads")
```

## Integration with Existing Code

### GUI Integration

The GUI has been updated to use the new Excel utilities:

```python
# In tiktok_gui.py
from utils.excel_loader import ExcelLoader

class TikTokDownloaderGUI:
    def __init__(self):
        # Initialize Excel loader
        self.excel_loader = ExcelLoader()
    
    def load_excel_columns(self):
        # Use the loader instead of direct openpyxl calls
        columns = self.excel_loader.get_column_names(excel_path)
    
    def get_excel_urls(self):
        # Use the loader for URL extraction
        urls = self.excel_loader.extract_urls_from_column(
            excel_path, 
            url_column, 
            self.downloader.validate_url
        )
```

### Command Line Integration

The `show_excel_data.py` script has been simplified:

```python
# In show_excel_data.py
from utils.excel_reader import show_excel_data

def main():
    print(show_excel_data())

if __name__ == "__main__":
    main()
```

## Benefits of This Structure

1. **Separation of Concerns**: Excel loading and reading are now separate, focused modules
2. **Reusability**: Functions can be used across different parts of the application
3. **Maintainability**: Changes to Excel handling only need to be made in one place
4. **Testability**: Each module can be tested independently
5. **Error Handling**: Centralized error handling for Excel operations
6. **Documentation**: Clear documentation and examples for each function

## Error Handling

Both modules include comprehensive error handling:

- File validation before processing
- Graceful handling of missing files or columns
- Detailed error messages for debugging
- Logging for tracking issues

## Performance Considerations

- Uses `read_only=True` for large Excel files
- Efficient column indexing
- Minimal memory usage through streaming operations
- Proper resource cleanup with workbook closing

## Testing

Run the test script to verify functionality:

```bash
python test_excel_utils.py
```

This will test all major functions in both modules and provide feedback on their operation.
