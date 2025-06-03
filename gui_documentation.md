# GUI Module Documentation

This document provides a summary of the Python files within the `gui` directory and its subdirectories, explaining their purpose and functionality.

## `gui` Directory

### `board_cell.py`
The `BoardCell` class (a `QFrame`) represents a single interactive cell on a game board. It can display an image (like a game piece or a move indicator) and has a defined background color based on its `CellType` (LIGHT or DARK).

- **Initialization**: Takes an optional image name, cell type, and its board position. It sets a fixed size based on `Constants.CELL_SIZE` and applies styling for background, border-radius, and a drop shadow.
- **Image Handling**:
    - `set_image(image_name)`: Loads and displays an image (e.g., 'xMark.svg', 'whitePiece.svg') from the `gui/assets/svg` or `gui/assets/images` directory. Images are scaled: player pieces are scaled to a calculated `target_image_dimension` (derived from cell size and padding), while other images are scaled only if they exceed this dimension. If an image is not found or fails to load, the cell's image label is cleared.
    - `_find_image_path(root_dir, image_name)`: A helper to locate image files within a specified root directory and its subdirectories.
- **Interaction**: Emits `bus.cellClicked.emit(self.position)` via the global signal bus when clicked with the left mouse button.
- **Styling**: Uses `Constants` and `Colors` from `gui.core.confiq` for sizing and theming. The cell has rounded corners and a drop shadow effect.

### `board.py`
The `Board` class is a `QWidget` that visually represents a game board, such as for Tic-Tac-Toe or Checkers (Dame). It uses a `QGridLayout` to arrange `BoardCell` widgets. The board's appearance (background color, cell spacing) is configured using constants from `gui.core.confiq`.

- **Initialization**: Takes the initial `board_state` (a 2D list or similar representing pieces), a boolean `is_dame` to handle game-specific logic (like row inversion for Dame and different piece images), and optionally a list of `possible_moves`. For each cell, it determines if it's a `LIGHT` or `DARK` cell type for alternating colors. It then sets the appropriate image on the `BoardCell`: a move indicator if the cell is a possible move, or a piece image ('xMark.svg', 'oMark.svg' for TicTacToe; 'whitePiece.svg', 'blackPiece.svg' for Dame) based on the `board_state`.
- **Methods**:
    - `show_possible_moves(possible_moves)`: Clears previous indicators and displays new ones for valid moves. It handles different formats for `possible_moves` (e.g., a list of tuples for target positions, or more complex move structures including start and end positions).
    - `update_board(new_board_state)`: Refreshes the entire board by updating the images in all `BoardCell` instances based on the `new_board_state`.
- **Sizing**: The overall size of the board widget is calculated based on cell size, board dimensions, and spacing.

### `customListWidget.py`
The `CustomListWidget` class implements a custom dropdown/select widget. It consists of a `QLabel` (`display_label`) that shows the current selection or a title, and a `QListWidget` that pops up below the label when clicked. This mimics a standard combobox behavior but with custom styling.

- **Initialization**: Takes a title and a list of items to display.
- **Styling**: Items in the popup list and the display label are styled with specific background and foreground colors from `gui.core.confiq.Colors`. The overall appearance (borders, colors, font size) is customized.
- **Interaction**:
    - Clicking the `display_label` toggles the visibility of the popup `QListWidget`.
    - When an item is selected from the popup list, the `display_label` updates, a `selectionChanged` signal is emitted with the selected text, and the popup closes.
    - The popup list closes automatically if the user clicks outside of the widget (handled by an event filter).
- **Methods**:
    - `add_items(items)`: Populates or repopulates the list.
    - `get_selected_item_text()`: Returns the currently selected item's text.
    - `set_selected_index(index)`: Programmatically sets the selection.

### `gameController.py`
The `GameController` class acts as an intermediary between the game logic (from `games.dame` or `games.tic_tac_toe`) and the GUI. It manages the game state, player turns, and AI moves using the `ai.minimax.Minimax` algorithm.

