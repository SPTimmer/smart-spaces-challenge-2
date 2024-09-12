import turtle

# These are the width and height in pixels of map.gif
MAP_WIDTH = 1518
MAP_HEIGHT = 685

# These coordinates are the closest to what I could get of the corners of the Zilverling building
top_left = (52.239610, 6.856340)
bottom_right = (52.239120, 6.856850)

screen = None
marker = None


# This function calculates the pixel coordinates relative to the image size
def convert_to_pixel_coords(lat, lon):
    lat_range = top_left[0] - bottom_right[0]
    lon_range = bottom_right[1] - top_left[1]

    x_ratio = (lon - top_left[1]) / lon_range
    y_ratio = (top_left[0] - lat) / lat_range

    x_pixel = int(x_ratio * MAP_WIDTH)
    y_pixel = int(y_ratio * MAP_HEIGHT)

    print(f"Debug: Latitude: {lat}, Longitude: {lon}")
    print(f"Debug: Converted X pixel: {x_pixel}, Y pixel: {y_pixel}")

    return x_pixel, y_pixel


# This function visualizes the estimated coordinates
def visualize_estimated_position(lat, lon):
    global screen, marker

    if screen is None:
        screen = turtle.Screen()
        screen.setup(width=MAP_WIDTH, height=MAP_HEIGHT)
        screen.bgpic("src/data/map.gif")

    screen.clearscreen()
    screen.bgpic("src/data/map.gif")

    x_pixel, y_pixel = convert_to_pixel_coords(lat, lon)

    if x_pixel < 0 or x_pixel > MAP_WIDTH or y_pixel < 0 or y_pixel > MAP_HEIGHT:
        print(f"Coordinates ({x_pixel}, {y_pixel}) are out of bounds. Skipping visualization.")
        return

    marker = turtle.Turtle()
    marker.penup()
    marker.shape("circle")
    marker.color("red")

    marker.goto(x_pixel - MAP_WIDTH // 2, y_pixel - MAP_HEIGHT // 2)
    marker.stamp()

    print(f"Displaying marker at ({x_pixel}, {y_pixel}) on the map.")
