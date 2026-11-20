---
layout: post
title: "Alt+Left/Right Tab Switching in the PhpStorm 2026.3 Terminal"
description: "PhpStorm 2026.3's new terminal swallows Alt+Left/Right on Windows and Linux. A free 2 KB plugin brings terminal tab switching back, or build it from 15 lines."
date: 2026-11-19
last_modified_at: 2026-11-20
tags: [phpstorm, jetbrains, terminal, plugin]
---

I keep several terminal tabs open in PhpStorm: one for the dev server, one for tests, one or two for Claude Code sessions. For years I've switched between them with **Alt+Left / Alt+Right** (Select Previous / Next Tab). After the update to PhpStorm 2026.3 that stopped working inside the terminal: the keys went straight to the shell and the tab stayed where it was.

I fixed it with a tiny plugin. It's free and open source, so you can just install it.

## Fix it in one minute

1. Download **[terminal-tab-switch.zip](https://github.com/ciuc123/phpstorm-terminal-tabs/releases/latest/download/terminal-tab-switch.zip)** (2 KB, don't unzip it).
2. In PhpStorm: **Settings → Plugins → ⚙ → Install Plugin from Disk…**, pick the zip.
3. Restart the IDE.

Alt+Left / Alt+Right switch terminal tabs again, and every other key still goes to the shell. If you've remapped Select Next/Previous Tab to other keys, those work too: the plugin allows the actions, not specific shortcuts.

To remove it: **Settings → Plugins → Installed → Terminal Tab Switch Shortcuts → Uninstall**.

Source, issues and releases: [github.com/ciuc123/phpstorm-terminal-tabs](https://github.com/ciuc123/phpstorm-terminal-tabs).

## Does this affect you?

You have this problem if all of these are true:

- PhpStorm (or another JetBrains IDE) **2026.3 or newer**, using the new terminal.
- **Windows or Linux.** On macOS tab switching was not taken away.
- Pressing your Select Next/Previous Tab shortcut while the terminal has focus does nothing, or moves the cursor in the shell, instead of switching tabs.

I've tested it in PhpStorm 2026.3 on Windows. It should work in IntelliJ IDEA, WebStorm, PyCharm and the rest, because the terminal plugin is shared across all of them. If it doesn't in yours, [open an issue](https://github.com/ciuc123/phpstorm-terminal-tabs/issues).

## What changed

PhpStorm 2026.3 ships the reworked terminal. To let shells and TUI apps have their key bindings, it only lets a short list of IDE actions through while the terminal has focus. On Windows and Linux, `NextTab` and `PreviousTab` are no longer on that list.

The good news: the terminal plugin builds that list from an extension point, `org.jetbrains.plugins.terminal.allowedActionsProvider`, and adds whatever every provider returns. So the fix is a plugin that returns two action ids.

## How the plugin works

One Java class:

```java
package local.terminaltabs;

import com.intellij.terminal.frontend.view.TerminalAllowedActionsProvider;
import java.util.List;

public final class TabActionsProvider implements TerminalAllowedActionsProvider {
  @Override
  public List<String> getActionIds() {
    return List.of("NextTab", "PreviousTab");
  }
}
```

The interface lives in the terminal's frontend module, so the extension has to be registered from a content module that depends on it:

```xml
<idea-plugin>
  <dependencies>
    <module name="intellij.terminal.frontend"/>
  </dependencies>
  <extensions defaultExtensionNs="org.jetbrains.plugins.terminal">
    <allowedActionsProvider implementation="local.terminaltabs.TabActionsProvider"/>
  </extensions>
</idea-plugin>
```

The main `META-INF/plugin.xml` declares `since-build="263"`, depends on `org.jetbrains.plugins.terminal` and pulls that module in with `<content><module name="…"/></content>`. The zip layout is what the IDE expects: `terminal-tab-switch/lib/*.jar`, with content modules under `lib/modules/`.

One caveat: JetBrains marks this extension point as experimental, so a future IDE version may change it. If the plugin stops loading after an update, that's the reason, and an issue on GitHub gets it fixed.

## Building it yourself, without Gradle or the IDE

For something this small I didn't want the IntelliJ Platform Gradle plugin and a multi-gigabyte SDK download. The plugin only needs the interface at compile time, and that interface has a single method. So the repo has a stub of it that's used for compiling and left out of the zip, and the IDE provides the real one at runtime. I checked that the class compiled against the stub is byte-for-byte identical to one compiled against PhpStorm's own jar.

With JDK 21+ on your PATH:

```bash
git clone https://github.com/ciuc123/phpstorm-terminal-tabs.git
cd phpstorm-terminal-tabs
./build.sh        # -> dist/terminal-tab-switch.zip
```

No JDK installed? Docker works too:

```bash
docker run --rm -v "$PWD":/p -w /p eclipse-temurin:21-jdk ./build.sh
```

That's also how the releases are made: pushing a `v*` tag runs the same `build.sh` in GitHub Actions and attaches the zip to a GitHub release.

*Sometimes the quickest fix for an IDE annoyance isn't a setting or a support ticket, it's 15 lines against the right extension point.*
