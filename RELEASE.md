# 🚀 Creating Releases for HORUS

This guide explains how to create releases with Mac and Windows builds automatically.

## Method 1: Manual Release (Recommended for First Release)

1. **Go to GitHub Actions**
   - Navigate to your repository on GitHub
   - Click on the "Actions" tab
   - Click on "Build and Release" workflow

2. **Run Workflow Manually**
   - Click "Run workflow" button (on the right)
   - Enter a version number (e.g., `v1.0.0`)
   - Click "Run workflow" (green button)

3. **Wait for Build to Complete**
   - The workflow will build for both Mac and Windows (takes ~10-15 minutes)
   - You can watch the progress in the Actions tab

4. **Check Your Release**
   - Go to "Releases" section in your repository
   - You'll see a new release with downloadable files:
     - `HORUS-{version}.dmg` (Mac installer)
     - `HORUS-{version}-mac.zip` (Mac archive)
     - `HORUS Setup {version}.exe` (Windows installer)
     - `HORUS {version}.exe` (Windows portable)

## Method 2: Automatic Release with Git Tags

1. **Create and Push a Tag**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **Automatic Build**
   - GitHub Actions will automatically trigger
   - Builds will be created for Mac and Windows
   - Release will be published automatically

## Method 3: Build Locally

If you want to build on your own machine:

### Prerequisites
- macOS (for Mac builds) or Windows (for Windows builds)
- Node.js 18+ installed
- npm installed

### Build Commands

```bash
# Install dependencies first
npm install

# Build for your current platform
npm run build

# Or build for specific platforms
npm run build:mac    # macOS only (must run on macOS)
npm run build:win    # Windows only
npm run build:all    # Both (only works if you have both environments)
```

Built files will be in the `dist/` directory.

## Release Versioning

Follow semantic versioning:
- `v1.0.0` - Major release
- `v1.1.0` - Minor update (new features)
- `v1.0.1` - Patch (bug fixes)

## GitHub Actions Workflow

The workflow automatically:
1. ✅ Builds on macOS runner (for Mac app)
2. ✅ Builds on Windows runner (for Windows app)
3. ✅ Creates installers and portable versions
4. ✅ Uploads artifacts
5. ✅ Creates GitHub release
6. ✅ Attaches all build files
7. ✅ Generates release notes

## Troubleshooting

### Build Fails
- Check GitHub Actions logs for errors
- Ensure `package.json` is correct
- Make sure all dependencies are listed

### No Artifacts in Release
- Check if builds completed successfully
- Look for error messages in the Actions log
- Verify the `dist/` folder has files

### Code Signing (macOS)
For distribution outside the App Store, you'll need:
- Apple Developer account
- Add signing certificate to repository secrets
- Update `electron-builder.yml` with signing config

## First Release Checklist

- [ ] Workflow file committed and pushed
- [ ] Go to GitHub → Actions tab
- [ ] Click "Build and Release" workflow
- [ ] Click "Run workflow"
- [ ] Enter version (e.g., `v1.0.0`)
- [ ] Click green "Run workflow" button
- [ ] Wait for builds to complete (~10-15 min)
- [ ] Check Releases page for new release
- [ ] Download and test the installers
- [ ] Share the release URL!

## Example Release URL

After creating a release, share it with users:
```
https://github.com/itsgiddd/Horus/releases/latest
```

Or specific version:
```
https://github.com/itsgiddd/Horus/releases/tag/v1.0.0
```

---

🎉 **That's it!** Your Mac and Windows builds will be automatically created and published!
