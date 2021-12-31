<!--suppress HtmlDeprecatedAttribute -->
<h1 align="center">
  <a href="https://github.com/zakuciael/ulauncher-jetbrains">
    <img alt="Ulauncher JetBrains" src="https://raw.githubusercontent.com/zakuciael/ulauncher-jetbrains/master/.github/logo.svg?sanitize=true" width="130">
  </a>
	<br>
	<br>
  Ulauncher JetBrains
</h1>

<h6 align="center">Overview</h6>
<h4 align="center">
<a href="https://ulauncher.io/" target="_blank">Ulauncher</a> extension that let's you open your projects in <a href="https://www.jetbrains.com/products/" target="_blank">JetBrains IDEs</a>
</h4>

<p align="center">
  <a href="https://www.npmjs.com/package/@zakku/tabby-theme">
    <img src="https://img.shields.io/badge/Ulauncher-Extension-green.svg"
      alt="Ulauncher Extension" />
  </a>
  <a href="https://github.com/zakuciael/ulauncher-jetbrains/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/zakuciael/ulauncher-jetbrains.svg"
      alt="License" />
  </a>
</p>

## Install

### Requirements

- Ulauncher 5
- Python 3
- Jetbrains IDE

To install this extension:
1. Open `Preferences` window
2. Select `Extensions` tab
3. Click `Add extension` button on the sidebar
4. Paste the following url: `https://github.com/zakuciael/ulauncher-jetbrains`

## Usage

### Supported IDEs

- PHPStorm
- WebStorm
- PyCharm
- IntelliJ IDEA
- CLion
- Rider

To use this extension first **generate shell scripts** in the JetBrains Toolbox app by doing the following:
1. Open JetBrains Toolbox app
2. Go to settings
3. Click on the `Tools` dropdown
4. Check `Generate shell scripts` checkbox
5. Enter the shell scripts location

After that, follow below instructions to configure the extension settings:
1. Open `Preferences` window
2. Select `Extensions` tab
3. Click on `JetBrains Launcher` extension
4. Set the `Shell scripts location` value to the path configured in the JetBrains Toolbox app 
5. Set the `Configs location` value to the folder in which JetBrains IDEs store their configurations  
    **Default location:** ``~/.config/JetBrains/``

## Contributing

Clone this repository and run:
```bash
make link
```

The `make link` command will symlink the project into the ulauncher extensions folder.

To see your changes, stop ulauncher and run it from the command line with: `make dev`.

The output will display something like this:

```
2020-11-15 10:24:16,869 | WARNING | ulauncher.api.server.ExtensionRunner: _run_process() | VERBOSE=1 ULAUNCHER_WS_API=ws://127.0.0.1:5054/ulauncher-jetbrains PYTHONPATH=/usr/lib/python3.10/site-packages /usr/bin/python3 /home/zakku/.local/share/ulauncher/extensions/ulauncher-jetbrains/main.py
```

In another terminal run `make PORT=<PORT> start` command to run the extension backend.
> Note: The ``<PORT>`` variable refers to the port number found in the ``ULAUNCHER_WS_API`` env located in the above log.

To see your changes, CTRL+C the previous command and run it again to refresh.

## Credits
[Bruno Paz](https://github.com/brpaz) - Original author

## License
MIT © [Krzysztof Saczuk \<zakku@zakku.eu\>](https://github.com/zakuciael)