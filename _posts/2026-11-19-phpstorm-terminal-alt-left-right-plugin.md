---
layout: post
title: "Getting Alt+Left / Alt+Right Back in the PhpStorm Terminal with a 15-Line Plugin"
date: 2026-11-19
tags: []
---

I keep several terminal tabs open in PhpStorm: one for the dev server, one for tests, one or two for Claude Code sessions. For years I've switched between them with **Alt+Left / Alt+Right** (Select Previous / Next Tab). After the update to PhpStorm 2026.3 that stopped working inside the terminal: the keys went straight to the shell and the tab stayed where it was.

## What changed

PhpStorm 2026.3 ships the reworked terminal. To let shells and TUI apps have their key bindings, it only lets a short list of IDE actions through while the terminal has focus. On Windows and Linux, `NextTab` and `PreviousTab` are no longer on that list.

The good news: the terminal plugin builds that list from an extension point, `org.jetbrains.plugins.terminal.allowedActionsProvider`, and adds whatever every provider returns. So the fix is a plugin that returns two action ids.

## The plugin

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

The interface lives in the terminal's frontend module, so the extension has to be registered from a content module that depends on it (`local.terminalTabSwitch.frontend.xml`):

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

And the main `META-INF/plugin.xml` pulls that module in:

```xml
<idea-plugin>
  <id>local.terminal-tab-switch</id>
  <name>Terminal Tab Switch Shortcuts</name>
  <version>1.0.0</version>
  <vendor>local</vendor>
  <description>Lets Select Next/Previous Tab (Alt+Right/Left) work inside the reworked terminal on Windows and Linux.</description>
  <idea-version since-build="263"/>
  <depends>com.intellij.modules.platform</depends>
  <depends>org.jetbrains.plugins.terminal</depends>
  <content>
    <module name="local.terminalTabSwitch.frontend"/>
  </content>
</idea-plugin>
```

## Building it without Gradle

For something this small I didn't want the IntelliJ Platform Gradle plugin and a multi-gigabyte SDK download. PhpStorm already contains a JDK and the jar with the interface, so a shell script is enough. I run it from WSL against the Windows install:

```bash
#!/usr/bin/env bash
set -euo pipefail
IDE="/mnt/c/Users/<you>/AppData/Local/Programs/PhpStorm"
JAVAC="$IDE/jbr/bin/javac.exe"
CP="$(wslpath -w "$IDE/plugins/terminal/lib/modules/intellij.terminal.frontend.jar")"

rm -rf build dist && mkdir -p build/classes build/pkg/terminal-tab-switch/lib/modules dist
"$JAVAC" --release 21 -nowarn -cp "$CP" -d "$(wslpath -w build/classes)" \
  "$(wslpath -w src/local/terminaltabs/TabActionsProvider.java)"

# main jar: just plugin.xml
(cd resources/main && zip -qr ../../build/pkg/terminal-tab-switch/lib/terminal-tab-switch.jar META-INF)

# module jar: module descriptor + the class
M=build/pkg/terminal-tab-switch/lib/modules/local.terminalTabSwitch.frontend.jar
(cd resources/module && zip -q "../../$M" local.terminalTabSwitch.frontend.xml)
(cd build/classes && zip -qr "../../$M" local)

(cd build/pkg && zip -qr ../../dist/terminal-tab-switch.zip terminal-tab-switch)
```

The zip layout is what the IDE expects: `terminal-tab-switch/lib/*.jar`, with content modules under `lib/modules/`.

## Installing

**Settings → Plugins → ⚙ → Install Plugin from Disk…**, pick `dist/terminal-tab-switch.zip`, restart. Alt+Left / Alt+Right switch terminal tabs again, and every other key still goes to the shell.

If you've remapped Select Next/Previous Tab to other keys, those work too: the plugin allows the actions, not specific shortcuts.

*Sometimes the quickest fix for an IDE annoyance isn't a setting or a support ticket, it's 15 lines against the right extension point.*
