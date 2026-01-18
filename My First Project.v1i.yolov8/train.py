from ultralytics import YOLO
import torch

# Check if CUDA is available for GPU acceleration
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Load YOLOv8 small model for better accuracy
# yolov8s.pt provides better accuracy than yolov8n.pt while still being fast
# For even better accuracy, use: yolov8m.pt (medium) or yolov8l.pt (large)
print("\n📦 Loading YOLOv8 small model for improved accuracy...")
model = YOLO("yolov8s.pt")

# Train the model with optimized parameters for maximum accuracy
print("\n🚀 Starting training with optimized parameters...")
model.train(
    data="data.yaml",
    epochs=200,              # Increased epochs for better convergence
    imgsz=640,               # Image size (640 is optimal for YOLOv8)
    batch=16,                # Batch size (adjust based on GPU memory: 8, 16, 32)
    device=device,            # Use GPU if available, else CPU
    patience=100,             # Early stopping patience (increased for better convergence)
    save=True,
    save_period=10,          # Save checkpoint every N epochs
    # Optimized data augmentation for better generalization
    hsv_h=0.02,              # Hue augmentation (slightly increased)
    hsv_s=0.7,               # Saturation augmentation  
    hsv_v=0.4,               # Value/brightness augmentation
    degrees=15,              # Rotation augmentation (increased for better angle coverage)
    translate=0.15,         # Translation augmentation (increased)
    scale=0.6,               # Scaling augmentation (increased range)
    fliplr=0.5,              # Horizontal flip probability
    mosaic=1.0,              # Mosaic augmentation (helps with small objects)
    mixup=0.15,              # Mixup augmentation (increased for better scratch detection)
    copy_paste=0.1,          # Copy-paste augmentation (helps with defect detection)
    # Advanced training parameters for better accuracy
    optimizer='AdamW',       # AdamW optimizer for better convergence
    lr0=0.001,               # Initial learning rate
    lrf=0.01,                # Final learning rate (lr0 * lrf)
    momentum=0.937,          # SGD momentum/Adam beta1
    weight_decay=0.0005,     # Weight decay
    warmup_epochs=3.0,       # Warmup epochs
    warmup_momentum=0.8,     # Warmup initial momentum
    warmup_bias_lr=0.1,      # Warmup initial bias lr
    box=7.5,                 # Box loss gain
    cls=0.5,                 # Class loss gain
    dfl=1.5,                 # DFL loss gain
    pose=12.0,               # Pose loss gain (if using pose)
    kobj=1.0,                # Keypoint obj loss gain (if using pose)
    # Validation and plotting settings
    val=True,                # Validate during training
    plots=True,              # Save training plots
    # Better NMS settings (for validation/inference)
    iou=0.7,                 # NMS IoU threshold
    conf=0.25,               # Confidence threshold for validation
    max_det=300,             # Maximum detections per image
)

print("\n✅ Training completed!")
print("📊 Check results in: runs/detect/train/")
print("🎯 Best model saved at: runs/detect/train/weights/best.pt")


