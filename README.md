# Ulauncher Jetbrains

[![Build Status](https://img.shields.io/travis/com/brpaz/ulauncher-jetbrains.svg)](https://github.com/brpaz/ulauncher-jetbrains)
[![GitHub license](https://img.shields.io/github/license/brpaz/ulauncher-jetbrains.svg)](https://github.com/brpaz/ulauncher-jetbrains/blob/master/LICENSE)

> Open your recent projects from Jetbrains IDEs from Ulauncher

## Demo

[demo](demo.gif)

## Requirements

- Ulauncher
- Python >= 2.7

## Install

Open ulauncher preferences window -> extensions -> add extension and paste the following url:

```
https://github.com/brpaz/ulauncher-jetbrains
```

## Usage

Before using this extension, you must create a command line launcher for your Jetbrains IDE. For that you can go to "Tools -> Create Command Line Launcher" in your IDE.
After that, you should configure the path to the created launcher in the plugin settings.

You also need to configure the path of your IDE "recentProjects" file in the plugin settings. The path is something like "~/.PhpStorm2018.1/config/options/recentProjectDirectories.xml". You will probably just need to change the ".PhpStorm2018.1/" part to match your IDE version.

This extension suports the following keywords:

`pstorm` -> To open a PHPStorm project
`webstorm`-> To open a WebStorm project

In the future I will add support for more IDEs like Idea and Goland.

**Note: To avoid creating a separate extension for each IDE, I use the keyword to identify which projects to look for. Because of this, you cant change the default keywords, without changing the code.
This will be no longer an issue after [this](https://github.com/Ulauncher/Ulauncher/issues/284) is fixed on Ulauncher side.**

## Development

```
git clone https://github.com/brpaz/ulauncher-jetbrains
make link
```

The `make link` command will symlink the cloned repo into the appropriate location on the ulauncher extensions folder.

To see your changes, stop ulauncher and run it from the command line with: `ulauncher -v`.

## Contributing

- Fork it!
- Create your feature branch: git checkout -b my-new-feature
- Commit your changes: git commit -am 'Add some feature'
- Push to the branch: git push origin my-new-feature
- Submit a pull request :D

## License

MIT &copy; [Bruno Paz]
