# WHO ANC Properties

A tool written in Python to help developers translate WHO ANC (Antenatal Care) mobile application easier.

## Brief

WHO ANC mobile application is using `.properties` files to handle forms translation. This helps developers around the world to localize the app and implement antenatal care procedures suggested by the World Health Organization. But, managing thousands of strings and multiple languages is a daunting work.

This tool helps translating `.properties` files more seamless by converting it to CSV files first so we can use spreadsheet editor such as Microsoft Excel or Google Sheet, then generate `.properties` files for multiple languages automatically.

To learn more about WHO ANC, see information below:
- [WHO Antenatal Care Publication](https://www.who.int/publications/i/item/9789241549912)
- [OpenSRP](https://smartregister.org/)
- [WHO ANC App (Global) Repository](https://github.com/opensrp/opensrp-client-anc)

## Requirements

To use this tool, we need to have Python installed in our system. This tool is built and tested using Python version 3.9.13. We will also need to have a working WHO ANC application source code.

## Usage

### Preparation

This tool works using command line. First, clone this repository to our computer. Alternatively, just download the ZIP file of this repository.

```
$ git clone https://github.com/nainawa/who-anc-properties.git
```

Then, make sure there is WHO ANC application source code in our computer. This is not absolutely necessary, but it will make it easier to build and debug the app later. The `.properties` files are located in `/opensrp-anc/src/main/resources/` directory of the source code. WHO ANC application is using these files to generate form strings. So, we need to briefly understand how it works.

WHO ANC application is using `opensrp-client-native-form` library to handle forms and its translation. To learn more about `.properties` files and how form works in the app, read more in [its repository](https://github.com/opensrp/opensrp-client-native-form).