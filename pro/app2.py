import flet as ft
import json
import os
import asyncio

# Directory for storing state files
STATE_DIR = "clicker_states"
os.makedirs(STATE_DIR, exist_ok=True)

# Base directory for static files (e.g., images, fonts)
BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, "assets")

# Paths for images and fonts
COIN_IMAGE_PATH = "/root/lilcoin/lil_coinbot/pro/LaCoin.png.png"
FONT_PATH = os.path.join(STATIC_DIR, "fonts", "FulboArgenta.ttf")

# State file path for a specific user
def get_state_file(user_id):
    return os.path.join(STATE_DIR, f"{user_id}_state.json")

# Load state from file
def load_state(user_id):
    state_file = get_state_file(user_id)
    try:
        if os.path.exists(state_file):
            with open(state_file, "r") as file:
                state = json.load(file)
            return state
    except Exception as e:
        print(f"Error loading state: {e}")
    return {"score": 0, "progress_value": 0}

# Save state to file
def save_state(user_id, score, progress_value):
    state_file = get_state_file(user_id)
    try:
        with open(state_file, "w") as file:
            json.dump({"score": score, "progress_value": progress_value}, file)
    except Exception as e:
        print(f"Error saving state: {e}")

async def main(page: ft.Page) -> None:
    user_id = "user123"  # Set a unique ID for the user
    page.title = "Lil Clicker"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#141221"
    page.fonts = {"FulboArgenta": FONT_PATH}
    page.theme = ft.Theme(font_family="FulboArgenta")

    # Load state
    state = load_state(user_id)
    score_value = state["score"]
    progress_value = state["progress_value"]

    # Create interface elements
    score_text = ft.Text(value=str(score_value), size=60, color="white", weight="bold")

    # Coin image
    coin_image = ft.Image(
        src=COIN_IMAGE_PATH,
        fit=ft.ImageFit.CONTAIN,
        scale=1.0,
        width=150,
        height=150,
    )

    # Progress bar
    progress_bar = ft.ProgressBar(
        value=progress_value,
        width=300,
        bar_height=20,
        color="#ff8b1f",
        bgcolor="#bf6524"
    )

    async def score_up(event: ft.ContainerTapEvent) -> None:
        nonlocal score_value, progress_value
        score_value += 1
        score_text.value = str(score_value)

        # Animate coin scale on click
        coin_image.scale = 0.85  # Scale down to 85%
        page.update()  # Update UI
        await asyncio.sleep(0.1)  # Delay for smoothness
        coin_image.scale = 1.0  # Scale back to 100%
        page.update()  # Update UI

        # Update progress bar
        progress_value = min(1, progress_value + 0.01)
        progress_bar.value = progress_value
        progress_bar.animate_value = ft.Animation(
            duration=100,
            curve=ft.AnimationCurve.EASE_IN_OUT
        )
        page.update()  # Update UI

        # Save user state
        save_state(user_id, score_value, progress_value)

    # Clickable container with the coin image
    click_container = ft.Container(
        content=coin_image,
        on_click=score_up,
        alignment=ft.alignment.center,
        width=200,
        height=200,
    )

    # Layout with centered elements
    page.add(
        ft.Column(
            controls=[
                score_text,
                click_container,
                ft.Container(
                    content=progress_bar,
                    border_radius=ft.BorderRadius(10),
                    alignment=ft.alignment.center
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=8001)
