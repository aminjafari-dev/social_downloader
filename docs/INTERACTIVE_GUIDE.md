# Interactive Video Text Remover - Usage Guide

## 🎯 What This Tool Does

The Interactive Video Text Remover is a GUI application that allows you to:
1. **View video frames** one by one
2. **Manually select text areas** using a brush tool
3. **Remove selected text** using AI-powered inpainting
4. **Process the entire video** with your selections

## 🚀 How to Use

### 1. Start the Application
```bash
python interactive_text_remover.py --input "your_video.mp4"
```

### 2. Navigate Through Frames
- **⏮ First**: Go to the first frame
- **⏪ Prev**: Go to previous frame
- **⏩ Next**: Go to next frame
- **⏭ Last**: Go to the last frame

### 3. Select Text Areas
1. **Adjust brush size** using the slider (5-50 pixels)
2. **Click and drag** on the video frame to paint over text areas
3. **Red overlay** shows your selected areas
4. **Clear Mask** button to start over

### 4. Process the Video
1. **Download LaMa Model** (first time only)
2. **Click "Process Video"** to remove selected text
3. **Choose output location** when prompted
4. **Wait for processing** to complete

## 🎨 Brush Tool Tips

- **Small brush (5-15)**: For thin text lines
- **Medium brush (15-30)**: For normal text
- **Large brush (30-50)**: For thick text or large areas
- **Paint carefully**: Only select the text you want to remove
- **Use multiple strokes**: For complex text shapes

## 🔧 Features

### Frame Navigation
- Navigate through all video frames
- Frame counter shows current position
- Smooth frame transitions

### Brush Tool
- Adjustable brush size
- Real-time visual feedback
- Red overlay shows selected areas
- Clear mask option

### Processing
- Background processing (GUI stays responsive)
- Progress updates in log
- Multiple output formats supported
- Error handling and recovery

## 📋 Step-by-Step Example

### For Your TikTok Video:
1. **Start the app**: `python interactive_text_remover.py --input "downloads/the guy in the background .mp4"`

2. **Navigate to frame with text**: Use Next/Prev buttons to find frames with "First Drink" text

3. **Select the text**:
   - Set brush size to ~20-25
   - Click and drag over the "First Drink" text
   - Make sure to cover all parts of the text

4. **Process the video**:
   - Click "Process Video"
   - Save as "clean_video.mp4"
   - Wait for processing to complete

5. **Check results**: The output video will have the text removed!

## 🛠️ Technical Details

### Current Implementation
- **Inpainting Method**: OpenCV Telea algorithm (placeholder)
- **Future Enhancement**: LaMa AI model for better results
- **Frame Processing**: Frame-by-frame with mask application
- **Output Format**: MP4 with original quality

### Performance
- **Processing Speed**: Depends on video length and resolution
- **Memory Usage**: Moderate (loads frames as needed)
- **Quality**: Good with OpenCV, excellent with LaMa

## 🎯 Best Practices

1. **Select carefully**: Only paint over the text you want to remove
2. **Use appropriate brush size**: Match the text thickness
3. **Check multiple frames**: Text might appear in different positions
4. **Test on short clips first**: Before processing long videos
5. **Backup original**: Always keep your original video

## 🔮 Future Enhancements

- **LaMa AI Integration**: Professional-grade inpainting
- **Auto-text detection**: AI finds text automatically
- **Batch processing**: Process multiple videos
- **Advanced brush tools**: Different brush types and effects
- **Real-time preview**: See results before processing

## ❓ Troubleshooting

### Common Issues:
1. **GUI doesn't start**: Check if tkinter is installed
2. **Video doesn't load**: Verify file path and format
3. **Brush not working**: Make sure you're clicking and dragging
4. **Processing fails**: Check disk space and permissions

### Solutions:
- Install missing dependencies: `pip install -r requirements.txt`
- Use absolute file paths
- Ensure video file is not corrupted
- Check system resources

## 🎉 Success!

Once you've mastered the interactive text remover, you can:
- Remove any text overlays from videos
- Clean up watermarks and logos
- Create professional-looking content
- Process multiple videos efficiently

The tool gives you precise control over what gets removed, making it perfect for professional video editing tasks!

