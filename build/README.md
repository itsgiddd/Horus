# HORUS App Icons

This directory contains the app icons for HORUS desktop application.

## Required Files

You need to add two icon files to this directory:

1. **icon.icns** - macOS app icon (Apple Icon Image format)
2. **icon.ico** - Windows app icon (Windows Icon format)

## How to Create Icon Files

### Option 1: Using Online Converters (Easiest)

1. **CloudConvert** (https://cloudconvert.com/)
   - Upload your icon image (PNG, JPG, etc.)
   - Convert to:
     - `.icns` for macOS
     - `.ico` for Windows
   - Download both files and place them in this directory

2. **iConvert Icons** (https://iconverticons.com/online/)
   - Upload your icon image
   - Select "ICNS" for macOS and "ICO" for Windows
   - Download and place in this directory

### Option 2: Using Command Line Tools

**macOS (for .icns):**
```bash
# Install iconutil (comes with Xcode)
# Create an iconset directory
mkdir icon.iconset

# Resize your icon to multiple sizes (use ImageMagick or similar)
sips -z 16 16     icon.png --out icon.iconset/icon_16x16.png
sips -z 32 32     icon.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32     icon.png --out icon.iconset/icon_32x32.png
sips -z 64 64     icon.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128   icon.png --out icon.iconset/icon_128x128.png
sips -z 256 256   icon.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256   icon.png --out icon.iconset/icon_256x256.png
sips -z 512 512   icon.png --out icon.iconset/icon_256x256@2x.png
sips -z 512 512   icon.png --out icon.iconset/icon_512x512.png
sips -z 1024 1024 icon.png --out icon.iconset/icon_512x512@2x.png

# Convert to .icns
iconutil -c icns icon.iconset
```

**Windows (for .ico):**
```bash
# Using ImageMagick
convert icon.png -define icon:auto-resize=256,128,96,64,48,32,16 icon.ico
```

**Cross-platform (using electron-icon-builder):**
```bash
# Install globally
npm install -g electron-icon-builder

# Generate both .icns and .ico from a single PNG
electron-icon-builder --input=./icon.png --output=./build
```

### Option 3: Using npm package (Recommended for automation)

Install `electron-icon-maker`:
```bash
npm install --save-dev electron-icon-maker
```

Add to package.json scripts:
```json
"scripts": {
  "build-icon": "electron-icon-maker --input=./icon.png --output=./build"
}
```

Then run:
```bash
npm run build-icon
```

## Icon Requirements

### Size Requirements
- **Minimum recommended size:** 1024x1024 pixels
- **Format:** PNG with transparent background works best for conversion
- **Aspect ratio:** Square (1:1)

### Quality Guidelines
- Use high-resolution source image
- Transparent background recommended
- Simple, recognizable design (works well at small sizes)
- Avoid fine details that won't be visible at 16x16

## Current Configuration

The app is configured to use these icons in `package.json`:

```json
"build": {
  "mac": {
    "icon": "build/icon.icns"
  },
  "win": {
    "icon": "build/icon.ico"
  }
}
```

## Testing Your Icons

After placing icon files in this directory:

**macOS:**
```bash
npm run build:mac
```

**Windows:**
```bash
npm run build:win
```

**Both platforms:**
```bash
npm run build:all
```

The built app will have your custom icon!

## Troubleshooting

**Icon not showing on macOS:**
- Clear icon cache: `sudo rm -rf /Library/Caches/com.apple.iconservices.store`
- Rebuild the app
- Restart Finder: `killall Finder`

**Icon not showing on Windows:**
- Clear icon cache by deleting `%userprofile%\AppData\Local\IconCache.db`
- Restart Windows Explorer

**Build fails:**
- Ensure icon files are in correct format
- Check file names match exactly: `icon.icns` and `icon.ico`
- Verify files are in `build/` directory

---

**Need help?** Check the electron-builder documentation:
https://www.electron.build/icons
