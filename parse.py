import os

VALID_KEYS = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'SEED', 'PERFECT']


def parse_config_file(config_file):
    config = {}
    try:
        with open(config_file, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        raise ValueError(f"The file {config_file} does not exist.")
    except PermissionError:
        raise ValueError(f"{config_file} must have read permission.")

    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        if '=' in line:
            parts = line.split('=', 1)
            if len(parts) == 2:
                key = parts[0].strip().upper()
                value = parts[1].strip()

                if key in VALID_KEYS:
                    if key not in config:
                        config[key] = value
                    else:
                        raise ValueError(f"Duplicate key found at line {line_num}: '{key}'")
                else:
                    raise ValueError(f"Invalid key found at line {line_num}: '{key}'")
            else:
                raise ValueError(f"Format error at line {line_num}: '{line}'")
        else:
            raise ValueError(f"Format error at line {line_num}: '{line}'")
    return config


def parse_width_height(config):
    if 'WIDTH' in config and 'HEIGHT' in config:
        try:
            width = int(config['WIDTH'])
            height = int(config['HEIGHT'])
        except ValueError:
            raise ValueError('the WIDTH and HEIGHT has to be numerical.')

        if height < 0 or width < 0:
            raise ValueError('the WIDTH and HEIGHT values must be positive')

        if width < 10 or width > 30:
            raise ValueError("WIDTH must be between 10 and 30.")

        if height < 10 or height > 30:
            raise ValueError("HEIGHT must be between 10 and 30.")

        config['WIDTH'] = width
        config['HEIGHT'] = height
    else:
        raise ValueError('the WIDTH or HEIGHT is missing.')


def parse_entry_exit(config):
    if 'ENTRY' in config and 'EXIT' in config:
        try:
            entry_parts = [p.strip() for p in config['ENTRY'].split(',')]
            if len(entry_parts) != 2:
                raise ValueError("Format error at ENTRY. Use X,Y")
            ex, ey = int(entry_parts[0]), int(entry_parts[1])

            exit_parts = [p.strip() for p in config['EXIT'].split(',')]
            if len(exit_parts) != 2:
                raise ValueError("Format error at EXIT. Use X,Y")
            qx, qy = int(exit_parts[0]), int(exit_parts[1])
        except ValueError as e:
            if "int()" in str(e):
                raise ValueError('ENTRY and EXIT must have numerical values')
            raise e

        if ex < 0 or ey < 0 or qx < 0 or qy < 0:
            raise ValueError('ENTRY and EXIT coordinates must be positive')

        if ex >= config['WIDTH'] or ey >= config['HEIGHT']:
            raise ValueError("ENTRY must be within maze bounds")
        if qx >= config['WIDTH'] or qy >= config['HEIGHT']:
            raise ValueError("EXIT must be within maze bounds")

        config['ENTRY'] = (ex, ey)
        config['EXIT'] = (qx, qy)

    else:
        raise ValueError('ENTRY or EXIT is missing.')

    if config['EXIT'] == config['ENTRY']:
        raise ValueError("ENTRY AND EXIT CAN'T BE THE SAME")


def parse_file(config):
    if "OUTPUT_FILE" not in config:
        raise ValueError("The OUTPUT_FILE key is missing.")

    file_name = config['OUTPUT_FILE']
    if not file_name:
        file_name = 'maze.txt'
        config['OUTPUT_FILE'] = file_name

    directory = os.path.dirname(os.path.abspath(file_name))
    if not os.access(directory, os.W_OK):
        raise ValueError(f"No write permission for directory: {directory}")


def parse_perfect(config):
    if "PERFECT" not in config:
        raise ValueError("Error: PERFECT missing")

    value = config["PERFECT"].lower()
    if value == "true":
        config["PERFECT"] = True
    elif value == "false":
        config["PERFECT"] = False
    else:
        raise ValueError("PERFECT must be True or False.")


def parse_seed(config):
    value = config.get('SEED')
    if not value or (isinstance(value, str) and value.lower() == "none"):
        config['SEED'] = None
    else:
        try:
            config['SEED'] = int(value)
        except ValueError:
            try:
                config['SEED'] = float(value)
            except ValueError:
                if value.lower() in ['true', 'false']:
                    config['SEED'] = value.lower() == 'true'
                else:
                    config['SEED'] = value


def get_config(config_file):
    config = parse_config_file(config_file)
    parse_width_height(config)
    parse_entry_exit(config)
    parse_file(config)
    parse_perfect(config)
    parse_seed(config)
    return config