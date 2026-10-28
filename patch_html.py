import re

with open('preview/full_body_capture_preview.html', 'r') as f:
    content = f.read()

# 1. Update the CSS to include photo strip styles
css_to_add = """
    /* Photos Strip Section */
    .photos-strip-section {
      display: flex;
      flex-direction: column;
      margin-top: 24px;
      margin-bottom: 32px;
      padding-bottom: 24px;
    }
    .strip-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }
    .strip-title {
      font-size: 10px;
      font-weight: 600;
      letter-spacing: 1.0px;
      color: var(--wardrobe-muted);
    }
    .strip-counter {
      font-size: 10px;
      color: var(--wardrobe-muted);
    }
    .strip-row {
      display: flex;
      gap: 12px;
      overflow-x: auto;
      padding-bottom: 8px;
    }
    .strip-row::-webkit-scrollbar { display: none; }
    .photo-thumb-card {
      position: relative;
      width: 64px;
      height: 86px;
      border-radius: 8px;
      overflow: hidden;
      flex-shrink: 0;
      background: var(--wardrobe-border);
      cursor: pointer;
    }
    .photo-thumb-card img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
    .thumb-angle-tag {
      position: absolute;
      bottom: 0;
      left: 0;
      width: 100%;
      background: rgba(26, 23, 21, 0.7);
      color: white;
      font-size: 8px;
      font-weight: 600;
      text-align: center;
      padding: 3px 0;
      letter-spacing: 0.5px;
    }
    .thumb-delete-btn {
      position: absolute;
      top: 4px;
      right: 4px;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: rgba(26, 23, 21, 0.6);
      color: white;
      border: none;
      font-size: 14px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
    }
    .add-photo-card {
      width: 64px;
      height: 86px;
      border-radius: 8px;
      border: 1px dashed var(--wardrobe-border);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      cursor: pointer;
      color: var(--wardrobe-sage);
    }
    .shutter-flash {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: white;
      opacity: 0;
      pointer-events: none;
      z-index: 50;
      transition: opacity 0.1s ease-out;
    }
    .shutter-flash.flashing { opacity: 0.8; }
    .hint-badge {
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: rgba(125, 139, 114, 0.2);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      margin-right: 6px;
    }
    .hint-badge svg {
      width: 9px;
      height: 9px;
      stroke: #5D6B52;
      stroke-width: 2.2;
      fill: none;
    }
    .quality-hint {
      display: flex;
      align-items: center;
      font-size: 11px;
      color: var(--wardrobe-muted);
    }
    .quality-hint > svg {
      display: none; /* hide old plain svg */
    }
  </style>
"""
content = content.replace("  </style>", css_to_add)

# 2. Add Shutter Flash inside camera viewport & ID to image
content = content.replace('<img src="full_body_background.png" alt="Full Body Camera Preview">', '<img id="previewImage" src="full_body_background.png" alt="Full Body Camera Preview"><div class="shutter-flash" id="shutterFlash"></div>')

# 3. Add ID to view pills to control active state dynamically
content = content.replace('<div class="view-pill active">', '<div class="view-pill active" id="pill-FRONT">')
content = content.replace('<div class="view-pill">\n            <div class="indicator-dot"></div>\n            SIDE\n          </div>', '<div class="view-pill" id="pill-SIDE">\n            <div class="indicator-dot"></div>\n            SIDE\n          </div>')
content = content.replace('<div class="view-pill">\n            <div class="indicator-dot"></div>\n            BACK\n          </div>', '<div class="view-pill" id="pill-BACK">\n            <div class="indicator-dot"></div>\n            BACK\n          </div>')

# 4. Add ID to step badge
content = content.replace('<span class="proportion-value" style="font-size: 11px;">01 / 03</span>', '<span class="proportion-value" id="stepAngleValue" style="font-size: 11px;">01 / 03</span>')
content = content.replace('<span class="proportion-label" style="font-size: 10px;">- FRONT</span>', '<span class="proportion-label" id="stepAngleLabel" style="font-size: 10px;">- FRONT</span>')

# 5. Replace Quality Hints with Hint Badges
hints_html = """
      <!-- Quality Indicators -->
      <div class="quality-row">
        <div class="quality-hint">
          <div class="hint-badge"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"></polyline></svg></div>
          Good lighting
        </div>
        <div class="quality-hint">
          <div class="hint-badge"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"></polyline></svg></div>
          Face visible
        </div>
        <div class="quality-hint">
          <div class="hint-badge"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"></polyline></svg></div>
          Look straight
        </div>
      </div>
"""
content = re.sub(r'<!-- Quality Indicators -->.*?</div>.*?</div>', hints_html, content, flags=re.DOTALL)


# 6. Add on clicks to buttons
content = content.replace('<button class="btn-primary" type="button">', '<button class="btn-primary" type="button" onclick="handleTakePhoto()">')
content = content.replace('<button class="btn-secondary" type="button">', '<button class="btn-secondary" type="button" onclick="document.getElementById(\'galleryInput\').click()">')
content = content.replace('<button class="btn-secondary" type="button" onclick="document.getElementById(\'galleryInput\').click()">', '<button class="btn-secondary" type="button" onclick="document.getElementById(\'galleryInput\').click()">\n<input type="file" id="galleryInput" multiple accept="image/*" style="display:none;" onchange="handleGalleryUpload(event)">')

