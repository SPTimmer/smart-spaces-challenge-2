import turtle


def interpolate_to_pixels(lon, lat, real_top_left, real_bottom_right, img_top_left, img_bottom_right):
    real_min_lon, real_max_lat = real_top_left
    real_max_lon, real_min_lat = real_bottom_right

    img_min_x, img_min_y = img_top_left
    img_max_x, img_max_y = img_bottom_right

    x = img_min_x + (img_max_x - img_min_x) * (lon - real_min_lon) / (real_max_lon - real_min_lon)
    y = img_min_y + (img_max_y - img_min_y) * (real_max_lat - lat) / (real_max_lat - real_min_lat)

    return x, y


def visualize_estimated_position(lon, lat):
    real_top_left = (6.856322520445769, 52.239400231057886)
    real_bottom_right = (6.8568134791365365, 52.2390876824689)

    img_top_left = (0, 0)
    img_bottom_right = (1518, 685)  # Adjust based on image size

    x, y = interpolate_to_pixels(lon, lat, real_top_left, real_bottom_right, img_top_left, img_bottom_right)

    screen = turtle.Screen()
    screen.setup(width=1518, height=685)
    screen.bgpic('src/data/map.gif')  # Adjust path if needed

    turtle.penup()
    turtle.goto(x, y)
    turtle.dot(10, "red")
    turtle.done()
    return
