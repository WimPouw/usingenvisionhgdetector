# Create the enhanced webcam demo script
from envisionhgdetector import RealtimeGestureDetector
import pandas as pd
import os
from datetime import datetime

def run_webcam_demo():
    """
    Enhanced webcam demo with post-processing and organized output.
    """
    print("LightGBM Real-time Gesture Detection Demo")
    print("=" * 50)
    
    # Initialize detector with refinement parameters
    try:
        detector = RealtimeGestureDetector(
            confidence_threshold=0.7,
            min_gap_s=0.2,          # Minimum gap between gesture segments
            min_length_s=0.1        # Minimum gesture duration
        )
        print("LightGBM detector initialized successfully!")
        print(f"Model features: {detector.model.expected_features}")
        print(f"Gesture labels: {detector.model.gesture_labels}")
        print(f"Advanced features: {'ENABLED' if detector.model.includes_fingers else 'DISABLED'}")
    except Exception as e:
        print(f"Error initializing detector: {e}")
        return None
    
    print("\nStarting enhanced webcam demo...")
    print("Controls:")
    print("  - Q: Quit session")
    print("  - SPACE: Show current status")
    print("  - +/=: Increase confidence threshold")
    print("  - -: Decrease confidence threshold")
    print("\nPosition yourself in front of the camera and start gesturing!")
    print("   (The system will start detecting after a few frames to build a buffer)\n")
    
    try:
        # Run enhanced webcam processing with post-processing
        raw_results, segments = detector.process_webcam(
            duration=None,               # Unlimited duration (use Q to quit)
            camera_index=0,              # Default camera
            show_display=True,           # Show real-time window
            save_video=True,             # Save annotated video
            apply_post_processing=True   # Apply segment refinement
        )
        
        print(f"\nSession complete! Processed {len(raw_results)} frames")
        
        if not raw_results.empty:
            # Analyze raw results
            gesture_frames = len(raw_results[raw_results['gesture'] != 'NoGesture'])
            gesture_percentage = (gesture_frames/len(raw_results)*100) if len(raw_results) > 0 else 0
            unique_gestures = raw_results[raw_results['gesture'] != 'NoGesture']['gesture'].unique()
            avg_confidence = raw_results['confidence'].mean()
            
            print(f"Raw gesture frames: {gesture_frames} ({gesture_percentage:.1f}%)")
            print(f"Average confidence: {avg_confidence:.3f}")
            print(f"Unique gestures detected: {list(unique_gestures)}")
            
            # Analyze processed segments
            if not segments.empty:
                total_segments = len(segments)
                total_gesture_time = segments['duration'].sum()
                avg_segment_duration = segments['duration'].mean()
                
                print(f"\nProcessed Segments:")
                print(f"Total segments: {total_segments}")
                print(f"Total gesture time: {total_gesture_time:.1f}s")
                print(f"Average segment duration: {avg_segment_duration:.1f}s")
                print(f"Gestures per minute: {total_segments / (raw_results['timestamp'].max() / 60):.1f}")
                
                # Show segment details
                print(f"\nSegment Details:")
                for idx, seg in segments.iterrows():
                    print(f"  {idx+1}: {seg['label']} ({seg['start_time']:.1f}s - {seg['end_time']:.1f}s, {seg['duration']:.1f}s)")
            else:
                print("\nNo gesture segments found after post-processing")
                
            # Show output files
            print(f"\nFiles saved in output_realtime/ folder:")
            print(f"- Raw frame results CSV")
            print(f"- Processed segments CSV")
            print(f"- Webcam session video")
            print(f"- Session summary JSON")
        else:
            print("No data recorded (session may have been too short)")
        
        return raw_results, segments
        
    except KeyboardInterrupt:
        print("\nSession interrupted by user")
        return None, None
    except Exception as e:
        print(f"\nError during webcam processing: {e}")
        return None, None

def quick_test():
    """Quick test without webcam to verify installation."""
    print("Quick Installation Test")
    print("-" * 30)
    try:
        detector = RealtimeGestureDetector(confidence_threshold=0.2)
        print("RealtimeGestureDetector imported successfully")
        print("LightGBM model loaded")
        print("MediaPipe initialized")
        print("Installation test passed! Ready for webcam demo.")
        return True
    except Exception as e:
        print(f"Installation test failed: {e}")
        return False

def analyze_previous_session():
    """Analyze a previous session from output_realtime folder."""
    import glob
    
    # Find most recent session
    session_folders = glob.glob("output_realtime/session_*")
    if not session_folders:
        print("No previous sessions found in output_realtime/")
        return
    
    latest_session = max(session_folders, key=lambda x: os.path.getctime(x))
    print(f"Loading latest session: {latest_session}")
    
    try:
        detector = RealtimeGestureDetector(confidence_threshold=0.2)
        raw_df, segments_df = detector.load_and_analyze_session(latest_session)
        
        if not raw_df.empty:
            print("\nSession Analysis:")
            gesture_frames = len(raw_df[raw_df['gesture'] != 'NoGesture'])
            print(f"Total frames: {len(raw_df)}")
            print(f"Gesture frames: {gesture_frames} ({gesture_frames/len(raw_df)*100:.1f}%)")
            print(f"Session duration: {raw_df['timestamp'].max():.1f}s")
            
            if not segments_df.empty:
                print(f"Processed segments: {len(segments_df)}")
                print(f"Total gesture time: {segments_df['duration'].sum():.1f}s")
        
        return raw_df, segments_df
        
    except Exception as e:
        print(f"Error analyzing session: {e}")
        return None, None

if __name__ == "__main__":
    import sys
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            quick_test()
        elif sys.argv[1] == "analyze":
            analyze_previous_session()
        else:
            print("Usage:")
            print("  python webcam_demo.py        # Run webcam demo")
            print("  python webcam_demo.py test   # Test installation")
            print("  python webcam_demo.py analyze # Analyze previous session")
    else:
        # Run the full webcam demo
        if quick_test():
            print("\n" + "="*50)
            input("Press Enter to start webcam demo (or Ctrl+C to cancel)...")
            raw_results, segments = run_webcam_demo()
        else:
            print("\nPlease fix installation issues before running webcam demo")