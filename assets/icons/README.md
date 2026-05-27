# Icons and Images

This folder contains icon files for the py-care application.

## System Tray Icon

The system tray icon can be customized by placing your icon file here.

### Recommended Formats

#### 1. ICO Format (Preferred for Windows)
- **Best choice for Windows**: Native support, multi-resolution in one file
- **Recommended sizes in one .ico file**:
  - 16x16 pixels
  - 32x32 pixels
  - 48x48 pixels
  - 64x64 pixels
  - 256x256 pixels

#### 2. PNG Format (Alternative)
- **Recommended sizes**: 256x256 or 512x512 pixels
- Works on all platforms but may not scale as well on Windows

### Creating Icons

**Online Tools**:
- [ICO Convert](https://icoconvert.com/) - Convert PNG to ICO
- [Favicon.io](https://favicon.io/) - Generate icons from text or image
- [RealFaviconGenerator](https://realfavicongenerator.net/) - Comprehensive icon generator

**Desktop Tools**:
- **Windows**: Paint.NET with ICO plugin
- **macOS**: Icon Composer (part of Xcode)
- **Cross-platform**: GIMP (can export as ICO)

### Icon Design Guidelines

For best results:
- **Simple design**: Icons appear small in the system tray
- **High contrast**: Ensure visibility on different backgrounds
- **Recognizable at small sizes**: Test at 16x16 to ensure clarity
- **Match application purpose**: Consider health/care/reminder themes
- **Transparent background**: For PNG files

### Example Icon Concepts for py-care

1. **Eye icon** - Represents eye care and screen breaks
2. **Clock/timer** - Represents scheduled reminders
3. **Heart** - Represents health and self-care
4. **Coffee cup** - Represents break time
5. **Lotus/meditation symbol** - Represents wellness
6. **Computer with check mark** - Represents healthy computer use

### Color Suggestions

- **Blue** (#4A90E2) - Calm, trustworthy, tech-friendly
- **Green** (#4CAF50) - Health, wellness, growth
- **Purple** (#9C27B0) - Care, mindfulness
- **Teal** (#00BCD4) - Fresh, modern, caring

### Using Your Custom Icon

1. **Place your icon file** in this folder (e.g., `tray_icon.ico` or `tray_icon.png`)

2. **Update the code** in `src/tray_icon.py`:

   ```python
   from pathlib import Path
   from PIL import Image
   
   def _create_default_icon(self) -> Image.Image:
       """Load custom icon from assets folder."""
       icon_path = Path(__file__).parent.parent / 'assets' / 'icons' / 'tray_icon.png'
       
       if icon_path.exists():
           return Image.open(icon_path)
       else:
           # Fallback to generated icon
           # ... existing code ...
   ```

### Default Icon

The application includes a generated default icon (blue circle with "C") if no custom icon is provided.

## Dialog Images (Optional)

You can also store images for future enhancements:
- Background images for dialogs
- Logo for about screen
- Custom graphics for different reminder types

---

**Ready-to-use icon templates and examples can be added here!**
