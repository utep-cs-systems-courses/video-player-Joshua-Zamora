
import cv2, os
from threading import Thread
from pc import ProductConsumer


def extract_frames(color_images):
    clipFileName = 'clip.mp4'
    count = 0
    vidcap = cv2.VideoCapture(clipFileName)
    success,image = vidcap.read()
    while success and count < 72:
        color_images.put(image)
        
        success,image = vidcap.read()
        
        print(f'Reading frame {count}')
        count += 1
    
    color_images.put(None)

def convert_frames_to_grayscale(gray_images, color_images):
    count = 0
    inputFrame = color_images.get()
    
    while inputFrame is not None:
        print(f'Converting frame {count}')
        grayscaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)

        gray_images.put(grayscaleFrame)
        count += 1

        inputFrame = color_images.get()
    
    gray_images.put(None)


def display_frames(gray_images):
    frameDelay = 42
    count = 0
    frame = gray_images.get()
    
    while frame is not None:
        print(f'Displaying frame {count}')
        cv2.imshow('Video', frame)

        if cv2.waitKey(frameDelay) and 0xFF == ord("q"):
            break    
    
        count += 1
        frame = gray_images.get()
    
    cv2.destroyAllWindows()
    

def main():
    color_images = ProductConsumer()
    gray_images = ProductConsumer()
    
    extract_thread = Thread(target=extract_frames, args=(color_images,))
    convert_thread = Thread(target=convert_frames_to_grayscale, args=(gray_images, color_images))
    display_thread = Thread(target=display_frames, args=(gray_images,))
    
    extract_thread.start()
    convert_thread.start()
    display_thread.start()

    extract_thread.join()
    convert_thread.join()
    display_thread.join()
    
if __name__ == "__main__":
    main()
