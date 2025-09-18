// AR Viewer for dish models
class ARViewer {
    constructor() {
        this.isARSupported = false;
        this.checkARSupport();
    }
    
    checkARSupport() {
        if (navigator.xr) {
            navigator.xr.isSessionSupported('immersive-ar')
                .then(supported => {
                    this.isARSupported = supported;
                    if (supported) {
                        console.log('AR is supported on this device');
                    } else {
                        console.log('AR is not supported on this device');
                    }
                })
                .catch(err => {
                    console.error('Error checking AR support:', err);
                    this.isARSupported = false;
                });
        } else {
            console.log('WebXR not available');
            this.isARSupported = false;
        }
    }
    
    initViewer(modelUrl, canvasElement) {
        if (!this.isARSupported) {
            this.showFallbackViewer(modelUrl, canvasElement);
            return;
        }
        
        // Set up Three.js scene for AR
        this.setupThreeJSScene(modelUrl, canvasElement);
    }
    
    setupThreeJSScene(modelUrl, canvasElement) {
        // This would be a complete Three.js AR implementation
        // For this example, we'll show a simplified version
        
        console.log('Initializing AR viewer for model:', modelUrl);
        
        // In a real implementation, we would:
        // 1. Set up scene, camera, renderer
        // 2. Load the 3D model
        // 3. Set up AR session
        // 4. Handle rendering
        
        // For demonstration, we'll show a placeholder
        canvasElement.innerHTML = `
            <div class="ar-placeholder">
                <h3>AR View</h3>
                <p>AR functionality would be displayed here</p>
                <p>Model: ${modelUrl.split('/').pop()}</p>
                <button class="ar-fallback-btn">View 3D Model</button>
            </div>
        `;
        
        // Add event listener for fallback button
        const fallbackBtn = canvasElement.querySelector('.ar-fallback-btn');
        fallbackBtn.addEventListener('click', () => {
            this.showFallbackViewer(modelUrl, canvasElement);
        });
    }
    
    showFallbackViewer(modelUrl, container) {
        // Show a fallback 3D viewer for devices that don't support AR
        console.log('Showing fallback 3D viewer for:', modelUrl);
        
        // Determine file type
        const extension = modelUrl.split('.').pop().toLowerCase();
        
        if (extension === 'glb' || extension === 'gltf') {
            // For GLB/GLTF models, we could use a library like Three.js
            container.innerHTML = `
                <div class="fallback-viewer">
                    <h3>3D Model View</h3>
                    <p>AR is not supported on your device. Showing 3D model instead.</p>
                    <div class="model-container" id="model-container"></div>
                    <div class="viewer-controls">
                        <button class="rotate-btn">Rotate</button>
                        <button class="zoom-in-btn">Zoom In</button>
                        <button class="zoom-out-btn">Zoom Out</button>
                    </div>
                </div>
            `;
            
            // In a real implementation, we would load the model here
            this.load3DModel(modelUrl, container.querySelector('#model-container'));
        } else {
            // For images or unsupported formats
            container.innerHTML = `
                <div class="image-fallback">
                    <h3>Model Preview</h3>
                    <p>AR is not supported on your device.</p>
                    <img src="${modelUrl}" alt="3D Model Preview" style="max-width: 100%;">
                </div>
            `;
        }
    }
    
    load3DModel(modelUrl, container) {
        // This would load the 3D model using Three.js or similar library
        console.log('Loading 3D model:', modelUrl);
        
        // Placeholder implementation
        container.innerHTML = `
            <div style="width: 100%; height: 300px; background: #eee; display: flex; 
                        justify-content: center; align-items: center; border: 1px solid #ccc;">
                <p>3D Model would be displayed here: ${modelUrl.split('/').pop()}</p>
            </div>
        `;
        
        // In a real implementation, we would:
        // 1. Initialize Three.js renderer
        // 2. Load the model
        // 3. Set up controls
        // 4. Animate the scene
    }
    
    // Method to launch AR from a button
    launchAR(modelUrl) {
        if (!this.isARSupported) {
            alert('AR is not supported on your device. Please try on a compatible smartphone.');
            return;
        }
        
        // In a real implementation, this would launch the AR experience
        console.log('Launching AR experience for:', modelUrl);
        
        // For demonstration, open a new window with a placeholder
        const arWindow = window.open('', '_blank');
        arWindow.document.write(`
            <html>
            <head>
                <title>AR Experience</title>
                <style>
                    body { font-family: Arial, sans-serif; text-align: center; padding: 2rem; }
                    .ar-placeholder { margin: 2rem auto; padding: 2rem; border: 2px dashed #ccc; }
                </style>
            </head>
            <body>
                <h1>AR Experience</h1>
                <div class="ar-placeholder">
                    <h2>AR View Would Appear Here</h2>
                    <p>Point your camera at a flat surface to place the model.</p>
                    <p>Model: ${modelUrl.split('/').pop()}</p>
                </div>
                <button onclick="window.close()">Close AR</button>
            </body>
            </html>
        `);
    }
}

// Initialize AR viewer when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.arViewer = new ARViewer();
    
    // Add AR buttons to dish detail pages
    const arButtons = document.querySelectorAll('.view-ar-btn');
    arButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const modelUrl = this.dataset.modelUrl;
            window.arViewer.launchAR(modelUrl);
        });
    });
});