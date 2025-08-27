import sys

def parse_args():
    args = sys.argv[1:]
    filters = {
        'showAllies': '--allies' in args,
        'showAxis': '--axis' in args,
        'ids': []
    }
    if '--id' in args:
        id_index = args.index('--id')
        if id_index + 1 < len(args):
            filters['ids'].append(args[id_index + 1])
    return filters

def should_show_kill(log, filters):
    message = log.get('message', '')
    killer_team = 'Axis' if '(Axis' in message else 'Allies'
    victim_team = 'Allies' if '->' in message and '(Allies' in message else 'Axis'
    show_allies = filters.get('showAllies')
    show_axis = filters.get('showAxis')
    ids = filters.get('ids', [])
    if show_allies and killer_team != 'Allies' and victim_team != 'Allies':
        return False
    if show_axis and killer_team != 'Axis' and victim_team != 'Axis':
        return False
    if ids and log.get('steam_id_64_1') not in ids and log.get('steam_id_64_2') not in ids:
        return False
    return True
