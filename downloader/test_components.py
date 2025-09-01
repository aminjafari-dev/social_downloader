"""
Test Script for Modular GUI Components

This script demonstrates how the modular components work together and can be
tested independently. It creates a simple test GUI that shows all components
in action.

Usage:
    python test_components.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add components directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'components'))

try:
    from components import (
        VideoURLComponent,
        BatchModeComponent,
        DownloadSettingsComponent,
        ExcelIntegrationComponent,
        LogComponent
    )
except ImportError as e:
    print(f"Error importing components: {e}")
    print("Make sure all component files are in the components/ directory")
    sys.exit(1)


class ComponentTestGUI:
    """
    Test GUI for demonstrating modular components.
    
    This class creates a simple interface to test all components
    and show how they work together.
    """
    
    def __init__(self):
        """Initialize the test GUI."""
        self.root = tk.Tk()
        self.root.title("Component Test GUI")
        self.root.geometry("800x600")
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create title
        title_label = ttk.Label(
            self.main_frame, 
            text="Modular Component Test Interface", 
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Create components
        self._create_components()
        
        # Create test buttons
        self._create_test_buttons()
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(5, weight=1)  # Log component row
        
        # Start message processing
        self.root.after(100, self._process_messages)
    
    def _create_components(self):
        """Create all test components."""
        # Video URL component
        self.video_url_component = VideoURLComponent(self.main_frame)
        self.video_url_component.get_widget().grid(
            row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10)
        )
        
        # Batch mode component
        self.batch_mode_component = BatchModeComponent(self.main_frame)
        self.batch_mode_component.get_widget().grid(
            row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10)
        )
        
        # Download settings component
        self.download_settings_component = DownloadSettingsComponent(self.main_frame)
        self.download_settings_component.get_widget().grid(
            row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10)
        )
        
        # Excel integration component (with mock Excel loader)
        self.excel_integration_component = ExcelIntegrationComponent(
            self.main_frame, 
            MockExcelLoader()
        )
        self.excel_integration_component.get_widget().grid(
            row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10)
        )
        
        # Log component
        self.log_component = LogComponent(self.main_frame)
        self.log_component.get_widget().grid(
            row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0)
        )
    
    def _create_test_buttons(self):
        """Create test buttons for component testing."""
        test_frame = ttk.LabelFrame(self.main_frame, text="Component Tests", padding="10")
        test_frame.grid(row=6, column=0, columnspan=2, pady=(10, 0))
        
        # Row 1: Basic component tests
        row1_frame = ttk.Frame(test_frame)
        row1_frame.grid(row=0, column=0, pady=(0, 10))
        
        ttk.Button(
            row1_frame, 
            text="Test Video URL", 
            command=self._test_video_url
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            row1_frame, 
            text="Test Batch Mode", 
            command=self._test_batch_mode
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            row1_frame, 
            text="Test Settings", 
            command=self._test_settings
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Row 2: Advanced component tests
        row2_frame = ttk.Frame(test_frame)
        row2_frame.grid(row=1, column=0, pady=(0, 10))
        
        ttk.Button(
            row2_frame, 
            text="Test Excel Integration", 
            command=self._test_excel_integration
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            row2_frame, 
            text="Test Log Component", 
            command=self._test_log_component
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            row2_frame, 
            text="Test All Components", 
            command=self._test_all_components
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Row 3: Utility buttons
        row3_frame = ttk.Frame(test_frame)
        row3_frame.grid(row=2, column=0)
        
        ttk.Button(
            row3_frame, 
            text="Reset All", 
            command=self._reset_all_components
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            row3_frame, 
            text="Show Component Info", 
            command=self._show_component_info
        ).pack(side=tk.LEFT, padx=(0, 10))
    
    def _process_messages(self):
        """Process messages from the log component."""
        self.log_component.process_messages()
        self.root.after(100, self._process_messages)
    
    def _test_video_url(self):
        """Test the video URL component."""
        try:
            # Test setting and getting URL
            test_url = "https://www.tiktok.com/@testuser/video/123456789"
            self.video_url_component.set_url(test_url)
            
            retrieved_url = self.video_url_component.get_url()
            if retrieved_url == test_url:
                self.log_component.log_message("Video URL component test: PASSED", "SUCCESS")
                messagebox.showinfo("Test Result", "Video URL component test: PASSED")
            else:
                self.log_component.log_message("Video URL component test: FAILED", "ERROR")
                messagebox.showerror("Test Result", "Video URL component test: FAILED")
                
        except Exception as e:
            self.log_component.log_message(f"Video URL test error: {str(e)}", "ERROR")
            messagebox.showerror("Test Error", f"Video URL test error: {str(e)}")
    
    def _test_batch_mode(self):
        """Test the batch mode component."""
        try:
            # Test batch mode functionality
            test_urls = [
                "https://www.tiktok.com/@user1/video/111111111",
                "https://www.tiktok.com/@user2/video/222222222",
                "https://www.tiktok.com/@user3/video/333333333"
            ]
            
            self.batch_mode_component.set_urls(test_urls)
            
            retrieved_urls = self.batch_mode_component.get_urls()
            if len(retrieved_urls) == len(test_urls):
                self.log_component.log_message("Batch mode component test: PASSED", "SUCCESS")
                messagebox.showinfo("Test Result", "Batch mode component test: PASSED")
            else:
                self.log_component.log_message("Batch mode component test: FAILED", "ERROR")
                messagebox.showerror("Test Result", "Batch mode component test: FAILED")
                
        except Exception as e:
            self.log_component.log_message(f"Batch mode test error: {str(e)}", "ERROR")
            messagebox.showerror("Test Error", f"Batch mode test error: {str(e)}")
    
    def _test_settings(self):
        """Test the download settings component."""
        try:
            # Test settings functionality
            test_settings = {
                'output_dir': 'test_downloads',
                'quality': '720p',
                'custom_base_name': 'test_video',
                'extract_audio': True,
                'add_metadata': False,
                'export_to_excel': True
            }
            
            self.download_settings_component.update_settings(**test_settings)
            
            retrieved_settings = self.download_settings_component.get_settings()
            
            # Check if settings were updated correctly
            settings_match = all(
                retrieved_settings.get(key) == value 
                for key, value in test_settings.items()
            )
            
            if settings_match:
                self.log_component.log_message("Download settings component test: PASSED", "SUCCESS")
                messagebox.showinfo("Test Result", "Download settings component test: PASSED")
            else:
                self.log_component.log_message("Download settings component test: FAILED", "ERROR")
                messagebox.showerror("Test Result", "Download settings component test: FAILED")
                
        except Exception as e:
            self.log_component.log_message(f"Settings test error: {str(e)}", "ERROR")
            messagebox.showerror("Test Error", f"Settings test error: {str(e)}")
    
    def _test_excel_integration(self):
        """Test the Excel integration component."""
        try:
            # Test Excel integration functionality
            self.log_component.log_message("Testing Excel integration component...", "INFO")
            
            # Simulate Excel file selection
            self.excel_integration_component.excel_file_var.set("test_file.xlsx")
            self.excel_integration_component.url_column_var.set("URL")
            
            # Test URL extraction
            urls = self.excel_integration_component.get_selected_urls()
            
            self.log_component.log_message("Excel integration component test: PASSED", "SUCCESS")
            messagebox.showinfo("Test Result", "Excel integration component test: PASSED")
                
        except Exception as e:
            self.log_component.log_message(f"Excel integration test error: {str(e)}", "ERROR")
            messagebox.showerror("Test Error", f"Excel integration test error: {str(e)}")
    
    def _test_log_component(self):
        """Test the log component."""
        try:
            # Test various log levels
            self.log_component.log_message("This is an INFO message", "INFO")
            self.log_component.log_message("This is a WARNING message", "WARNING")
            self.log_component.log_message("This is an ERROR message", "ERROR")
            self.log_component.log_message("This is a SUCCESS message", "SUCCESS")
            
            # Test status setting
            self.log_component.set_status("Testing log component...")
            
            # Test progress bar
            self.log_component.start_progress()
            self.root.after(2000, self.log_component.stop_progress)  # Stop after 2 seconds
            
            self.log_component.log_message("Log component test: PASSED", "SUCCESS")
            messagebox.showinfo("Test Result", "Log component test: PASSED")
                
        except Exception as e:
            self.log_component.log_message(f"Log component test error: {str(e)}", "ERROR")
            messagebox.showerror("Test Error", f"Log component test error: {str(e)}")
    
    def _test_all_components(self):
        """Test all components in sequence."""
        try:
            self.log_component.log_message("Starting comprehensive component test...", "INFO")
            
            # Test each component
            self._test_video_url()
            self.root.after(500, self._test_batch_mode)
            self.root.after(1000, self._test_settings)
            self.root.after(1500, self._test_excel_integration)
            self.root.after(2000, self._test_log_component)
            
            self.log_component.log_message("All component tests completed", "SUCCESS")
                
        except Exception as e:
            self.log_component.log_message(f"Comprehensive test error: {str(e)}", "ERROR")
    
    def _reset_all_components(self):
        """Reset all components to their default state."""
        try:
            self.video_url_component.clear_url()
            self.batch_mode_component.clear_urls()
            self.batch_mode_component.batch_mode_var.set(False)
            self.download_settings_component.reset_to_defaults()
            self.excel_integration_component.clear_selection()
            self.log_component.clear_log()
            self.log_component.set_status("Ready")
            
            self.log_component.log_message("All components reset to defaults", "INFO")
            messagebox.showinfo("Reset Complete", "All components have been reset to their default state")
                
        except Exception as e:
            self.log_component.log_message(f"Reset error: {str(e)}", "ERROR")
            messagebox.showerror("Reset Error", f"Error resetting components: {str(e)}")
    
    def _show_component_info(self):
        """Show information about all components."""
        try:
            info = "Component Information:\n\n"
            
            # Video URL component info
            url = self.video_url_component.get_url()
            info += f"Video URL: {'Set' if url else 'Not set'}\n"
            
            # Batch mode component info
            batch_enabled = self.batch_mode_component.is_batch_mode_enabled()
            batch_urls = self.batch_mode_component.get_urls()
            info += f"Batch Mode: {'Enabled' if batch_enabled else 'Disabled'}\n"
            info += f"Batch URLs: {len(batch_urls)} found\n"
            
            # Settings component info
            settings = self.download_settings_component.get_settings()
            info += f"Output Directory: {settings['output_dir']}\n"
            info += f"Quality: {settings['quality']}\n"
            info += f"Audio Only: {'Yes' if settings['extract_audio'] else 'No'}\n"
            info += f"Metadata: {'Yes' if settings['add_metadata'] else 'No'}\n"
            info += f"Excel Export: {'Yes' if settings['export_to_excel'] else 'No'}\n"
            
            # Excel integration info
            excel_file = self.excel_integration_component.get_excel_file_path()
            url_column = self.excel_integration_component.get_selected_url_column()
            info += f"Excel File: {'Selected' if excel_file else 'Not selected'}\n"
            info += f"URL Column: {'Selected' if url_column else 'Not selected'}\n"
            
            # Log component info
            log_lines = self.log_component.get_log_line_count()
            info += f"Log Lines: {log_lines}\n"
            
            messagebox.showinfo("Component Information", info)
                
        except Exception as e:
            self.log_component.log_message(f"Component info error: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"Error getting component information: {str(e)}")
    
    def run(self):
        """Run the test GUI."""
        try:
            self.log_component.log_message("Component test GUI started", "INFO")
            self.log_component.log_message("Use the test buttons to test individual components", "INFO")
            self.root.mainloop()
        except Exception as e:
            print(f"Test GUI error: {e}")
            raise


class MockExcelLoader:
    """
    Mock Excel loader for testing purposes.
    
    This class provides mock implementations of Excel loader methods
    to allow testing of the Excel integration component without
    requiring actual Excel files.
    """
    
    def get_column_names(self, file_path):
        """Mock method to return column names."""
        return ["ID", "Title", "URL", "Description", "Date"]
    
    def get_excel_preview(self, file_path, column_name, max_preview=5):
        """Mock method to return Excel preview."""
        return f"Preview of column '{column_name}':\n- Sample URL 1\n- Sample URL 2\n- Sample URL 3"
    
    def extract_urls_from_column(self, file_path, column_name, validator=None):
        """Mock method to return sample URLs."""
        sample_urls = [
            "https://www.tiktok.com/@user1/video/111111111",
            "https://www.tiktok.com/@user2/video/222222222",
            "https://www.tiktok.com/@user3/video/333333333"
        ]
        return sample_urls


def main():
    """Main function to run the component test GUI."""
    try:
        print("Starting Component Test GUI...")
        print("This will test all modular components of the TikTok Downloader GUI")
        print("Use the test buttons to verify component functionality")
        print()
        
        app = ComponentTestGUI()
        app.run()
        
    except Exception as e:
        print(f"Failed to start test GUI: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
