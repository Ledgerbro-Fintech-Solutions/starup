import re

for filename in ['app/src/main/java/com/example/emiyo/feature/capture/FaceCaptureScreen.kt', 'app/src/main/java/com/example/emiyo/feature/capture/FullBodyCaptureScreen.kt']:
    with open(filename, 'r') as f:
        code = f.read()

    # Add imports
    imports = """
import androidx.camera.core.ImageCapture
import androidx.core.content.ContextCompat
import com.example.emiyo.core.design.InAppCameraPreview
import com.example.emiyo.core.design.takePhoto
"""
    code = code.replace("import com.example.emiyo.core.design.WardrobeTheme\n", "import com.example.emiyo.core.design.WardrobeTheme\n" + imports)

    # Replace takePictureLauncher with imageCapture
    old_launcher = """    // Camera Capture Launcher
    val takePictureLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.TakePicturePreview()
    ) { bitmap: Bitmap? ->
        if (bitmap != null) {
            val newPhoto = CapturedFacePhoto(
                bitmap = bitmap,
                angle = currentAngle
            )
            capturedPhotos = capturedPhotos + newPhoto
            latestBitmap = bitmap
        }
    }"""
    new_launcher = """    val imageCapture = remember { ImageCapture.Builder().build() }
    val mainExecutor = ContextCompat.getMainExecutor(context)"""
    code = code.replace(old_launcher, new_launcher)

    # Replace launchCamera
    old_launchCamera = """    fun launchCamera() {
        val permissionCheck = ContextCompat.checkSelfPermission(context, Manifest.permission.CAMERA)
        if (permissionCheck == PackageManager.PERMISSION_GRANTED) {
            takePictureLauncher.launch(null)
        } else {
            cameraPermissionLauncher.launch(Manifest.permission.CAMERA)
        }
    }"""
    new_launchCamera = """    fun launchCamera() {
        val permissionCheck = ContextCompat.checkSelfPermission(context, Manifest.permission.CAMERA)
        if (permissionCheck == PackageManager.PERMISSION_GRANTED) {
            takePhoto(
                imageCapture = imageCapture,
                executor = mainExecutor,
                onImageCaptured = { bitmap ->
                    val newPhoto = CapturedFacePhoto(bitmap = bitmap, angle = currentAngle)
                    capturedPhotos = capturedPhotos + newPhoto
                    latestBitmap = bitmap
                },
                onError = { exc ->
                    Toast.makeText(context, "Photo capture failed: ${exc.message}", Toast.LENGTH_SHORT).show()
                }
            )
        } else {
            cameraPermissionLauncher.launch(Manifest.permission.CAMERA)
        }
    }"""
    code = code.replace(old_launchCamera, new_launchCamera)

    # Replace preview inside the Box
    old_preview_block_1 = """                // Portrait Feed: latest captured photo or default demo portrait
                if (latestBitmap != null) {
                    Image(
                        bitmap = latestBitmap!!.asImageBitmap(),
                        contentDescription = "Live camera photo preview",
                        contentScale = ContentScale.Crop,
                        modifier = Modifier.fillMaxSize()
                    )
                } else {
                    Image(
                        painter = painterResource(id = R.drawable.face_capture_demo),
                        contentDescription = "Default camera demo preview",
                        contentScale = ContentScale.Crop,
                        alignment = Alignment.Center,
                        modifier = Modifier.fillMaxSize()
                    )
                }"""
                
    old_preview_block_2 = """                // Background dummy or live image
                if (latestBitmap != null) {
                    Image(
                        bitmap = latestBitmap!!.asImageBitmap(),
                        contentDescription = "Captured Photo",
                        contentScale = ContentScale.Crop,
                        modifier = Modifier.fillMaxSize()
                    )
                } else {
                    Image(
                        painter = painterResource(id = R.drawable.full_body_capture_demo),
                        contentDescription = "Live Camera Preview",
                        contentScale = ContentScale.Crop,
                        modifier = Modifier.fillMaxSize()
                    )
                }"""

    new_preview_block = """                val permissionCheck = ContextCompat.checkSelfPermission(context, Manifest.permission.CAMERA)
                if (permissionCheck == PackageManager.PERMISSION_GRANTED) {
                    InAppCameraPreview(imageCapture = imageCapture)
                } else {
                    Box(modifier = Modifier.fillMaxSize().background(Color.Black))
                }
                
                // Show latest captured photo frozen over the preview if exists
                if (latestBitmap != null) {
                    Image(
                        bitmap = latestBitmap!!.asImageBitmap(),
                        contentDescription = "Live camera photo preview",
                        contentScale = ContentScale.Crop,
                        modifier = Modifier.fillMaxSize()
                    )
                }"""
                
    if "face_capture_demo" in code:
        code = code.replace(old_preview_block_1, new_preview_block)
    else:
        code = code.replace(old_preview_block_2, new_preview_block)

    with open(filename, 'w') as f:
        f.write(code)
