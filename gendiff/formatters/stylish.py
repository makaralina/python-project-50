import itertools


STATUS_SYMBOLS = {
    'unchanged': '  ',
    'removed': '- ',
    'changed': '+ ',
    'added': '+ ',
    'nested': '  '
}


def format_dict(content, depth):
    '''Format the dictionary without statuses for
    values into a structured string representation.'''
    indent = " "
    formatted_lines = []
    for key, value in content.items():
        current_indent = indent * (depth * 2 + 2)
        formatted_lines.append(
            f"{current_indent}{key}: "
            f"{format_value(value, depth + 2)}"
        )
        closing_indent_level = indent * ((depth - 1) * 2)
    result = itertools.chain("{", formatted_lines, [closing_indent_level + "}"])
    return '\n'.join(result)


def format_value(value, depth=0):
    '''Convert a value to its string representation.'''
    if isinstance(value, bool):
        return 'true' if value else 'false'
    elif isinstance(value, dict):
        return format_dict(value, depth)
    return 'null' if value is None else value


def make_stylish(diffs, replacer=' ', spaces_count=2):
    ''' Generate a stylish representation of a list of differences.'''

    def iter_(current_level, depth):
        deep_indent = replacer * (depth * spaces_count)
        lines = []

        for diff in current_level:
            key = diff.get('key')
            value1 = diff.get('value1')
            value2 = diff.get('value2')
            status = STATUS_SYMBOLS.get(diff['type'])

            match diff['type']:
                case 'unchanged' | 'removed' | 'added':
                    lines.append(
                        f"{deep_indent}{status}{key}: "
                        f"{format_value(value1, depth + 2)}"
                    )
                case 'updated':
                    lines.append(
                        f"{deep_indent}{STATUS_SYMBOLS['removed']}{key}: "
                        f"{format_value(value1, depth + 2)}"
                    )
                    lines.append(
                        f"{deep_indent}{STATUS_SYMBOLS['added']}{key}: "
                        f"{format_value(value2, depth + 2)}"
                    )
                case 'nested':
                    lines.append(
                        f"{deep_indent}{status}{key}: "
                        f"{iter_(diff['children'], depth + 2)}"
                    )
                case _:
                    raise ValueError(f"Unknown type: {diff['type']}")
        closing_indent = replacer * ((depth - 1) * 2)
        result = itertools.chain("{", lines, [closing_indent + "}"])
        return '\n'.join(result)

    return iter_(diffs, 1)
