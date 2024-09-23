import re

def parse_spl(spl_query):
    commands = [cmd.strip() for cmd in spl_query.strip().split('|')]
    fields = set()
    for cmd in commands:
        if cmd.startswith('stats'):
            # Parse stats command
            fields = parse_stats(cmd)
        elif cmd.startswith('rename'):
            # Parse rename command
            fields = parse_rename(cmd, fields)
        elif cmd.startswith('lookup'):
            # Parse lookup command
            fields = parse_lookup(cmd, fields)
        elif cmd.startswith('eval'):
            # Parse eval command
            fields = parse_eval(cmd, fields)
        else:
            # Base search or other commands, skip or handle as needed
            pass
    return fields

def parse_stats(cmd):
    fields = set()
    # Extract functions and by clause
    pattern = r'stats\s+(.*?)(?:\s+by\s+(.*))?$'
    match = re.match(pattern, cmd)
    if match:
        functions_part = match.group(1)
        by_fields = match.group(2)
        # Extract fields from functions
        functions = re.findall(r'(?:\w+\((.*?)\)(?:\s+as\s+(\w+))?)', functions_part)
        for func_field, alias in functions:
            field_name = alias if alias else func_field
            fields.add(field_name.strip())
        # Add by fields
        if by_fields:
            for field in by_fields.split():
                fields.add(field.strip())
    return fields

def parse_rename(cmd, fields):
    # Extract rename mappings
    mappings = re.findall(r'(\w+)\s+as\s+(\w+)', cmd)
    rename_map = {old: new for old, new in mappings}
    # Rename fields
    new_fields = set()
    for field in fields:
        if field in rename_map:
            new_fields.add(rename_map[field])
        else:
            new_fields.add(field)
    return new_fields

def parse_lookup(cmd, fields):
    # Extract OUTPUT fields
    pattern = r'OUTPUT\s+(.*)'
    match = re.search(pattern, cmd)
    if match:
        output_fields = match.group(1).split()
        for field in output_fields:
            fields.add(field.strip())
    return fields

def parse_eval(cmd, fields):
    # Extract eval assignments
    assignments = re.findall(r'(\w+)\s*=', cmd)
    for field in assignments:
        fields.add(field.strip())
    return fields

# Example usage
spl_query = '''
index=main
| stats values(action) as action values(username) as username by dest 
| rename username as user
| lookup my_lookup dest OUTPUT dest_priority
| eval severity=if(dest_priority=="high", "critical", "medium")
| rename dest_priority as priority
'''
# severity, user, potato

result_fields = parse_spl(spl_query)
print("Fields returned:")
print(', '.join(sorted(result_fields)))