- **Initialization**: Takes `game_type` ("Dame" or "TicTacToe") and `difficulty`.
- **Methods**:
    - `get_board()`: Returns the current game board state.
    - `set_difficulty(max_depth)`: Changes AI difficulty and resets the game.
    - `handle_cell_click(position)`: Processes a human player's click. For Dame, it handles piece selection and move execution (including multi-captures). For TicTacToe, it attempts a direct move. Returns possible moves or a game status string (e.g., "ai_turn_pending", win status).
    - `make_ai_move()`: Uses Minimax AI to find and make a move. Returns game status and a boolean indicating if the AI has more moves (for Dame multi-captures).
    - `reset_game()`: Resets the game to its initial state.
    - `reset_selection()`: Clears selected piece/moves (Dame).
    - `_is_valid_position()`: Validates board coordinates.
    - `_resync_dame_piece_sets()`: Utility to update internal piece sets for Dame.

### `gameOverDialog.py`
The `GameOverOverlayWidget` is a `QWidget` shown when a game ends. It displays a status message (e.g., "You Won!"), a leaderboard, and "Restart Game" / "Game Select" buttons.

- **Initialization**: Sets a fixed size, loads "JetBrainsMono-Bold" font from assets.
- **Styling**: Uses `Colors` from `gui.core.confiq` for background, text, borders, and table/button elements.
- **Content**:
    - `statusLabel`: Displays the game outcome.
    - `scoreboardTable`: A `QTableWidget` showing top player scores (username, wins, losses) for the game mode/difficulty, fetched via `database.DataQueries.getPlayersWithMostWins`.
- **Interaction**: Emits `restartClicked` or `mainMenuClicked` signals.
- **Methods**:
    - `_populate_scoreboard(gamemode, difficulty)`: Fills the table with scores. Handles errors by showing a "Could not load" message.
    - `update_contents(status_message, gamemode_int, difficulty_int)`: Sets the status message and refreshes the scoreboard.
- Includes an `if __name__ == '__main__':` block for standalone testing.

### `gameSetupForm.py`
The `GameSetupForm` (a `MenuContainer`) allows users to select a game ("Dame", "TicTacToe") and difficulty ("Easy", "Medium", "Hard") via segmented button controls.

- **Initialization**: Loads "JetBrainsMono-Bold" font. Sets up UI elements for game and difficulty selection.
- **Styling**: Uses `Colors` from `gui.core.confiq`. Buttons are styled to indicate selection.
- **Interaction**:
    - Clicking game/difficulty buttons updates the selection and button styles.
    - "Start" button emits `playRequested` signal with the selected game (string) and difficulty (integer: Easy=1, Medium=3, Hard=5).
- **Layout**: Dynamically adjusts button group heights for consistency.

### `imageWidget.py`
The `ImageWidget` (a `QLabel`) simplifies displaying images from the `gui/assets` directory.

