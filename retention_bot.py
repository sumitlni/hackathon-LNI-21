#!/usr/bin/env python3
"""
Retention Bot - Single run version
Combines existing video and audio files for employee retention messages
"""

import os
import json
import time
import logging
import subprocess
from typing import List, Optional
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class Employee:
    """Employee data structure"""
    name: str
    position: str

class RetentionBot:
    """Handles video generation and combination for employee retention"""
    
    def __init__(self, output_dir: str = "retention_videos"):
        """Initialize the retention bot"""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def generate_retention_video(self) -> Optional[str]:
        """Generate base retention video using Minimax"""
        try:
            # Generate the video
            video_response = self._run_mcp_tool("mini_max___generate_video", {
                "model": "MiniMax-Hailuo-02",
                "prompt": """
                A young woman in a modern, well-lit office space singing emotionally. 
                She's wearing professional attire and is surrounded by colorful balloons. 
                As she sings 'Please Don't Go' with genuine emotion, she gracefully throws 
                balloons into the air. The balloons float down around her creating a 
                visually striking scene. Her expression conveys both sincerity and warmth.
                """,
                "duration": 6,
                "resolution": "1080P",
                "output_directory": self.output_dir,
                "async_mode": True
            })
            
            # Extract task ID and wait for completion
            task_id = self._extract_task_id(video_response)
            if not task_id:
                logger.error("Failed to get task ID from video generation response")
                return None
            
            logger.info(f"Video generation started with task ID: {task_id}")
            return self._wait_for_video(task_id)
            
        except Exception as e:
            logger.error(f"Error generating retention video: {e}")
            return None
    
    def generate_audio_message(self) -> Optional[str]:
        """Generate base audio message using Minimax"""
        try:
            audio_response = self._run_mcp_tool("mini_max___text_to_audio", {
                "text": """
                You're an invaluable part of our team.
                Your expertise has helped us achieve amazing things.
                We see your potential and have exciting opportunities ahead.
                Please don't go - let's build the future together.
                """,
                "voice_id": "female-shaonv",
                "emotion": "sad",
                "speed": 0.8,
                "output_directory": self.output_dir
            })
            
            audio_path = os.path.join(self.output_dir, "retention_audio.mp3")
            if os.path.exists(audio_path):
                return audio_path
            return None
            
        except Exception as e:
            logger.error(f"Error generating audio message: {e}")
            return None
    
    def create_employee_videos(self, employees: List[Employee], video_path: str, audio_path: str) -> List[str]:
        """Create personalized videos for each employee"""
        output_files = []
        
        for employee in employees:
            output_path = self._combine_media(video_path, audio_path, employee.name)
            if output_path:
                output_files.append(output_path)
                logger.info(f"Created retention video for {employee.name}: {output_path}")
            else:
                logger.error(f"Failed to create retention video for {employee.name}")
        
        return output_files
    
    def _wait_for_video(self, task_id: str, max_attempts: int = 30) -> Optional[str]:
        """Wait for video generation to complete"""
        attempts = 0
        while attempts < max_attempts:
            try:
                logger.info(f"Checking video status (attempt {attempts + 1}/{max_attempts})")
                response = self._run_mcp_tool("mini_max___query_video_generation", {
                    "task_id": task_id,
                    "output_directory": self.output_dir
                })
                
                if "Video generation task is still processing" not in str(response):
                    video_path = os.path.join(self.output_dir, "retention_video.mp4")
                    if os.path.exists(video_path):
                        logger.info("Video generation completed successfully")
                        return video_path
                    else:
                        logger.error("Video file not found after generation")
                        return None
                
            except Exception as e:
                logger.error(f"Error checking video status: {e}")
            
            logger.info("Video still processing, waiting 10 seconds...")
            time.sleep(10)  # Wait 10 seconds between checks
            attempts += 1
        
        logger.error("Video generation timed out")
        return None
    
    def _combine_media(self, video_path: str, audio_path: str, employee_name: str) -> Optional[str]:
        """Combine video and audio using ffmpeg"""
        try:
            output_path = os.path.join(
                self.output_dir, 
                f"retention_message_{employee_name.replace(' ', '_')}.mp4"
            )
            
            cmd = [
                "ffmpeg", "-i", video_path, "-i", audio_path,
                "-c:v", "copy", "-c:a", "aac", "-shortest",
                output_path
            ]
            
            logger.info(f"Combining media for {employee_name}")
            subprocess.run(cmd, check=True, capture_output=True)
            return output_path
            
        except Exception as e:
            logger.error(f"Error combining media for {employee_name}: {e}")
            return None
    
    @staticmethod
    def _run_mcp_tool(tool_name: str, params: dict) -> Optional[dict]:
        """Run an MCP server tool using the AWS CLI"""
        try:
            cmd = [
                "aws", "q", "tools", "call",
                "--tool-name", tool_name,
                "--parameters", json.dumps(params)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return json.loads(result.stdout) if result.stdout else None
            
        except Exception as e:
            logger.error(f"Error running MCP tool {tool_name}: {e}")
            return None
    
    @staticmethod
    def _extract_task_id(response: Optional[dict]) -> Optional[str]:
        """Extract task ID from video generation response"""
        if not response:
            return None
            
        response_str = str(response)
        if "Task ID:" in response_str:
            return response_str.split("Task ID:")[-1].strip().split(".")[0].strip()
        return None

def main():
    """Main function"""
    # Initialize retention bot
    bot = RetentionBot()
    
    # Example employees
    employees = [
        Employee(name="Technical Lead", position="AI/ML Division"),
        Employee(name="Research Scientist", position="NLP Team"),
        Employee(name="ML Engineer", position="Infrastructure Team"),
        Employee(name="AI Ethics", position="Ethics Team")
    ]
    
    # Generate base video
    logger.info("Generating base retention video...")
    video_path = bot.generate_retention_video()
    if not video_path:
        logger.error("Failed to generate base video")
        return
    
    # Generate base audio
    logger.info("Generating base audio message...")
    audio_path = bot.generate_audio_message()
    if not audio_path:
        logger.error("Failed to generate audio message")
        return
    
    # Create personalized videos for each employee
    logger.info("Creating personalized videos for employees...")
    output_files = bot.create_employee_videos(employees, video_path, audio_path)
    
    # Report results
    logger.info("\nGeneration Summary:")
    logger.info(f"Total employees processed: {len(employees)}")
    logger.info(f"Successfully generated videos: {len(output_files)}")
    logger.info("\nGenerated video files:")
    for file in output_files:
        logger.info(f"- {file}")

if __name__ == "__main__":
    main()
