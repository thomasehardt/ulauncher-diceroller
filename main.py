import logging
import random

from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.CopyToClipboardAction import \
    CopyToClipboardAction
from ulauncher.api.shared.action.RenderResultListAction import \
    RenderResultListAction
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

logger = logging.getLogger(__name__)


def roll_dice(dice_count, dice_faces):
    totals = []

    for i in range(1, dice_count + 1):
        this_roll = random.randint(1, dice_faces)
        totals.append(this_roll)

    return totals


class DiceRollerExtension(Extension):
    def __init__(self):
        super(DiceRollerExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    default_result_item = ExtensionResultItem(
        icon='images/icon.png',
        name="Please enter dice count and number of faces",
        description="Example: dr 2 5",
        on_enter=None,
        highlightable=False
    )

    def on_event(self, event, extension):
        argument = event.get_argument() or ""

        # split into values
        arguments = [x.strip() for x in argument.split() if x.strip()]
        if len(arguments) < 2:
            return RenderResultListAction([self.default_result_item])

        try:
            values = [int(x) for x in arguments]

            totals = roll_dice(values[0], values[1])
            total = sum(totals)

            results = f"{totals}"
            result = f"{total}"

            items = [
                ExtensionResultItem(
                    icon='images/icon.png',
                    name=f"Rolls: {results}\nTotal: {result}",
                    description="Press enter to copy total to clipboard",
                    on_enter=CopyToClipboardAction(f"{result}"),
                    highlightable=False
                )
            ]
        except ValueError:
            items = [self.default_result_item]

        return RenderResultListAction(items)


if __name__ == '__main__':
    DiceRollerExtension().run()
