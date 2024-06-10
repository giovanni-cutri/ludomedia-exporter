# Ludomedia Exporter
Thanks to this Python script, you can export the videogames collection of any user on [Ludomedia](https://www.ludomedia.it/), including your own!

The following metadata is saved to a CSV file:
- Title
- Platform
- Genre
- Release Date
- Publisher
- Developer
- Recommended Age
- Link

## Dependencies

All the necessary libraries are listed in the *requirements.txt* file.

You can install them by running:

```
pip install -r requirements.txt
```

## Usage

- Run *main.py*: you will be prompted to provide the URL of the profile of the user on Ludomedia.
- Wait for the script to finish.
- The data is exported in a CSV file named after the user, in a folder called *data*.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/giovanni-cutri/ludomedia-exporter/blob/main/LICENSE) file for details.