# 7. Add Photo Strip Section and Script
photos_strip_html = """
      <!-- Horizontal Photo Strip (YOUR PHOTOS) -->
      <div class="photos-strip-section" id="photosStripSection" style="display: none;">
        <div class="strip-header">
          <span class="strip-title">YOUR PHOTOS</span>
          <span class="strip-counter" id="photoCounterText">0 captured</span>
        </div>
        <div class="strip-row" id="photoThumbnailRow">
          <!-- Thumbnail Cards dynamically injected -->
          <div class="add-photo-card" onclick="handleTakePhoto()" title="Add another photo">
            <span class="add-photo-plus">+</span>
            <span class="add-photo-text">ADD</span>
          </div>
        </div>
      </div>
"""
content = content.replace('<!-- Continue Button (Disabled State) -->', photos_strip_html + '\n      <!-- Continue Button (Disabled State) -->')

# Update continue button ID
content = content.replace('<button class="btn-continue" type="button">', '<button class="btn-continue" type="button" id="btnContinue" onclick="handleContinue()">')


script_html = """
  <script>
    let capturedPhotos = [];
    const defaultDemoImage = 'full_body_background.png';

    const previewImage = document.getElementById('previewImage');
    const shutterFlash = document.getElementById('shutterFlash');
    const photosStripSection = document.getElementById('photosStripSection');
    const photoThumbnailRow = document.getElementById('photoThumbnailRow');
    const photoCounterText = document.getElementById('photoCounterText');
    const btnContinue = document.getElementById('btnContinue');
    
    const stepAngleValue = document.getElementById('stepAngleValue');
    const stepAngleLabel = document.getElementById('stepAngleLabel');
    
    const pillFront = document.getElementById('pill-FRONT');
    const pillSide = document.getElementById('pill-SIDE');
    const pillBack = document.getElementById('pill-BACK');

    function triggerFlash() {
      shutterFlash.classList.add('flashing');
      setTimeout(() => shutterFlash.classList.remove('flashing'), 100);
    }

    function handleTakePhoto() {
      triggerFlash();
      const nextIndex = capturedPhotos.length;
      let angle = nextIndex === 0 ? 'FRONT' : nextIndex === 1 ? 'SIDE' : 'BACK';

      capturedPhotos.push({
        id: 'photo_' + Date.now(),
        src: defaultDemoImage,
        angle: angle
      });
      renderState();
    }

    function handleGalleryUpload(e) {
      const files = e.target.files;
      if (!files || files.length === 0) return;
      Array.from(files).forEach((file) => {
        const reader = new FileReader();
        reader.onload = function(evt) {
          const nextIndex = capturedPhotos.length;
          let angle = nextIndex === 0 ? 'FRONT' : nextIndex === 1 ? 'SIDE' : 'BACK';
          capturedPhotos.push({
            id: 'photo_' + Date.now() + '_' + Math.random(),
            src: evt.target.result,
            angle: angle
          });
          renderState();
        };
        reader.readAsDataURL(file);
      });
      e.target.value = '';
    }

    function removePhoto(id, e) {
      if (e) e.stopPropagation();
      capturedPhotos = capturedPhotos.filter(p => p.id !== id);
      renderState();
    }

    function selectPhoto(src) {
      previewImage.src = src;
    }

    function renderState() {
      const count = capturedPhotos.length;

      pillFront.classList.remove('active');
      pillSide.classList.remove('active');
      pillBack.classList.remove('active');

      if (count === 0) {
        stepAngleValue.textContent = '01 / 03';
        stepAngleLabel.textContent = '- FRONT';
        previewImage.src = defaultDemoImage;
        pillFront.classList.add('active');
      } else if (count === 1) {
        stepAngleValue.textContent = '02 / 03';
        stepAngleLabel.textContent = '- SIDE';
        previewImage.src = capturedPhotos[0].src;
        pillSide.classList.add('active');
      } else if (count === 2) {
        stepAngleValue.textContent = '03 / 03';
        stepAngleLabel.textContent = '- BACK';
        previewImage.src = capturedPhotos[1].src;
        pillBack.classList.add('active');
      } else {
        stepAngleValue.textContent = '03 / 03';
        stepAngleLabel.textContent = '- COMPLETE';
        previewImage.src = capturedPhotos[capturedPhotos.length - 1].src;
        pillFront.classList.add('active'); // front is active when complete too
      }

      if (count > 0) {
        photosStripSection.style.display = 'flex';
        photoCounterText.textContent = `${count} captured`;
        let html = '';
        capturedPhotos.forEach((photo) => {
          html += `
            <div class="photo-thumb-card" onclick="selectPhoto('${photo.src}')">
              <img src="${photo.src}" alt="${photo.angle}">
              <div class="thumb-angle-tag">${photo.angle}</div>
              <button class="thumb-delete-btn" onclick="removePhoto('${photo.id}', event)">×</button>
            </div>
          `;
        });
        html += `
          <div class="add-photo-card" onclick="handleTakePhoto()">
            <span class="add-photo-plus">+</span>
            <span class="add-photo-text">ADD</span>
          </div>
        `;
        photoThumbnailRow.innerHTML = html;
      } else {
        photosStripSection.style.display = 'none';
      }

      if (count >= 3) {
        btnContinue.classList.add('active');
      } else {
        btnContinue.classList.remove('active');
      }
    }
  </script>
</body>
"""
content = content.replace('</body>', script_html)

with open('preview/full_body_capture_preview.html', 'w') as f:
    f.write(content)
