import time
import sys
import random
import threading
import keyboard
import tkinter as tk
import pyautogui  # For typing text easily

from PIL import Image
import win32api
import win32con

# ------------------------------
# GLOBALS for the Tkinter GUI
# ------------------------------
root = None
counter_label = None

# ------------------------------
# TKINTER GUI FUNCTIONS
# ------------------------------
def update_gui(total_pixels):
    global root, counter_label
    root = tk.Tk()
    root.title("Pixel Counter")

    screen_width = root.winfo_screenwidth()
    window_width = 200
    window_height = 100
    x_position = screen_width - window_width - 300
    y_position = 50

    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    root.attributes('-topmost', True)

    counter_label = tk.Label(root, text=f"Pixels Left: {total_pixels}", font=("Arial", 14))
    counter_label.pack(pady=20)

    root.mainloop()

def update_pixel_count(pixels_left):
    if counter_label and counter_label.winfo_exists():
        counter_label.config(text=f"Pixels Left: {pixels_left}")
        counter_label.update_idletasks()

# ------------------------------
# HELPER: MOUSE CLICK
# ------------------------------
def click(x, y):
    win32api.SetCursorPos((x, y))
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    time.sleep(0.01)

# ------------------------------
# COLOR SELECTION IN PAINT
# ------------------------------
color_chooser_coords = {
    "open":  (1044, 109),
    "red":   (1078, 378),
    "green": (1081, 422),
    "blue":  (1080, 468),
    "ok":    (814,  786),
}

def set_color_in_paint(r, g, b):
    click(*color_chooser_coords["open"])
    time.sleep(0.3)
    
    click(*color_chooser_coords["red"])
    for _ in range(3):
        keyboard.press_and_release('backspace')
    pyautogui.typewrite(str(r), interval=0.02)
    time.sleep(0.1)

    click(*color_chooser_coords["blue"])
    for _ in range(3):
        keyboard.press_and_release('backspace')
    pyautogui.typewrite(str(b), interval=0.02)
    time.sleep(0.1)

    click(*color_chooser_coords["green"])
    for _ in range(3):
        keyboard.press_and_release('backspace')
    pyautogui.typewrite(str(g), interval=0.02)
    time.sleep(0.1)

    click(*color_chooser_coords["ok"])
    time.sleep(0.2)

