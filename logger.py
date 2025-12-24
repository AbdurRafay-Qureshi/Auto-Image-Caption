"""
Logger Script - Captures terminal output and saves to log file
Usage: python logger.py python main.py
"""
import sys
import os
import subprocess
from datetime import datetime
from config import LOG_FOLDER


def capture_and_log(command):
    """
    Run a command and capture its output to both terminal and log file
    
    Args:
        command: Command to run (e.g., ['python', 'main.py'])
    """
    # Create logs folder if it doesn't exist
    os.makedirs(LOG_FOLDER, exist_ok=True)
    
    # Create timestamped log filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(LOG_FOLDER, f"image_processing_{timestamp}.txt")
    
    print(f"Starting logging to: {log_filename}\n")
    print("="*80)
    
    # Open log file for writing
    with open(log_filename, 'w', encoding='utf-8') as log_file:
        # Write header to log file
        log_file.write(f"Image Processing Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write("="*80 + "\n\n")
        log_file.flush()
        
        # Run the command and capture output in real-time
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Read output line by line
        for line in process.stdout:
            # Print to terminal
            print(line, end='')
            # Write to log file
            log_file.write(line)
            log_file.flush()
        
        # Wait for process to complete
        process.wait()
        
        # Write footer
        log_file.write("\n" + "="*80 + "\n")
        log_file.write(f"Process completed with exit code: {process.returncode}\n")
        log_file.write(f"Log ended at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print("="*80)
    print(f"\nLog saved to: {log_filename}")
    print(f"Exit code: {process.returncode}")
    
    return process.returncode


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python logger.py <command>")
        print("Example: python logger.py python main.py")
        sys.exit(1)
    
    # Get the command to run
    command = sys.argv[1:]
    
    # Run and capture
    exit_code = capture_and_log(command)
    
    # Exit with same code as the process
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
