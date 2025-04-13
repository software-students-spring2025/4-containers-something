// Wait until the page is fully loaded
window.addEventListener("DOMContentLoaded", () => {
    const video = document.getElementById("video");
    const captureButton = document.getElementById("capture-btn");
    const canvas = document.createElement("canvas");
  
    // Set canvas size for 100x100 image
    canvas.width = 100;
    canvas.height = 100;
    const ctx = canvas.getContext("2d");
  
    // Access webcam with 100x100 constraint
    navigator.mediaDevices.getUserMedia({
      video: { width: 100, height: 100 },
      audio: false
    }).then((stream) => {
      video.srcObject = stream;
      video.play();
    }).catch((err) => {
      console.error("🚨 Camera access failed:", err);
    });
  
    // Capture image on button click
    captureButton.addEventListener("click", () => {
      ctx.drawImage(video, 0, 0, 100, 100);
      const imageData = canvas.toDataURL("image/jpeg");
  
      // Send to Flask backend
      fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: imageData })
      })
      .then(res => res.json())
      .then(data => {
        console.log("✅ Prediction result:", data);
        alert(`Prediction: ${data.prediction} (Confidence: ${data.confidence.toFixed(2)})`);
      })
      .catch(err => {
        console.error("❌ Prediction error:", err);
      });
    });
  });
  