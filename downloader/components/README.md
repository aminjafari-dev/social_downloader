# GUI Components Package

This package contains modular GUI components for the TikTok Downloader application. Each component is responsible for a specific functionality area, making the codebase more maintainable and reusable.

## Overview

The components package follows a modular architecture pattern where each GUI functionality is encapsulated in its own class. This approach provides several benefits:

- **Maintainability**: Each component can be modified independently
- **Reusability**: Components can be reused in other GUI applications
- **Testability**: Individual components can be tested in isolation
- **Separation of Concerns**: Each component has a single, well-defined responsibility

## Component Structure

### 1. VideoURLComponent (`video_url_component.py`)

**Purpose**: Handles single video URL input functionality.

**Features**:
- Single URL input field
- URL validation support
- Focus management
- Clear functionality

**Usage**:
```python
from components import VideoURLComponent

# Create component
url_component = VideoURLComponent(parent_frame)

# Get entered URL
url = url_component.get_url()

# Clear URL input
url_component.clear_url()
```

### 2. BatchModeComponent (`batch_mode_component.py`)

**Purpose**: Manages batch URL input functionality.

**Features**:
- Batch mode toggle
- Multi-line text area for URLs
- URL counting and validation
- Enable/disable text area based on mode

**Usage**:
```python
from components import BatchModeComponent

# Create component
batch_component = BatchModeComponent(parent_frame)

# Check if batch mode is enabled
is_enabled = batch_component.is_batch_mode_enabled()

# Get all batch URLs
urls = batch_component.get_urls()

# Add single URL to batch
batch_component.add_url("https://example.com")
```

### 3. DownloadSettingsComponent (`download_settings_component.py`)

**Purpose**: Manages download configuration settings.

**Features**:
- Output directory selection with browse functionality
- Quality selection (best, 720p, 480p, 360p)
- Custom naming options
- Audio-only and metadata toggles
- Excel export option
- Settings validation

**Usage**:
```python
from components import DownloadSettingsComponent

# Create component
settings_component = DownloadSettingsComponent(parent_frame)

# Get all current settings
settings = settings_component.get_settings()

# Update specific settings
settings_component.update_settings(output_dir="new_path", quality="720p")

# Reset to defaults
settings_component.reset_to_defaults()
```

### 4. ExcelIntegrationComponent (`excel_integration_component.py`)

**Purpose**: Handles Excel file operations and integration.

**Features**:
- Excel file selection and browsing
- Column loading and selection
- URL preview functionality
- Download from Excel capability
- Process existing downloads
- Callback system for integration

**Usage**:
```python
from components import ExcelIntegrationComponent

# Create component with Excel loader
excel_component = ExcelIntegrationComponent(parent_frame, excel_loader)

# Set callbacks for events
excel_component.set_callbacks(
    on_columns_loaded=handle_columns_loaded,
    on_excel_download_start=handle_download_start,
    on_process_existing=handle_process_existing
)

# Get selected URLs
urls = excel_component.get_selected_urls()
```

### 5. LogComponent (`log_component.py`)

**Purpose**: Manages logging and status display functionality.

**Features**:
- Timestamped log messages with levels
- Thread-safe message handling via queue
- Progress bar for operations
- Status display with color coding
- Log export and copy functionality
- Text search and highlighting

**Usage**:
```python
from components import LogComponent

# Create component
log_component = LogComponent(parent_frame)

# Add log message
log_component.log_message("Download started", "INFO")

# Set status
log_component.set_status("Processing...")

# Start/stop progress
log_component.start_progress()
log_component.stop_progress()

# Process queued messages (call periodically)
log_component.process_messages()
```

## Integration Pattern

### Main GUI Integration

The main GUI class (`TikTokDownloaderModularGUI`) orchestrates all components:

```python
class TikTokDownloaderModularGUI:
    def __init__(self):
        # Initialize components
        self.components = {}
        self.components['video_url'] = VideoURLComponent(self.main_frame)
        self.components['batch_mode'] = BatchModeComponent(self.main_frame)
        self.components['download_settings'] = DownloadSettingsComponent(self.main_frame)
        self.components['excel_integration'] = ExcelIntegrationComponent(self.main_frame, excel_loader)
        self.components['log'] = LogComponent(self.main_frame)
        
        # Setup callbacks
        self._setup_callbacks()
    
    def _setup_callbacks(self):
        # Connect component events to main GUI methods
        self.components['excel_integration'].set_callbacks(
            on_excel_download_start=self._on_excel_download_start
        )
```

### Callback System

Components use a callback system for loose coupling:

```python
# Component defines callback interface
def set_callbacks(self, on_event=None):
    self.on_event = on_event

# Main GUI sets callbacks
component.set_callbacks(on_event=self._handle_event)

# Component triggers callback when needed
if hasattr(self, 'on_event') and self.on_event:
    self.on_event(data)
```

## Thread Safety

Components that handle logging use a message queue for thread-safe updates:

```python
class LogComponent:
    def __init__(self):
        self.message_queue = queue.Queue()
    
    def log_message(self, message, level="INFO"):
        # Add to queue for thread-safe update
        self.message_queue.put(formatted_message)
    
    def process_messages(self):
        # Process queued messages (call from main thread)
        try:
            while True:
                message = self.message_queue.get_nowait()
                self._add_message_direct(message)
        except queue.Empty:
            pass
```

## Customization and Extension

### Adding New Components

To add a new component:

1. Create a new file in the `components/` directory
2. Follow the established pattern with `get_widget()` method
3. Add the component to `__init__.py`
4. Integrate it into the main GUI

### Component Communication

Components communicate through:
- **Callbacks**: For event-driven communication
- **Shared State**: Through the main GUI class
- **Message Queue**: For thread-safe logging

## Best Practices

1. **Single Responsibility**: Each component should have one clear purpose
2. **Interface Consistency**: All components should implement `get_widget()`
3. **Thread Safety**: Use message queues for cross-thread communication
4. **Error Handling**: Components should handle their own errors gracefully
5. **Documentation**: Each component should have comprehensive docstrings

## Testing

Each component can be tested independently:

```python
import unittest
from components import VideoURLComponent
import tkinter as tk

class TestVideoURLComponent(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.component = VideoURLComponent(self.root)
    
    def test_get_url(self):
        self.component.set_url("https://example.com")
        self.assertEqual(self.component.get_url(), "https://example.com")
    
    def tearDown(self):
        self.root.destroy()
```

## Dependencies

- **tkinter**: Standard Python GUI library
- **ttk**: Themed tkinter widgets
- **queue**: Thread-safe message handling
- **datetime**: Timestamp functionality
- **typing**: Type hints for better code quality

## Future Enhancements

- **Theme Support**: Customizable appearance
- **Internationalization**: Multi-language support
- **Plugin System**: Extensible component architecture
- **Configuration Persistence**: Save/restore component states
- **Accessibility**: Screen reader and keyboard navigation support