# ------------------------------
# LOCAL DRAWING FUNCTIONS
# ------------------------------
def draw_pixels_locally(pixel_set, total_remaining, offset_x, offset_y):
    """
    Draws all pixels in pixel_set using the provided offset values.
    """
    if not pixel_set:
        return
    
    current_pixel = random.choice(list(pixel_set))

    while pixel_set:
        if keyboard.is_pressed('q'):
            print("Exiting on 'q' press.")
            sys.exit()
        
        if current_pixel not in pixel_set:
            if pixel_set:
                current_pixel = random.choice(list(pixel_set))
            else:
                break

        x, y = current_pixel
        screen_x = x + offset_x + random.randint(-1, 1)
        screen_y = y + offset_y + random.randint(-1, 1)
        win32api.SetCursorPos((screen_x, screen_y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, screen_x, screen_y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, screen_x, screen_y, 0, 0)
        
        time.sleep(0.00001)

        pixel_set.remove(current_pixel)
        total_remaining[0] -= 1
        update_pixel_count(total_remaining[0])

        # Find next neighbor
        next_neighbor = find_neighbor_within_radius(x, y, pixel_set)
        if next_neighbor is not None:
            current_pixel = next_neighbor
        else:
            if pixel_set:
                current_pixel = random.choice(list(pixel_set))
            else:
                break

def find_neighbor_within_radius(cx, cy, remaining_pixels):
    """
    Searches for a valid neighbor in an expanding radius around (cx, cy).
    Returns a single random neighbor if found, otherwise None.
    """
    radius = 1
    while True:
        candidates = [(cx + dx, cy + dy)
                      for dx in range(-radius, radius + 1)
                      for dy in range(-radius, radius + 1)
                      if (dx, dy) != (0, 0) and (cx + dx, cy + dy) in remaining_pixels]

        if candidates:
            return random.choice(candidates)

        radius += 1
        if radius > 100:  # Prevent infinite loops
            return None

# ------------------------------
# BOUNDARY TESTING FUNCTION
# ------------------------------
def draw_test_boundaries(bbox, offset_x, offset_y, line_half_length=5):
    """
    Draws short horizontal lines at the top (min_y) and bottom (max_y) edges,
    and short vertical lines at the left (min_x) and right (max_x) edges of the image.
    The lines are drawn centered horizontally or vertically.
    """
    min_x, min_y, max_x, max_y = bbox
    center_x = (min_x + max_x) // 2
    center_y = (min_y + max_y) // 2

    # Draw horizontal line at the top (highest pixel)
    for dx in range(-line_half_length, line_half_length + 1):
        x = center_x + dx
        y = min_y
        win32api.SetCursorPos((x + offset_x, y + offset_y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x + offset_x, y + offset_y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x + offset_x, y + offset_y, 0, 0)
        time.sleep(0.005)

    # Draw horizontal line at the bottom (lowest pixel)
    for dx in range(-line_half_length, line_half_length + 1):
        x = center_x + dx
        y = max_y
        win32api.SetCursorPos((x + offset_x, y + offset_y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x + offset_x, y + offset_y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x + offset_x, y + offset_y, 0, 0)
        time.sleep(0.005)

    # Draw vertical line at the left (most left pixel)
    for dy in range(-line_half_length, line_half_length + 1):
        x = min_x
        y = center_y + dy
        win32api.SetCursorPos((x + offset_x, y + offset_y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x + offset_x, y + offset_y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x + offset_x, y + offset_y, 0, 0)
        time.sleep(0.005)

    # Draw vertical line at the right (most right pixel)
    for dy in range(-line_half_length, line_half_length + 1):
        x = max_x
        y = center_y + dy
        win32api.SetCursorPos((x + offset_x, y + offset_y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x + offset_x, y + offset_y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x + offset_x, y + offset_y, 0, 0)
        time.sleep(0.005)

# ------------------------------
# IMAGE PREPROCESSING FUNCTION
# ------------------------------
def preprocess_image(image_path):
    """
    Converts the image to 8-bit color (256 colors max), computes a palette,
    groups pixels by color (skipping near-white), and computes the bounding box
    of all drawn pixels.
    Returns a tuple: (sorted_colors, bounding_box)
    """
    original = Image.open(image_path).convert('RGB')
    width, height = original.size

    # Reduce the image to 8-bit (256 colors max)
    quantized_img = original.quantize(colors=256, method=2)
    palette = quantized_img.getpalette()
    pixels_by_color = {}

    # Initialize bounding box values
    min_x, min_y = width, height
    max_x, max_y = 0, 0

    for x in range(width):
        for y in range(height):
            color_index = quantized_img.getpixel((x, y)) * 3
            r, g, b = palette[color_index], palette[color_index + 1], palette[color_index + 2]

            # Skip near-white colors
            if r >= 253 and g >= 253 and b >= 253:
                continue  

            # Update bounding box
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y

            if (r, g, b) not in pixels_by_color:
                pixels_by_color[(r, g, b)] = set()
            pixels_by_color[(r, g, b)].add((x, y))

    sorted_colors = sorted(pixels_by_color.items(), key=lambda item: len(item[1]), reverse=True)
    bounding_box = (min_x, min_y, max_x, max_y)
    return sorted_colors, bounding_box

# ------------------------------
# MAIN FUNCTION
# ------------------------------
def main():
    IMAGE_PATH = 'koga1.png'
    # Define offset values here (change these to reposition the drawing)
    offset_x = 100
    offset_y = 185

    print("Precomputing colors and pixel sets...")
    sorted_colors, bounding_box = preprocess_image(IMAGE_PATH)

    total_pixels = sum(len(s) for _, s in sorted_colors)
    print(f"Total pixels across 8-bit colors: {total_pixels}")

    print("Press 'p' to start drawing, or 'w' to test boundaries.")
    # Wait until the user presses 'p' to begin drawing;
    # allow testing the boundaries with 'w' in the meantime.
    while True:
        if keyboard.is_pressed('p'):
            break
        if keyboard.is_pressed('w'):
            print("Drawing test boundaries...")
            draw_test_boundaries(bounding_box, offset_x, offset_y)
            time.sleep(0.5)  # Pause to avoid multiple triggers
        time.sleep(0.1)

    total_remaining = [total_pixels]
    gui_thread = threading.Thread(target=update_gui, args=(total_remaining[0],))
    gui_thread.daemon = True
    gui_thread.start()

    for (r, g, b), pixel_set in sorted_colors:
        if not pixel_set:
            continue
        set_color_in_paint(r, g, b)
        draw_pixels_locally(pixel_set, total_remaining, offset_x, offset_y)

    print("All colors processed (white & near-white skipped)! Press 'q' to quit.")
    while True:
        if keyboard.is_pressed('q'):
            sys.exit()
        time.sleep(0.1)

if __name__ == "__main__":
    main()
