import json
import asyncio

from deep_translator import GoogleTranslator

from ..bot      import bot
from ..Storage  import Storage


class CommandsManager():
    translator = None

    def SetCommands():
        storage     = Storage()
        back_info   = storage.GetBackInfo() 
        c           = back_info['contents']
        ids         = list()
        ids.append( c['start_id'] )
        ids.extend( c['always_open_ids'] )

        commands_descs = [ c['states_names'][id] for id in ids ] 
        commands_names = \
            CommandsManager.__TransformToCommandsNames(commands_descs)
        commands_names[0] = 'start'
        commands = CommandsManager.__GetCommands(commands_names, 
                                                 commands_descs,
                                                 ids)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            CommandsManager.__SetCommands(commands)
        )

        storage.SetCommands(commands)

    @staticmethod
    def __TransformToCommandsNames(list_of_names):
        def trans(s):
            if not CommandsManager.translator:
                CommandsManager.translator = \
                    GoogleTranslator(source='auto', target='en')
            s = CommandsManager.translator.translate(s)
            trantab = s.maketrans(' ', '_')
            return s.translate(trantab).lower()
        return list( map(trans, list_of_names) )

    @staticmethod
    def __GetCommands(names, descs, ids):
        return [
            { 'command' : c, 'description' : d, 'back_id' : i  } for 
                c, d, i in zip(names, descs, ids)
        ]

    @staticmethod
    async def __SetCommands(commands):
        print(commands)
        await bot.set_my_commands(commands=json.dumps(commands))

