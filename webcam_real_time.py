# Create the webcam demo script
from envisionhgdetector import RealtimeGestureDetector
import pandas as pd
import os
from datetime import datetime

def run_webcam_demo():
    """
    Full webcam demo - run this outside Jupyter notebook.
    """
    print("🚀 LightGBM Real-time Gesture Detection Demo")
    print("=" * 50)
    
    # Initialize detector
    try:
        detector = RealtimeGestureDetector(confidence_threshold=0.2)
        print("✓ LightGBM detector initialized successfully!")
        print(f"✓ Model features: {detector.model.expected_features}")
        print(f"✓ Gesture labels: {detector.model.gesture_labels}")
        print(f"✓ Advanced features: {'ENABLED' if detector.model.includes_fingers else 'DISABLED'}")
    except Exception as e:
        print(f"❌ Error initializing detector: {e}")
        return None
    
    print("\\n🎥 Starting webcam demo...")
    print("📋 Controls:")
    print("  - Q: Quit")
    print("  - Spacebar: Show current status")
    print("  - +/=: Increase confidence threshold")
    print("  - -: Decrease confidence threshold")
    print("\\n📸 Position yourself in front of the camera and start gesturing!")
    print("   (The system will start detecting after a few frames to build a buffer)\\n")
    
    # Create timestamped output files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_csv = f"webcam_results_{timestamp}.csv"
    
    try:
        # Run webcam processing
        results_df = detector.process_webcam(
            duration=None,           # Unlimited duration (use Q to quit)
            camera_index=0,          # Default camera
            show_display=True,       # Show real-time window
            save_video=True,         # Save annotated video
            output_csv=output_csv    # Save results with timestamp
        )
        
        print(f"\\n📊 Session complete! Processed {len(results_df)} frames")
        
        if not results_df.empty:
            # Analyze results
            gesture_frames = len(results_df[results_df['gesture'] != 'NoGesture'])
            gesture_percentage = (gesture_frames/len(results_df)*100) if len(results_df) > 0 else 0
            unique_gestures = results_df[results_df['gesture'] != 'NoGesture']['gesture'].unique()
            avg_confidence = results_df['confidence'].mean()
            
            print(f"Detected gestures in {gesture_frames} frames ({gesture_percentage:.1f}%)")
            print(f"Average confidence: {avg_confidence:.3f}")
            print(f"Unique gestures detected: {list(unique_gestures)}")
            print(f"Results saved to: {output_csv}")
            
            # Find the saved video file
            video_files = [f for f in os.listdir('.') if f.startswith('realtime_webcam_') and f.endswith('.mp4')]
            if video_files:
                latest_video = max(video_files, key=lambda x: os.path.getctime(x))
                print(f"🎬 Annotated video saved to: {latest_video}")
        else:
            print("No data recorded (session may have been too short)")
        
        return results_df
        
    except KeyboardInterrupt:
        print("\\n  Session interrupted by user")
        return None
    except Exception as e:
        print(f"\\n Error during webcam processing: {e}")
        return None

def quick_test():
    """Quick test without webcam to verify installation."""
    print("🔧 Quick Installation Test")
    print("-" * 30)
    try:
        detector = RealtimeGestureDetector(confidence_threshold=0.2)
        print("✓ RealtimeGestureDetector imported successfully")
        print("✓ LightGBM model loaded")
        print("✓ MediaPipe initialized")
        print("✅ Installation test passed! Ready for webcam demo.")
        return True
    except Exception as e:
        print(f"❌ Installation test failed: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    # Check if user wants to run quick test
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        quick_test()
    else:
        # Run the full webcam demo
        if quick_test():
            print("\\n" + "="*50)
            input("Press Enter to start webcam demo (or Ctrl+C to cancel)...")
            results = run_webcam_demo()
        else:
            print("\\n❌ Please fix installation issues before running webcam demo")