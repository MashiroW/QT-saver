import cv2
import customtkinter
from PIL import Image, ImageDraw


def _rounded_mask(size, radius, supersample=4):
    w, h = size
    big_w, big_h, big_r = w * supersample, h * supersample, radius * supersample
    mask = Image.new("L", (big_w, big_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, big_w - 1, big_h - 1), radius=big_r, fill=255)
    return mask.resize((w, h), Image.LANCZOS)


class VideoPlayer(customtkinter.CTkFrame):
    """
        A minimal in-app video player: play/pause + seek, built on
        opencv frame-stepping. Muted -- Tkinter has no native
        video/audio pipeline, and the usual add-on (PyAV, used by
        tkVideoPlayer) doesn't have a prebuilt wheel for this Python
        and fails to compile here, so this trades audio for something
        that reliably works without extra native dependencies.
    """

    def __init__(self, master, path, max_width=480, max_height=640,
                 accent_color="#4fc3f7", text_color="#eaf2ff", corner_radius=0, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.max_w = max_width
        self.max_h = max_height
        self.corner_radius = corner_radius
        self._mask_cache_size = None
        self._mask_cache = None

        self.cap = cv2.VideoCapture(path)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 24
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        self.delay_ms = max(15, int(1000 / self.fps))

        self.playing = False
        self._after_id = None
        self._seeking = False

        self.video_label = customtkinter.CTkLabel(self, text="")
        self.video_label.pack(padx=10, pady=(10, 6))

        self.muted_hint = customtkinter.CTkLabel(self, text="\U0001F507 Muted preview (no in-app audio)",
                                        text_color=text_color, font=customtkinter.CTkFont(size=10))
        self.muted_hint.pack(pady=(0, 6))

        controls = customtkinter.CTkFrame(self, fg_color="transparent")
        controls.pack(fill="x", padx=20, pady=(0, 14))
        controls.grid_columnconfigure(1, weight=1)

        self.play_button = customtkinter.CTkButton(controls, text="▶", width=40,
                                        fg_color=accent_color, hover_color=accent_color, text_color="#08111d",
                                        command=self.toggle_play)
        self.play_button.grid(row=0, column=0, padx=(0, 10))

        self.seek_slider = customtkinter.CTkSlider(controls, from_=0, to=max(1, self.frame_count - 1),
                                        progress_color=accent_color, button_color=accent_color,
                                        button_hover_color=accent_color, command=self._on_seek_drag)
        self.seek_slider.set(0)
        self.seek_slider.grid(row=0, column=1, sticky="ew")
        self.seek_slider.bind("<ButtonPress-1>", lambda e: setattr(self, "_seeking", True))
        self.seek_slider.bind("<ButtonRelease-1>", lambda e: self._on_seek_release())

        self._show_frame_at(0)
        self.bind("<Destroy>", self._on_destroy)

    def toggle_play(self):
        self.playing = not self.playing
        self.play_button.configure(text="⏸" if self.playing else "▶")
        if self.playing:
            self._tick()

    def _on_seek_drag(self, value):
        if self._seeking:
            self._show_frame_at(int(float(value)))

    def _on_seek_release(self):
        self._seeking = False
        self._show_frame_at(int(self.seek_slider.get()))

    def _show_frame_at(self, frame_idx):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ok, frame = self.cap.read()
        if ok:
            self._render(frame)

    def _render(self, frame):
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        img.thumbnail((self.max_w, self.max_h))

        if self.corner_radius:
            if self._mask_cache_size != img.size:
                self._mask_cache = _rounded_mask(img.size, self.corner_radius)
                self._mask_cache_size = img.size
            rounded = Image.new("RGBA", img.size, (0, 0, 0, 0))
            rounded.paste(img.convert("RGBA"), (0, 0), self._mask_cache)
            img = rounded

        ctk_img = customtkinter.CTkImage(img, size=img.size)
        self.video_label.configure(image=ctk_img)
        self.video_label.image = ctk_img

    def _tick(self):
        if not self.playing:
            return

        ok, frame = self.cap.read()
        if not ok:
            self.playing = False
            self.play_button.configure(text="▶")
            self._show_frame_at(0)
            self.seek_slider.set(0)
            return

        self._render(frame)
        if not self._seeking:
            self.seek_slider.set(self.cap.get(cv2.CAP_PROP_POS_FRAMES))

        self._after_id = self.after(self.delay_ms, self._tick)

    def _on_destroy(self, event):
        if event.widget is not self:
            return
        self.playing = False
        if self._after_id is not None:
            try:
                self.after_cancel(self._after_id)
            except Exception:
                pass
        if self.cap is not None:
            self.cap.release()
