# AvitoParser
AvitoParser target direction is Car, but you can use sometime targets

### requriments for system:

    sudo apt-get install firefox-geckodriver
    sudo apt-get install poetry
    

### Instruction

- install all requirements
    ```sh
    poetry install
    ```
- put geckodriver to root folder
- enterence to env
    ```sh
    poetry shell
    ```
    or
    ```sh
    poetry run python you_script.py
    ```

- copy past url from you browser
- example url
    ```sh
    url = 'https://www.avito.ru/moskva_i_mo/avtomobili/audi/a4-ASgBAgICAkTgtg2emSjitg2MtSg'
    ```
- For example сode for serach
    ```sh
    from core.avito import AvitoParser
    from core.export_to import save_to_file

    avito = AvitoParser(url)
    avito_sale_items = get_sales_items(with_recomendations = True)
    save_to_file(data = avito_sale_items, filename='avita_sale_items')
    ```

## License

MIT

**Free Software, Hell Yeah!**
