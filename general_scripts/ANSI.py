import shutil


class ANSI:
    """A collection of ANSI escape sequences for terminal styling and control."""

    #!^ ── Main ───────────────────────────────────────────────────────────────
    RESET           = "\033[0m"
    NEW_LINE        = "\n"
    SAPERATOR       = "─" * shutil.get_terminal_size().columns

    #!^ ── Text styles ────────────────────────────────────────────────────────
    BOLD            = "\033[1m"
    DIM             = "\033[2m"
    ITALIC          = "\033[3m"
    UNDERLINE       = "\033[4m"
    BLINK           = "\033[5m"
    BLINK_FAST      = "\033[6m"
    INVERSE         = "\033[7m"
    HIDDEN          = "\033[8m"
    STRIKE          = "\033[9m"

    #!^ ── Foreground (text) colors ───────────────────────────────────────────
    BLACK           = "\033[30m"
    RED             = "\033[31m"
    GREEN           = "\033[32m"
    YELLOW          = "\033[33m"
    BLUE            = "\033[34m"
    MAGENTA         = "\033[35m"
    CYAN            = "\033[36m"
    WHITE           = "\033[37m"
    DEFAULT_FG      = "\033[39m"

    #!^ ── Bright variants ────────────────────────────────────────────────────
    BRIGHT_BLACK    = "\033[90m"
    BRIGHT_RED      = "\033[91m"
    BRIGHT_GREEN    = "\033[92m"
    BRIGHT_YELLOW   = "\033[93m"
    BRIGHT_BLUE     = "\033[94m"
    BRIGHT_MAGENTA  = "\033[95m"
    BRIGHT_CYAN     = "\033[96m"
    BRIGHT_WHITE    = "\033[97m"

    #!^ ── Background colors ──────────────────────────────────────────────────
    BG_BLACK         = "\033[40m"
    BG_RED           = "\033[41m"
    BG_GREEN         = "\033[42m"
    BG_YELLOW        = "\033[43m"
    BG_BLUE          = "\033[44m"
    BG_MAGENTA       = "\033[45m"
    BG_CYAN          = "\033[46m"
    BG_WHITE         = "\033[47m"
    DEFAULT_BG       = "\033[49m"

    #!^ ── Bright background variants ────────────────────────────────────────
    BG_BRIGHT_BLACK   = "\033[100m"
    BG_BRIGHT_RED     = "\033[101m"
    BG_BRIGHT_GREEN   = "\033[102m"
    BG_BRIGHT_YELLOW  = "\033[103m"
    BG_BRIGHT_BLUE    = "\033[104m"
    BG_BRIGHT_MAGENTA = "\033[105m"
    BG_BRIGHT_CYAN    = "\033[106m"
    BG_BRIGHT_WHITE   = "\033[107m"

    #!^ ── Cursor movement ────────────────────────────────────────────────────
    CURSOR_UP           = "\033[A"      ## Move up 1 line
    CURSOR_DOWN         = "\033[B"      ## Move down 1 line
    CURSOR_RIGHT        = "\033[C"      ## Move right 1 column
    CURSOR_LEFT         = "\033[D"      ## Move left 1 column
    CURSOR_HOME         = "\033[H"      ## Move to top-left (0, 0)
    CURSOR_LINE_START   = "\033[G"      ## Move to start of current line (col 1)
    CURSOR_LINE_END     = "\033[999C"   ## Move to end of current line (far right)
    CURSOR_SAVE         = "\033[s"      ## Save cursor position
    CURSOR_RESTORE      = "\033[u"      ## Restore saved cursor position
    CURSOR_HIDE         = "\033[?25l"   ## Hide the cursor
    CURSOR_SHOW         = "\033[?25h"   ## Show the cursor

    #!^ ── Line control ───────────────────────────────────────────────────────
    LINE_UP             = "\033[F"  ## Move to start of previous line
    LINE_DOWN           = "\033[E"  ## Move to start of next line
    ERASE_LINE          = "\033[2K" ## Erase entire current line
    ERASE_LINE_END      = "\033[0K" ## Erase from cursor to end of line
    ERASE_LINE_START    = "\033[1K" ## Erase from cursor to start of line
    CARRIAGE_RETURN     = "\r"      ## Move to start of current line (no erase)

    #!^ ── Screen control ─────────────────────────────────────────────────────
    CLEAR_SCREEN         = "\033[2J"     ## Clear entire screen
    CLEAR_SCREEN_END     = "\033[0J"     ## Clear from cursor to end of screen
    CLEAR_SCREEN_START   = "\033[1J"     ## Clear from cursor to start of screen
    CLEAR_SCROLLBACK     = "\033[3J"     ## Clear screen + scrollback buffer
    SCREEN_SAVE          = "\033[?47h"   ## Save screen state
    SCREEN_RESTORE       = "\033[?47l"   ## Restore saved screen state
    ALT_SCREEN_ON        = "\033[?1049h" ## Switch to alternate screen buffer
    ALT_SCREEN_OFF       = "\033[?1049l" ## Switch back from alternate screen buffer

    #!^ ── Scrolling ──────────────────────────────────────────────────────────
    SCROLL_UP           = "\033[S"  ## Scroll viewport up 1 line
    SCROLL_DOWN         = "\033[T"  ## Scroll viewport down 1 line

    #!^ ── Dynamic cursor helpers ─────────────────────────────────────────────
    @staticmethod
    def up(n: int = 1) -> str:
        """
        Generates an ANSI sequence to move the cursor up.
        Args:
            n (int): Number of lines to move.
        Returns:
            str: The ANSI escape sequence.
        """
        return f"\033[{n}A"

    @staticmethod
    def down(n: int = 1) -> str:
        """
        Generates an ANSI sequence to move the cursor down.
        Args:
            n (int): Number of lines to move.
        Returns:
            str: The ANSI escape sequence.
        """
        return f"\033[{n}B"

    @staticmethod
    def right(n: int = 1) -> str:
        """
        Generates an ANSI sequence to move the cursor right.
        Args:
            n (int): Number of columns to move.
        Returns:
            str: The ANSI escape sequence.
        """
        return f"\033[{n}C"

    @staticmethod
    def left(n: int = 1) -> str:
        """
        Generates an ANSI sequence to move the cursor left.
        Args:
            n (int): Number of columns to move.
        Returns:
            str: The ANSI escape sequence.
        """
        return f"\033[{n}D"

    @staticmethod
    def move_to(row: int, col: int) -> str:
        """
        Generates an ANSI sequence to move cursor to an absolute position.
        Args:
            row (int): The 1-indexed row number.
            col (int): The 1-indexed column number.
        Returns:
            str: The ANSI escape sequence.
        """
        return f"\033[{row};{col}H"

    @staticmethod
    def line_up(n: int = 1) -> str:
        """
        Moves the cursor to the start of the line N lines up.
        Args:
            n (int): Number of lines to move up.
        Returns:
            str: The ANSI escape sequence.
        """
        return f"\033[{n}F"

    @staticmethod
    def line_down(n: int = 1) -> str:
        """
        Moves the cursor to the start of the line N lines down.
        Args:
            n (int): Number of lines to move down.
        Returns:
            str: The ANSI escape sequence.
        """
        return f"\033[{n}E"

    @staticmethod
    def scroll_up(n: int = 1) -> str:
        """
        Generates sequence to scroll the viewport up.
        Args:
            n (int): Number of lines to scroll.
        Returns:
            str: The ANSI escape sequence.
        """
        return f"\033[{n}S"

    @staticmethod
    def scroll_down(n: int = 1) -> str:
        """
        Generates sequence to scroll the viewport down.
        Args:
            n (int): Number of lines to scroll.
        Returns:
            str: The ANSI escape sequence.
        """
        return f"\033[{n}T"
    
    @staticmethod
    def move_to_col(n: int) -> str:
        """
        Moves cursor to an absolute column on the current line.
        Args:
            n (int): The 1-indexed column number.
        Returns:
            str: The ANSI escape sequence.
        """
        return f"\033[{n}G"

    #!^ ── Color helpers ──────────────────────────────────────────────────────
    @staticmethod
    def rgb(r: int, g: int, b: int) -> str:
        """
        Generates a 24-bit true-color foreground ANSI sequence.
        Args:
            r (int): Red component (0-255).
            g (int): Green component (0-255).
            b (int): Blue component (0-255).
        Returns:
            str: The ANSI escape sequence.
        """
        return f"\033[38;2;{r};{g};{b}m"

    @staticmethod
    def bg_rgb(r: int, g: int, b: int) -> str:
        """
        Generates a 24-bit true-color background ANSI sequence.
        Args:
            r (int): Red component (0-255).
            g (int): Green component (0-255).
            b (int): Blue component (0-255).
        Returns:
            str: The ANSI escape sequence.
        """
        return f"\033[48;2;{r};{g};{b}m"

    @staticmethod
    def color256(n: int) -> str:
        """
        Generates a 256-color foreground ANSI sequence.
        Args:
            n (int): Color index (0-255).
        Returns:
            str: The ANSI escape sequence.
        """
        return f"\033[38;5;{n}m"

    @staticmethod
    def bg_color256(n: int) -> str:
        """
        Generates a 256-color background ANSI sequence.
        Args:
            n (int): Color index (0-255).
        Returns:
            str: The ANSI escape sequence.
        """
        return f"\033[48;5;{n}m"

    #!^ ── Text helpers ───────────────────────────────────────────────────────
    @staticmethod
    def wrap(text: str, *codes: str) -> str:
        """
        Wraps text with one or more ANSI codes and appends a reset.
        Args:
            text (str): The string to be formatted.
            *codes (str): Variable number of ANSI escape sequences.
        Returns:
            str: The formatted string ending with RESET.
        """
        return "".join(codes) + text + ANSI.RESET

    @staticmethod
    def overwrite(text: str) -> str:
        """
        Returns a sequence to clear the current line and write new text.
        Args:
            text (str): The text to write on the cleared line.
        Returns:
            str: The ANSI sequence and text.
        """
        return f"\r\033[2K{text}"

    @staticmethod
    def overwrite_above(text: str, n: int = 1) -> str:
        """
        Moves up N lines, clears that line, and writes new text.
        Args:
            text (str): The text to write.
            n (int): How many lines to move up before overwriting.
        Returns:
            str: The ANSI escape sequence and text.
        """
        return f"\033[{n}F\033[2K{text}"


#!^ ── Quick demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import time

    print(f"{ANSI.RED}Red text{ANSI.RESET}")
    print(f"{ANSI.BOLD}{ANSI.BLUE}Bold blue{ANSI.RESET}")
    print(f"{ANSI.BG_YELLOW}{ANSI.BLACK}Black on yellow{ANSI.RESET}")
    print(f"{ANSI.UNDERLINE}{ANSI.GREEN}Underlined green{ANSI.RESET}")
    print(ANSI.wrap("Wrapped magenta + bold", ANSI.MAGENTA, ANSI.BOLD))
    print(ANSI.rgb(255, 128, 0) + "True-color orange" + ANSI.RESET)
    print(ANSI.color256(214) + "256-color orange" + ANSI.RESET)

    print(ANSI.SAPERATOR)

    ## Line overwrite demo
    print("Thinking...", end="", flush=True)
    time.sleep(1)
    print(ANSI.overwrite("Done!"))

    ## Overwrite a previous line demo
    print("Step 1: pending")
    print("Step 2: pending")
    time.sleep(1)
    print(ANSI.overwrite_above(ANSI.wrap("Step 1: complete", ANSI.GREEN), n=2), end="")
    print(ANSI.line_down(1), end="")  ## restore position to step 2's line