- **Initialization**: Takes `image_name`, and optional `scaled` (bool), `max_size` (tuple), `alignment`.
- **Functionality**:
    - `_find_image_path()`: Searches `gui/assets` and subdirectories for the image.
    - Loads the image into a `QPixmap`.
    - Scales the image if `max_size` is provided or `scaled` is true (though `setScaledContents` is the primary scaling mechanism if `max_size` isn't used for pre-scaling).
    - Handles image not found/load errors silently (after cleanup).
- **Debugging**: A `DEBUGGING` flag, if `True`, adds a red border for layout aid.

### `inputField.py`
The `InputField` class is a subclass of `QLineEdit` providing a styled text input field.

- **Initialization**: Configurable `width`, `height`, `padding`, `background` color, `text_color`, `placeholder_text`, and `is_password` (for password echo mode).
- **Styling**: Applies a stylesheet for background color, text color, padding, border (none), border-radius, and font size. Placeholder text color is also styled.
- **Interaction**: Emits a `returnPressed` signal when the Enter or Return key is pressed.

### `loginForm.py`
The `LoginForm` (a `MenuContainer`) provides a UI for user login.

- **Elements**: Username/password `InputField`s, "Login" button (`MyButton`), "Play as Guest" button (`MyButton`), and a "sign up here" link (`MyButton` of type `LINK`).
- **Signals**:
    - `loginAttempt(username, password)`
    - `guestAccessRequested`
    - `signupRequested`
- **Functionality**:
    - Basic validation (non-empty fields).
    - `display_error()` / `clear_error()` methods for on-form error messages.
    - Enter key in input fields triggers login attempt.
- **Styling**: Uses `Colors` from `gui.core.confiq`.

### `menuContainer.py`
The `MenuContainer` class is a base `QFrame` for menu-like widgets (e.g., `LoginForm`, `SignupForm`).

- **Properties**:
    - Fixed size: `_fixed_width = 600`, `_fixed_height = 608`.
    - Default background: `Colors.SECONDARY`, 10px border-radius (configurable).
- **Layout**: `QVBoxLayout` with configurable padding (default 50px) and fixed spacing (15px). Widgets added via `addWidget()` are centered horizontally, aligned top.
- `sizeHint()`: Returns its fixed size.
- **Purpose**: Provides a standardized container for forms.

### `myButton.py`
The `MyButton` class is a custom `QPushButton` with enhanced styling capabilities.

- **Types**: `ButtonType.NORMAL` (standard button with border, background, optional shadow) and `ButtonType.LINK` (styled like a hyperlink).
- **Initialization**: Takes `text`, `button_type`, `borderWidth`, `fontSize`, `padding`, `background_color`, `border_color`, `text_color`, and `font` (supports 'jbmono' for JetBrainsMono-Bold or 'suburbia' for SUBURBIA font, loaded from `gui/assets/fonts`).
- **Styling**:
    - Loads specified font.
    - Sets pointing hand cursor.
    - **Normal Button**: Applies background color, border, border-radius, padding, and text color. Adds a `QGraphicsDropShadowEffect` if `borderWidth > 0`.
    - **Link Button**: Transparent background, no border, underlined text. Text color defaults to blue if not specified or if `Colors.FONT_PRIMARY` is passed (unless overridden). Hover color changes.
- Uses `Colors` from `gui.core.confiq`.

### `rule.py`
The `Rule` class (a `QLabel`) displays a single game rule.

- **Initialization**: Takes `rule_id`, `text`, and optional `bold` state. Enables word wrap.
- **Methods**:
    - `updateStyle()`: Sets text and applies stylesheet (text color, font weight based on `self.bold`).
    - `setBold(bold: bool)`: Updates bold state and refreshes style.
- Used by `RulesToggle` to display individual, highlightable rules.

### `rules.py`
The `RulesToggle` widget displays a list of game rules, toggleable by a button.

- **Initialization**: Takes a game instance (subclass of `BaseGame`) and optional `violated_ids`. Has a fixed size.
- **Content**:
    - Rules are fetched via `game.get_rules()` and displayed as `Rule` objects within a `rulesWidget` (styled with `Colors.SECONDARY` background).
    - Uses "JetBrainsMono-Bold" font for rule text.
- **Toggle Button**: Uses `rulesButton.svg` from `gui/assets/svg` (falls back to "!" text if not found). Clicking it shows/hides `rulesWidget`.
- **Method**: `setViolatedRules(violated_ids)`: Highlights rules (makes them bold) whose IDs are in `violated_ids`.

### `signalBus.py`
Defines a global signal bus for application-wide communication between Qt components.
- `SignalBus(QObject)`:
    - `cellClicked = Signal(object)`: Emitted by `BoardCell` when clicked, carrying cell position.
- `bus = SignalBus()`: A global instance for easy access.

### `signupForm.py`
The `SignupForm` (a `MenuContainer`) provides a UI for new user registration.

- **Elements**: Username/password `InputField`s, "Sign up" button, "Already have an account?" label, "login here" link (`MyButton` type `LINK`), "Play as Guest" button.
- **Signals**:
    - `signupAttempted(username, password)`
    - `loginLinkActivated`
    - `guestAccessRequested`
- **Functionality**:
    - Basic validation (non-empty fields).
    - `display_error()` / `clear_error()` for on-form error messages.
- **Styling**: Uses `Colors` from `gui.core.confiq`.

### `window.py`
The `WindowModule` class is the main QWidget that structures the application window, including a persistent navbar and a content frame for dynamic views.

- **Structure**:
    - `navbar`: A top bar (`NAVBAR_HEIGHT` = 80px, `Colors.SECONDARY` background) containing:
        - `navbarLabel`: "NOTEPADGAMES" title (SUBURBIA font from assets).
        - `usernameLabel`: Displays logged-in user's name (SUBURBIA font, hidden by default).
        - `logoutButton`: SVG icon button, shown when user is logged in. Emits `logoutButtonClicked`.
        - `homeButton`: SVG icon button, shown conditionally. Emits `homeButtonClicked`.
    - `contentFrame`: A `QFrame` where different views/widgets (like forms, game boards) are displayed.
- **Pivot Enum**: `TOP_LEFT`, `TOP_RIGHT`, `BOTTOM_LEFT`, `BOTTOM_RIGHT`, `CENTER` for positioning child widgets.
- **Methods**:
    - `addChildWidget(widget, x, y, pivot)`: Adds a widget to `contentFrame` at specified coordinates relative to the frame, using a pivot point for alignment. Handles widgets with `_fixed_width`/`_fixed_height` (like `MenuContainer`) or uses `sizeHint`.
    - `removeWidget(widget)`: Hides, unparents, and deletes a widget from `contentFrame`.
    - `showHomeButton()` / `hideHomeButton()`: Controls visibility of the home button.
    - `update_username_display(username)`: Shows/hides username and logout button.
    - `getContentFrameCenter()`: Returns the center coordinates of `contentFrame`.
- **Styling**: Uses `Colors` for navbar and fonts. Loads "SUBURBIA.ttf" and SVG icons from `gui/assets`.

### `__init__.py`
An empty initialization file, marking the `gui` directory as a Python package. This allows modules within `gui` to be imported using package notation (e.g., `from gui.window import WindowModule`).

## `gui/assets` Directory
This directory serves as a central repository for all static assets used by the GUI. It is organized into subdirectories:
-   `fonts/`: Contains font files (e.g., `.ttf`) used for custom text rendering in various UI elements. Examples include "SUBURBIA.ttf" and "JetBrainsMono-Bold.ttf".
-   `svg/`: Contains Scalable Vector Graphics (`.svg`) files, typically used for icons (e.g., "homeButton.svg", "logoutButton.svg", "rulesButton.svg", piece images like "xMark.svg", "oMark.svg", "whitePiece.svg", "blackPiece.svg", and indicators like "moveIndicator.svg").
-   It might also contain other image formats (like `.png`, `.jpeg`) in subdirectories like `images/` or directly within `assets/` if not categorized further, though the current usage seems to favor SVGs for icons and game pieces.

The `ImageWidget` and `BoardCell` classes, for instance, load images from this directory structure. Fonts are loaded by various widgets like `WindowModule`, `GameOverOverlayWidget`, `RulesToggle`, and `MyButton`.

## `gui/core` Directory

### `confiq.py`
This module centralizes configuration constants for the GUI. It defines three classes:
-   `Colors`: Contains static string attributes representing hex color codes (e.g., `PRIMARY`, `SECONDARY`, `FONT_PRIMARY`) used for theming the application.
-   `Constants`: Defines numerical constants for UI dimensions and layout (e.g., `CELL_SIZE`, `PADDING`, `BOARD_WIDTH`).
-   `CellType(Enum)`: An enumeration (`LIGHT`, `DARK`) for styling game board cells.

### `test_confiq.py`
This file, named `test_confiq.py`, appears to be either a leftover test file or an incorrectly named/placed configuration file. It contains a commented-out path `# ui/core/rules_config.py` (this comment may still be present if automated cleanup failed) and defines a list named `RULES`. This list contains dictionaries, each representing a rule with an "id" and "text". This structure is not directly related to the contents of `gui/core/confiq.py` and doesn't seem to be actively used by the main GUI components. 