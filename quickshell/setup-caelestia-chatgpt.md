
Great! I’ll explore the quickshell GitHub repository to explain step-by-step how the shell framework for Hyprland is set up, including how to install and run it on your system. I’ll also break down each element of the repository, show how to recreate the demo video, and guide you on customizing the color themes, widget layout, and adding new features.

I’ll be back shortly with a complete guide tailored for a beginner.


# Overview

The **Caelestia “shell”** repo is a QuickShell-based desktop shell configuration designed for the Hyprland Wayland compositor.  In other words, it uses [QuickShell](https://quickshell.outfoxxed.me/) – a QML/QtQuick toolkit for building panels, widgets, lockscreens, etc. – on top of Hyprland.  The user’s Hyprland config (“Caelestia dots”) is paired with QuickShell to create a customizable status bar and dashboard.  By default, QuickShell loads the `shell.qml` in `~/.config/quickshell/caelestia/` as the main UI definition.  (This repo’s structure is set up so that copying it into `~/.config/quickshell/caelestia` makes `shell.qml` the active config.)  In short, `shell.qml` (and the QML files it uses) define the on-screen panels, widgets, and interactions, while supporting code in **assets/**, **modules/**, **services/**, **widgets/**, etc. enables features like media controls, workspaces, system monitors, and the lockscreen.

# Installation and Startup

1. **Clone the repo:**  Install the necessary tools (see below), then clone this repository into QuickShell’s config folder.  For example:

   ```bash
   cd ~/.config/quickshell
   git clone https://github.com/caelestia-dots/shell.git caelestia
   ```

   (This makes QuickShell treat `caelestia/shell.qml` as the shell config.)

2. **Install dependencies:**  As the README notes, the shell requires several utilities (e.g. `quickshell-git`, `ddcutil`, `brightnessctl`, `cava`, `networkmanager`, etc.).  In particular, you **must use the Git (rolling) version of QuickShell**, not an older tag.  Many dependencies (PipeWire, libaubio, etc.) support features like the audio visualizer and system monitoring.

3. **Compile the beat detector:**  The `assets/beat_detector.cpp` program is used to feed audio spectrum data to the visualizer on the dashboard.  After cloning, compile it:

   ```bash
   g++ -std=c++17 -Wall -Wextra \
       -I/usr/include/pipewire-0.3 -I/usr/include/spa-0.2 -I/usr/include/aubio \
       -o beat_detector caelestia/assets/beat_detector.cpp \
       -lpipewire-0.3 -laubio
   sudo mv beat_detector /usr/lib/caelestia/beat_detector
   ```

   This matches the README’s instructions to compile `assets/beat_detector.cpp` and install the `beat_detector` binary.

4. **Start the shell:**  You can now launch the shell.  If you installed the Caelestia dotfiles, it may auto-start on login.  Otherwise run:

   ```
   caelestia shell -d
   ```

   or equivalently

   ```
   qs -c caelestia
   ```

   These commands tell QuickShell to load the “caelestia” config (your cloned folder).  (QuickShell logs will show e.g. `Launching config: "~/.config/quickshell/caelestia/shell.qml"`.)  Once running, you should see the top panel and other UI elements appear.  Note that QuickShell auto-reloads on every QML save, so you can edit files and see instant updates.

# Repository Structure (Key Files and Folders)

* **`shell.qml`:** The main QML file that defines the shell’s windows, panels, and layout.  This file uses QuickShell components (like PanelWindow, PopupWindow, etc.) to create the status bar, menus, dashboard, and lock screen.  For example, it will import the custom widgets and services defined below and arrange them.  Modifying `shell.qml` changes what appears on your bar or dashboard.

* **`run.fish`:** A helper Fish-shell script to launch the shell (likely setting some environment variables and calling QuickShell).  (You can look inside to see exactly how it runs `qs` or `caelestia shell`.)  In general you can launch via the `caelestia` wrapper CLI or directly with QuickShell.

* **`assets/`:** Contains static assets.  Notably it includes `beat_detector.cpp` (the C++ code compiled above for audio visualization) and various images/animations.  For example, the sample config uses GIFs like `assets/bongocat.gif` and `assets/kurukuru.gif` (as seen in the config’s `"mediaGif"` and `"sessionGif"` paths).  You can swap these out for your own animations/images to change the look.  Any file in `assets/` can be referenced in the QML (using the `root:/assets/...` URL syntax).

* **`config/`:** This folder provides default JSON configuration files for the shell.  The README explains that *all* user-adjustable options live in `~/.config/caelestia/shell.json`.  It’s likely that `config/caelestia/shell.json` in the repo is installed as the template.  Inspect this JSON to see defaults for things like the bar and dashboard.  (The example snippet in the README shows many settings: workspace icons, border rounding, number of audio visualizer bars, etc.)  You can copy or modify that JSON in your home directory to tweak the shell behavior without editing QML code.

* **`modules/`:** QML modules or components that can be reused across the shell.  For instance, this might include custom shapes, dialogs, or wrappers.  (QuickShell also has its own modules, but anything in `modules/` in this repo is specific to the Caelestia shell.)

* **`services/`:** Implements QuickShell services for background tasks and system integration.  Typical services include things like MPRIS (media player control), notifications, sensors, network status, Bluetooth, etc.  For example, QuickShell has built-in service modules for media playback (`Quickshell.Services.Mpris`), for notifications, UPower (battery), etc. The Caelestia shell likely uses these or custom variants.  By editing or adding files here, you can change how the shell polls system information.

* **`utils/`:** Utility scripts or QML that don’t fit under widgets or services.  This might contain helper scripts or JS functions used by the UI (for example, converting units or running shell commands).

* **`widgets/`:** Contains QML files for each UI widget.  Think of these as building blocks of the interface: e.g. a workspace list, a clock, network monitor, volume slider, app launcher, etc.  Each widget file defines how a particular piece of the panel or dashboard looks and behaves.  The `shell.qml` will import and position these widgets.  To add features (like a new system monitor or menu), you typically add a new QML widget here and then include it in `shell.qml`.

* **`LICENSE` / `README.md`:** Standard repository metadata.  The README (which we’ve been quoting) is especially useful for installation steps and configuration tips.

* **`out.mp4`:** A demo video showing the shell in action.  (YouTube or mp4 file.)  Recreating the exact video setup means running the shell with the provided config and placing the same wallpapers and images.

# How It All Comes Together

When you run the shell (`qs -c caelestia`), QuickShell reads `shell.qml`.  That QML will use the imported components (from **modules**, **widgets**, **services**, etc.) to build windows.  For example, it might create a `PanelWindow` at the top of the screen containing workspace buttons, a taskbar, and system tray; it might create a hidden `PopupWindow` or fullscreen overlay for the “dashboard” (launcher/search/lock screen); and so on.  Under the hood, QuickShell handles input (hotkeys can open the dashboard or lock the screen, as shown in the Hyprland shortcuts).  The shell also exposes an IPC interface (`caelestia shell ...`) to toggle drawers, clear notifications, control media, etc., as listed in the README (this is built into QuickShell and the Caelestia CLI).  For example, a music widget could call `caelestia shell mpris next` when you click “Next”.

QuickShell is highly dynamic: **it automatically reloads the UI whenever you save a QML file**.  This means you can tweak `shell.qml`, the widget QML, or even `shell.json`, and see your changes live.  For example, changing `"visualiserBars": 45` in the JSON (as in the README example) would immediately alter how many bars the audio visualizer shows on your dashboard.  (In fact, the example config sets up a 45-bar audio spectrum display and a weather widget location.)  This live-reload feature is why development iteration is very fast with QuickShell.

# Customizing Themes, Layout, and Features

* **Colors and Theme:** Color schemes are generally defined in QML or via theme variables.  You can change colors by editing the QML properties (many items have a `color:` or `backgroundColor:` setting) or by using a different JSON config if the shell supports theming.  For instance, you could modify the workspace icon color or bar background by changing values in `shell.qml` or by passing different symbols in the JSON.  If you want a completely different look (e.g. Catppuccin theme), you would replace the color codes or images accordingly in the QML/widget files.  (QuickShell doesn’t enforce one theme engine – you’re free to use Qt’s styling or hard-coded colors.)

* **Widget Layout:** The arrangement of widgets (clock, battery indicator, launcher, etc.) is defined in `shell.qml`.  To rearrange or remove items, edit `shell.qml` and the corresponding QML files in **widgets/**.  For example, to add a new clock format widget, you would create a new QML file (or enable an existing one) under **widgets/**, and then instantiate it in `shell.qml`’s PanelWindow.  Likewise, sidebar or dashboard panels are defined there.  Think of `shell.qml` as the “scene graph” tying all components together.

* **Adding Features:** Since QuickShell is just QML/JS, you can add new features by writing QML or JavaScript and using QuickShell services.  For example, to add a system monitor, you could import QuickShell’s sensor/UPower APIs or call external commands via a `Process` element.  Then place that logic in a new widget file.  QuickShell’s documentation (see the [type references](https://quickshell.outfoxxed.me/docs/guide/introduction/)) shows many helpful types.

* **Replicating the Demo:** To recreate the exact setup from the video, ensure you have the same wallpapers and images.  By default, the shell looks for `~/.face` for your profile picture and `~/Pictures/Wallpapers` for the wallpaper rotator.  You can place the same images or edit `shell.json`’s `"wallpaperDir"` path.  Then simply launch the shell as above.  Everything (bar appearance, dashboard layout, audio visualizer, etc.) is determined by the QML and the JSON config you cloned, so running it out-of-the-box should match the demo.  Any changes (like different icon colors or widget visibility) require editing the repo files or your `shell.json`, after which you’ll see the changes instantly.

# Citing Key Points

* The Caelestia shell is built on **QuickShell** (a QtQuick toolkit for Wayland shells) and **Hyprland**.
* Installation is done by cloning into `~/.config/quickshell/caelestia` and compiling `assets/beat_detector.cpp`.
* Start it with `caelestia shell -d` or `qs -c caelestia`.
* All user settings live in `~/.config/caelestia/shell.json` (example snippet in README).
* The QuickShell framework auto-reloads on save, so you can edit QML and see changes in real time.
* For example, the sample config’s `"visualiserBars": 45` sets up a 45-bar audio spectrum on the dashboard.

By following the above and referring to the README and QuickShell docs, you can step through the installation, examine each folder’s purpose, and begin customizing colors, widget placement, and functionality to match the demo or your personal taste.  Always keep in mind that `shell.qml` and the files in **widgets/** are what determine the visible UI, while **config/shell.json** holds tweakable parameters.

**Sources:** Caelestia shell README; QuickShell documentation.
