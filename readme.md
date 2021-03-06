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

**Note:** Please backup your work before proceeding.

### Preparation

This tool works using command line. First, clone this repository to our computer. Alternatively, just download the ZIP file of this repository.

```
$ git clone https://github.com/nainawa/who-anc-properties.git
```

Then, make sure there is WHO ANC application source code in our computer. This is not absolutely necessary, but it will make it easier to build and debug the app later. The `.properties` files are located in `/opensrp-anc/src/main/resources/` directory of the source code. WHO ANC application is using these files to generate form strings. So, we need to briefly understand how it works.

WHO ANC application is using `opensrp-client-native-form` library to handle forms and its translation. To learn more about `.properties` files and how form works in the app, read more on [its repository](https://github.com/opensrp/opensrp-client-native-form).

### Convert .properties files to CSV

Enter the directory of this tool, then use `convert` command to convert `.properties` files to CSV.

https://user-images.githubusercontent.com/106649086/171562921-82f5d347-8c37-4c7d-aa4f-1a71fd711145.mov

```
python props.py convert <source_directory>
```

Change the `<source_directory>` to the path of where we store WHO ANC source code. For example, if it is inside home folder and named `who-anc-client`, the command will look like this:

```
python props.py convert "~/who-anc-client"
```

This command will merge multiple languages `.properties` files to a single CSV file for each `.properties` name to the `csv` folder. For example:

```
-------------------------------------------------------------------------------------
 WHO ANC source (/opensrp-anc/src/main/resources/) |       Output folder (csv)
-------------------------------------------------------------------------------------
anc_physical_exam.properties                       | anc_physical_exam.csv
anc_physical_exam_fr.properties                    |
anc_physical_exam_ind.properties                   |
anc_profile.properties                             | anc_profile.csv
anc_profile_fr.properties                          |
anc_profile_ind.properties                         |
...                                                | ...
-------------------------------------------------------------------------------------
```

Now, we can use spreadsheet editor to manage translations instead of editing each translation files line-by-line which is daunting, time consuming, and error-prone.

### Working with CSV files

You can edit the generated CSV files directly on Microsot Excel or Google Sheets or any editor that you can use.

<img width="1920" alt="generated_csv" src="https://user-images.githubusercontent.com/106649086/171563308-b8c0b591-f7fe-4461-abb3-75452e9e7535.png">

The first column is the key that will be used as identifier inside the application form definition. The later columns are the string value and its translations. To add more language, don't forget to add them at the first row. For example in screenshot above, "ind" (Bahasa Indonesia) is added after "default" (English) column.

### Generate CSV files to .properties

If we are done editing translations in the CSV files, we can generate them back to `.properties` files using `generate` command.

https://user-images.githubusercontent.com/106649086/171564353-8ef54d98-7ff6-42d0-85bd-dcc54768a202.mov

```
$ python props.py generate
```

This command will check for missing translations. If there is none, it will generate `.properties` files to `properties` folder. Then we can copy these files and overwrite the `.properties` files inside the application source code.

## Bugs and Issues

If you found bugs, error, or having issues when working with this tool, please [create an issue](https://github.com/nainawa/who-anc-properties/issues) on this repository.

## Contribution

This tool is an open source, everyone can help to make the world a better place. Or, at least make this tool better.
If you are considering to contribute to this repository, you can help solve unresolved issues or maybe suggesting features to improve this tool.
