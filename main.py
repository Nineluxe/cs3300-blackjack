import asyncio
import pygame
import traceback
from scripts.gameController import GameController

pygame.init()
pygame.font.init()

# Main asynchronous game loop, needed to work with pygbag
async def main():
    try:
        game = GameController()
        
        frame_count = 0
        while game.isRunning:
            game.run()
            frame_count += 1
            
            # Add a safety exit after 1000 frames for testing
            if frame_count > 1000:
                print(f"Ran {frame_count} frames successfully")
            
            await asyncio.sleep(0)
        
        print("Game loop ended normally")
    except Exception as e:
        print(f"Error in game loop: {e}")
        traceback.print_exc()
    
    pygame.quit()

asyncio.run(main())