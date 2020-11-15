# Ulauncher Jetbrains

[![Ulauncher Extension](https://img.shields.io/badge/Ulauncher-Extension-green.svg?style=for-the-badge)](https://ext.ulauncher.io/-/github-brpaz-ulauncher-jetbrains)
[![CircleCI](https://img.shields.io/circleci/build/github/brpaz/ulauncher-jetbrains.svg?style=for-the-badge)](https://circleci.com/gh/brpaz/ulauncher-jetbrains)
![License](https://img.shields.io/github/license/brpaz/ulauncher-jetbrains.svg?style=for-the-badge)

> Open your recent projects from Jetbrains based IDEs from [ulauncher](https://ulauncher.io/).

## Demo

[demo](demo.gif)

## Requirements

- Ulauncher 5
- Python >= 3 
- The Jetbrains IDE you want to use.

## Install

Open ulauncher preferences window -> extensions -> add extension and paste the following url:

```
https://github.com/brpaz/ulauncher-jetbrains
```

## Usage

The following Jetbrains IDEs are supported:

* PHPStorm
* WebStorm
* PyCharm
* InteliJ

Before using this extension, you must create a command line launcher for your Jetbrains IDE. For that you can go to "Tools -> Create Command Line Launcher" in your IDE.
After that, you should configure the path to the created launcher in the plugin settings.

You also need to configure the path of your IDE "recentProjects" file in the plugin settings. The path is something like "~/.PhpStorm2018.1/config/options/recentProjectDirectories.xml". You will probably just need to change the ".PhpStorm2018.1/" part to match your IDE version.

This extension suports the following keywords:

`pstorm` -> To open a PHPStorm project
`webstorm`-> To open a WebStorm project
`intellij` -> To open a Intelij project
`pycharm`-> To open a Pycharm project.

**Note: To avoid creating a separate extension for each IDE, I use the keyword to identify which projects to look for. Because of this, you cant change the default keywords, without changing the code.
This will be no longer an issue after [this](https://github.com/Ulauncher/Ulauncher/issues/284) is fixed on Ulauncher side.**

## Development

```
git clone https://github.com/brpaz/ulauncher-jetbrains
cd ulauncher-jetbrains
make link
```

The `make link` command will symlink the cloned repo into the appropriate location on the ulauncher extensions folder.

To see your changes, stop ulauncher and run it from the command line with: `ulauncher -v`.

## Contributing

All contributions are welcome.

## 💛 Support the project

If this project was useful to you in some form, I would be glad to have your support.  It will help to keep the project alive and to have more time to work on Open Source.

The sinplest form of support is to give a ⭐️ to this repo.

You can also contribute with [GitHub Sponsors](https://github.com/sponsors/brpaz).

[![GitHub Sponsors](https://img.shields.io/badge/GitHub%20Sponsors-Sponsor%20Me-red?style=for-the-badge)](https://github.com/sponsors/brpaz)


Or if you prefer a one time donation to the project, you can simple:

<a href="https://www.buymeacoffee.com/Z1Bu6asGV" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>

## Author

👤 **Bruno Paz**

* Website: [brunopaz.dev](https://brunopaz.dev)
* Github: [@brpaz](https://github.com/brpaz)
* Twitter: [@brunopaz88](https://twitter.com/brunopaz88)
  
## 📝 License

Copyright © 2020 [Bruno Paz](https://github.com/brpaz).

This project is [MIT](https://opensource.org/licenses/MIT) licensed.


