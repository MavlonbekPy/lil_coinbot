import flet as ft
import json
import os
import asyncio

# Папка для хранения состояния
STATE_DIR = "clicker_states"

# Убедитесь, что папка существует
os.makedirs(STATE_DIR, exist_ok=True)

# Файл для хранения состояния
def get_state_file(user_id):
    return os.path.join(STATE_DIR, f"{user_id}_state.json")

# Load state from file
def load_state(user_id):
    state_file = get_state_file(user_id)
    try:
        if os.path.exists(state_file):
            with open(state_file, "r") as file:
                state = json.load(file)
            print(f"Loaded state for {user_id}: Score = {state['score']}, Progress = {state['progress_value']}")
            return state
        else:
            print(f"State file for {user_id} does not exist. Returning default state.")
    except Exception as e:
        print(f"Error loading state: {e}")
    return {"score": 0, "progress_value": 0}

# Save state to file
def save_state(user_id, score, progress_value):
    state_file = get_state_file(user_id)
    try:
        with open(state_file, "w") as file:
            json.dump({"score": score, "progress_value": progress_value}, file)
        print(f"Saved state for {user_id}: Score = {score}, Progress = {progress_value}")
    except Exception as e:
        print(f"Error saving state: {e}")

async def main(page: ft.Page) -> None:
    user_id = "user123"  # Здесь можно добавить логику для получения уникального ID пользователя
    page.title = "Lil Clicker"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#141221"
    page.fonts = {"FulboArgenta": "fonts/FulboArgenta.ttf"}
    page.theme = ft.Theme(font_family="FulboArgenta")

    # Load state
    state = load_state(user_id)
    score_value = state["score"]
    progress_value = state["progress_value"]

    # Create interface elements
    score = ft.Text(value=str(score_value), size=50)  # Уменьшен размер текста

    # Coin image
    coin_image = ft.Image(
        src="lacoin.png",  # Убедитесь, что путь к изображению корректен
        fit=ft.ImageFit.CONTAIN,
        scale=1.0
    )

    progress_bar = ft.ProgressBar(
        value=progress_value,
        width=page.width - 100,
        bar_height=20,
        color="#ff8b1f",
        bgcolor="#bf6524"
    )

    async def score_up(event: ft.ContainerTapEvent) -> None:
        nonlocal score_value, progress_value
        score_value += 1
        score.value = str(score_value)

        # Coin image scale animation
        coin_image.scale = 0.8  # Уменьшаем до 80%
        page.update()  # Обновляем интерфейс
        await asyncio.sleep(0.1)  # Задержка для плавности
        coin_image.scale = 1.0  # Возвращаем к 100%
        page.update()  # Обновляем интерфейс

        progress_value = min(1, progress_value + 0.01)
        progress_bar.value = progress_value
        progress_bar.animate_value = ft.Animation(
            duration=100,
            curve=ft.AnimationCurve.EASE_IN_OUT
        )
        page.update()  # Обновляем интерфейс

        save_state(user_id, score_value, progress_value)  # Сохраняем состояние для текущего пользователя

    click_container = ft.Container(
        content=coin_image,
        on_click=score_up,
        margin=ft.Margin(0, 0, 0, 30)
    )

    # Проверяем наличие файла перед загрузкой изображения
    small_image_path = "Coin2.png.png"  # Убедитесь, что путь к изображению корректен
    if os.path.exists(small_image_path):
        small_image = ft.Image(
            src=small_image_path,
            fit=ft.ImageFit.CONTAIN,
            scale=1.0,
            width=50,
            height=50
        )
    else:
        small_image = ft.Text("Image not found", size=20)

    page.add(
        ft.Column(
            controls=[
                score,
                click_container,
                ft.Container(
                    content=progress_bar,
                    border_radius=ft.BorderRadius(top_left=10, top_right=10, bottom_left=10, bottom_right=10)
                ),
                small_image  # Добавляем маленькую фотографию внизу
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=8000)